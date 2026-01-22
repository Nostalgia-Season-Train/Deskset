package router

import (
	"DesksetBack/internal/router/_unify"

	Battery "github.com/distatus/battery"
	"github.com/gofiber/fiber/v3"
	GopsutilDisk "github.com/shirou/gopsutil/v4/disk"
)

func RegisterDevice(app *fiber.App) {
	router := app.Group("/device")

	_unify.BoundGet(router, "/monitor", monitor)
	_unify.BoundGet(router, "/disk", disk)
	_unify.BoundGet(router, "/battery", battery)
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

/* ==== 电池电量 ==== */
type BatteryResult struct {
	IsCharge bool    `json:"is_charge"` // 是否正在充电
	Percent  float64 `json:"percent"`   // 电量百分比
}

func battery(ctx *_unify.DesksetCtx) error {
	batterys, err := Battery.GetAll()
	if err != nil {
		return ctx.DesksetSendError(1, err.Error(), nil)
	}

	var results []BatteryResult

	for _, battery := range batterys {
		is_charge := false
		if battery.State.Raw == Battery.Charging || battery.State.Raw == Battery.Full {
			is_charge = true
		}

		percent := battery.Current / battery.Full

		results = append(results, BatteryResult{
			IsCharge: is_charge,
			Percent:  percent,
		})
	}

	return ctx.DesksetSend(results)
}
