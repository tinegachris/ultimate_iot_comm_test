#
# This module is used to test the Modbus TCP protocol.
#

from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus import iteritems
from tools import Timer
from tools import Logger

# This class is used to test the Modbus TCP protocol.
class ModbusTcpTest:
    def __init__(self):
        pass
    
    