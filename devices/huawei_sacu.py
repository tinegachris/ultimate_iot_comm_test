#
# This module is used to test Huawei SACU and sub-devices.
#

# SACU device communicates using Modbus TCP protocol.


## Importing required modules.
from comm_protocols import ModbusTcpTest
from tools import Timer
from tools import Logger

# HuaweiSacu ip address.
ip_address = "192.168.0.5"

# HuaweiSacu port number.
port_number = 502

# HuaweiSacu slave id.
slave_id = 0

# HuaweiSacu sub_devices slave ids.
sacu_pcs_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sacu_bms_id = [11]

# HuaweiSacu PCS device list.
pcs_list = []
for i in range(0, len(sacu_pcs_id)):
    pcs_list.append("PCS" + str(sacu_pcs_id[i]))

# HuaweiSacu BMS device list.
bms_list = []
for i in range(0, len(sacu_bms_id)):
    bms_list.append("BMS" + str(sacu_bms_id[i]))

# HuaweiSacu registers list.
sacu_serial_number_register = 40713


# This class is used to test Huawei SACU device.
class test_HuaweiSacu:
    def __init__(self):
        pass

