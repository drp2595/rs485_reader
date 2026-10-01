RS485 / Modbus Reader & Relay Control

Python scripts for reading industrial energy meters and genset controllers, and controlling relays, over Modbus (RTU and TCP).

Built from real-world industrial IoT work — polling multi-function energy meters and genset controllers over Modbus, and switching relays (e.g. genset start/stop) based on live readings.

What's in here

- **`3_Para_tcp.py`** — Polls a 3-phase energy meter over Modbus TCP: per-phase voltage (32-bit registers), frequency, and total power (kW). Runs a continuous poll loop with basic error handling.
- **`4_Para_rtu.py`** — Work-in-progress script for reading genset controller parameters (oil pressure, coolant temp, battery voltage, fuel level) over Modbus RTU/RS485. Multi-port/multi-slave handling is scaffolded but not yet wired up — currently a reference for the register map and parsing logic rather than a finished poller.
- **`Relay_Control.py`** — Sends raw Modbus write-single-coil frames over serial to turn a relay on/off (e.g. genset start/stop control).
- **`pycrc.py`** — Modbus CRC16 calculation (table-based), used to validate/generate frames for `Relay_Control.py`.

## Hardware used

- Raspberry Pi
- L&T energy meter (Modbus RTU over RS485 / TCP)
- RS485-to-USB converter

## Why

Industrial meters and controllers (L&T, Deep Sea, Woodward, and similar) commonly expose live data over Modbus RTU/TCP. These scripts are minimal, working examples of polling real meter/controller data and acting on it (relay control) — the same pattern used in production energy monitoring and genset automation systems.

## Next steps

- Finish wiring up `4_Para_rtu.py` to actually connect per-port/per-slave and output readings
- Add logging/storage of polled readings (CSV or a time-series DB)
- Add reconnect-on-failure handling for long-running polls
- Add response/ack checking in `Relay_Control.py`
- Add a simple live dashboard

## Requirements

\`\`\`
pip install pymodbus pyserial websockets
\`\`\`
