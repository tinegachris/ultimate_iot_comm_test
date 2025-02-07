import os
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from time import sleep
import logging
from typing import Callable, List, Optional, Union

# Configure the client logging
logging.basicConfig(
  format='[%(asctime)s] [%(filename)s: %(lineno)s - %(funcName)s] => %(levelname)s: %(message)s',
  level=logging.DEBUG
)
log = logging.getLogger()

# Constants
PORT = os.getenv("MODBUS_PORT", "COM6") # "COM7" for Windows or "/dev/ttyUSB2" for Linux
STOPBITS = int(os.getenv("MODBUS_STOPBITS", 1))
BYTESIZE = int(os.getenv("MODBUS_BYTESIZE", 8))
PARITY = os.getenv("MODBUS_PARITY", 'N')
BAUDRATE = int(os.getenv("MODBUS_BAUDRATE", 11500))
TIMEOUT = int(os.getenv("MODBUS_TIMEOUT", 2))
UNIT_IDS = range(1, 37)
MAX_RETRIES = 1

# register_address, register_count, decode, register_name
REGISTER_ADDRESSES_READ = [
  (40101, 1, None, 'status')
]

# register_address, register_count, builder_key, register_name, value
REGISTER_ADDRESSES_WRITE = [
  (40100, 1, 'build_16bit_uint', 'dcdc_command', 14),
]

DECODERS = {
  'decode_8bit_uint': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_8bit_uint(),
  'decode_8bit_int': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_8bit_int(),
  'decode_16bit_uint': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_16bit_uint(),
  'decode_16bit_int': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_16bit_int(),
  'decode_32bit_uint': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_32bit_uint(),
  'decode_32bit_int': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_32bit_int(),
  'decode_64bit_uint': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_64bit_uint(),
  'decode_64bit_int': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_64bit_int(),
  'decode_16bit_float': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_16bit_float(),
  'decode_32bit_float': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_32bit_float(),
  'decode_64bit_float': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_64bit_float(),
  'decode_string': lambda registers, length: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_string(length).decode('utf-8').strip('\x00'),
  'decode_string_list': lambda registers, length: [BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_string(length).decode('utf-8').strip('\x00')] * 2,
  'decode_bits': lambda registers: BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE).decode_bits(),
}

BUILDERS = {
  'build_8bit_uint': lambda value: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_8bit_uint(value),
  'build_8bit_int': lambda value: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_8bit_int(value),
  'build_16bit_uint': lambda value: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_16bit_uint(value),
  'build_16bit_int': lambda value: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_16bit_int(value),
  'build_32bit_uint': lambda value: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_32bit_uint(value),
  'build_32bit_int': lambda value: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_32bit_int(value),
  'build_64bit_uint': lambda value: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_64bit_uint(value),
  'build_64bit_int': lambda value: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_64bit_int(value),
  'build_32bit_float': lambda value: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_32bit_float(value),
  'build_64bit_float': lambda value: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_64bit_float(value),
  'build_string': lambda value, length: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_string(value, length),
  'build_bits': lambda value: BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE).add_bits(value),
}

def read_register(client: ModbusClient, unit_id: int, register_address: int, register_count: int, decode: Optional[str]) -> Union[int, float, str, None]:
  for _ in range(MAX_RETRIES):
    try:
      rr = client.read_input_registers(address=register_address, count=register_count, slave=unit_id)
      if not rr.isError():
        if decode:
          return DECODERS[decode](rr.registers)
        return rr.registers
      log.error(f"Error reading register {register_address} from unit {unit_id}")
    except Exception as e:
      log.error(f"Exception reading register {register_address} from unit {unit_id}: {e}")
    sleep(1)
  return None

def get_register_address_by_name(register_name: str, read: bool = True) -> Optional[int]:
  registers = REGISTER_ADDRESSES_READ if read else REGISTER_ADDRESSES_WRITE
  for address, _, _, name in registers:
    if name == register_name:
      return address
  return None

def read_register_by_name(client: ModbusClient, unit_id: int, register_name: str) -> Union[int, float, str, None]:
  register_address = get_register_address_by_name(register_name)
  if register_address is not None:
    for address, count, decode, name in REGISTER_ADDRESSES_READ:
      if name == register_name:
        return read_register(client, unit_id, address, count, decode)
  log.error(f"Register name {register_name} not found")
  return None

def write_register(client: ModbusClient, unit_id: int, register_address: int, value: Union[int, float]) -> bool:
  for _ in range(MAX_RETRIES):
    try:
      builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
      if isinstance(value, int):
        builder.add_16bit_int(value)
      elif isinstance(value, float):
        builder.add_32bit_float(value)
      else:
        log.error(f"Invalid value type for register {register_address}")
        return False
      wb = client.write_registers(register_address, builder.to_registers(), slave=unit_id)
      if not wb.isError():
        log.info(f"Successfully wrote value {value} to register {register_address} for unit {unit_id}")
        return True
      log.error(f"Error writing value {value} to register {register_address} for unit {unit_id}")
    except Exception as e:
      log.error(f"Exception writing value {value} to register {register_address} for unit {unit_id}: {e}")
    sleep(1)
  return False

def write_register_by_name(client: ModbusClient, unit_id: int, register_name: str, value: Union[int, float]) -> bool:
  register_address = get_register_address_by_name(register_name, read=False)
  if register_address is not None:
    for address, _, builder_key, name, _ in REGISTER_ADDRESSES_WRITE:
      if name == register_name:
        builder = BUILDERS[builder_key](value)
        return write_register(client, unit_id, address, builder.to_registers())
  log.error(f"Register name {register_name} not found")
  return False

def connect_to_modbus_client() -> ModbusClient:
  return ModbusClient(port=PORT, stopbits=STOPBITS, bytesize=BYTESIZE, parity=PARITY, baudrate=BAUDRATE, timeout=TIMEOUT)

def process_unit(client: ModbusClient, unit_id: int):
  log.info(f"Connected to unit {unit_id}")
  for register_address, register_count, decode, register_name in REGISTER_ADDRESSES_READ:
    result = read_register(client, unit_id, register_address, register_count, decode)
    if result is not None:
      log.info(f"{register_name}: {result}")
  for register_address, _, builder_key, register_name, value in REGISTER_ADDRESSES_WRITE:
    if write_register(client, unit_id, register_address, value):
      log.info(f"Wrote {value} to {register_name}")
  log.info(f"Disconnected from unit {unit_id}")

def main():
  for unit_id in UNIT_IDS:
    try:
      with connect_to_modbus_client() as client:
        if client.connect():
          process_unit(client, unit_id)
        else:
          log.error(f"Failed to connect to unit {unit_id}")
    except Exception as e:
      log.error(f"Exception occurred while communicating with unit {unit_id}: {e}")
    sleep(1)

if __name__ == "__main__":
  main()