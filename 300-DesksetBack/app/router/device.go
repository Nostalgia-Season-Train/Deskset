package router

import (
	"DesksetBack/feature/device"

	"github.com/gofiber/fiber/v3"
)

func RegisterDevice(app *fiber.App) {
	router := app.Group("/device")

	router.Get("/monitor", monitor)
	router.Get("/disk", disk)
	router.Get("/battery", battery)
	router.Get("/system", system)
}

func monitor(ctx fiber.Ctx) error {
	return ctx.JSON(device.Monitor())
}

func disk(ctx fiber.Ctx) error {
	return ctx.JSON(device.DiskStorage())
}

func battery(ctx fiber.Ctx) error {
	return ctx.JSON(device.BatteryPower())
}

func system(ctx fiber.Ctx) error {
	return ctx.JSON(device.System())
}
