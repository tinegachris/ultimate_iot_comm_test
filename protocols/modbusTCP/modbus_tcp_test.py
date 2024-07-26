#
# This module is used to test the Modbus TCP protocol.
#

from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from utils import Logger

# This class is used to test the Modbus TCP protocol.
class ModbusTcpTest:
    def __init__(self):
        self.client = None

    # Connect to the Modbus TCP server.
    def connect(self, host, port):
        self.client = ModbusClient(host, port)
        self.client.connect()
        # Check if the connection is successful.
        if self.client.is_socket_open():
            Logger.log("Connected to the Modbus TCP server.")
        else:
            Logger.log("Failed to connect to the Modbus TCP server.")
        # Return the connection status.
        return self.client.is_socket_open()

    # Disconnect from the Modbus TCP server.
    def disconnect(self):
        self.client.close()
        # Check if the disconnection is successful.
        if not self.client.is_socket_open():
            Logger.log("Disconnected from the Modbus TCP server.")
        else:
            Logger.log("Failed to disconnect from the Modbus TCP server.")
        # Return the disconnection status.
        return not self.client.is_socket_open()

    # Read 16-bit integer values from the Modbus TCP server.
    def read_int16(self, address, count):
        # Read 16-bit integer values from the Modbus TCP server.
        result = self.client.read_input_registers(address, count, unit=1)
        # Check if the reading is successful.
        if result.isError():
            Logger.log("Failed to read 16-bit integer values from the Modbus TCP server.")
            return None
        # Decode the 16-bit integer values.
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
        values = []
        for _ in range(count):
            values.append(decoder.decode_16bit_int())
        # Return the 16-bit integer values.
        return values

    # Write 16-bit integer values to the Modbus TCP server.
    def write_int16(self, address, values):
        # Encode the 16-bit integer values.
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        for value in values:
            builder.add_16bit_int(value)
        payload = builder.build()
        # Write 16-bit integer values to the Modbus TCP server.
        result = self.client.write_registers(address, payload, unit=1)
        # Check if the writing is successful.
        if result.isError():
            Logger.log("Failed to write 16-bit integer values to the Modbus TCP server.")
            return False
        # Return the writing status.
        return True

    # Read 16-bit float values from the Modbus TCP server.
    def read_float16(self, address, count):
        # Read 16-bit float values from the Modbus TCP server.
        result = self.client.read_input_registers(address, count, unit=1)
        # Check if the reading is successful.
        if result.isError():
            Logger.log("Failed to read 16-bit float values from the Modbus TCP server.")
            return None
        # Decode the 16-bit float values.
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
        values = []
        for _ in range(count):
            values.append(decoder.decode_16bit_float())
        # Return the 16-bit float values.
        return values

    # Write 16-bit float values to the Modbus TCP server.
    def write_float16(self, address, values):
        # Encode the 16-bit float values.
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        for value in values:
            builder.add_16bit_float(value)
        payload = builder.build()
        # Write 16-bit float values to the Modbus TCP server.
        result = self.client.write_registers(address, payload, unit=1)
        # Check if the writing is successful.
        if result.isError():
            Logger.log("Failed to write 16-bit float values to the Modbus TCP server.")
            return False
        # Return the writing status.
        return True

    # Read 32-bit integer values from the Modbus TCP server.
    def read_int32(self, address, count):
        # Read 32-bit integer values from the Modbus TCP server.
        result = self.client.read_input_registers(address, count, unit=1)
        # Check if the reading is successful.
        if result.isError():
            Logger.log("Failed to read 32-bit integer values from the Modbus TCP server.")
            return None
        # Decode the 32-bit integer values.
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
        values = []
        for _ in range(count):
            values.append(decoder.decode_32bit_int())
        # Return the 32-bit integer values.
        return values

    # Write 32-bit integer values to the Modbus TCP server.
    def write_int32(self, address, values):
        # Encode the 32-bit integer values.
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        for value in values:
            builder.add_32bit_int(value)
        payload = builder.build()
        # Write 32-bit integer values to the Modbus TCP server.
        result = self.client.write_registers(address, payload, unit=1)
        # Check if the writing is successful.
        if result.isError():
            Logger.log("Failed to write 32-bit integer values to the Modbus TCP server.")
            return False
        # Return the writing status.
        return True

    # Read 32-bit float values from the Modbus TCP server.
    def read_float32(self, address, count):
        # Read 32-bit float values from the Modbus TCP server.
        result = self.client.read_input_registers(address, count * 2, unit=1)
        # Check if the reading is successful.
        if result.isError():
            Logger.log("Failed to read 32-bit float values from the Modbus TCP server.")
            return None
        # Decode the 32-bit float values.
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
        values = []
        for _ in range(count):
            values.append(decoder.decode_32bit_float())
        # Return the 32-bit float values.
        return values

    # Write 32-bit float values to the Modbus TCP server.
    def write_float32(self, address, values):
        # Encode the 32-bit float values.
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        for value in values:
            builder.add_32bit_float(value)
        payload = builder.build()
        # Write 32-bit float values to the Modbus TCP server.
        result = self.client.write_registers(address, payload, unit=1)
        # Check if the writing is successful.
        if result.isError():
            Logger.log("Failed to write 32-bit float values to the Modbus TCP server.")
            return False
        # Return the writing status.
        return True

    # Read 64-bit integer values from the Modbus TCP server.
    def read_int64(self, address, count):
        # Read 64-bit integer values from the Modbus TCP server.
        result = self.client.read_input_registers(address, count * 2, unit=1)
        # Check if the reading is successful.
        if result.isError():
            Logger.log("Failed to read 64-bit integer values from the Modbus TCP server.")
            return None
        # Decode the 64-bit integer values.
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
        values = []
        for _ in range(count):
            values.append(decoder.decode_64bit_int())
        # Return the 64-bit integer values.
        return values

    # Write 64-bit integer values to the Modbus TCP server.
    def write_int64(self, address, values):
        # Encode the 64-bit integer values.
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        for value in values:
            builder.add_64bit_int(value)
        payload = builder.build()
        # Write 64-bit integer values to the Modbus TCP server.
        result = self.client.write_registers(address, payload, unit=1)
        # Check if the writing is successful.
        if result.isError():
            Logger.log("Failed to write 64-bit integer values to the Modbus TCP server.")
            return False
        # Return the writing status.
        return True

    # Read 64-bit float values from the Modbus TCP server.
    def read_float64(self, address, count):
        # Read 64-bit float values from the Modbus TCP server.
        result = self.client.read_input_registers(address, count * 4, unit=1)
        # Check if the reading is successful.
        if result.isError():
            Logger.log("Failed to read 64-bit float values from the Modbus TCP server.")
            return None
        # Decode the 64-bit float values.
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
        values = []
        for _ in range(count):
            values.append(decoder.decode_64bit_float())
        # Return the 64-bit float values.
        return values

    # Write 64-bit float values to the Modbus TCP server.
    def write_float64(self, address, values):
        # Encode the 64-bit float values.
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        for value in values:
            builder.add_64bit_float(value)
        payload = builder.build()
        # Write 64-bit float values to the Modbus TCP server.
        result = self.client.write_registers(address, payload, unit=1)
        # Check if the writing is successful.
        if result.isError():
            Logger.log("Failed to write 64-bit float values to the Modbus TCP server.")
            return False
        # Return the writing status.
        return True

    # Read boolean values from the Modbus TCP server.
    def read_bool(self, address, count):
        # Read boolean values from the Modbus TCP server.
        result = self.client.read_coils(address, count, unit=1)
        # Check if the reading is successful.
        if result.isError():
            Logger.log("Failed to read boolean values from the Modbus TCP server.")
            return None
        # Return the boolean values.
        return result.bits

    # Write boolean values to the Modbus TCP server.
    def write_bool(self, address, values):
        # Write boolean values to the Modbus TCP server.
        result = self.client.write_coils(address, values, unit=1)
        # Check if the writing is successful.
        if result.isError():
            Logger.log("Failed to write boolean values to the Modbus TCP server.")
            return False
        # Return the writing status.
        return True

    # Read string values from the Modbus TCP server.
    def read_string(self, address, count):
        # Read string values from the Modbus TCP server.
        result = self.client.read_input_registers(address, count * 2, unit=1)
        # Check if the reading is successful.
        if result.isError():
            Logger.log("Failed to read string values from the Modbus TCP server.")
            return None
        # Decode the string values.
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
        values = []
        for _ in range(count):
            values.append(decoder.decode_string(2))
        # Return the string values.
        return values

    # Write string values to the Modbus TCP server.
    def write_string(self, address, values):
        # Encode the string values.
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        for value in values:
            builder.add_string(value, 2)
        payload = builder.build()
        # Write string values to the Modbus TCP server.
        result = self.client.write_registers(address, payload, unit=1)
        # Check if the writing is successful.
        if result.isError():
            Logger.log("Failed to write string values to the Modbus TCP server.")
            return False
        # Return the writing status.
        return True

    if __name__ == "__main__":
        pass

# End of file: comm_protocols/modbus_tcp_test.py