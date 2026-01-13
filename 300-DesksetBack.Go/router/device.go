package router

import "github.com/gofiber/fiber/v3"

func RegisterDevice(app *fiber.App) {
	router := app.Group("/device")

	router.Get("/hardware_status", hardware_status)
}

func hardware_status(ctx fiber.Ctx) error {
	return ctx.SendString("From DesksetBack/router/device: Hello, World!")
}
