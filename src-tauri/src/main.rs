// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{
  menu::{Menu, MenuItem},
  tray::TrayIconBuilder, tray::TrayIconEvent,
  Manager,  // 调用位置：app.get_webview_window
  Emitter,  // 调用位置：app.emit
  WebviewWindowBuilder, WebviewUrl, WindowEvent
};
use tauri_utils::{WindowEffect, config::WindowEffectsConfig};

mod desktop;


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
    .build(tauri::generate_context!())
    .expect("error while running tauri application");


  /* === 托盘 === */
  // 参考：https://github.com/tauri-apps/tauri/blob/dev/examples/api/src-tauri/src/lib.rs
  let show_i = MenuItem::with_id(&app, "show", "显示", true, None::<&str>)?;
  let quit_i = MenuItem::with_id(&app, "quit", "退出", true, None::<&str>)?;
  let menu = Menu::with_items(&app, &[&show_i, &quit_i])?;

  let _tray = TrayIconBuilder::new()
    /* 图标 */
    .icon(app.default_window_icon().unwrap().clone())
    /* 双击图标 */
    .on_tray_icon_event({
      let app_handle = app.handle().clone();  // 克隆 app 句柄
      move |_tray_icon, event| match event {
      TrayIconEvent::DoubleClick { .. } => {
        let window = app_handle.get_webview_window("manager").unwrap();
        window.show().unwrap();
        window.set_focus().unwrap();  // 窗口显示后聚焦
      },
      _ => {}
    }})
    /* 菜单 */
    .menu(&menu)
    .show_menu_on_left_click(false)
    .on_menu_event(|app, event| match event.id.as_ref() {
      "show" => {
        let window = app.get_webview_window("manager").unwrap();
        window.show().unwrap();
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


  /* === 桌面窗口 === */
  let _desktop_win = desktop::build(&app)?;


  /* === 管理窗口 === */
  let manager_win = WebviewWindowBuilder::new(
    &app,
    "manager",
    WebviewUrl::App("manager.html".into())
  )
  .title("Deskset")
  .inner_size(650.0, 436.0).resizable(false).maximizable(false)
  .transparent(true).decorations(false).shadow(false)
  .effects(WindowEffectsConfig{
    effects: vec![WindowEffect::Blur],  // Acrylic 改变窗口大小会有性能问题，拖动不会
    state: None,
    radius: None,
    color: None
  })
  .center()  // 窗口屏幕居中
  .build().unwrap();

  manager_win.clone().on_window_event(move |event| {
    match event {
      WindowEvent::CloseRequested { api, .. } => {
        api.prevent_close();
        manager_win.hide().unwrap();  // 有点蠢，没找到 on_window_event 传递自身的示例
      },
      _ => {}
    }
  });


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
