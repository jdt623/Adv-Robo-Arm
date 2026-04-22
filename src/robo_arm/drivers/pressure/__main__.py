"""Console test harness: python -m robo_arm.drivers.pressure"""
from __future__ import annotations

import time

from robo_arm.common.logging_config import configure
from robo_arm.drivers.pressure.driver import PressureDriver


def main() -> None:
    configure()
    with PressureDriver() as p:
        print("Reading pressure sensor. Ctrl+C to stop.")
        print(f"{'t (s)':>8} | {'pressure (kPa)':>16}")
        print("-" * 30)
        t0 = time.monotonic()
        try:
            while True:
                r = p.read()
                print(f"{r.timestamp - t0:8.2f} | {r.pressure_kpa:16.3f}")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()
