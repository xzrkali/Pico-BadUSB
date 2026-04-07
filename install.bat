@echo off
title Pico BadUSB Installer
echo ========================================
echo    Pico BadUSB - One-click Installer
echo ========================================
echo.
echo Please connect your Pico and note its drive letter (e.g., G:)
echo.
set /p "drive=Enter Pico drive letter (just the letter, e.g. G): "
set "drive=%drive::=%"
set "drive=%drive%:"
if not exist "%drive%" (
    echo.
    echo [ERROR] Drive %drive% does not exist.
    echo Please check the drive letter and try again.
    pause
    exit /b 1
)
echo.
echo [OK] Found %drive%
echo.

echo [1/4] Copying code.py...
if exist "code.py" (
    copy /Y "code.py" "%drive%\code.py"
) else (
    echo WARNING: code.py not found
)

echo.
echo [2/4] Copying boot.py...
if exist "boot.py" (
    copy /Y "boot.py" "%drive%\boot.py"
) else (
    echo WARNING: boot.py not found
)

echo.
echo [3/4] Copying lib folder...
if exist "lib" (
    xcopy /E /I /Y "lib" "%drive%\lib\"
) else (
    echo WARNING: lib folder not found
)

echo.
echo [4/4] Copying payloads folder...
if exist "payloads" (
    xcopy /E /I /Y "payloads" "%drive%\payloads\"
) else (
    echo WARNING: payloads folder not found
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