#!/usr/bin/env python3
from pymavlink import mavutil
from datetime import datetime, timezone
from pathlib import Path
import json
import time

output = Path.home() / (
    "uav-soc/evidence/logs/attack-05/eavesdrop_log.jsonl"
)

listener = mavutil.mavlink_connection(
    "udpin:127.0.0.1:14551"
)

print("[*] Listening for MAVLink telemetry")

heartbeat = listener.wait_heartbeat(timeout=15)

if heartbeat is None:
    raise SystemExit("[!] No heartbeat received")

print("[+] MAVLink heartbeat received")
print("[+] Vehicle system:", listener.target_system)

count = 0
deadline = time.monotonic() + 30

with output.open("w") as log:
    while time.monotonic() < deadline:
        msg = listener.recv_match(blocking=True, timeout=1)

        if msg is None or msg.get_type() == "BAD_DATA":
            continue

        msg_type = msg.get_type()

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message_type": msg_type,
            "system_id": msg.get_srcSystem(),
            "component_id": msg.get_srcComponent(),
            "data": msg.to_dict()
        }

        log.write(json.dumps(record, default=str) + "\n")
        count += 1

        if msg_type == "HEARTBEAT":
            print("[HEARTBEAT]", record["system_id"])

        elif msg_type == "GLOBAL_POSITION_INT":
            print(
                "[GPS]",
                msg.lat / 1e7,
                msg.lon / 1e7,
                msg.alt / 1000
            )

        elif msg_type == "SYS_STATUS":
            print(
                "[BATTERY]",
                msg.voltage_battery,
                "mV",
                msg.battery_remaining,
                "%"
            )

print("[+] Messages logged:", count)
print("[+] Output:", output)

listener.close()
