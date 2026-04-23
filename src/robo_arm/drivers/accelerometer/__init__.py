"""Accelerometer driver.

Provides a chip-agnostic ``AccelerometerDriver`` that returns (ax, ay, az) in g.
Replace the ``_read_raw`` method with the chip-specific bus read once hardware
is chosen (e.g. LIS3DH, MPU6050, ADXL345).
"""

from robo_arm.drivers.accelerometer.driver import AccelerometerDriver, Reading

__all__ = ["AccelerometerDriver", "Reading"]
