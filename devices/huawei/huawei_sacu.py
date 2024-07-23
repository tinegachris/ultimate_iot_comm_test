#
# This module is used to test Huawei SACU and sub-devices.
#

# SACU device communicates using Modbus TCP protocol.


## Importing required modules.
from comm_protocols.modbus_tcp_test import ModbusTcpTest
from tools.timer import Timer
from tools.logger import Logger

# HuaweiSacu ip address.
sacu_ip_address = "192.168.0.5"

# HuaweiSacu port number.
port_number = 502

# HuaweiSacu slave id.
sacu_slave_id = 0

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

# HuaweiSacu registers list
sacu_serial_num_reg = 40713 # string type, 10 registers

# This class is used to test Huawei SACU device.
class test_HuaweiSacu:
    def __init__(self):
        # Create a ModbusTcpTest object.
        self.modbus = ModbusTcpTest(sacu_ip_address, port_number)
        # Create a Timer object.
        self.timer = Timer()
        self.logger = Logger()
    
    # initiate connection to HuaweiSacu device.
    def connect(self):
        # Connect to the HuaweiSacu device.
        self.modbus.connect()
        
    # close connection to HuaweiSacu device.
    def disconnect(self):
        # Close the connection to the HuaweiSacu device.
        self.modbus.disconnect()
        
    # Read the serial number of HuaweiSacu device.
    def read_serial_num(self):
        # Read the serial number of HuaweiSacu device.
        serial_num = self.modbus.read_string(sacu_slave_id, sacu_serial_num_reg, 10)
        return serial_num

if __name__ == "__main__":
    # Create a test_HuaweiSacu object.
    test_sacu = test_HuaweiSacu()
    # Connect to the HuaweiSacu device.
    
    test_sacu.connect()
    
    if test_sacu.modbus.is_connected() == True:
        Logger.info("Connection to HuaweiSacu device is successful.")
        # Read the serial number of HuaweiSacu device.
        Logger.info("Reading the serial number of HuaweiSacu device...")
        # Reset the timer.
        test_sacu.timer.reset()
        # Start the timer.
        test_sacu.timer.start()
        # Read the serial number of HuaweiSacu device.
        serial_num = test_sacu.read_serial_num()
        # Stop the timer.
        test_sacu.timer.stop()
        # Display the serial number of HuaweiSacu device.
        Logger.info("Serial number of HuaweiSacu device: " + serial_num)
        # Display the time taken to read the serial number.
        Logger.info("Time taken to read the serial number: " + str(test_sacu.timer.elapsed_time()) + " seconds.")
        
    else:
        Logger.error("Connection to HuaweiSacu device is unsuccessful.")
    
    # Close the connection to the HuaweiSacu device.
    test_sacu.disconnect()

# End of script.