"""Console test harness: python -m robo_arm.drivers.vision"""
from __future__ import annotations

import time

from robo_arm.common.logging_config import configure
from robo_arm.drivers.vision.driver import VisionDriver


def main() -> None:
    configure()
    with VisionDriver() as cam:
        print("Capturing frames. Ctrl+C to stop.")
        n = 0
        t0 = time.monotonic()
        try:
            while True:
                cam.read()
                n += 1
                if n % 30 == 0:
                    dt = time.monotonic() - t0
                    print(f"{n} frames in {dt:.2f} s  ({n / dt:.1f} fps)")
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()
