package device

import (
	"fmt"
	"runtime"
	"sync"
	"time"

	Battery "github.com/distatus/battery"
	"github.com/shirou/gopsutil/v4/cpu"
	"github.com/shirou/gopsutil/v4/disk"
	"github.com/shirou/gopsutil/v4/host"
	"github.com/shirou/gopsutil/v4/mem"
	"github.com/shirou/gopsutil/v4/net"
)

type CPU struct {
	Percent float64 `json:"percent"`
	Freq    float64 `json:"freq"`
	Count   int     `json:"count"`
}

type RAM struct {
	Percent float64 `json:"percent"`
	Used    float64 `json:"used"`
	Total   int     `json:"total"`
}

type Disk struct {
	Percent float64 `json:"percent"`
}

type Network struct {
	Sent int `json:"sent"`
	Recv int `json:"recv"`
}

type Hardware struct {
	CPU     CPU     `json:"cpu"`
	RAM     RAM     `json:"ram"`
	Disk    Disk    `json:"disk"`
	Network Network `json:"network"`
}

type Device struct {
	hardware     Hardware
	mu           sync.RWMutex
	lastNetStats net.IOCountersStat
	lastNetTime  time.Time
}

var device *Device = nil

func init() {
	physicalCores, _ := cpu.Counts(false)
	if physicalCores == 0 {
		physicalCores = runtime.NumCPU()
	}

	device = &Device{
		hardware: Hardware{
			CPU: CPU{
				Count: physicalCores,
			},
		},
	}
}

// 硬件监控：刷新一次硬件信息
func monitor() {
	device.mu.Lock()
	defer device.mu.Unlock()

	perfData := GetPerformanceCounterData()

	device.updateCPU(perfData)
	device.updateRAM()
	device.updateDisk(perfData)
	device.updateNetwork()
}

func (d *Device) updateCPU(perfData PerformanceCounterData) {
	percent, err := cpu.Percent(0, false)
	if err == nil && len(percent) > 0 {
		d.hardware.CPU.Percent = percent[0]
	}

	freqInfo, err := cpu.Info()
	if err == nil && len(freqInfo) > 0 {
		maxFreq := freqInfo[0].Mhz
		if maxFreq > 0 {
			if perfData.ErrorCpuFreq == 0 && perfData.ResultCpuFreq > 0 {
				d.hardware.CPU.Freq = perfData.ResultCpuFreq * maxFreq
			}
		}
	}
}

func (d *Device) updateRAM() {
	memInfo, err := mem.VirtualMemory()
	if err == nil {
		d.hardware.RAM.Percent = memInfo.UsedPercent
		d.hardware.RAM.Used = float64(memInfo.Used) / (1024 * 1024 * 1024)
		d.hardware.RAM.Total = int(float64(memInfo.Total) / (1024 * 1024 * 1024))
	}
}

func (d *Device) updateDisk(perfData PerformanceCounterData) {
	if perfData.ErrorDiskTime == 0 {
		d.hardware.Disk.Percent = perfData.ResultDiskTime
	} else {
		d.hardware.Disk.Percent = 0.0
	}
}

func (d *Device) updateNetwork() {
	netStats, err := net.IOCounters(false)
	if err != nil || len(netStats) == 0 {
		return
	}

	currentStats := netStats[0]
	currentTime := time.Now()

	if !d.lastNetTime.IsZero() {
		timeDiff := currentTime.Sub(d.lastNetTime).Seconds()
		if timeDiff > 0 {
			sentDiff := currentStats.BytesSent - d.lastNetStats.BytesSent
			recvDiff := currentStats.BytesRecv - d.lastNetStats.BytesRecv

			d.hardware.Network.Sent = int(float64(sentDiff) / timeDiff)
			d.hardware.Network.Recv = int(float64(recvDiff) / timeDiff)
		}
	}

	d.lastNetStats = currentStats
	d.lastNetTime = currentTime
}

func Monitor() Hardware {
	device.mu.RLock()
	defer device.mu.RUnlock()

	return device.hardware
}

// 结束标志
var endFlag = make(chan bool)
var endDoneFlag = make(chan bool)

// 结束硬件监控
func EndMonitor() {
	close(endFlag)
	<-endDoneFlag
	EndPerformanceCounter()
}

// 开始硬件监控
func StartMonitor() {
	netStats, err := net.IOCounters(false)
	if err == nil && len(netStats) > 0 {
		device.lastNetStats = netStats[0]
	}
	device.lastNetTime = time.Now()

	StartPerformanceCounter()

	ticker := time.NewTicker(1 * time.Second)
	go func() {
		defer func() {
			fmt.Println("Start hardware monitor")
			ticker.Stop()
			close(endDoneFlag)
			fmt.Println("End hardware monitor")
		}()

		monitor()
		for {
			select {
			case <-ticker.C:
				monitor()
			case <-endFlag:
				return
			}
		}
	}()
}

/* ==== 硬盘存储值 ==== */
type DiskResult struct {
	Root    string  `json:"root"`    // 硬盘驱动号
	Total   float64 `json:"total"`   // 硬盘容量
	Free    float64 `json:"free"`    // 硬盘可用空间
	Percent float64 `json:"percent"` // 硬盘使用率
}

func DiskStorage() []DiskResult {
	partitions, err := disk.Partitions(false)
	if err != nil {
		return []DiskResult{}
	}

	var results []DiskResult

	for _, partition := range partitions {
		root := partition.Mountpoint

		usage, err := disk.Usage(root)
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

	return results
}

/* ==== 电池电量 ==== */
type BatteryResult struct {
	IsCharge bool    `json:"is_charge"` // 是否正在充电
	Percent  float64 `json:"percent"`   // 电量百分比
}

func BatteryPower() BatteryResult {
	batterys, err := Battery.GetAll()
	if err != nil {
		// 电池获取失败，返回正在充电和满电量，默认是插电台式机
		return BatteryResult{
			IsCharge: true,
			Percent:  1.0,
		}
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

	return results[0] // 暂时只返回主电池
}

/* ==== 系统信息 ==== */
type SystemInfo struct {
	Name    string `json:"name"`    // 主机名
	System  string `json:"system"`  // 操作系统
	Version string `json:"version"` // 操作系统版本
	Machine string `json:"machine"` // CPU 架构（x86_64、arm64）
}

func System() SystemInfo {
	hostInfo, err := host.Info()
	if err != nil {
		return SystemInfo{
			Name:    "Unknown",
			System:  "Unknown",
			Version: "Unknown",
			Machine: "Unknown",
		}
	}

	return SystemInfo{
		Name:    hostInfo.Hostname,
		System:  hostInfo.OS,
		Version: hostInfo.PlatformVersion,
		Machine: hostInfo.KernelArch,
	}
}
