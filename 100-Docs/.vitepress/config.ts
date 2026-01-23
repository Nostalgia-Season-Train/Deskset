import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  head: [['link', { rel: 'icon', href: '/Deskset LOGO v2.1.png' }]],
  title: '数字桌搭 Deskset',

  // https://vitepress.dev/reference/default-theme-config
  themeConfig: {
    logo: '/Deskset LOGO v2.1.png',
    siteTitle: '数字桌搭 Deskset',

    nav: [
      { text: '用户手册', link: '/manual/what-is-deskset' },
      { text: '开发文档', link: '/develop' }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Nostalgia-Season-Train/Deskset' }
    ],

    outlineTitle: '导航',  // 替换右侧大纲 On this page 文本

    sidebar: {
      '/manual/': [
        { text: '简介', collapsed: false, items: [
          { text: '什么是数字桌搭？', link: '/manual/what-is-deskset' },
          { text: '入门指南', link: '/manual/get-started' }
        ]},
        { text: '部件', collapsed: false, items: [
          { text: '笔记', collapsed: true, items: [
            { text: '数据库' },
            { text: '数字统计' },
            { text: '热力图' },
            { text: '仓库状态' },
            { text: '日记' }
          ]},
          { text: '时间和日期', collapsed: true, items: [
            { text: '时钟' },
            { text: '日历' },
            { text: '秒表' },
            { text: '定时器' },
            { text: '日期计数器' },
            { text: '闹钟' },
            { text: '番茄钟' },
            { text: '时间进度条' },
            { text: '日期进度条' },
            { text: '世界时钟' }
          ]},
          { text: '设备信息', collapsed: true, items: [
            { text: '硬件监控' },
            { text: '硬盘存储值' },
            { text: '电池电量' }
          ]}
        ]}
      ]
    }
  }
})
