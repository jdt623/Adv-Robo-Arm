"""Pressure sensor driver.

Returns force/pressure in kilopascals or newtons depending on sensor class.
Swap ``_read_raw`` for your specific part (e.g. force-sensitive resistor via
ADC, BMP390 for absolute pressure, etc.).

Run:  python -m robo_arm.drivers.pressure
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from robo_arm.common import DriverError, SensorDriver

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Reading:
    pressure_kpa: float
    timestamp: float


class PressureDriver(SensorDriver):
    name = "pressure"

    def __init__(self, i2c_bus: int = 1, address: int = 0x77) -> None:
        self.i2c_bus = i2c_bus
        self.address = address
        self._device = None

    def open(self) -> None:
        if self._device is not None:
            return
        log.info("Opening pressure sensor on i2c-%d @ 0x%02X", self.i2c_bus, self.address)
        self._device = object()

    def close(self) -> None:
        if self._device is None:
            return
        log.info("Closing pressure sensor")
        self._device = None

    def read(self) -> Reading:
        if self._device is None:
            raise DriverError("pressure sensor not open")
        return Reading(pressure_kpa=self._read_raw(), timestamp=time.monotonic())

    def _read_raw(self) -> float:
        """Return pressure in kPa. Replace with real chip read."""
        return 101.325  # placeholder: standard atmosphere
