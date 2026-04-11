package main

import (
	"os"
	"os/signal"
	"strconv"
	"syscall"

	"DesksetBack/app/router"
	"DesksetBack/feature"
	"DesksetBack/shared/log"

	"DesksetBack/app/args"

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
