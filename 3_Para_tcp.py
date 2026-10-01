import json
import threading
import time

from pymodbus.client.sync import ModbusTcpClient
from websockets.sync.client import connect as ws_connect

# ---- Modbus config -----------------------------------------------------
HOST_IP = "192.168.88.45"
MODBUS_PORT = 502
UNIT_ID = 10

ADDR_VOLTAGE = 1098   # 6 registers: 3 phases x 2 registers each (32-bit each)
COUNT_VOLTAGE = 6
ADDR_FREQUENCY = 1488  # 1 register, 2 decimal places
ADDR_WATT = 1536       # 2 registers, 32-bit total watts

def combine_32bit(regs):
    #High word first (regs[0] << 16 | regs[1])
    return (regs[0] << 16) | regs[1]


def read_data(client):
    rr_v = client.read_holding_registers(address=ADDR_VOLTAGE, count=COUNT_VOLTAGE, unit=UNIT_ID)
    rr_f = client.read_holding_registers(address=ADDR_FREQUENCY, count=1, unit=UNIT_ID)
    rr_w = client.read_holding_registers(address=ADDR_WATT, count=2, unit=UNIT_ID)

    if rr_v.isError() or rr_f.isError() or rr_w.isError():
        raise RuntimeError(f"Modbus read error: v={rr_v} f={rr_f} w={rr_w}")

    v_regs = rr_v.registers
    v1 = combine_32bit(v_regs[0:2]) / 10.0
    v2 = combine_32bit(v_regs[2:4]) / 10.0
    v3 = combine_32bit(v_regs[4:6]) / 10.0
    voltage_avg = round((v1 + v2 + v3) / 3, 1)

    freq = round(rr_f.registers[0] / 100.0, 2)

    watts = combine_32bit(rr_w.registers)
    kw = round(watts / 1000.0, 1)

    return {
        "reader1": {
            "kw": kw,
            "voltage": voltage_avg,
            "freq": freq,
        }
    }


def main():
    modbus_client = ModbusTcpClient(host=HOST_IP, port=MODBUS_PORT, timeout=5)
    modbus_client.connect()

    try:
        while True:
            try:
                payload = read_data(modbus_client)
            except Exception as exc:
                print(f"Poll/send error: {exc}")

            time.sleep(0.48)
    except KeyboardInterrupt:
        print("Stopping.")
    finally:
        modbus_client.close()


if __name__ == "__main__":
    main()