import board
import busio
import digitalio
import storage
import sdcardio
import os
import time
import usb_hid
import adafruit_ssd1306
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# ========== 1. 初始化硬件并显示炫酷启动界面 ==========
def show_progress(step, total, message):
    oled.fill(0)
    oled.text("BadUSB v3.3", 20, 5, 1)
    oled.text(message, 10, 25, 1)
    bar_width = int(100 * step / total)
    oled.fill_rect(14, 45, bar_width, 8, 1)
    oled.rect(14, 45, 100, 8, 1)
    oled.show()

# 初始化 I2C
i2c = busio.I2C(board.GP5, board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()

step = 0
total_steps = 4
show_progress(step, total_steps, "Init I2C..."); step += 1

# SD 卡
spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
cs = board.GP13
sdcard = sdcardio.SDCard(spi, cs, baudrate=500000)  # 降频至500kHz
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
show_progress(step, total_steps, "SD Card Ready"); step += 1

# 脚本列表
payload_dir = "/sd/payloads"
payload_files = []
try:
    payload_files = [f for f in os.listdir(payload_dir) if f.endswith(".txt")]
    payload_files.sort()
except:
    pass
show_progress(step, total_steps, f"Found {len(payload_files)} scripts"); step += 1

# 键盘
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
show_progress(step, total_steps, "HID Ready"); step += 1

time.sleep(0.5)
oled.fill(0)
oled.text("System Ready", 15, 30, 1)
oled.show()
time.sleep(0.8)

# ========== 2. 按钮 ==========
btn_up = digitalio.DigitalInOut(board.GP0)
btn_up.direction = digitalio.Direction.INPUT
btn_up.pull = digitalio.Pull.UP
btn_down = digitalio.DigitalInOut(board.GP1)
btn_down.direction = digitalio.Direction.INPUT
btn_down.pull = digitalio.Pull.UP
btn_exec = digitalio.DigitalInOut(board.GP2)
btn_exec.direction = digitalio.Direction.INPUT
btn_exec.pull = digitalio.Pull.UP
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# ========== 3. 菜单（带闪烁“>”符号） ==========
selected = 0
blink_state = True          # 当前是否显示 ">"
last_blink = time.monotonic()
BLINK_INTERVAL = 0.4        # 闪烁间隔（秒）

def show_menu():
    oled.fill(0)
    oled.text("BadUSB Payloads", 5, 0, 1)
    if payload_files:
        for i in range(min(3, len(payload_files))):
            y = 16 + i * 12
            # 仅当该项被选中且闪烁状态为 True 时显示 ">"
            if i == selected and blink_state:
                prefix = "> "
            else:
                prefix = "  "
            name = payload_files[i][:13]
            oled.text(prefix + name, 5, y, 1)
    else:
        oled.text("No payloads found", 10, 30, 1)
    oled.show()

# ========== 4. 执行脚本（增强组合键 + 实时动画）==========
def send_key(key_name):
    """发送单个键"""
    if key_name.startswith('F') and key_name[1:].isdigit():
        f_num = int(key_name[1:])
        if 1 <= f_num <= 12:
            key = getattr(Keycode, f'F{f_num}', None)
            if key:
                keyboard.send(key)
                return True
    else:
        key = getattr(Keycode, key_name.upper(), None)
        if key:
            keyboard.send(key)
            return True
    return False

def run_payload(filename):
    led.value = True
    # 开始动画
    oled.fill(0)
    oled.text("Executing", 20, 25, 1)
    oled.show()
    for _ in range(2):
        oled.fill_rect(70, 25, 4, 4, 1)
        oled.show()
        time.sleep(0.08)
        oled.fill_rect(70, 25, 4, 4, 0)
        oled.show()
        time.sleep(0.08)

    full_path = payload_dir + "/" + filename
    with open(full_path, "r") as f:
        lines = f.readlines()

    keyboard.release_all()
    time.sleep(0.05)

    spinner = ['|', '/', '-', '\\']
    spin_idx = 0
    total_lines = len(lines)

    for idx, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split(' ', 1)
        cmd = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else ""

        # 显示当前命令和进度动画
        oled.fill(0)
        oled.text("Exec: " + cmd[:8], 0, 0, 1)
        short_name = filename[:10] + ".." if len(filename) > 12 else filename
        oled.text(short_name, 0, 12, 1)
        percent = int((idx+1) / total_lines * 100)
        oled.text(f"{percent}%", 100, 50, 1)
        spin_char = spinner[spin_idx % 4]
        oled.text(spin_char, 120, 50, 1)
        oled.show()
        spin_idx += 1

        # 执行指令
        if cmd == "DELAY":
            ms = int(arg) if arg else 0
            time.sleep(ms / 1000.0)
        elif cmd == "STRING":
            if arg:
                layout.write(arg)
        elif cmd in ("ENTER", "TAB", "SPACE"):
            key_map = {"ENTER": Keycode.ENTER, "TAB": Keycode.TAB, "SPACE": Keycode.SPACE}
            keyboard.send(key_map[cmd])
        elif cmd in ("CTRL", "ALT", "SHIFT", "WINDOWS", "GUI"):
            mod = cmd
            if arg:
                if len(arg) == 1 and arg.isalpha():
                    target = getattr(Keycode, arg.upper(), None)
                    if target:
                        mod_key = getattr(Keycode, mod, Keycode.CONTROL if mod=="CTRL" else Keycode.ALT if mod=="ALT" else Keycode.SHIFT if mod=="SHIFT" else Keycode.GUI)
                        keyboard.send(mod_key, target)
                elif arg.startswith('F') and arg[1:].isdigit():
                    f_num = int(arg[1:])
                    if 1 <= f_num <= 12:
                        target = getattr(Keycode, f'F{f_num}', None)
                        mod_key = getattr(Keycode, mod, Keycode.CONTROL if mod=="CTRL" else Keycode.ALT if mod=="ALT" else Keycode.SHIFT if mod=="SHIFT" else Keycode.GUI)
                        if target:
                            keyboard.send(mod_key, target)
                else:
                    target = getattr(Keycode, arg.upper(), None)
                    mod_key = getattr(Keycode, mod, Keycode.CONTROL if mod=="CTRL" else Keycode.ALT if mod=="ALT" else Keycode.SHIFT if mod=="SHIFT" else Keycode.GUI)
                    if target:
                        keyboard.send(mod_key, target)
            else:
                mod_key = getattr(Keycode, mod, Keycode.CONTROL if mod=="CTRL" else Keycode.ALT if mod=="ALT" else Keycode.SHIFT if mod=="SHIFT" else Keycode.GUI)
                keyboard.send(mod_key)
        else:
            send_key(cmd)

        time.sleep(0.008)

    keyboard.release_all()
    oled.fill(0)
    oled.text("Done!", 50, 30, 1)
    oled.show()
    time.sleep(0.8)
    led.value = False
    show_menu()

# ========== 5. 防抖 ==========
def wait_for_release(pin):
    while not pin.value:
        time.sleep(0.02)
    time.sleep(0.03)

# ========== 6. 主循环（含菜单闪烁） ==========
if payload_files:
    show_menu()
else:
    oled.fill(0)
    oled.text("No payloads", 20, 30, 1)
    oled.show()

while True:
    # 定时翻转闪烁状态
    now = time.monotonic()
    if now - last_blink >= BLINK_INTERVAL:
        blink_state = not blink_state
        last_blink = now
        if payload_files:
            show_menu()   # 刷新菜单，实现 ">" 闪烁

    # 按钮检测
    if not btn_up.value:
        if payload_files:
            selected = (selected - 1) % len(payload_files)
            blink_state = True          # 按下按钮时强制显示 ">"
            show_menu()
        wait_for_release(btn_up)
    if not btn_down.value:
        if payload_files:
            selected = (selected + 1) % len(payload_files)
            blink_state = True
            show_menu()
        wait_for_release(btn_down)
    if not btn_exec.value and payload_files:
        run_payload(payload_files[selected])
        wait_for_release(btn_exec)
    time.sleep(0.01)
