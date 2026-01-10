#include <pdh.h>
#include <stdio.h>

typedef struct returnData {
    DWORD errorDiskTime;
    double resultDiskTime;
    DWORD errorCpuFreq;
    double resultCpuFreq;
} data;

PDH_HQUERY hQuery = NULL;  // 查询句柄
PDH_HCOUNTER hCounterDiskTime = NULL;  // 硬盘计数器句柄
PDH_HCOUNTER hCounterCpuFreq = NULL;   // CPU 计数器句柄

#define CPU_MAX_FREQ 1.0  // 当前频率 = CpuFreq * CPU_MAX_FREQ

// 注：首次调用返回 0xC0000BC6，后续调用正常
  // 原因：PdhCollectQueryData 首次调用得到的数据无效，
    // 随后 PdhGetFormattedCounterValue 对该无效数据出错 0xC0000BC6
data get() {
    if (hQuery == NULL || hCounterDiskTime == NULL || hCounterCpuFreq == NULL) {
        data data = { ERROR_SUCCESS, 0.0, ERROR_SUCCESS, 0.0 };
        return data;
    }

    PDH_STATUS pdhStatus;

    // 第一步：收集数据
    pdhStatus = PdhCollectQueryData(hQuery);
    if (pdhStatus != ERROR_SUCCESS) {
        data data = { pdhStatus, 0.0, ERROR_SUCCESS, 0.0 };
        return data;
    }

    // 第二步：获取并格式化数据
    PDH_STATUS pdhStatusDiskTime;
    PDH_FMT_COUNTERVALUE counterValueDiskTime;
    pdhStatusDiskTime = PdhGetFormattedCounterValue(hCounterDiskTime, PDH_FMT_DOUBLE, 0, &counterValueDiskTime);

    PDH_STATUS pdhStatusCpuFreq;
    PDH_FMT_COUNTERVALUE counterValueCpuFreq;
    pdhStatusCpuFreq = PdhGetFormattedCounterValue(hCounterCpuFreq, PDH_FMT_DOUBLE, 0, &counterValueCpuFreq);

    data data = {
        pdhStatusDiskTime,
        counterValueDiskTime.doubleValue,
        pdhStatusCpuFreq,
        counterValueCpuFreq.doubleValue / 100000 * CPU_MAX_FREQ
    };
    return data;
}

DWORD start() {
    PDH_STATUS pdhStatus;  // 实测类型为 unsigned long 跟 DWORD 一致

    // 第一步：创建并打开查询
    pdhStatus = PdhOpenQuery(NULL, 0, &hQuery);
    if (pdhStatus != ERROR_SUCCESS) {
        return pdhStatus;
    }

    // 第二步：添加计数器
    pdhStatus = PdhAddCounter(hQuery, "\\PhysicalDisk(_Total)\\% Disk Time", 0, &hCounterDiskTime);  // 性能监视器/PhysicalDisk
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

    // 第一步：移除计数器
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

    // 第二步：关闭查询
    pdhStatus = PdhCloseQuery(hQuery);
    if (pdhStatus != ERROR_SUCCESS) {
        pdhError = pdhStatus;
    }

    return pdhError;
}


/* 测试程序 */
int main() {
    start();
    while (TRUE) {
        printf("磁盘活动时间: %.2f%%\n", get().resultDiskTime);
        Sleep(1000);
    }
    end();

    return 0;
}
