use tauri::{
  App,
  WebviewWindow, WebviewWindowBuilder, WebviewUrl
};
use windows::core::{BOOL, w};
use windows::Win32::{
  Foundation::{HINSTANCE, HWND, LPARAM, LRESULT, WPARAM, POINT},
  UI::WindowsAndMessaging::{
    SendMessageTimeoutW, FindWindowW, SMTO_NORMAL,
    EnumWindows, FindWindowExW,
    SetParent,
    PostMessageW, WM_MOUSEMOVE, WM_LBUTTONDOWN, WM_LBUTTONUP, WM_VSCROLL
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

  // 嵌入桌面（C 动态库）
  // unsafe {
  //   // setBottom.dll：将 Tauri 绑定为桌面子窗口
  //   let lib = libloading::Library::new("setBottom.dll")?;  // target/debug 目录
  //   let main: libloading::Symbol<unsafe extern fn(i32, i32) -> i32> = lib.get(b"main")?;
  //   main((win.hwnd().unwrap()).0 as i32, 0 as i32);
  //   log::info!("HWND: 0x{:08X}", (win.hwnd().unwrap()).0 as usize);  // win11 临时调试用
  // }

  // 嵌入桌面（纯 Rust 版）
  let mode = 1;

  match mode {
    // 模式 0：放在系统桌面之下（z 轴），不影响桌面图标和鼠标右键
    0 => {
      attach(win.hwnd().unwrap(), "WorkerW");
      forward_input(win.hwnd().unwrap());
    },
    // 模式 1：完全替换系统桌面，可以输入文本、改变光标样式
    1 => {
      attach(win.hwnd().unwrap(), "DefView");
    },
    _ => todo!()
  }

  // 消除 Windows DPI 缩放，非整数倍缩放影响 CSS 效果
  win.set_zoom(1.0 / win.scale_factor().unwrap()).unwrap();

  return Ok(win);
}


/* ==== setBottom ==== */
  // 参考：https://github.com/meslzy/electron-as-wallpaper
/* --- 嵌入桌面 --- */
// 查找类名 WorkerW 的窗口
unsafe extern "system" fn enum_window_workerw(hwnd: HWND, lparm: LPARAM) -> BOOL {
  let h_def_view = FindWindowExW(
    Some(hwnd),
    Some(HWND::default()),
    w!("SHELLDLL_DefView"),
    None,
  ).unwrap_or(HWND::default());

  if !HWND::is_invalid(&h_def_view) {
    // 1、直接返回 SHELLDLL_DefView 句柄
    // *(lparm.0 as *mut HWND) = h_def_view;

    // 2、Win10 下返回 WorkerW
      // |-- WorkerW <- hwnd
      //   |-- DefView
      // |-- WorkerW <- 返回第二个 WorkerW
    let h_worker_w = WindowsAndMessaging::GetWindow(hwnd, WindowsAndMessaging::GW_HWNDNEXT);
    match h_worker_w {
      Ok(h_worker_w) => {
        if !HWND::is_invalid(&h_worker_w) {
          *(lparm.0 as *mut HWND) = h_worker_w;
        }
      },
      _ => {}
    }

    // 3、Win11 下返回 WorkerW
      // |-- Progman
      //   |-- DefView <- h_def_view
      //   |-- WorkerW <- 返回下一个窗口（兄弟窗口）
    let h_win11_worker_w = WindowsAndMessaging::GetWindow(h_def_view, WindowsAndMessaging::GW_HWNDNEXT);
    match h_win11_worker_w {
      Ok(h_win11_worker_w) => {
        if !HWND::is_invalid(&h_win11_worker_w) {
          *(lparm.0 as *mut HWND) = h_win11_worker_w;
        }
      },
      _ => {}
    }
  }

  BOOL(1)
}

// 查找类名 SHELLDLL_DefView 的窗口
unsafe extern "system" fn enum_window_defview(hwnd: HWND, lparm: LPARAM) -> BOOL {
  let h_def_view = FindWindowExW(
    Some(hwnd),
    Some(HWND::default()),
    w!("SHELLDLL_DefView"),
    None,
  ).unwrap_or(HWND::default());

  if !HWND::is_invalid(&h_def_view) {
    *(lparm.0 as *mut HWND) = h_def_view;
  }

  BOOL(1)
}

pub fn attach(h_tauri: HWND, which_class: &str) {
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

    // 第二步：遍历查找父窗口句柄（类名包含 WorkerW 或 DefView）
    let mut h_parent: HWND = HWND::default();
    match which_class {
      "WorkerW" => EnumWindows(Some(enum_window_workerw), LPARAM(&mut h_parent as *mut HWND as isize)).unwrap(),
      "DefView" => EnumWindows(Some(enum_window_defview), LPARAM(&mut h_parent as *mut HWND as isize)).unwrap(),
      &_ => todo!()
    }

    // 第三步：嵌入桌面
    SetParent(h_tauri, Some(h_parent)).unwrap();
  }
}

/* --- 转发输入 --- */
static mut H_CHROME_WIDGETWIN_1: Option<HWND> = None;

