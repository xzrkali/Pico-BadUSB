@echo off
title Pico BadUSB Installer
echo ========================================
echo    Pico BadUSB - 一键安装脚本
echo ========================================
echo.

:: 寻找 CIRCUITPY 盘符
set "CIRCUITPY_DRIVE="
for %%d in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%d:\CIRCUITPY" (
        set "CIRCUITPY_DRIVE=%%d:"
        goto :found
    )
)

:not_found
echo [错误] 未找到 CIRCUITPY 盘符！
echo 请确保：
echo   1. Pico 已通过 USB 连接到电脑
echo   2. Pico 已刷入 CircuitPython 固件
echo   3. 如果已经连接，请按一下 Pico 上的 RESET 键重试
echo.
pause
exit /b 1

:found
echo [成功] 检测到 CIRCUITPY 盘符：%CIRCUITPY_DRIVE%
echo.

:: 复制文件
echo [1/4] 复制 code.py ...
if exist "code.py" (
    copy /Y "code.py" "%CIRCUITPY_DRIVE%\code.py" >nul
    echo       完成
) else (
    echo       警告：code.py 不存在，跳过
)

echo [2/4] 复制 boot.py ...
if exist "boot.py" (
    copy /Y "boot.py" "%CIRCUITPY_DRIVE%\boot.py" >nul
    echo       完成
) else (
    echo       警告：boot.py 不存在，跳过
)

echo [3/4] 复制 lib 文件夹 ...
if exist "lib" (
    xcopy /E /I /Y "lib" "%CIRCUITPY_DRIVE%\lib\" >nul
    echo       完成
) else (
    echo       警告：lib 文件夹不存在，跳过
)

echo [4/4] 复制 payloads 示例文件夹 ...
if exist "payloads" (
    xcopy /E /I /Y "payloads" "%CIRCUITPY_DRIVE%\payloads\" >nul
    echo       完成
) else (
    echo       警告：payloads 文件夹不存在，跳过
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 接下来请：
echo   1. 安全弹出 Pico（右键弹出磁盘）
echo   2. 将 SD 卡插入模块（格式化为 FAT32，根目录创建 payloads 文件夹）
echo   3. 重新插拔 Pico，即可使用 OLED 菜单
echo.
pause
exit /b 0
