"""Stepper motor driver.

Placeholder — move your existing working stepper code into this module,
conforming it to the ``ActuatorDriver`` interface (open/close + whatever
motion primitives you already have: step, move_to, set_speed, home, etc).

Keeping it here (instead of outside the repo) is what makes the whole arm
modular: the controller and the Phase 2 ROS 2 node will both import
``StepperDriver`` from this one place.
"""
from __future__ import annotations

import logging

from robo_arm.common import ActuatorDriver, DriverError

log = logging.getLogger(__name__)


class StepperDriver(ActuatorDriver):
    """Single stepper motor. Replace the internals with your working code."""

    name = "stepper"

    def __init__(
        self,
        step_pin: int,
        dir_pin: int,
        enable_pin: int | None = None,
        steps_per_rev: int = 200,
    ) -> None:
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.enable_pin = enable_pin
        self.steps_per_rev = steps_per_rev
        self._opened = False
        self._position_steps = 0

    def open(self) -> None:
        if self._opened:
            return
        log.info(
            "Opening stepper (step=%d dir=%d enable=%s)",
            self.step_pin,
            self.dir_pin,
            self.enable_pin,
        )
        # TODO: initialize GPIO here using your existing approach
        self._opened = True

    def close(self) -> None:
        if not self._opened:
            return
        log.info("Closing stepper")
        # TODO: release GPIO
        self._opened = False

    # ---- motion primitives (stubs) --------------------------------------

    def step(self, n: int = 1, direction: int = 1, delay_s: float = 0.001) -> None:
        """Advance by ``n`` steps in ``direction`` (+1 / -1)."""
        if not self._opened:
            raise DriverError("stepper not open")
        # TODO: toggle step pin n times
        self._position_steps += n * direction

    def move_to(self, target_steps: int, delay_s: float = 0.001) -> None:
        delta = target_steps - self._position_steps
        if delta == 0:
            return
        self.step(n=abs(delta), direction=1 if delta > 0 else -1, delay_s=delay_s)

    @property
    def position_steps(self) -> int:
        return self._position_steps
