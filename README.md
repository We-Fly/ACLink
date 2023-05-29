# A9 自定义控制协议 —— ACLink

兼容 [conductor](https://github.com/We-Fly/conductor) 库

## 协议规范

通信协议包括了起始标记，有效荷载长度，消息ID，消息序列号，有效载荷数据，校验。

协议通过起始标记和有效荷载长度计算结束位置。

有效荷载长度不包括消息ID，消息序列号，和校验。

校验采用BCC校验

一个标准的数据帧格式如下

| 字段         | 长度(字节) | 描述                     |
| ------------ | ---------- | ------------------------ |
| 起始标记     | 1          | 0xFD                     |
| 有效荷载长度 | 1          | 0-255                    |
| 消息ID       | 1          | 0-255                    |
| 消息序列号   | 1          | 发送计数器，用于检测丢包 |
| 有效载荷数据 | 可变       | 消息的具体内容           |
| BCC校验      | 1          |                          |

## 消息ID的定义

| 值  | 字段名                                                          | 描述             |
| --- | --------------------------------------------------------------- | ---------------- |
| 0   | [ACLINK_ACK](#aclink_ack)                         | 心跳包         |
| 1   | [ACLINK_MOTORS_ARM](#aclink_motors_arm)                         | 解锁电机         |
| 2   | [ACLINK_MOTORS_DISARM](#aclink_motors_disarm)                   | 电机上锁         |
| 3   | [ACLINK_TAKEOFF](#aclink_takeoff)                               | 起飞到指定高度   |
| 4   | [ACLINK_LAND](#aclink_land)                                     | 降落             |
| 5   | [ACLINK_CTRL_SPEED_ABSOLUTE](#aclink_ctrl_speed_absolute)       | 绝对矢量速度控制 |
| 6   | [ACLINK_CTRL_SPEED_RELATIVE](#aclink_ctrl_speed_relative)       | 相对矢量速度控制 |
| 7   | [ACLINK_CTRL_POSITION_ABSOLUTE](#aclink_ctrl_position_absolute) | 绝对位置控制     |
| 8   | [ACLINK_CTRL_POSITION_RELATIVE](#aclink_ctrl_position_relative) | 相对位置控制     |
| 9   | [ACLINK_HOLD](#aclink_hold)                                     | 悬停（刹车）     |

### ACLINK_ACK

- `荷载` 没有荷载

- `作用` 用于测试对方是否在线，如果在线，对方会发送一个ACK作为应答

### ACLINK_MOTORS_ARM

- `荷载` 没有荷载

- `作用` 命令电机解锁，会进入怠速

### ACLINK_MOTORS_DISARM

- `荷载` 没有荷载

- `作用` 命令电机上锁，会令电机立即停止转动并上锁，不会判断飞行状态，请保证已经降落

### ACLINK_TAKEOFF

- `荷载`
  - `长度` 4 字节

  | 参数   | 数据类型 | 长度（字节） | 描述                |
  | ------ | -------- | ------------ | ------------------- |
  | height | float    | 4            | 起飞到指定高度（M） |

- `作用` 起飞到指定高度，如果已经起飞，就调整到指定高度。请确保飞机已经解锁

### ACLINK_LAND

- `荷载` 没有荷载

- `作用` 自动降落到地面，不会自动上锁，电机会进入怠速模式

### ACLINK_CTRL_SPEED_ABSOLUTE

- `荷载`
  - `长度` 13 字节

  | 参数 | 数据类型 | 长度（字节） | 描述                               | 单位  |
  | ---- | -------- | ------------ | ---------------------------------- | ----- |
  | MASK | uint8_t  | 1            | [位掩码](#位掩码)                  |       |
  | VX   | float    | 4            | 正值为向北前进，负值为向南前进     | cm/s  |
  | VY   | float    | 4            | 正值为向东前进，负值为向西前进     | cm/s  |
  | VZ   | float    | 4            | 正值为向下降落，负值为向上飞行     | cm/s  |
  | VYAW | float    | 4            | 正值为顺时针偏航，负值为逆时针偏航 | rad/s |

- `作用` 绝对速度控制，参考[NED坐标系](#ned坐标系)，由飞机上电初始化位置为基准，无论飞机朝向

### ACLINK_CTRL_SPEED_RELATIVE

- `荷载`
  - `长度` 13 字节

  | 参数 | 数据类型 | 长度（字节） | 描述                               | 单位  |
  | ---- | -------- | ------------ | ---------------------------------- | ----- |
  | MASK | uint8_t  | 1            | [位掩码](#位掩码)                  |       |
  | VX   | float    | 4            | 正值为向机头前进，负值为向机尾后退 | cm/s  |
  | VY   | float    | 4            | 正值为向右前进，负值为向左前进     | cm/s  |
  | VZ   | float    | 4            | 正值为向下降落，负值为向上飞行     | cm/s  |
  | VYAW | float    | 4            | 正值为顺时针偏航，负值为逆时针偏航 | rad/s |

- `作用` 相对速度控制，以飞机自身为参考系

### ACLINK_CTRL_POSITION_ABSOLUTE

- `荷载`
  - `长度` 13 字节

  | 参数 | 数据类型 | 长度（字节） | 描述                               | 单位 |
  | ---- | -------- | ------------ | ---------------------------------- | ---- |
  | MASK | uint8_t  | 1            | [位掩码](#位掩码)                  |      |
  | TX   | float    | 4            | 正值为向北前进，负值为向南前进     | cm   |
  | TY   | float    | 4            | 正值为向东前进，负值为向西前进     | cm   |
  | TZ   | float    | 4            | 正值为向下降落，负值为向上飞行     | cm   |
  | TYAW | float    | 4            | 正值为顺时针偏航，负值为逆时针偏航 | rad  |

- `作用` 绝对距离控制，参考[NED坐标系](#ned坐标系)，由飞机上电初始化位置为基准，无论飞机朝向

### ACLINK_CTRL_POSITION_RELATIVE

- `荷载`
  - `长度` 13 字节

  | 参数 | 数据类型 | 长度（字节） | 描述                               | 单位 |
  | ---- | -------- | ------------ | ---------------------------------- | ---- |
  | MASK | uint8_t  | 1            | [位掩码](#位掩码)                  |      |
  | TX   | float    | 4            | 正值为向机头前进，负值为向机尾后退 | cm   |
  | TY   | float    | 4            | 正值为向右前进，负值为向左前进     | cm   |
  | TZ   | float    | 4            | 正值为向下降落，负值为向上飞行     | cm   |
  | TYAW | float    | 4            | 正值为顺时针偏航，负值为逆时针偏航 | rad  |

- `作用` 相对距离控制，以飞机自身为参考系

### ACLINK_HOLD

- `荷载`
  - `长度` 1 字节

  | 参数 | 数据类型 | 长度（字节） | 描述     |
  | ---- | -------- | ------------ | -------- |
  | MASK | uint8_t  | 1            | 制动掩码 |

制动掩码代表一系列标记位，默认为 `b'00000000'` ，代表所有方向都上锁

```python
ACLINK_MASK_HOLD_X = 0b00001110 # 锁X
ACLINK_MASK_HOLD_Y = 0b00001101 # 锁Y
ACLINK_MASK_HOLD_Z = 0b00001011 # 锁Z
ACLINK_MASK_HOLD_YAW = 0b00000111 # 锁偏航角
```

- `作用` 命令飞机刹车，需要的话可以只锁偏航或者速度

## NED坐标系

```text
   北 ↑ X
      │ 
      │ ┄┄┄┄YAW ╮ 顺时针
      │         ↓
      │           东
      x ─────────────>
    地  z          Y
```

X为北

Y为东

Z为下

## 位掩码

位掩码用于表示一系列标记位，例如

```python
ACLINK_MASK_DISABLE_X = 0b00001110 # 无效化对X的控制
ACLINK_MASK_DISABLE_Y = 0b00001101 # 无效化对Y的控制
ACLINK_MASK_DISABLE_Z = 0b00001011 # 无效化对Z的控制
ACLINK_MASK_DISABLE_YAW = 0b00000111 # 无效化对偏航角的控制
```

从右往左代表参数1~8是否有效，0为False，1为True

或者代表一系列布尔值

## 许可信息

本仓库使用 `Apache-2.0` 协议进行许可。如果有任何侵权行为或者认为本仓库侵犯了您的权利，请在 [issue](https://github.com/We-Fly/ACLink/issues) 中提出，我会尽快反馈。

```text
Copyright 2023 Cody_Gu

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

```
