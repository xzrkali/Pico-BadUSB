import storage

# 禁用 USB 大容量存储，电脑不会识别为磁盘，避免资源管理器卡顿
# 如需修改代码，请按住 BOOTSEL 键再插入 USB 即可进入安全模式
storage.disable_usb_drive()
