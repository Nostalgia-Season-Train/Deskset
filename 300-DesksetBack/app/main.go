package main

import (
	"fmt"
	"os"
	"os/signal"
	"strconv"
	"syscall"

	"DesksetBack/app/router"
	"DesksetBack/feature"
	"DesksetBack/shared/log"

	"DesksetBack/app/args"

	"github.com/gofiber/contrib/v3/websocket"
	"github.com/gofiber/fiber/v3"
)

func main() {
	// 打开日志器
	cleanupLogger, err := log.SetupLogger()
	if err != nil {
		panic(err)
	}
	// 启动硬件监控
	feature.StartMonitor()

	// 启动 Fiber 服务器
	app := fiber.New()

	// - [ ] 测试：websocket 连接
	// websocket 连接升级中间件
	app.Use("/obsidian/rpc", func(c fiber.Ctx) error {
		if websocket.IsWebSocketUpgrade(c) {
			c.Locals("allowed", true)
			// 设置 Authorization 子协议，前后端均须该子协议，否则报错 1006
			c.Set("Sec-Websocket-Protocol", "Authorization")
			return c.Next()
		}
		return fiber.ErrUpgradeRequired
	})
	// websocket 路由
	app.Get("/obsidian/rpc", websocket.New(func(c *websocket.Conn) {
		// 消息循环
		for {
			mt, msg, err := c.ReadMessage()
			if err != nil {
				fmt.Println("read:", err)
				break
			}
			fmt.Printf("recv: %s\n", msg)
			writeErr := c.WriteMessage(mt, msg)
			if writeErr != nil {
				fmt.Println("write:", err)
				break
			}
		}
	}))

	router.RegisterDevice(app)

	go func() {
		app.Listen("127.0.0.1:" + strconv.Itoa(args.Port))
	}()

	/* --- 等待终止信号 --- */
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	<-c

	// 停止 Fiber 服务器
	app.Shutdown()

	// 停止硬件监控
	feature.EndMonitor()
	// 关闭日志器
	defer cleanupLogger()
}
