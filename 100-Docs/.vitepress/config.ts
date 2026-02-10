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
          { text: '部件简介', link: '/manual/widget/widget-overview' },
          { text: '笔记', collapsed: true, items: [
            { text: '数据库', link: '/manual/widget/note/base' },
            { text: '数字统计', link: '/manual/widget/note/num-stats' },
            { text: '日记', link: '/manual/widget/note/diary' },
            { text: '热力图', link: '/manual/widget/note/heatmap' },
            { text: '仓库状态', link: '/manual/widget/note/vault-status' }
          ]},
          { text: '时间和日期', collapsed: true, items: [
            { text: '时钟', link: '/manual/widget/datetime/clock' },
            { text: '日历', link: '/manual/widget/datetime/calendar' },
            { text: '秒表', link: '/manual/widget/datetime/stopwatch' },
            { text: '定时器', link: '/manual/widget/datetime/timer' },
            { text: '日期计数器' },
            { text: '闹钟' },
            { text: '番茄钟' },
            { text: '时间进度条' },
            { text: '日期进度条' },
            { text: '世界时钟' }
          ]},
          { text: '设备信息', collapsed: true, items: [
            { text: '硬件监控', link: '/manual/widget/device/hardware-monitor' },
            { text: '硬盘存储值', link: '/manual/widget/device/disk-storage' },
            { text: '电池电量', link: '/manual/widget/device/battery' }
          ]}
        ]}
      ]
    }
  }
})
