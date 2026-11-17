#!/usr/bin/env python3
from pymavlink import mavutil
import time

master = mavutil.mavlink_connection(
    "udp:127.0.0.1:14562",
    source_system=250,
    source_component=190
)

hb = master.wait_heartbeat(timeout=10)

if hb is None:
    raise SystemExit("No heartbeat received")

print("[+] Connected to SITL")
print("[*] Requesting SYS_STATUS")

master.mav.command_long_send(
    master.target_system,
    1,
    mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
    0,
    mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS,
    0, 0, 0, 0, 0, 0
)

deadline = time.monotonic() + 5

while time.monotonic() < deadline:
    msg = master.recv_match(blocking=True, timeout=1)
    if msg and msg.get_type() == "COMMAND_ACK":
        if msg.command == mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE:
            print("ACK command:", msg.command)
            print("ACK result:", msg.result)
            break

master.close()

