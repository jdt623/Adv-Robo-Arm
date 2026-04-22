"""Console test harness for the accelerometer driver.

Run with:  python -m robo_arm.drivers.accelerometer

Prints readings at ~10 Hz until you Ctrl+C.
"""
from __future__ import annotations

import time

from robo_arm.common.logging_config import configure
from robo_arm.drivers.accelerometer import AccelerometerDriver


def main() -> None:
    configure()
    with AccelerometerDriver() as accel:
        print("Reading accelerometer. Ctrl+C to stop.")
        print(f"{'t (s)':>8} | {'ax (g)':>8} | {'ay (g)':>8} | {'az (g)':>8}")
        print("-" * 44)
        t0 = time.monotonic()
        try:
            while True:
                r = accel.read()
                print(f"{r.timestamp - t0:8.2f} | {r.ax:8.3f} | {r.ay:8.3f} | {r.az:8.3f}")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()
