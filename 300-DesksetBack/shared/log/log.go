package log

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"

	"DesksetBack/shared/constant"
)

var (
	logFile *os.File
	logger  *log.Logger
)

type LogLevel int

const (
	INFO LogLevel = iota
	WARNING
	ERROR
	EXCEPTION
	PANIC
)

func openLogger() error {
	if err := os.MkdirAll(constant.LogDir, 0o755); err != nil {
		return fmt.Errorf("Failed to create log directory: %w", err)
	}

	logTime := time.Now().Format(constant.LogStemFormat)
	logPath := filepath.Join(constant.LogDir, constant.LogStemPrefix+logTime+"."+constant.LogExtn)

	var err error
	logFile, err = os.OpenFile(logPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0o644)
	if err != nil {
		return fmt.Errorf("Failed to create log file: %w", err)
	}

	logger = log.New(logFile, "", 0)
	return nil
}

func closeLogger() {
	if logFile != nil {
		logFile.Close()
	}
}

func SetupLogger() (func(), error) {
	if err := openLogger(); err != nil {
		return nil, err
	}
	return closeLogger, nil
}

func logMessage(level LogLevel, message string) {
	if logger == nil {
		if err := openLogger(); err != nil {
			log.Printf("Failed to open logger: %v", err)
			return
		}
	}

	timestamp := time.Now().Format("2006-01-02 15:04:05")
	levelStr := ""
	switch level {
	case INFO:
		levelStr = "INFO"
	case WARNING:
		levelStr = "WARNING"
	case ERROR:
		levelStr = "ERROR"
	case EXCEPTION:
		levelStr = "EXCEPTION"
	case PANIC:
		levelStr = "PANIC"
	default:
		levelStr = "UNKNOWN"
		return
	}

	logger.Printf("[%s] [%s]: %s", timestamp, levelStr, message)
}

func Info(message string) {
	logMessage(INFO, message)
}

func Warning(message string) {
	logMessage(WARNING, message)
}

func Error(message string) {
	logMessage(ERROR, message)
}
