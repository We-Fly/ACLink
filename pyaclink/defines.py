# 消息ID

message_id = {
    "ACLINK_ACK": (0, 0),
    "ACLINK_MOTORS_ARM": (1, 0),
    "ACLINK_MOTORS_DISARM": (2, 0),
    "ACLINK_TAKEOFF": (3, 4),
    "ACLINK_LAND": (4, 0),
    "ACLINK_CTRL_SPEED_ABSOLUTE": (5, 13),
    "ACLINK_CTRL_SPEED_RELATIVE": (6, 13),
    "ACLINK_CTRL_POSITION_ABSOLUTE": (7, 13),
    "ACLINK_CTRL_POSITION_RELATIVE": (8, 13),
    "ACLINK_HOLD": (9, 1),
}

# 掩码
ACLINK_MASK_HOLD_X = 0b00001110 # 锁X
ACLINK_MASK_HOLD_Y = 0b00001101 # 锁Y
ACLINK_MASK_HOLD_Z = 0b00001011 # 锁Z
ACLINK_MASK_HOLD_YAW = 0b00000111 # 锁偏航角

ACLINK_MASK_DISABLE_X = 0b00001110 # 无效化对X的控制
ACLINK_MASK_DISABLE_Y = 0b00001101 # 无效化对Y的控制
ACLINK_MASK_DISABLE_Z = 0b00001011 # 无效化对Z的控制
ACLINK_MASK_DISABLE_YAW = 0b00000111 # 无效化对偏航角的控制