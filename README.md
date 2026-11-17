# UAV SOC — Security Monitoring and Anomaly Detection for UAV Communications

A cybersecurity laboratory project focused on monitoring, analyzing, and detecting suspicious MAVLink communication in a simulated unmanned aerial vehicle (UAV) environment.

## Project Overview

The project uses PX4 Software-in-the-Loop (SITL), Gazebo X500, and QGroundControl to generate realistic UAV communication traffic. Controlled cybersecurity experiments provide data for subsequent SOC monitoring and machine-learning-based anomaly detection.

**Environment:** Ubuntu 24.04, VMware Workstation, PX4 SITL, Gazebo, QGroundControl, Python, PyMAVLink, Wireshark, and tcpdump.

## Project Progress

| Phase | Description | Status |
|---|---|---|
| Phase 1 | UAV simulation setup and normal telemetry capture | Completed |
| Phase 2 | Controlled MAVLink security experiments | Completed |
| Phase 3 | Zeek and Wazuh SOC monitoring | Planned |
| Phase 4 | Isolation Forest anomaly detection | Planned |

## Security Experiments

1. Controlled UDP traffic test — Availability testing
2. MAVLink command injection — Control-command integrity
3. GPS_INPUT spoofing — Navigation-data integrity
4. MAVLink command replay — Message freshness and replay behavior
5. MAVLink telemetry eavesdropping — Confidentiality

All experiments are performed against an authorized local PX4 SITL environment. Individual outcomes and limitations are documented in the lab journal and evidence records.

## Repository Structure

- `attacks/` — Python scripts for the security experiments
- `docs/` — Environment setup, lab journal, architecture, and screenshots
- `evidence/` — Local experiment captures and telemetry artifacts
- `tools/mavlink-decoder/` — MAVLink protocol analysis support
- `monitoring/` — Planned Zeek and Wazuh integration
- `ml/` — Planned anomaly detection implementation
- `report/` — Project reporting materials

Raw packet captures and telemetry datasets are excluded from the public Git repository by default.

## Reproducing the Environment

The project requires a working PX4 SITL and Gazebo X500 installation, QGroundControl, Python 3, PyMAVLink, tcpdump, and Wireshark.

See `docs/setup/` and `docs/experiments/lab-journal.md` for setup information and experiment records.

## Security and Ethical Scope

This repository documents controlled cybersecurity research in a local simulated environment. It is not intended for use against real UAVs, third-party systems, or networks without authorization.

## Next Steps

- Analyze captured MAVLink traffic with Zeek
- Integrate Wazuh alerts and security monitoring
- Extract network and telemetry features
- Train and evaluate an Isolation Forest anomaly detection model
- Document experimental results and detection performance
