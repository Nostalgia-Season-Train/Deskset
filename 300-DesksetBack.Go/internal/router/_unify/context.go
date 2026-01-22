package _unify

import "github.com/gofiber/fiber/v3"

type DesksetCtx struct {
	fiber.DefaultCtx
}

// 重写 Ctx.SendString 方法
func (ctx *DesksetCtx) SendString(data string) error {
	return ctx.DefaultCtx.JSON(DesksetResponseJSON{
		Success: true,
		Code:    0,
		Message: "",
		Result:  data,
	})
}
