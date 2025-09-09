use tauri::{
  App,
  WebviewWindow, WebviewWindowBuilder, WebviewUrl
};
use windows::core::{BOOL, w};
use windows::Win32::{
  Foundation::{HINSTANCE, HWND, LPARAM, LRESULT, WPARAM},
  UI::WindowsAndMessaging::{
    SendMessageTimeoutW, FindWindowW, SMTO_NORMAL,
    EnumWindows, FindWindowExW,
    SetParent
  },
  System::LibraryLoader::GetModuleHandleW,
  UI::{WindowsAndMessaging, Input},
  Devices::HumanInterfaceDevice::{HID_USAGE_PAGE_GENERIC, HID_USAGE_GENERIC_MOUSE, HID_USAGE_GENERIC_KEYBOARD}
};
// use libloading;
// use log;

pub fn build(app: &App) -> Result<WebviewWindow, Box<dyn std::error::Error>> {
  let win = WebviewWindowBuilder::new(
    app,
    "desktop",
    WebviewUrl::App("desktop.html".into())
  )
  .transparent(true).decorations(true).shadow(false).skip_taskbar(true)
  .fullscreen(true)
  .focused(false)  // 静默打开，不要聚焦这个窗口
  .build().unwrap();

  // unsafe {
  //   // setBottom.dll：将 Tauri 绑定为桌面子窗口
  //   let lib = libloading::Library::new("setBottom.dll")?;  // target/debug 目录
  //   let main: libloading::Symbol<unsafe extern fn(i32, i32) -> i32> = lib.get(b"main")?;
  //   main((win.hwnd().unwrap()).0 as i32, 0 as i32);
  //   log::info!("HWND: 0x{:08X}", (win.hwnd().unwrap()).0 as usize);  // win11 临时调试用
  // }
  attach(win.hwnd().unwrap());

  // 消除 Windows DPI 缩放，非整数倍缩放影响 CSS 效果
  win.set_zoom(1.0 / win.scale_factor().unwrap()).unwrap();

  return Ok(win);
}


/* ==== setBottom ==== */
  // 参考：https://github.com/meslzy/electron-as-wallpaper
/* --- 嵌入桌面 --- */
extern "system" fn enum_window(h_wnd: HWND, l_parm: LPARAM) -> BOOL {
  unsafe {
    let h_def_view = FindWindowExW(
      Some(h_wnd),
      Some(HWND::default()),
      w!("SHELLDLL_DefView"),
      None,
    ).unwrap_or(HWND::default());

    if !HWND::is_invalid(&h_def_view) {
      *(l_parm.0 as *mut HWND) = h_def_view;
    }

    BOOL(1)
  }
}

pub fn attach(h_tauri: HWND) {
  unsafe {
    // 第一步：发送 0x52C 指令
    SendMessageTimeoutW(
      FindWindowW(w!("Progman"), None).unwrap(),
      0x052C,
      WPARAM(0xD),
      LPARAM(0x1),
      SMTO_NORMAL,
      100,
      None,
    );

    // 第二步：遍历查找 SHELLDLL_DefView 窗口句柄
    let mut h_def_view: HWND = HWND::default();
    EnumWindows(Some(enum_window), LPARAM(&mut h_def_view as *mut HWND as isize)).unwrap();

    // 第三步：嵌入桌面
    SetParent(h_tauri, Some(h_def_view)).unwrap();
  }
}

/* --- 转发输入 --- */
unsafe extern "system" fn handle_window_message(hwnd: HWND, umsg: u32, wparam: WPARAM, lparam: LPARAM) -> LRESULT {
  if umsg == WindowsAndMessaging::WM_INPUT {
    print!("input\n");
  }
  WindowsAndMessaging::DefWindowProcW(hwnd, umsg, wparam, lparam)
}

pub fn forward_input() {
  unsafe {
    // 第一步：创建原始输入窗口
      // 附：还有个方法是子类化 Tauri 窗口，但在 Win11 的测试上发现此方法会导致程序崩溃
    let h_instance = GetModuleHandleW(None).unwrap();

    let wnd_class = WindowsAndMessaging::WNDCLASSW {
      lpfnWndProc: Some(handle_window_message),
      hInstance: HINSTANCE::from(h_instance),
      lpszClassName: w!("DesksetRawInputWindowClass"),
      ..WindowsAndMessaging::WNDCLASSW::default()
    };
    WindowsAndMessaging::RegisterClassW(&wnd_class);

    let raw_input_window = WindowsAndMessaging::CreateWindowExW(
      WindowsAndMessaging::WINDOW_EX_STYLE::default(),
      wnd_class.lpszClassName,      // 窗口类名
      w!("DesksetRawInputWindow"),  // 窗口标题
      WindowsAndMessaging::WINDOW_STYLE::default(),
      0, 0,  // 窗口位置 (x, y)
      0, 0,  // 窗口大小 [w, h]
      None,
      None,
      Some(HINSTANCE::from(h_instance)),
      None
    ).unwrap();

    // 第二步：注册原始输入设备
    let inputs: [Input::RAWINPUTDEVICE; 2] = [
      Input::RAWINPUTDEVICE {
        hwndTarget: raw_input_window,
        usUsagePage: HID_USAGE_PAGE_GENERIC,
        usUsage: HID_USAGE_GENERIC_MOUSE,
        dwFlags: Input::RIDEV_INPUTSINK
      },
      Input::RAWINPUTDEVICE {
        hwndTarget: raw_input_window,
        usUsagePage: HID_USAGE_PAGE_GENERIC,
        usUsage: HID_USAGE_GENERIC_KEYBOARD,
        dwFlags: Input::RIDEV_INPUTSINK
      }
    ];

    Input::RegisterRawInputDevices(&inputs, size_of::<Input::RAWINPUTDEVICE>() as u32).unwrap();
  }
}
