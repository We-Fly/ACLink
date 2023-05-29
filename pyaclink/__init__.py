# This is the __init__.py file for ACLink

from .defines import *
from .message import AC_MSG
import serial
import time

class AC_Vehicle():
    def __init__(self, port: str, baudrate: int = 115200, timeout:int = 3):
        self._msg = AC_MSG()
        while True:
            try:
                # 尝试打开串口
                self._serial = serial.Serial(port, baudrate, timeout = timeout)
                # 如果打开成功，就返回Vehicle对象，并且退出循环
                if isinstance(self._serial, serial.Serial):
                    print("串口设备 {} 打开成功".format(str(port)))
                    break
            except Exception as e:
                # 如果打开失败，就打印错误信息
                print(e)
                print("等待 {} 秒后重试...".format(timeout*3))
                time.sleep(timeout*3)
        
    def heartbeat(self, timeout:int = 1):
        '''
        心跳包检测功能
        '''
        if not self._serial.is_open:
            print("发送失败，串口设备已经关闭")
            return False
        self._serial.timeout = timeout
        ack = AC_MSG("ACLINK_ACK")
        bytes_to_send = bytes(ack.frame) # 把列表中的整数转换为字节
        self._serial.write(bytes_to_send) # 用串口对象的write()方法发送出去
        time.sleep(0.1) # 等待0.1秒
        read_buffer = list(self._serial.read(ack.payload_length + 5))
        if len(read_buffer) is not ack.payload_length + 5:
            print("心跳异常: 接收长度不一致")
            return False
        if read_buffer[0] is 0xFD:
            if read_buffer[ack.payload_length + 4] == ack.bcc and read_buffer[2] == 0 and read_buffer[1] == 0:
                return True
            else:
                print("心跳异常: 校验错误")
                return False
        else:
            print("心跳异常: 起始标记 != 0xFD")
            return False
    
    def close(self) -> None:
        self._serial.close()

