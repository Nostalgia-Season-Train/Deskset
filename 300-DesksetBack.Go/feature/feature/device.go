package feature

import (
	"fmt"
	"time"
)

// 硬件信息
var i = 0

// 硬件监控：刷新一次硬件信息
func monitor() {
	i++
	fmt.Println("i =", i)
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
