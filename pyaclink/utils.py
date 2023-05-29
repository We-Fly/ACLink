import struct # 导入struct模块

def float_to_list(num: float) -> list: # 定义一个函数，接受一个float类型的数字作为参数
    '''
    输入一个float类型的数字，转换成一个四个元素的列表，每个元素都是一个0~255的无符号整型。
    '''
    binary_data = struct.pack("f", num) # 把float类型的数字转换为一个四字节的二进制数据
    a, b, c, d = struct.unpack("BBBB", binary_data) # 把二进制数据解包为四个无符号整型
    lst = [a, b, c, d] # 把四个无符号整型放入一个列表中
    return lst # 返回列表

def write_float(payload: list, insert: int, num: float) -> list:
    payload[insert:insert + 4] = float_to_list(num)
    return payload

def read_float(payload: list, start: int) -> float:
    num = list_to_float(payload[start:start + 4])
    return num

def list_to_float(lst) -> float: # 定义一个函数，接受一个列表作为参数
    '''
    输入一个四个元素的列表，每个元素都是一个0~255的无符号整型，转换成一个float类型的数字。
    '''
    binary_data = struct.pack("BBBB", *lst) # 把列表中的四个无符号整型转换为一个四字节的二进制数据
    num, = struct.unpack("f", binary_data) # 把二进制数据解包为一个float类型的数字
    return num # 返回数字

