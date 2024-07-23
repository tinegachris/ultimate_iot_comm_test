#
# HUAWEI SACU communication test script
#

from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
import time
from time import sleep
import json
import logging
from logging.config import dictConfig

# SACU ip address, port and unit id
sacu_ip = '192.168.0.5'
sacu_port = 502
sacu_unit = 0

# Configure logging
logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

dictConfig(logging_config)
logger = logging.getLogger(__name__)

# Read SACU string value
def read_string_value(client, unit, address, length):
    # Read string value
    result = client.read_holding_registers(address, length, unit=unit)
    if result.isError():
        logger.error('Error reading string value')
        return None

    # Decode string value
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
    string_value = decoder.decode_string(length)

    return string_value
  
  # Read SACU 32-bit float value
def read_float_value(client, unit, address):
    # Read 32-bit float value
    result = client.read_holding_registers(address, 2, unit=unit)
    if result.isError():
        logger.error('Error reading 32-bit float value')
        return None

    # Decode 32-bit float value
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
    float_value = decoder.decode_32bit_float()

    return float_value
  
  # Write SACU 32-bit float value
def write_float_value(client, unit, address, value):
    # Encode 32-bit float value
    builder = BinaryPayloadBuilder(byteorder=Endian.Big)
    builder.add_32bit_float(value)
    payload = builder.build()

    # Write 32-bit float value
    result = client.write_registers(address, payload, unit=unit)
    if result.isError():
        logger.error('Error writing 32-bit float value')
        return False

    return True
  
  # Read SACU 16-bit integer value
def read_int_value(client, unit, address):
    # Read 16-bit integer value
    result = client.read_holding_registers(address, 1, unit=unit)
    if result.isError():
        logger.error('Error reading 16-bit integer value')
        return None

    # Decode 16-bit integer value
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
    int_value = decoder.decode_16bit_int()

    return int_value
  
  # Write SACU 16-bit integer value
def write_int_value(client, unit, address, value):
    # Encode 16-bit integer value
    builder = BinaryPayloadBuilder(byteorder=Endian.Big)
    builder.add_16bit_int(value)
    payload = builder.build()

    # Write 16-bit integer value
    result = client.write_registers(address, payload, unit=unit)
    if result.isError():
        logger.error('Error writing 16-bit integer value')
        return False

    return True
  
  # Read SACU digital value
def read_digital_value(client, unit, address):
    # Read digital value
    result = client.read_coils(address, 1, unit=unit)
    if result.isError():
        logger.error('Error reading digital value')
        return None

    return result.bits[0]
  
  # Write SACU digital value
def write_digital_value(client, unit, address, value):
    # Write digital value
    result = client.write_coil(address, value, unit=unit)
    if result.isError():
        logger.error('Error writing digital value')
        return False

    return True

# Calculate how long it takes to read or write a value
def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    elapsed_time = end_time - start_time

    return result, elapsed_time

if __name__ == '__main__':
    # Connect to SACU
    client = ModbusClient(sacu_ip, port=sacu_port)
    client.connect()

    if client.is_socket_open():
        logger.info('Connected to SACU %s:%d', sacu_ip, sacu_port)
    else:
        logger.error('Error connecting to SACU %s:%d', sacu_ip, sacu_port)
        exit(1)
    
    while True:
      # Read SACU serial number string from address 40713, length 10
      serial_number = read_string_value(client, sacu_unit, 40713, 10)
      # Measure how long it takes to read SACU serial number
      _, elapsed_time = measure_time(read_string_value, client, sacu_unit, 40713, 10)
      # Log the measured time
      logger.info('Reading SACU serial number took %.2f seconds', elapsed_time)
      # Log the SACU serial number if it is not None or log an error message
      if serial_number is not None:
        logger.info('SACU serial number: %s', serial_number)
      else:
        logger.error('Error reading SACU serial number')
      # Wait for 5 seconds
      sleep(5)