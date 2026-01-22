package router

import (
	"DesksetBack/internal/router/_unify"

	"github.com/gofiber/fiber/v3"
	GopsutilDisk "github.com/shirou/gopsutil/v4/disk"
)

func RegisterDevice(app *fiber.App) {
	router := app.Group("/device")

	_unify.BoundGet(router, "/monitor", monitor)
	_unify.BoundGet(router, "/disk", disk)
}

func monitor(ctx *_unify.DesksetCtx) error {
	return ctx.DesksetSend("From DesksetBack/router/device: Hello, World!")
}

/* ==== 硬盘存储值 ==== */
type DiskResult struct {
	Root    string  `json:"root"`    // 硬盘驱动号
	Total   float64 `json:"total"`   // 硬盘容量
	Free    float64 `json:"free"`    // 硬盘可用空间
	Percent float64 `json:"percent"` // 硬盘使用率
}

func disk(ctx *_unify.DesksetCtx) error {
	partitions, err := GopsutilDisk.Partitions(false)
	if err != nil {
		return ctx.DesksetSendError(1, err.Error(), nil)
	}

	var results []DiskResult

	for _, partition := range partitions {
		root := partition.Mountpoint

		usage, err := GopsutilDisk.Usage(root)
		if err != nil {
			continue
		}

		total := float64(usage.Total>>20) / 1024
		free := float64(usage.Free>>20) / 1024
		percent := usage.UsedPercent

		results = append(results, DiskResult{
			Root:    root,
			Total:   total,
			Free:    free,
			Percent: percent,
		})
	}

	return ctx.DesksetSend(results)
}
