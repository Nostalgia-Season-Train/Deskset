// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{
  menu::{Menu, MenuItem},
  tray::TrayIconBuilder,
  Manager,  // 调用位置：app.get_webview_window
  Emitter   // 调用位置：app.emit
};

fn main() -> Result<(), Box<dyn std::error::Error>> {
  let app = tauri::Builder::default()
    .plugin(tauri_plugin_opener::init())
    .plugin(tauri_plugin_fs::init())
    .plugin(tauri_plugin_shell::init())
    .build(tauri::generate_context!())
    .expect("error while running tauri application");

  // 参考：https://github.com/tauri-apps/tauri/blob/dev/examples/api/src-tauri/src/lib.rs
  let show_i = MenuItem::with_id(&app, "show", "显示", true, None::<&str>)?;
  let quit_i = MenuItem::with_id(&app, "quit", "退出", true, None::<&str>)?;
  let menu = Menu::with_items(&app, &[&show_i, &quit_i])?;

  let _tray = TrayIconBuilder::new()
    /* 图标 */
    .icon(app.default_window_icon().unwrap().clone())
    /* 菜单 */
    .menu(&menu)
    .show_menu_on_left_click(false)
    .on_menu_event(|app, event| match event.id.as_ref() {
      "show" => {
        let window = app.get_webview_window("manager").unwrap();
        window.show().unwrap();
        window.set_focus().unwrap();
      }
      "quit" => {
        app.emit("quit", "退出数字桌搭").unwrap();
        app.exit(0);  // 其他一切正常，除了报错 Failed to unregister class Chrome_WidgetWin_0. Error = 1412
      }
      _ => {
        println!("menu item {:?} not handled", event.id);
      }
    })
    /* 应用托盘 */
    .build(&app);

  app.run(|_app_handle, e| match e {
    /* 当所有窗口关闭后，阻止 Tauri 退出 */
    // tauri::RunEvent::ExitRequested { api, .. } => {
    //   api.prevent_exit();
    // }
    _ => {}
  });

  Ok(())  // 不要加分号
}
