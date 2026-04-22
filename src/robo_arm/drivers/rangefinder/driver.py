"""Range finder driver.

Supports a generic time-of-flight / ultrasonic sensor returning distance in
meters. Replace ``_read_raw`` with your chip's read routine (VL53L0X, HC-SR04,
VL53L1X, etc.).

Run the test harness with:  python -m robo_arm.drivers.rangefinder
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from robo_arm.common import DriverError, SensorDriver

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Reading:
    """Distance in meters and the monotonic timestamp of the sample."""

    distance_m: float
    timestamp: float


class RangefinderDriver(SensorDriver):
    """Generic single-channel range finder."""

    name = "rangefinder"

    def __init__(self, i2c_bus: int = 1, address: int = 0x29) -> None:
        self.i2c_bus = i2c_bus
        self.address = address
        self._device = None

    def open(self) -> None:
        if self._device is not None:
            return
        log.info("Opening rangefinder on i2c-%d @ 0x%02X", self.i2c_bus, self.address)
        # TODO: real device init
        self._device = object()

    def close(self) -> None:
        if self._device is None:
            return
        log.info("Closing rangefinder")
        self._device = None

    def read(self) -> Reading:
        if self._device is None:
            raise DriverError("rangefinder not open")
        return Reading(distance_m=self._read_raw(), timestamp=time.monotonic())

    # ---- chip-specific --------------------------------------------------
    def _read_raw(self) -> float:
        """Return distance in meters. Replace with real chip read."""
        # TODO: chip-specific register read
        return 0.500  # placeholder: 0.5 m
