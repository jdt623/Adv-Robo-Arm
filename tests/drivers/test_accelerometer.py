"""Unit tests for AccelerometerDriver.

These run WITHOUT hardware because the driver's ``_read_raw`` is a stub until
you wire up a real chip. Tests that need hardware should be marked
``@pytest.mark.hardware`` and will be skipped in CI.
"""
from __future__ import annotations

import pytest

from robo_arm.common import DriverError
from robo_arm.drivers.accelerometer import AccelerometerDriver, Reading


def test_read_requires_open() -> None:
    d = AccelerometerDriver()
    with pytest.raises(DriverError):
        d.read()


def test_context_manager_opens_and_closes() -> None:
    d = AccelerometerDriver()
    assert d._bus is None
    with d:
        assert d._bus is not None
        r = d.read()
        assert isinstance(r, Reading)
    assert d._bus is None


def test_offsets_applied() -> None:
    d = AccelerometerDriver(offsets=(0.1, 0.2, 0.3))
    with d:
        r = d.read()
    # stub returns (0, 0, 1); subtract offsets
    assert r.ax == pytest.approx(-0.1)
    assert r.ay == pytest.approx(-0.2)
    assert r.az == pytest.approx(0.7)


@pytest.mark.hardware
def test_real_hardware_present() -> None:
    """Verifies a real accelerometer is wired up. Skip in CI."""
    with AccelerometerDriver() as d:
        r = d.read()
        # Gravity should be detectable on at least one axis.
        assert abs(r.ax) + abs(r.ay) + abs(r.az) > 0.5
