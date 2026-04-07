@echo off
title Pico BadUSB Installer
echo ========================================
echo    Pico BadUSB - One-click Installer
echo ========================================
echo.

set "CIRCUITPY_DRIVE="
for %%d in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%d:\CIRCUITPY" (
        set "CIRCUITPY_DRIVE=%%d:"
        goto :found
    )
)

:not_found
echo [ERROR] CIRCUITPY drive not found!
echo Please make sure:
echo   1. Pico is connected via USB
echo   2. CircuitPython firmware is installed
echo   3. If connected, press RESET button on Pico and try again
echo.
pause
exit /b 1

:found
echo [OK] Found CIRCUITPY at %CIRCUITPY_DRIVE%
echo.

echo [1/4] Copying code.py ...
if exist "code.py" (
    copy /Y "code.py" "%CIRCUITPY_DRIVE%\code.py" >nul
    echo       Done
) else (
    echo       Warning: code.py not found, skipped
)

echo [2/4] Copying boot.py ...
if exist "boot.py" (
    copy /Y "boot.py" "%CIRCUITPY_DRIVE%\boot.py" >nul
    echo       Done
) else (
    echo       Warning: boot.py not found, skipped
)

echo [3/4] Copying lib folder ...
if exist "lib" (
    xcopy /E /I /Y "lib" "%CIRCUITPY_DRIVE%\lib\" >nul
    echo       Done
) else (
    echo       Warning: lib folder not found, skipped
)

echo [4/4] Copying payloads folder ...
if exist "payloads" (
    xcopy /E /I /Y "payloads" "%CIRCUITPY_DRIVE%\payloads\" >nul
    echo       Done
) else (
    echo       Warning: payloads folder not found, skipped
)

echo.
echo ========================================
echo   Installation complete!
echo ========================================
echo.
echo Next steps:
echo   1. Safely eject Pico
echo   2. Insert SD card (FAT32, create 'payloads' folder)
echo   3. Reconnect Pico, OLED menu will appear
echo.
pause
exit /b 0
