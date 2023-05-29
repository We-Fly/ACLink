import sys, os

sys.path.append(os.path.abspath("../ACLink"))
sys.path.append(os.path.abspath("../"))

from pyaclink import *

msg = AC_MSG("ACLINK_CTRL_SPEED_ABSOLUTE")
print(msg.frame)