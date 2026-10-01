import serial
import pycrc
from time import sleep

port = "/dev/ttyUSB0"
baudRate = 9600
oneRun = False
twoRun = False


def startRelay(chNo):
       relayNumber = chNo - 1
       sleep(0.5)
       s = serial.Serial(port,baudRate)
       cmd = [0, 0, 0, 0, 0, 0, 0, 0]

       cmd[0] = 0x20
       cmd[1] = 0x05
       cmd[2] = 0
       cmd[3] = relayNumber
       cmd[4] = 0xFF
       cmd[5] = 0
       crc = pycrc.ModbusCRC(cmd[0:6])
       cmd[6] = crc & 0xFF
       cmd[7] = crc >> 8
       s.write(cmd)

def stopRelay(chNo):
       relayNumber = chNo - 1
       sleep(0.5)
       s = serial.Serial(port,baudRate)
       cmd = [0, 0, 0, 0, 0, 0, 0, 0]

       cmd[0] = 0x20
       cmd[1] = 0x05
       cmd[2] = 0
       cmd[3] = relayNumber
       cmd[4] = 0
       crc = pycrc.ModbusCRC(cmd[0:6])
       cmd[6] = crc & 0xFF
       cmd[7] = crc >> 8
       s.write(cmd)
