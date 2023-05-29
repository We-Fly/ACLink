from pyaclink import AC_Vehicle
import time

a9 = AC_Vehicle("COM21")

while True:
    if a9.heartbeat():
        break
    time.sleep(0.1)

a9.aclink_motors_arm()
print("armed !")
time.sleep(3)

a9.aclink_takeoff(1.0)
print("takeoff to 1.0 M!")
time.sleep(3)

a9.aclink_land()
print("landing!")
time.sleep(3)

a9.close()