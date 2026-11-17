#!/usr/bin/env python3
from pymavlink import mavutil
import time

print("[*] Connecting to local PX4 SITL")

master = mavutil.mavlink_connection(
    "udp:127.0.0.1:14562",
    source_system=255,
    source_component=190
)

heartbeat = master.wait_heartbeat(timeout=10)

if heartbeat is None:
    raise SystemExit("[!] No heartbeat received. Test stopped.")

print("[+] PX4 heartbeat received")
print("[+] Target:", master.target_system, master.target_component)

print("[*] Sending one MAV_CMD_NAV_LAND")

master.mav.command_long_send(
    master.target_system,
    1,
    mavutil.mavlink.MAV_CMD_NAV_LAND,
    0,
    0, 0, 0, 0, 0, 0, 0
)

deadline = time.monotonic() + 5
ack = None

while time.monotonic() < deadline:
    msg = master.recv_match(blocking=True, timeout=1)
    if msg and msg.get_type() == "COMMAND_ACK":
        if msg.command == mavutil.mavlink.MAV_CMD_NAV_LAND:
            ack = msg
            break

if ack:
    print("[+] COMMAND_ACK received")
    print("Command:", ack.command)
    print("Result:", ack.result)
    print("ACK source:", ack.get_srcSystem(), ack.get_srcComponent())
else:
    print("[!] No matching COMMAND_ACK within timeout")

master.close()
