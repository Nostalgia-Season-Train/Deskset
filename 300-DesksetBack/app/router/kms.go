package router

import (
	"DesksetBack/feature/kms"

	"github.com/gofiber/fiber/v3"
)

func RegisterKMS(app *fiber.App) {
	router := app.Group("/kms")

	router.Get("/get-active-file", func(c fiber.Ctx) error {
		ret, err := kms.GetActiveFile()
		if err != nil {
			return c.SendString("Error")
		}
		return c.SendString(ret.(string))
	})
}
