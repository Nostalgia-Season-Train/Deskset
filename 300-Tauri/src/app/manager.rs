use tauri::{
  App,
  WebviewWindow, WebviewWindowBuilder, WebviewUrl,
  LogicalSize
};
use std::cell::Cell;

pub fn build(app: &App) -> Result<WebviewWindow, Box<dyn std::error::Error>> {
  // 页面首次加载的标志位。注意，这是一个闭包！
  let first_load_flag: Cell<bool> = Cell::new(true);

  let manager_win = WebviewWindowBuilder::new(
    app,
    "manager",
    WebviewUrl::App("manager.html".into())
  )
  .title("Deskset")
  .resizable(true).maximizable(false)
  .transparent(true).decorations(false).shadow(false)
  // 禁用模糊背景效果，实现跨平台兼容
//   .effects(WindowEffectsConfig{
//     effects: vec![WindowEffect::Blur],  // Acrylic 改变窗口大小会有性能问题，拖动不会
//     state: None,
//     radius: None,
//     color: None
//   })
  .center()  // 窗口屏幕居中
  // 禁止刷新页面
  .on_navigation(move |url| {
    if first_load_flag.get() {
      first_load_flag.set(false);
      return true;
    }
    println!("Forbidden Refresh, url: {}", url);
    return false;
  })
  .build().unwrap();

  // 获取系统 DPI 缩放
  let dpi = manager_win.scale_factor().unwrap();
  // 消除 DPI 缩放造成窗口变大的问题，强制尺寸等于 960.0 * 600.0
  manager_win.set_size(LogicalSize::new(960.0 / dpi, 600.0 / dpi)).unwrap();
  // 强制 DPI 缩放等于 1，方便实现 Linear 风格
  // manager_win.set_zoom(1.0 / dpi).unwrap();

  manager_win.clone().on_window_event(move |event| {
    match event {
      // 阻止系统边框（窗口标题栏）关闭事件
        // 包括通过 Alt + Tab 关闭
      // WindowEvent::CloseRequested { api, .. } => {
      //   api.prevent_close();
      //   manager_win.hide().unwrap();  // 有点蠢，没找到 on_window_event 传递自身的示例
      // },
      _ => {}
    }
  });

  return Ok(manager_win);
}
