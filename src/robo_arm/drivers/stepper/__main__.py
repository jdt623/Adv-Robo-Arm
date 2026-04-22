"""Console test harness: python -m robo_arm.drivers.stepper

Drives the motor back and forth by 1 revolution.
Edit the pin numbers below to match your wiring.
"""
from __future__ import annotations

import time

from robo_arm.common.logging_config import configure
from robo_arm.drivers.stepper.driver import StepperDriver

# TODO: set these to your actual wiring
STEP_PIN = 20
DIR_PIN = 21
ENABLE_PIN = None


def main() -> None:
    configure()
    with StepperDriver(STEP_PIN, DIR_PIN, ENABLE_PIN) as m:
        print(f"Stepping +{m.steps_per_rev} then -{m.steps_per_rev} steps…")
        m.step(n=m.steps_per_rev, direction=+1)
        time.sleep(0.5)
        m.step(n=m.steps_per_rev, direction=-1)
        print(f"final position: {m.position_steps} steps")


if __name__ == "__main__":
    main()
