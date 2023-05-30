'''本代码作为示例，演示如何使用本仓库pyaclink模块控制无人机起飞定高、降落。'''
# 导入pyaclink模块中的AC_Vehicle类和time模块
from pyaclink import AC_Vehicle
import time

# 创建一个AC_Vehicle实例，用于控制无人机
a9 = AC_Vehicle("COM21")

# 等待无人机的心跳信号，以确保与无人机建立了通信
while True:
    if a9.heartbeat():
        break
    time.sleep(0.1)

# 解锁无人机的电机，使其准备起飞
a9.aclink_motors_arm()
print("armed !")
time.sleep(3)

# 让无人机起飞到1米高度
a9.aclink_takeoff(1.0)
print("takeoff to 1.0 M!")
time.sleep(3)

# 让无人机降落
a9.aclink_land()
print("landing!")
time.sleep(3)

# 关闭与无人机的串口通信
a9.close()