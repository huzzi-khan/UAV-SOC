#!/usr/bin/env python3
import subprocess
from pymavlink import mavutil

pcap = (
    "/home/" + __import__("getpass").getuser()
    + "/uav-soc/evidence/pcaps/attack-02/during/"
    + "command_injection.pcap"
)

result = subprocess.run(
    [
        "tshark",
        "-r", pcap,
        "-Y", "udp",
        "-T", "fields",
        "-e", "frame.number",
        "-e", "udp.srcport",
        "-e", "udp.dstport",
        "-e", "udp.payload",
    ],
    capture_output=True,
    text=True,
    check=True,
)

found = 0

for line in result.stdout.splitlines():
    parts = line.split("\t")

    if len(parts) != 4:
        continue

    frame_no, src_port, dst_port, payload = parts

    if not payload:
        continue

    try:
        raw = bytes.fromhex(payload.replace(":", ""))
        parser = mavutil.mavlink.MAVLink(None)

        for byte in raw:
            msg = parser.parse_char(bytes([byte]))

            if msg is None:
                continue

            if msg.get_type() in ("COMMAND_LONG", "COMMAND_ACK"):
                found += 1

                print("\nFrame:", frame_no)
                print("UDP:", src_port, "->", dst_port)
                print("Message:", msg.get_type())

                if msg.get_type() == "COMMAND_LONG":
                    print("Command:", msg.command)
                    print("Target:", msg.target_system, msg.target_component)

                elif msg.get_type() == "COMMAND_ACK":
                    print("Command:", msg.command)
                    print("Result:", msg.result)

    except Exception:
        continue

print("\nTotal command/ACK messages:", found)