unsafe extern "system" fn handle_window_message(hwnd: HWND, umsg: u32, wparam: WPARAM, lparam: LPARAM) -> LRESULT {
  // 过滤：非输入消息
  if umsg != WindowsAndMessaging::WM_INPUT {
    return WindowsAndMessaging::DefWindowProcW(hwnd, umsg, wparam, lparam);
  }

  // 获取：指针及鼠标参数（指针位置）
  let mut point = POINT::default();
  let _ = WindowsAndMessaging::GetCursorPos(&mut point).unwrap();
  let mouse_param = LPARAM(((point.x as isize) & 0xFFFF) | ((point.y as isize) & 0xFFFF) << 16);

  // 过滤：指针不在桌面
  let h_point = WindowsAndMessaging::WindowFromPoint(point);  // 指针位于哪个窗口之上的句柄
  let mut point_class_name_buffer = vec![0; 256];
  let point_class_name_length = WindowsAndMessaging::GetClassNameW(h_point, point_class_name_buffer.as_mut_slice());
  point_class_name_buffer.truncate(point_class_name_length as usize);
  let point_class_name = String::from_utf16(&point_class_name_buffer).unwrap();
  if
    point_class_name != "SysListView32" &&
    point_class_name != "SHELLDLL_DefView" &&
    point_class_name != "Progman" &&
    point_class_name != "WorkerW"
  {
    return WindowsAndMessaging::DefWindowProcW(hwnd, umsg, wparam, lparam);
  }

  // 解析：原始（输入）数据
  let mut raw_data = Input::RAWINPUT::default();
  let mut raw_data_size = size_of::<Input::RAWINPUT>() as u32;
  let raw_data_header_size = size_of::<Input::RAWINPUTHEADER>() as u32;
  let _ = Input::GetRawInputData(
    Input::HRAWINPUT(lparam.0 as _),
    Input::RID_INPUT,
    Some(&mut raw_data as *mut _ as *mut _),
    &mut raw_data_size,
    raw_data_header_size
  );

  let device_type = Input::RID_DEVICE_INFO_TYPE(raw_data.header.dwType);

  // 转发：鼠标消息
  if device_type == Input::RIM_TYPEMOUSE {
    let mouse_button_flags = raw_data.data.mouse.Anonymous.Anonymous.usButtonFlags;
    match mouse_button_flags {
      0x0000 => { let _ = PostMessageW(H_CHROME_WIDGETWIN_1, WM_MOUSEMOVE, WPARAM(0x0020), mouse_param); }
      0x0001 => { let _ = PostMessageW(H_CHROME_WIDGETWIN_1, WM_LBUTTONDOWN, WPARAM(0x0001), mouse_param); }
      0x0002 => { let _ = PostMessageW(H_CHROME_WIDGETWIN_1, WM_LBUTTONUP, WPARAM(0x0001), mouse_param); }
      // 鼠标滚轮消息：高位(正值向前旋转，负值向后旋转) + 低位(虚拟按键)
      0x0400 => {
        let mouse_button_data = raw_data.data.mouse.Anonymous.Anonymous.usButtonData;
        let wheel_delta = mouse_button_data as i16;
        // H_CHROME_WIDGETWIN_1 无法处理 WM_MOUSEWHEEL 消息
        if wheel_delta > 0 {
          let _ = PostMessageW(H_CHROME_WIDGETWIN_1, WM_VSCROLL, WPARAM(0x0000), mouse_param);
        } else {
          let _ = PostMessageW(H_CHROME_WIDGETWIN_1, WM_VSCROLL, WPARAM(0x0001), mouse_param);
        }
      }
      _ => {}
    }
  }

  // 转发：键盘消息
  if device_type == Input::RIM_TYPEKEYBOARD {
    let keyboard_data = raw_data.data.keyboard;

    let is_pressed = keyboard_data.Flags as u32 != WindowsAndMessaging::RI_KEY_BREAK;
    let mut keyboard_param = 1u32;
    keyboard_param |= (keyboard_data.MakeCode as u32) << 16;
    keyboard_param |= 1u32 << 24;
    keyboard_param |= 0u32 << 29;
    keyboard_param = if is_pressed { keyboard_param } else { keyboard_param | 3u32 << 30 };

    let _ = PostMessageW(H_CHROME_WIDGETWIN_1, keyboard_data.Message, WPARAM(keyboard_data.VKey as usize), LPARAM(keyboard_param as isize));
  }

  return WindowsAndMessaging::DefWindowProcW(hwnd, umsg, wparam, lparam);
}

pub fn forward_input(h_tauri: HWND) {
  unsafe {
    // 第零步：获取 Chrome_WidgetWin_1 窗口的句柄
    let h_wry_webview = FindWindowExW(Some(h_tauri), Some(HWND::default()), w!("WRY_WEBVIEW"), None).unwrap();
    let h_chrome_widgetwin_0 = FindWindowExW(Some(h_wry_webview), Some(HWND::default()), w!("Chrome_WidgetWin_0"), None).unwrap();
    H_CHROME_WIDGETWIN_1 = Some(FindWindowExW(Some(h_chrome_widgetwin_0), Some(HWND::default()), w!("Chrome_WidgetWin_1"), None).unwrap());

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
