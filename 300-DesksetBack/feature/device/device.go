package device

import (
	"fmt"
	"runtime"
	"sync"
	"time"

	"github.com/shirou/gopsutil/v4/cpu"
	"github.com/shirou/gopsutil/v4/disk"
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

	device.updateCPU()
	device.updateRAM()
	device.updateDisk()
	device.updateNetwork()
}

func (d *Device) updateCPU() {
	percent, err := cpu.Percent(0, false)
	if err == nil && len(percent) > 0 {
		d.hardware.CPU.Percent = percent[0]
	}

	freqInfo, err := cpu.Info()
	if err == nil && len(freqInfo) > 0 {
		maxFreq := freqInfo[0].Mhz
		if maxFreq > 0 {
			d.hardware.CPU.Freq = float64(maxFreq) / 1000.0
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

func (d *Device) updateDisk() {
	diskInfo, err := disk.Usage("/")
	if err != nil {
		diskInfo, err = disk.Usage("C:\\")
	}
	if err == nil {
		d.hardware.Disk.Percent = diskInfo.UsedPercent
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
}

// 开始硬件监控
func StartMonitor() {
	netStats, err := net.IOCounters(false)
	if err == nil && len(netStats) > 0 {
		device.lastNetStats = netStats[0]
	}
	device.lastNetTime = time.Now()

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
