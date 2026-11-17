#!/usr/bin/env python3
import time
from pymavlink import mavutil

# Local PX4 SITL only.
TARGET = "udpout:127.0.0.1:18570"

conn = mavutil.mavlink_connection(
    TARGET,
    source_system=255,
    source_component=190
)

fake_lat = int(47.399247 * 1e7)
fake_lon = int(8.54044502 * 1e7)
fake_alt = 50.0  # GPS_INPUT altitude is in metres

print("[*] Sending bounded GPS_INPUT test")
print("[*] Target:", TARGET)
print("[*] Fabricated position:", fake_lat, fake_lon, fake_alt)

for i in range(20):
    conn.mav.gps_input_send(
        int(time.time() * 1e6),  # time_usec
        0,                       # gps_id
        0,                       # ignore_flags
        int((time.time() % 604800) * 1000),
        0,                       # gps_week (lab value)
        3,                       # 3D fix
        fake_lat,
        fake_lon,
        fake_alt,
        1.0,                     # HDOP
        1.0,                     # VDOP
        0.0, 0.0, 0.0,            # velocities
        0.5,                     # speed accuracy
        1.0,                     # horizontal accuracy
        1.0,                     # vertical accuracy
        10                       # satellites visible
    )
    time.sleep(0.1)

print("[+] Test packets transmitted")
conn.close()
