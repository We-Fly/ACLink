# 这个文件定义一个消息模板类和一些打包方法
from .defines import message_id as aclink_message_id

class AC_MSG():
    '''
    ACLink 的 消息打包类

    提供消息打包的一些功能
    '''

    def __init__(self, message_id = "ACLINK_ACK") -> None:
        self._start_tag = 0xFD # 起始标记
        self._seq = 0 # 消息序列号，发送计数器，用于检测丢包
        self.set_message_id(message_id)

    def set_message_id(self, message_id):
        '''
        设置消息ID
        '''
        if aclink_message_id[message_id] is not None: # 消息ID和有效荷载长度通过预定义字典获取
            self._message_id , self._payload_length = aclink_message_id[message_id]
        else:
            self._message_id = 0
            self._payload_length = 0
        self._payload = [0 for _ in range(self._payload_length)] # 使用列表推导式生成一个长度为n，元素为0的列表
        self._calc_bcc()

    def _calc_bcc(self) -> None:
        '''
        计算BCC校验
        '''
        bcc = 0
        m = lambda x: x % 0xff # 用于模0xff，限制一个字节的范围
        b = lambda x: bcc ^ m(x) # 取模后进行异或运算
        b(self._start_tag)
        b(self._payload_length)
        b(self._message_id)
        b(self.seq)
        for i in range(self._payload_length):
            b(self._payload[i])
        self._bcc = m(bcc)
        
    @property
    def frame(self): 
        '''
        打包成帧
        '''
        m = lambda x: x % 0xff # 用于模0xff，限制一个字节的范围
        frame = [0 for _ in range(self._payload_length + 5)]
        frame[0] = m(self._start_tag)
        frame[1] = m(self._payload_length)
        frame[2] = m(self._message_id)
        frame[3] = m(self.seq)
        for i in range(self._payload_length):
            frame[i + 4] = self._payload[i]
        frame[self._payload_length + 4] = m(self.bcc)
        return frame

    @property
    def seq(self):
        '''
        消息序列号，发送计数器，用于检测丢包

        返回模 `0xFF` 的结果
        '''
        return self._seq % 0xFF
        
    def set_seq(self, seq):
        '''
        设置消息序列号，没有模 `0xFF` 的数字
        '''
        self._seq = seq
    
    def seqpp(self):
        '''
        消息序列号自增
        '''
        self._seq += 1
    
    @property
    def bcc(self):
        '''
        计算并返回BCC校验值
        '''
        self._calc_bcc()
        return self._bcc
    
    def write_payload(self, payload):
        if len(payload) == self._payload_length:
            self._payload = payload
        else:
            print("error payload: length not match!\n")
