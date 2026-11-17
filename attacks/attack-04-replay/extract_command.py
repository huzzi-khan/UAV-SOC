#!/usr/bin/env python3
import subprocess
from pathlib import Path
from pymavlink import mavutil

pcap = Path.home() / (
    "uav-soc/evidence/pcaps/attack-04/before/original_command.pcap"
)

result = subprocess.run(
    [
        "tshark", "-r", str(pcap),
        "-Y", "udp.dstport == 14561",
        "-T", "fields", "-e", "udp.payload"
    ],
    capture_output=True,
    text=True,
    check=True
)

found = []

for line in result.stdout.splitlines():
    if not line.strip():
        continue

    raw = bytes.fromhex(line.strip())
    parser = mavutil.mavlink.MAVLink(None)

    try:
        for byte in raw:
            msg = parser.parse_char(bytes([byte]))
            if (
                msg
                and msg.get_type() == "COMMAND_LONG"
                and msg.command == mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE
            ):
                found.append(raw)
                break
    except Exception:
        continue

print("Matching captured UDP payloads:", len(found))

if found:
    output = Path.home() / (
        "uav-soc/evidence/logs/attack-04/captured_command.bin"
    )
    output.write_bytes(found[0])
    print("Saved:", output)
