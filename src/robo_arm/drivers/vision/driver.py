"""Accelerometer driver — ADXL345 via I2C.

Uses the Adafruit CircuitPython ADXL345 library over `adafruit-blinka`
(which adapts CircuitPython's hardware API to the Raspberry Pi).

Design preserved from the original stub:
- Stable public API (`open`, `read`, `close`, `calibrate`) returning `Reading`
  dataclass in g's.
- Chip-specific code isolated to `_open_device` and `_read_raw` — swap these
  two methods to support a different accelerometer without touching the rest.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from robo_arm.common import DriverError, SensorDriver

log = logging.getLogger(__name__)

# ADXL345 can report in g; blinka's adafruit_adxl34x returns m/s^2 by default.
# Convert using standard gravity.
_G = 9.80665  # m/s^2


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
    """ADXL345 I2C accelerometer driver.

    Parameters
    ----------
    i2c_bus:
        Linux I2C bus number (``/dev/i2c-<N>``). On Pi 5 the default user
        bus is 1.
    address:
        7-bit I2C device address. 0x53 is the ADXL345 default (SDO→GND).
        0x1D is the alternate address (SDO→VCC).
    offsets:
        Per-axis zero offsets in g, applied to every reading after the raw
        read. Call ``calibrate()`` once at rest to populate automatically.
    data_rate_hz:
        ADXL345 output data rate in Hz. 100 Hz is a good default for slow
        motion like a robot arm. Valid: 0.1, 0.2, 0.39, 0.78, 1.56, 3.13,
        6.25, 12.5, 25, 50, 100, 200, 400, 800, 1600, 3200.
    range_g:
        ±g range. 2 gives the finest resolution; use 16 only if you expect
        high-g impacts.
    """

    name = "accelerometer"

    def __init__(
        self,
        i2c_bus: int = 1,  # noqa: ARG002 — kept for API symmetry; blinka picks bus automatically
        address: int = 0x53,
        offsets: tuple[float, float, float] = (0.0, 0.0, 0.0),
        data_rate_hz: float = 100.0,
        range_g: int = 2,
    ) -> None:
        self.i2c_bus = i2c_bus
        self.address = address
        self.offsets = offsets
        self.data_rate_hz = data_rate_hz
        self.range_g = range_g
        self._device = None  # adafruit_adxl34x.ADXL345 instance once open
        self._i2c = None  # busio.I2C handle, released on close

    # ---- lifecycle ----------------------------------------------------

    def open(self) -> None:
        if self._device is not None:
            return  # idempotent

        log.info("Opening ADXL345 on i2c-%d @ 0x%02X", self.i2c_bus, self.address)
        try:
            import adafruit_adxl34x  # type: ignore[import-not-found]
            import board  # type: ignore[import-not-found]
            import busio  # type: ignore[import-not-found]
        except ImportError as e:
            raise DriverError(
                "Required libraries missing. Run: pip install adafruit-blinka "
                "adafruit-circuitpython-adxl34x"
            ) from e

        try:
            self._i2c = busio.I2C(board.SCL, board.SDA)
            self._device = adafruit_adxl34x.ADXL345(self._i2c, address=self.address)
        except Exception as e:  # noqa: BLE001
            raise DriverError(
                f"failed to open ADXL345 at 0x{self.address:02X}. "
                f"Check wiring and run `i2cdetect -y 1`. Cause: {e}"
            ) from e

        self._configure()

    def _configure(self) -> None:
        """Apply data rate and range settings to the chip."""
        import adafruit_adxl34x  # type: ignore[import-not-found]

        rate_map = {
            3200: adafruit_adxl34x.DataRate.RATE_3200_HZ,
            1600: adafruit_adxl34x.DataRate.RATE_1600_HZ,
            800: adafruit_adxl34x.DataRate.RATE_800_HZ,
            400: adafruit_adxl34x.DataRate.RATE_400_HZ,
            200: adafruit_adxl34x.DataRate.RATE_200_HZ,
            100: adafruit_adxl34x.DataRate.RATE_100_HZ,
            50: adafruit_adxl34x.DataRate.RATE_50_HZ,
            25: adafruit_adxl34x.DataRate.RATE_25_HZ,
        }
        range_map = {
            2: adafruit_adxl34x.Range.RANGE_2_G,
            4: adafruit_adxl34x.Range.RANGE_4_G,
            8: adafruit_adxl34x.Range.RANGE_8_G,
            16: adafruit_adxl34x.Range.RANGE_16_G,
        }

        rate_key = int(self.data_rate_hz)
        if rate_key not in rate_map:
            log.warning("data_rate_hz=%s not in standard set; using 100 Hz", self.data_rate_hz)
            rate_key = 100
        if self.range_g not in range_map:
            log.warning("range_g=%s not in {2,4,8,16}; using 2", self.range_g)
            self.range_g = 2

        self._device.data_rate = rate_map[rate_key]
        self._device.range = range_map[self.range_g]
        log.info("ADXL345 configured: %d Hz, ±%d g", rate_key, self.range_g)

    def close(self) -> None:
        if self._device is None:
            return
        log.info("Closing ADXL345")
        try:
            if self._i2c is not None and hasattr(self._i2c, "deinit"):
                self._i2c.deinit()
        finally:
            self._device = None
            self._i2c = None

    # ---- data ---------------------------------------------------------

    def read(self) -> Reading:
        """Return one calibrated reading in g."""
        if self._device is None:
            raise DriverError("accelerometer not open — call open() first")

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
        if self._device is None:
            raise DriverError("accelerometer not open — call open() first")

        log.info("Calibrating over %d samples — keep the sensor still", samples)
        sx = sy = sz = 0.0
        for _ in range(samples):
            r = self._read_raw()
            sx += r[0]
            sy += r[1]
            sz += r[2]
            time.sleep(1.0 / self.data_rate_hz)
        off = (sx / samples, sy / samples, sz / samples - 1.0)  # subtract 1g from Z
        self.offsets = off
        log.info("Calibration offsets: ax=%.4f, ay=%.4f, az=%.4f g", *off)
        return off

    # ---- chip-specific ------------------------------------------------

    def _read_raw(self) -> tuple[float, float, float]:
        """Return raw (ax, ay, az) in g from the ADXL345.

        The Adafruit library returns m/s^2; we convert to g for consistency
        with the driver's public units.
        """
        ax_ms2, ay_ms2, az_ms2 = self._device.acceleration
        return (ax_ms2 / _G, ay_ms2 / _G, az_ms2 / _G)
