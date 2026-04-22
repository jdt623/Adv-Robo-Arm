"""Base driver interface.

Every hardware driver inherits from ``SensorDriver`` (or ``ActuatorDriver``) so
that upstream code — and later the ROS 2 wrappers — can treat them uniformly.

Design rules:
- ``__init__`` should be cheap and not talk to hardware. Hardware I/O happens
  in ``open()`` so failures are explicit and recoverable.
- Drivers are context managers: ``with MyDriver() as d: d.read()``.
- No driver imports anything ROS 2 related. Phase 2 nodes will *wrap* drivers;
  drivers stay framework-free.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class DriverError(RuntimeError):
    """Raised when a driver cannot fulfill an operation."""


class SensorDriver(ABC):
    """Abstract base for all sensor drivers."""

    name: str = "sensor"

    def __enter__(self) -> SensorDriver:
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @abstractmethod
    def open(self) -> None:
        """Initialize hardware. Must be idempotent."""

    @abstractmethod
    def read(self) -> Any:
        """Return the latest reading. Shape is driver-specific."""

    @abstractmethod
    def close(self) -> None:
        """Release hardware resources. Must be idempotent."""


class ActuatorDriver(ABC):
    """Abstract base for all actuator drivers (motors, solenoids, etc.)."""

    name: str = "actuator"

    def __enter__(self) -> ActuatorDriver:
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @abstractmethod
    def open(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...
