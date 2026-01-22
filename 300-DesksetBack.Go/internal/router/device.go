package router

import (
	"DesksetBack/internal/router/_unify"

	"github.com/gofiber/fiber/v3"
)

func RegisterDevice(app *fiber.App) {
	router := app.Group("/device")

	_unify.BoundGet(router, "/monitor", monitor)
}

func monitor(ctx *_unify.DesksetCtx) error {
	return ctx.DesksetSend("From DesksetBack/router/device: Hello, World!")
}
