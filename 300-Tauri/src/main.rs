// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use log;
use deskset_lib::app::desktop;
use deskset_lib::app::manager;

fn main() -> Result<(), Box<dyn std::error::Error>> {
  /* ==== 创建应用 ==== */
  let app = tauri::Builder::default()
    .plugin(tauri_plugin_opener::init())
    .build(tauri::generate_context!())
    .expect("error while running tauri application");


  /* ==== 桌面窗口 ==== */
  let _desktop_win = desktop::build(&app)
  .map_err(|e| {
    log::error!("Build desktop win fail, error: {}", e);
    e  // 向上继续传递错误
  })?;


  /* ==== 管理窗口 ==== */
  let _manager_win = manager::build(&app)
  .map_err(|e| {
    log::error!("Build manager win fail, error: {}", e);
    e
  })?;


  /* ==== 启动应用 ==== */
  app.run(|_app_handle, e| match e {
    // 当所有窗口关闭后，阻止 Tauri 退出
    tauri::RunEvent::ExitRequested { api, .. } => {
      api.prevent_exit();
    }
    _ => {}
  });


  /* ==== 正常退出 ==== */
  Ok(())
}
