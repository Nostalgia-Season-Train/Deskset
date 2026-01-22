package main

import (
	"DesksetBack/internal/router"
	"DesksetBack/internal/router/_unify"

	"github.com/gofiber/fiber/v3"
)

func main() {
	app := fiber.NewWithCustomCtx(func(app *fiber.App) fiber.CustomCtx {
		return &_unify.DesksetCtx{
			DefaultCtx: *fiber.NewDefaultCtx(app),
		}
	})

	router.RegisterDevice(app)

	app.Listen("127.0.0.1:3000")
}
