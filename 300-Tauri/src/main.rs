// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() -> Result<(), Box<dyn std::error::Error>> {
  /* ==== 创建应用 ==== */
  let app = tauri::Builder::default()
    .plugin(tauri_plugin_opener::init())
    .build(tauri::generate_context!())
    .expect("error while running tauri application");


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
