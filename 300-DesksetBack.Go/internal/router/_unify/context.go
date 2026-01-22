package _unify

import "github.com/gofiber/fiber/v3"

type DesksetCtx struct {
	fiber.DefaultCtx
}

// router 无法绑定参数为自定义上下文的函数
func BoundGet(router fiber.Router, path string, handler func(*DesksetCtx) error) {
	router.Get(path, func(ctx fiber.Ctx) error {
		return handler(ctx.(*DesksetCtx))
	})
}

func (ctx *DesksetCtx) DesksetSend(result any) error {
	return ctx.DefaultCtx.JSON(DesksetResponseJSON{
		Success: true,
		Code:    0,
		Message: "",
		Result:  result,
	})
}

func (ctx *DesksetCtx) DesksetSendError(code int, message string, result any) error {
	return ctx.DefaultCtx.JSON(DesksetResponseJSON{
		Success: false,
		Code:    code,
		Message: message,
		Result:  result,
	})
}
