package main

import (
	"DesksetBack/router"

	"github.com/gofiber/fiber/v3"
)

func main() {
	app := fiber.New()

	router.RegisterDevice(app)

	app.Listen("127.0.0.1:3000")
}
