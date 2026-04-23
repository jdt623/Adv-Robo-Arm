"""Accelerometer driver implementation.

Intentionally split into two layers:
- ``AccelerometerDriver``: stable public API, units in g, calibration applied.
- ``_read_raw``: chip-specific bus access. Swap this when you choose a sensor.

This separation means the ROS 2 node (Phase 2) and arm controller (Phase 4)
never need to know which accelerometer chip is installed.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from robo_arm.common import DriverError, SensorDriver

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Reading:
    """A single accelerometer sample.

    Units: g (1 g ≈ 9.81 m/s^2). Timestamp is monotonic seconds.
    """

    ax: float
    ay: float
    az: float
    timestamp: float


class AccelerometerDriver(SensorDriver):
    """I2C accelerometer driver.

    Parameters
    ----------
    i2c_bus:
        Linux I2C bus number (``/dev/i2c-<N>``). On Pi 5, bus 1 is the default
        user I2C bus.
    address:
        7-bit I2C device address. Check your chip's datasheet.
    offsets:
        Per-axis zero offsets in g, applied to every reading.
    """

    name = "accelerometer"

    def __init__(
        self,
        i2c_bus: int = 1,
        address: int = 0x18,
        offsets: tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> None:
        self.i2c_bus = i2c_bus
        self.address = address
        self.offsets = offsets
        self._bus = None  # populated in open()

    # ---- lifecycle ----------------------------------------------------

    def open(self) -> None:
        if self._bus is not None:
            return  # idempotent
        log.info("Opening accelerometer on i2c-%d @ 0x%02X", self.i2c_bus, self.address)
        try:
            # TODO: replace with real bus init once chip is chosen.
            # Example (smbus2):
            #   import smbus2
            #   self._bus = smbus2.SMBus(self.i2c_bus)
            #   self._write_config()
            self._bus = object()  # placeholder so close() has something to release
        except Exception as e:  # noqa: BLE001
            raise DriverError(f"failed to open accelerometer: {e}") from e

    def close(self) -> None:
        if self._bus is None:
            return
        log.info("Closing accelerometer")
        # if hasattr(self._bus, "close"): self._bus.close()
        self._bus = None

    # ---- data ---------------------------------------------------------

    def read(self) -> Reading:
        """Return one calibrated reading in g."""
        if self._bus is None:
            raise DriverError("accelerometer not open — call open() first")
        import time

        ax_raw, ay_raw, az_raw = self._read_raw()
        return Reading(
            ax=ax_raw - self.offsets[0],
            ay=ay_raw - self.offsets[1],
            az=az_raw - self.offsets[2],
            timestamp=time.monotonic(),
        )

    def calibrate(self, samples: int = 200) -> tuple[float, float, float]:
        """Compute zero offsets by averaging ``samples`` readings.

        Assumes the sensor is at rest with +Z pointing up (so az ≈ 1 g).
        Stores the result on ``self.offsets`` and returns it.
        """
        if samples <= 0:
            raise ValueError("samples must be positive")
        log.info("Calibrating over %d samples — keep the sensor still", samples)
        sx = sy = sz = 0.0
        for _ in range(samples):
            r = self._read_raw()
            sx += r[0]
            sy += r[1]
            sz += r[2]
        off = (sx / samples, sy / samples, sz / samples - 1.0)  # subtract 1g from Z
        self.offsets = off
        log.info("Calibration offsets: %s", off)
        return off

    # ---- chip-specific (replace these two lines when hardware is chosen) ---

    def _read_raw(self) -> tuple[float, float, float]:
        """Return raw (ax, ay, az) in g straight from the chip.

        Replace this stub with the real register read for your accelerometer.
        """
        # Placeholder so the module runs end-to-end without hardware.
        # TODO: read OUT_X/Y/Z registers, combine bytes, apply sensitivity.
        return (0.0, 0.0, 1.0)
