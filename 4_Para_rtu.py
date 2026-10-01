from datetime import datetime
from time import sleep
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import json

port_map = {
    '/dev/ttyUSB0': [4, 5], 
    '/dev/ttyUSB1': [1, 2, 3],
    '/dev/ttyUSB2': [6]  
}
for port, slaves in port_map.items():
    print(f"\nConnecting to {port}")

client = ModbusClient(
    method = 'rtu',
    port=port, 
    timeout=5, 
    stopbits=1, 
    bytesize=8, 
    parity='N', 
    baudrate=115200
)
client.connect()
print("Modbus Connected")

regListS = {
    1025: 'OilPres',
    1026: 'coolerTemp',
    1030: 'BatteryVolt',
    1028: "FuelLevel"
}


slv = 3


def safe_float(value, default=0.0):
    try:
        return float(value) if value != "" else default
    except (ValueError, TypeError):
        return default

def safe_int(value, default=0):
    try:
        return int(float(value)) if value != "" else default
    except (ValueError, TypeError):
        return default


while True:
    for key, value in regListS.items():
        try:
            read = client.read_holding_registers(address=key-1, count=1, unit=slv, slave=slv)
            data = read.registers[0]
            if data == 32767:
                data = 0
            match value:
                case 'coolerTemp':
                    if data == 32763:
                        coolerTemp = "--"
                    else:
                        coolerTemp = str(round(data*1, 2))
                
                case 'BatteryVolt':
                    batteryVoltage = str(round(data*0.1, 2))
                case 'OilPres':
                    if data == 65531:
                        oilPressure = "--"
                    else:
                      oilPressure = str(round(data*1, 2))
                case 'FuelLevel':
                    fuellevel = str(data*1)
        except Exception as e:
            print(f"Error reading {value} (reg {key}) from slave {slv}: {e}")
            
            sleep(0.5)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')