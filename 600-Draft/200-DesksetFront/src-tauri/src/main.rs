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
    }
    _ => {
      println!("menu item {:?} not handled", event.id);
    }
  })
  /* 应用托盘 */
  .build(&app);
