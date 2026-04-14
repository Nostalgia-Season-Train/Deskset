package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/signal"
	"strconv"
	"syscall"

	"DesksetBack/app/router"
	"DesksetBack/feature/device"
	"DesksetBack/shared/log"

	"DesksetBack/app/args"
	"DesksetBack/feature/kms"

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
	device.StartMonitor()

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
		rpcClient := kms.NewRpcClient(c)
		kms.SetOnline(rpcClient)
		for {
			// 接收消息
			_, msg, err := c.ReadMessage()
			if err != nil {
				fmt.Println("read:", err)
				break
			}
			// 解析消息
			var data map[string]any
			err = json.Unmarshal(msg, &data)
			if err != nil {
				fmt.Println("Error unmarshal message:", err)
				continue
			}
			rpcClient.OnReceive(data)
		}
		kms.SetOffline()
	}))

	router.RegisterDevice(app)
	router.RegisterKMS(app)

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
	device.EndMonitor()
	// 关闭日志器
	defer cleanupLogger()
}
