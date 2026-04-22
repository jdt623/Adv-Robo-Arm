# Adv-Robo-Arm

Inverted articulated robot arm built on Raspberry Pi 5 (Ubuntu 24.04) with modular sensor drivers and ROS 2 Jazzy integration for kinematics and control.

## Project Phases

1. **Phase 1 — Sensor validation (Python, no framework)** _← current_
   Each sensor has a standalone driver module with a simple console-output test harness. Stepper driver already validated.
2. **Phase 2 — ROS 2 Jazzy integration**
   Wrap each driver as a ROS 2 node. Use `ros2 topic` for inter-module comms, `ros2 bag` for data capture.
3. **Phase 3 — Kinematics and control**
   MoveIt 2 for inverse kinematics, joint state broadcasting, RViz2 visualization.
4. **Phase 4 — Full system integration**
   End-effector behaviors, vision-guided pick-and-place, closed-loop control using feedback sensors.

## Hardware

- Raspberry Pi 5 (primary compute, Ubuntu 24.04 LTS)
- Stepper motors + drivers (joint actuation) — **validated**
- Accelerometer (orientation feedback)
- Camera (AI vision)
- Range finder(s) (proximity / workspace awareness)
- Pressure sensor(s) (end-effector force feedback)

See `hardware/bom/bom.md` for the full bill of materials.

## Repository Layout

```
Adv-Robo-Arm/
├── hardware/          CAD files, wiring diagrams, BOM, datasheets
├── firmware/          Any microcontroller firmware (future — e.g. if an STM32 handles real-time control)
├── src/               Phase 1 Python code (pre-ROS 2)
│   ├── drivers/       One subpackage per sensor/actuator
│   ├── common/        Shared utilities, config loading, logging
│   └── arm_controller/  Top-level integrator (built last)
├── ros2_ws/           Phase 2+ ROS 2 workspace (`colcon` build root)
├── tests/             pytest suite — unit tests + integration tests
├── scripts/           Deployment, calibration, one-off tools
├── config/            YAML/TOML configuration files
├── docs/              Architecture notes, decision log, setup guides
└── .github/           CI workflows
```

## Quickstart

```bash
# On the Pi (via VS Code Remote-SSH)
git clone https://github.com/jdt623/Adv-Robo-Arm.git
cd Adv-Robo-Arm

# Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .   # installs the `robo_arm` package in editable mode

# Run a sensor test (example)
python -m robo_arm.drivers.accelerometer
```

## Development Workflow

- Develop on the Pi directly via **VS Code Remote-SSH** (see `docs/setup.md`).
- One feature branch per driver; merge to `main` when the console test works.
- Commit early, commit often. See `docs/contributing.md`.

## License

See `LICENSE`.
