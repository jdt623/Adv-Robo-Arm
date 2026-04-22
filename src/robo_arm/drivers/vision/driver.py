"""AI vision driver.

Wraps a camera (Picamera2 on Pi 5 by default) and, optionally, an inference
model. Returns frames as numpy arrays plus structured detections.

Run the test harness with:  python -m robo_arm.drivers.vision

Phase 1 scope: just verify frames are captured and print shape + FPS.
Phase 2+: add an inference backend (YOLO via Hailo/Coral or ONNX Runtime).
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

from robo_arm.common import DriverError, SensorDriver

log = logging.getLogger(__name__)


@dataclass
class Frame:
    """One captured frame plus any detections found in it."""

    image: Any  # numpy.ndarray once picamera2 is wired in
    timestamp: float
    detections: list[dict] = field(default_factory=list)


class VisionDriver(SensorDriver):
    """Camera + (optional) object detector."""

    name = "vision"

    def __init__(self, resolution: tuple[int, int] = (640, 480), fps: int = 30) -> None:
        self.resolution = resolution
        self.fps = fps
        self._camera = None

    def open(self) -> None:
        if self._camera is not None:
            return
        log.info("Opening camera at %sx%s @ %d fps", *self.resolution, self.fps)
        # TODO: from picamera2 import Picamera2; self._camera = Picamera2(); ...
        self._camera = object()

    def close(self) -> None:
        if self._camera is None:
            return
        log.info("Closing camera")
        self._camera = None

    def read(self) -> Frame:
        if self._camera is None:
            raise DriverError("camera not open")
        # TODO: real capture
        return Frame(image=None, timestamp=time.monotonic())
