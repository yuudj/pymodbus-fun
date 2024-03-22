#!/usr/bin/env python3
"""Pymodbus synchronous client example.

An example of a single threaded synchronous client.

usage: simple_client_async.py

All options must be adapted in the code
The corresponding server must be started before e.g. as:
    python3 server_sync.py
"""

# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
import pymodbus.client as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus import (
    ExceptionResponse,
    Framer,
    ModbusException,
    pymodbus_apply_logging_config,
)


def run_sync_simple_client(comm, host, port, framer=Framer.SOCKET):
    """Run sync client."""
    # activate debugging
    pymodbus_apply_logging_config("DEBUG")

    print("get client")
    if comm == "tcp":
        client = ModbusClient.ModbusTcpClient(
            host,
            port=port,
            framer=framer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,y
            # close_comm_on_error=False,
            # strict=True,
            # source_address=("localhost", 0),
        )
    elif comm == "udp":
        client = ModbusClient.ModbusUdpClient(
            host,
            port=port,
            framer=framer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,
            # strict=True,
            # source_address=None,
        )
    elif comm == "serial":
        client = ModbusClient.ModbusSerialClient(
            port,
            framer=framer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,.
            # strict=True,
            baudrate=9600,
            bytesize=8,
            parity="N",
            stopbits=1,
            # handle_local_echo=False,
        )
    elif comm == "tls":
        client = ModbusClient.ModbusTlsClient(
            host,
            port=port,
            framer=Framer.TLS,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,
            # strict=True,
            # sslctx=None,
            certfile="../examples/certificates/pymodbus.crt",
            keyfile="../examples/certificates/pymodbus.key",
            # password=None,
            server_hostname="localhost",
        )
    else:  # pragma no cover
        print(f"Unknown client {comm} selected")
        return

    print("connect to server")
    client.connect()

    print("get and verify data")
    try:
        #int_16 = client.read_holding_registers(3, 1, slave=1)
        #int_32 = client.read_holding_registers(5, 2, slave=1)
        float_32= client.read_holding_registers(8,count=2)
        float_32_inc = client.read_holding_registers(10,count=4)
        float_32_random = client.read_holding_registers(14,count=2)
        float_32_uptime = client.read_holding_registers(21,count=2)
    except ModbusException as exc:
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return
    if float_32.isError():  # pragma no cover
        print(f"Received Modbus library error({float_32})")
        client.close()
        return
    if isinstance(float_32, ExceptionResponse):  # pragma no cover
        print(f"Received Modbus library exception ({float_32})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()
    
    floats_32= [
        BinaryPayloadDecoder.fromRegisters(float_32.registers, byteorder=Endian.BIG, wordorder=Endian.BIG),
        BinaryPayloadDecoder.fromRegisters(float_32_inc.registers, byteorder=Endian.BIG, wordorder=Endian.BIG),
        BinaryPayloadDecoder.fromRegisters(float_32_random.registers, byteorder=Endian.BIG, wordorder=Endian.BIG),
        BinaryPayloadDecoder.fromRegisters(float_32_uptime.registers, byteorder=Endian.BIG, wordorder=Endian.BIG)
        ]

    for x in floats_32:
      print(x.decode_32bit_float())
    
    print("close connection")  # pragma no cover
    client.close()  # pragma no cover


if __name__ == "__main__":
    run_sync_simple_client("serial", "" , "/dev/ttyUSB0",Framer.RTU)  # pragma: no cover