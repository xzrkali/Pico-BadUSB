@echo off
title Pico BadUSB Installer
echo ========================================
echo    Pico BadUSB - One-click Installer
echo ========================================
echo.

set "PICO_DRIVE="

:: 1. 优先通过卷标 CIRCUITPY 查找
for /f "tokens=2 delims==" %%d in ('wmic volume where "Label='CIRCUITPY'" get DeviceID /value 2^>nul ^| find "="') do (
    set "PICO_DRIVE=%%d"
    goto :found
)

:: 2. 如果没有，则查找可移动磁盘 (DriveType=2)
for /f "skip=1 tokens=1" %%d in ('wmic logicaldisk where "DriveType=2" get DeviceID 2^>nul') do (
    if exist "%%d\" (
        :: 检查是否包含项目文件
        if exist "%%d\code.py" (
            set "PICO_DRIVE=%%d"
            goto :found
        )
        if exist "%%d\boot.py" (
            set "PICO_DRIVE=%%d"
            goto :found
        )
        if exist "%%d\lib" (
            set "PICO_DRIVE=%%d"
            goto :found
        )
    )
)

:: 3. 最后回退到遍历 D-Z 查找（原逻辑）
for %%d in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%d:\code.py" (
        set "PICO_DRIVE=%%d:"
        goto :found
    )
    if exist "%%d:\boot.py" (
        set "PICO_DRIVE=%%d:"
        goto :found
    )
    if exist "%%d:\lib" (
        set "PICO_DRIVE=%%d:"
        goto :found
    )
)

:not_found
echo [ERROR] Could not find Pico drive.
echo Please ensure:
echo   1. Pico is connected via USB
echo   2. CircuitPython firmware is installed
echo   3. The drive letter is between D: and Z:
echo.
echo You can also manually copy files to the Pico drive.
pause
exit /b 1

:found
echo [OK] Found Pico at %PICO_DRIVE%
echo.

echo [1/4] Copying code.py...
if exist "code.py" (
    copy /Y "code.py" "%PICO_DRIVE%\code.py"
) else (
    echo WARNING: code.py not found, skipping
)

echo.
echo [2/4] Copying boot.py...
if exist "boot.py" (
    copy /Y "boot.py" "%PICO_DRIVE%\boot.py"
) else (
    echo WARNING: boot.py not found, skipping
)

echo.
echo [3/4] Copying lib folder...
if exist "lib" (
    xcopy /E /I /Y "lib" "%PICO_DRIVE%\lib\"
) else (
    echo WARNING: lib folder not found, skipping
)

echo.
echo [4/4] Copying payloads folder...
if exist "payloads" (
    xcopy /E /I /Y "payloads" "%PICO_DRIVE%\payloads\"
) else (
    echo WARNING: payloads folder not found, skipping
)

echo.
echo ========================================
echo   Installation complete!
echo ========================================
echo.
echo Next steps:
echo   1. Safely eject Pico
echo   2. Insert SD card (FAT32, with 'payloads' folder)
echo   3. Reconnect Pico
echo.
pause
exit /b 0