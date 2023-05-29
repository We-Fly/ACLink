import sys, os

sys.path.append(os.path.abspath("../ACLink"))
sys.path.append(os.path.abspath("../"))

from pyaclink import AC_MSG , AC_Vehicle
import time

a9 = AC_Vehicle("COM21")

while True:
    print("frame : {}".format(str(a9._msg.frame)))
    print(a9.heartbeat())
    time.sleep(0.1)