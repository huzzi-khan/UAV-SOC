#!/usr/bin/env python3
from pathlib import Path
import socket

payload_file = Path.home() / (
    "uav-soc/evidence/logs/attack-04/captured_command.bin"
)

payload = payload_file.read_bytes()

if not payload or len(payload) > 512:
    raise SystemExit("Unexpected payload size")

target = ("127.0.0.1", 14561)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.sendto(payload, target)

print("[+] One saved MAVLink UDP payload retransmitted")
print("Destination:", target)
print("Bytes:", len(payload))
