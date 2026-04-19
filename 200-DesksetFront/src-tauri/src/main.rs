// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{
  menu::{Menu, MenuItem},
  tray::TrayIconBuilder, tray::TrayIconEvent,
  Manager,  // 调用位置：app.get_webview_window
  Emitter,  // 调用位置：app.emit
  // WebviewWindowBuilder, WebviewUrl,
  // WindowEvent
};
// use tauri_utils::{WindowEffect, config::WindowEffectsConfig};
use log;

mod desktop;
mod manager;


fn main() -> Result<(), Box<dyn std::error::Error>> {
  let app = tauri::Builder::default()
    .plugin(tauri_plugin_log::Builder::new()
      .level(log::LevelFilter::Info)
      .target(
        tauri_plugin_log::Target::new(
          tauri_plugin_log::TargetKind::Folder {
            path: std::path::PathBuf::from("./logs"),
            file_name: None
      }))
      .build()
    )
    .plugin(tauri_plugin_opener::init())
    .plugin(tauri_plugin_fs::init())
    .plugin(tauri_plugin_shell::init())
    .plugin(tauri_plugin_upload::init())
    .plugin(tauri_plugin_autostart::init(
      tauri_plugin_autostart::MacosLauncher::LaunchAgent,
      None
    ))
    .plugin(tauri_plugin_process::init())
    .build(tauri::generate_context!())
    .expect("error while running tauri application");


  /* === 桌面窗口 === */
  let _desktop_win = desktop::build(&app)
  .map_err(|e| {
    log::error!("Build desktop win fail, error: {}", e);
    e  // 向上继续传递错误
  })?;


  /* === 管理窗口 === */
  let _manager_win = manager::build(&app)
  .map_err(|e| {
    log::error!("Build manager win fail, error: {}", e);
    e
  })?;


  /* === 启动应用 === */
  app.run(|_app_handle, e| match e {
    /* 当所有窗口关闭后，阻止 Tauri 退出 */
    // tauri::RunEvent::ExitRequested { api, .. } => {
    //   api.prevent_exit();
    // }
    _ => {}
  });

  Ok(())  // 不要加分号
}
