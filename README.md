# Pico BadUSB – 可编程橡皮鸭 (Rubber Ducky) 带 OLED 菜单

[English](#english) | [中文](#中文)

---

## 中文

### 简介
这是一个基于 **树莓派 Pico** + **CircuitPython** 的 BadUSB 工具。它通过模拟键盘执行预先存储在 SD 卡中的脚本，可用于自动化测试、教学演示或授权的安全评估。  
**特点**：  
- 0.96 寸 OLED 屏幕 (SSD1306, I2C) 显示菜单  
- 三个物理按钮：上/下选择，执行脚本  
- 支持 SD 卡存储多个脚本（格式类似 Ducky Script）  
- 支持 `DELAY`, `STRING`, `ENTER`, `TAB`, `CTRL`, `ALT`, `SHIFT`, `WINDOWS`, `GUI`, `RUN` 等指令  
- 执行时实时显示进度百分比和动画  
- 启动进度条，菜单选中项闪烁  
- 可禁用 USB 大容量存储（避免电脑卡顿），通过按住 BOOTSEL 键进入安全模式修改代码  

### 免责声明 ⚠️
**本工具仅供学习、自动化测试、授权安全评估使用。严禁用于任何非法活动。**  
任何未经授权使用本工具造成的后果与本人无关。使用者须自行承担所有法律责任。  
**我是一名 16 岁的学生，可能无法长期维护该项目，请理解。**  
如果你觉得这个项目有帮助，可以请我喝杯咖啡 ☕️（微信支持二维码见下方）。如果你基于本项目扩展或改进，希望你能记得提及原作者，谢谢！

### 支持作者
<img src="https://raw.githubusercontent.com/xzrkali/Pico-BadUSB/main/%E5%BE%AE%E4%BF%A1%E6%94%AF%E4%BB%98.png" width="200" alt="微信赞赏码" />  

### 硬件接线
| 组件         | Pico 引脚       |
|--------------|-----------------|
| OLED SDA     | GP4 (I2C0 SDA)  |
| OLED SCL     | GP5 (I2C0 SCL)  |
| 按钮 上      | GP0 (内部上拉)  |
| 按钮 下      | GP1 (内部上拉)  |
| 按钮 执行    | GP2 (内部上拉)  |
| SD 卡 CS     | GP13            |
| SD 卡 SCK    | GP10 (SPI1)     |
| SD 卡 MOSI   | GP11            |
| SD 卡 MISO   | GP12            |
| 所有 GND     | GND             |

> 注意：SD 卡模块请使用 3.3V 或 5V 供电（取决于模块），并确保与 Pico 共地。

### 快速开始
1. **安装 CircuitPython**：从 [circuitpython.org](https://circuitpython.org/board/raspberry_pi_pico/) 下载对应 Pico 的固件，按住 BOOTSEL 键将 `.uf2` 文件拖入 `RPI-RP2` 盘。
2. **下载本项目**：将 `code.py`, `boot.py` 以及 `lib` 文件夹复制到 `CIRCUITPY` 盘的根目录。
3. **准备 SD 卡**：格式化为 FAT32，在根目录创建 `payloads` 文件夹，将你的脚本（`.txt` 文件）放入其中。
4. **接线并重启**：按接线图连接硬件，重启 Pico 即可看到 OLED 菜单。
5. **使用**：通过上/下键选择脚本，按执行键运行。脚本格式见下文。

### 脚本语法
每行一条指令，支持：
- `DELAY 500`   → 延时 500 毫秒
- `STRING Hello` → 输入字符串 "Hello"
- `ENTER` / `TAB` / `SPACE` → 发送按键
- `CTRL c` / `ALT F4` / `SHIFT a` / `WINDOWS r` → 组合键
- `RUN notepad.exe` → 按 Win+R 并输入命令运行（不复制文件）
- 单键：`A`, `B`, `1`, `F1` 等

示例脚本 (`popup.txt`)：

'''txt
DELAY 1000
WINDOWS r
DELAY 500
STRING notepad
ENTER
DELAY 1000
STRING Hello from BadUSB!
ENTER
txt'''


### 注意事项
- 默认禁用 USB 存储（避免电脑资源管理器卡顿）。如需修改代码，请按住 Pico 上的 **BOOTSEL** 键再插入 USB，此时会进入安全模式，`CIRCUITPY` 盘会重新出现。
- SD 卡质量可能影响稳定性，推荐使用 4-32GB 的 Class 10 卡。

### 项目链接
GitHub: [https://github.com/xzrkali/Pico-BadUSB](https://github.com/xzrkali/Pico-BadUSB)  
*（如果你喜欢这个项目，欢迎 Star 或 Fork！）*

### 许可证
[MIT License](LICENSE)

---

## English

### Pico BadUSB – Rubber Ducky with OLED Menu

### Introduction
This is a **Raspberry Pi Pico** + **CircuitPython** based BadUSB tool. It emulates a keyboard to execute pre‑stored scripts from an SD card, suitable for automation testing, educational demos, or authorized security assessments.  

**Features**:  
- 0.96" OLED display (SSD1306, I2C) with menu  
- Three physical buttons: Up / Down / Execute  
- SD card storage for multiple scripts (Ducky‑Script like syntax)  
- Supported commands: `DELAY`, `STRING`, `ENTER`, `TAB`, `CTRL`, `ALT`, `SHIFT`, `WINDOWS`, `GUI`, `RUN`  
- Real‑time progress percentage and animation during execution  
- Boot progress bar, blinking selected menu item  
- USB mass storage can be disabled (prevents Windows explorer freeze); hold BOOTSEL while connecting to enter safe mode for code modifications  

### Disclaimer ⚠️
**This tool is intended for educational purposes, automation testing, and authorized security assessments only. Do NOT use it for any illegal activities.**  
The author is not responsible for any consequences arising from unauthorized or illegal use. You assume all legal liabilities.  
**I am a 16‑year‑old student and may not be able to maintain this project long‑term – please understand.**  
If you find this project helpful, you can buy me a coffee ☕️ (WeChat QR code below). If you extend or improve this project, I would appreciate it if you could mention the original author. Thank you!

### Support the Author
<img src="https://raw.githubusercontent.com/xzrkali/Pico-BadUSB/main/%E5%BE%AE%E4%BF%A1%E6%94%AF%E4%BB%98.png" width="200" alt="WeChat Donation QR Code" />  

### Hardware Wiring
| Component      | Pico Pin           |
|----------------|--------------------|
| OLED SDA       | GP4 (I2C0 SDA)     |
| OLED SCL       | GP5 (I2C0 SCL)     |
| Button Up      | GP0 (internal pull‑up) |
| Button Down    | GP1 (internal pull‑up) |
| Button Execute | GP2 (internal pull‑up) |
| SD Card CS     | GP13               |
| SD Card SCK    | GP10 (SPI1)        |
| SD Card MOSI   | GP11               |
| SD Card MISO   | GP12               |
| All GND        | GND                |

> Note: Use 3.3V or 5V for the SD card module depending on its specification, and make sure to share ground with the Pico.

### Quick Start
1. **Install CircuitPython** – Download the firmware for Pico from [circuitpython.org](https://circuitpython.org/board/raspberry_pi_pico/), hold BOOTSEL and drag the `.uf2` file onto the `RPI-RP2` drive.
2. **Download this repository** – Copy `code.py`, `boot.py`, and the `lib` folder to the root of the `CIRCUITPY` drive.
3. **Prepare the SD card** – Format as FAT32, create a folder `payloads` in the root, and put your script (`.txt`) files inside it.
4. **Connect hardware and reboot** – Follow the wiring table, restart the Pico, and the OLED menu should appear.
5. **Usage** – Use Up/Down to select a script, press Execute to run it. Script syntax described below.

### Script Syntax
One command per line. Supported:
- `DELAY 500`   → Wait 500 ms
- `STRING Hello` → Type "Hello"
- `ENTER` / `TAB` / `SPACE` → Send key
- `CTRL c` / `ALT F4` / `SHIFT a` / `WINDOWS r` → Modifier + key
- `RUN notepad.exe` → Win+R and enter command (no file copy)
- Single keys: `A`, `B`, `1`, `F1`, etc.

Example script (`popup.txt`):

```txt
DELAY 1000
WINDOWS r
DELAY 500
STRING notepad
ENTER
DELAY 1000
STRING Hello from BadUSB!
ENTER
text

### Important Notes
- USB mass storage is disabled by default (to prevent Windows explorer from freezing). To modify the code, hold the **BOOTSEL** button while connecting the Pico to USB – this enters safe mode and the `CIRCUITPY` drive will reappear.
- SD card quality may affect stability; a 4‑32 GB Class 10 card is recommended.

### Project Link
GitHub: [https://github.com/xzrkali/Pico-BadUSB](https://github.com/xzrkali/Pico-BadUSB)  
*(If you like this project, please give it a Star or Fork!)*

### License
[MIT License](LICENSE)
