"""Console test harness: python -m robo_arm.drivers.rangefinder"""

from __future__ import annotations

import time

from robo_arm.common.logging_config import configure
from robo_arm.drivers.rangefinder.driver import RangefinderDriver


def main() -> None:
    configure()
    with RangefinderDriver() as rf:
        print("Reading rangefinder. Ctrl+C to stop.")
        print(f"{'t (s)':>8} | {'distance (m)':>14}")
        print("-" * 28)
        t0 = time.monotonic()
        try:
            while True:
                r = rf.read()
                print(f"{r.timestamp - t0:8.2f} | {r.distance_m:14.3f}")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()
