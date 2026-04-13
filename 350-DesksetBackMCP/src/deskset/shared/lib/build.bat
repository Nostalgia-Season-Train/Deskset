gcc -fPIC -shared "./Win32PerformanceCounter.c" -o "./Win32PerformanceCounter.dll" -lpdh


@REM === Test C Code ===

@REM chcp 65001
@REM gcc "./main.c" -o "./main.exe" -lpdh
@REM main.exe
@REM pause
