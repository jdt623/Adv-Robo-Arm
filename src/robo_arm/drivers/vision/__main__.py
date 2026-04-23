"""Console test harness for the accelerometer driver.

Run:  python -m robo_arm.drivers.accelerometer

Prints readings at the configured data rate. Tilt the sensor and watch the
axes change. Ctrl+C to stop.

Options:
  --calibrate    Average 200 readings and store offsets before streaming.
                 Keep the sensor flat and still (az should read ~1 g) during
                 this step.
"""

from __future__ import annotations

import argparse
import time

from robo_arm.common.logging_config import configure
from robo_arm.drivers.accelerometer import AccelerometerDriver


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream ADXL345 readings")
    parser.add_argument("--address", type=lambda x: int(x, 0), default=0x53)
    parser.add_argument("--rate", type=float, default=100.0, help="data rate Hz")
    parser.add_argument("--range", type=int, default=2, choices=[2, 4, 8, 16], dest="range_g")
    parser.add_argument("--calibrate", action="store_true")
    args = parser.parse_args()

    configure()

    with AccelerometerDriver(
        address=args.address, data_rate_hz=args.rate, range_g=args.range_g
    ) as accel:
        if args.calibrate:
            accel.calibrate()

        print("Reading accelerometer. Tilt it around. Ctrl+C to stop.")
        print(f"{'t (s)':>8} | {'ax (g)':>8} | {'ay (g)':>8} | {'az (g)':>8} | {'|a| (g)':>8}")
        print("-" * 56)
        t0 = time.monotonic()
        period = 1.0 / args.rate
        try:
            while True:
                r = accel.read()
                mag = (r.ax**2 + r.ay**2 + r.az**2) ** 0.5
                print(
                    f"{r.timestamp - t0:8.2f} | "
                    f"{r.ax:8.3f} | {r.ay:8.3f} | {r.az:8.3f} | {mag:8.3f}"
                )
                time.sleep(period)
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()
