package device

/*
#cgo LDFLAGS: -lpdh

#include <pdh.h>
#include <windows.h>

typedef struct returnData {
    DWORD errorDiskTime;
    double resultDiskTime;
    DWORD errorCpuFreq;
    double resultCpuFreq;
} data;

PDH_HQUERY hQuery = NULL;
PDH_HCOUNTER hCounterDiskTime = NULL;
PDH_HCOUNTER hCounterCpuFreq = NULL;

#define CPU_MAX_FREQ 1.0

data get() {
    data result;
    result.errorDiskTime = ERROR_SUCCESS;
    result.resultDiskTime = 0.0;
    result.errorCpuFreq = ERROR_SUCCESS;
    result.resultCpuFreq = 0.0;

    if (hQuery == NULL || hCounterDiskTime == NULL || hCounterCpuFreq == NULL) {
        return result;
    }

    PDH_STATUS pdhStatus = PdhCollectQueryData(hQuery);
    if (pdhStatus != ERROR_SUCCESS) {
        result.errorDiskTime = pdhStatus;
        return result;
    }

    PDH_FMT_COUNTERVALUE counterValueDiskTime;
    pdhStatus = PdhGetFormattedCounterValue(hCounterDiskTime, PDH_FMT_DOUBLE, 0, &counterValueDiskTime);
    result.errorDiskTime = pdhStatus;
    result.resultDiskTime = counterValueDiskTime.doubleValue;

    PDH_FMT_COUNTERVALUE counterValueCpuFreq;
    pdhStatus = PdhGetFormattedCounterValue(hCounterCpuFreq, PDH_FMT_DOUBLE, 0, &counterValueCpuFreq);
    result.errorCpuFreq = pdhStatus;
    result.resultCpuFreq = counterValueCpuFreq.doubleValue / 100000.0 * CPU_MAX_FREQ;

    return result;
}

DWORD start() {
    PDH_STATUS pdhStatus = PdhOpenQuery(NULL, 0, &hQuery);
    if (pdhStatus != ERROR_SUCCESS) {
        return pdhStatus;
    }

    pdhStatus = PdhAddCounter(hQuery, "\\PhysicalDisk(_Total)\\% Disk Time", 0, &hCounterDiskTime);
    if (pdhStatus != ERROR_SUCCESS) {
        return pdhStatus;
    }

    pdhStatus = PdhAddCounter(hQuery, "\\Processor Information(_Total)\\% Processor Performance", 0, &hCounterCpuFreq);
    if (pdhStatus != ERROR_SUCCESS) {
        return pdhStatus;
    }

    return ERROR_SUCCESS;
}

DWORD end() {
    if (hQuery == NULL) {
        return ERROR_SUCCESS;
    }

    PDH_STATUS pdhStatus;
    PDH_STATUS pdhError = ERROR_SUCCESS;

    if (hCounterDiskTime != NULL) {
        pdhStatus = PdhRemoveCounter(hCounterDiskTime);
        if (pdhStatus != ERROR_SUCCESS) {
            pdhError = pdhStatus;
        }
    }

    if (hCounterCpuFreq != NULL) {
        pdhStatus = PdhRemoveCounter(hCounterCpuFreq);
        if (pdhStatus != ERROR_SUCCESS) {
            pdhError = pdhStatus;
        }
    }

    pdhStatus = PdhCloseQuery(hQuery);
    if (pdhStatus != ERROR_SUCCESS) {
        pdhError = pdhStatus;
    }

    return pdhError;
}
*/
import "C"
import (
	"fmt"
)

type PerformanceCounterData struct {
	ErrorDiskTime  uint32
	ResultDiskTime float64
	ErrorCpuFreq   uint32
	ResultCpuFreq  float64
}

var (
	performanceCounterInitialized bool
)

func StartPerformanceCounter() error {
	if performanceCounterInitialized {
		return nil
	}

	result := C.start()
	if result != C.ERROR_SUCCESS {
		return fmt.Errorf("PDH start failed with error: 0x%08X", uint32(result))
	}

	performanceCounterInitialized = true

	GetPerformanceCounterData()

	return nil
}

func GetPerformanceCounterData() PerformanceCounterData {
	if !performanceCounterInitialized {
		return PerformanceCounterData{}
	}

	cData := C.get()

	result := PerformanceCounterData{
		ErrorDiskTime:  uint32(cData.errorDiskTime),
		ResultDiskTime: float64(cData.resultDiskTime),
		ErrorCpuFreq:   uint32(cData.errorCpuFreq),
		ResultCpuFreq:  float64(cData.resultCpuFreq),
	}

	const PDH_NO_DATA = 0xC0000BC6

	if result.ErrorDiskTime == PDH_NO_DATA {
		result.ErrorDiskTime = 0
		result.ResultDiskTime = 0.0
	}

	if result.ErrorCpuFreq == PDH_NO_DATA {
		result.ErrorCpuFreq = 0
		result.ResultCpuFreq = 0.0
	}

	return result
}

func EndPerformanceCounter() error {
	if !performanceCounterInitialized {
		return nil
	}

	result := C.end()
	if result != C.ERROR_SUCCESS {
		return fmt.Errorf("PDH end failed with error: 0x%08X", uint32(result))
	}

	performanceCounterInitialized = false
	return nil
}
