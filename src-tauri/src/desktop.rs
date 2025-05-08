use tauri::{
  App,
  WebviewWindow, WebviewWindowBuilder, WebviewUrl
};
use libloading;

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

  unsafe {
    // setBottom.dll：将 Tauri 绑定为桌面子窗口
    let lib = libloading::Library::new("setBottom.dll")?;  // target/debug 目录
    let main: libloading::Symbol<unsafe extern fn(i32, i32) -> i32> = lib.get(b"main")?;
    main((win.hwnd().unwrap()).0 as i32, 0 as i32);
  }

  return Ok(win);
}
