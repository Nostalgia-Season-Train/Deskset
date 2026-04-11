package main

import (
	"os"
	"os/signal"
	"syscall"

	"DesksetBack/app/router"
	"DesksetBack/feature"

	"github.com/gofiber/fiber/v3"
)

func main() {
	// 启动硬件监控
	feature.StartMonitor()

	// 启动 Fiber 服务器
	app := fiber.New()

	router.RegisterDevice(app)

	go func() {
		app.Listen("127.0.0.1:3000")
	}()

	/* --- 等待终止信号 --- */
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	<-c

	// 停止 Fiber 服务器
	app.Shutdown()

	// 停止硬件监控
	feature.EndMonitor()
}
