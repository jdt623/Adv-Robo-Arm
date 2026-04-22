# Architecture

## Layered design

```
┌───────────────────────────────────────────────────────┐
│  Phase 4: Arm controller (kinematics, behaviors)      │
├───────────────────────────────────────────────────────┤
│  Phase 3: MoveIt 2 / ros2_control                     │
├───────────────────────────────────────────────────────┤
│  Phase 2: ROS 2 Jazzy nodes (one per driver)          │
├───────────────────────────────────────────────────────┤
│  Phase 1: Python drivers  ← src/robo_arm/drivers/ *   │
├───────────────────────────────────────────────────────┤
│  Hardware (I2C / SPI / GPIO / CSI)                    │
└───────────────────────────────────────────────────────┘
```

Key rule: **layers only call downward.** A ROS 2 node imports a driver;
a driver never imports ROS 2. This is why drivers stay reusable if we
ever change frameworks or move a sensor onto a microcontroller.

## Driver contract

Every sensor driver implements `SensorDriver`:
- `open()` — idempotent hardware init.
- `read()` → a frozen dataclass with a timestamp. Units spelled out in field
  names (`distance_m`, `pressure_kpa`, `ax` in g).
- `close()` — idempotent cleanup.
- Context-manager support (`with MyDriver() as d:`).
- Chip-specific code isolated in a single method (e.g. `_read_raw`) so the
  rest of the stack never cares which part number is installed.

Actuators implement `ActuatorDriver` with open/close plus whatever motion
primitives the device exposes.

## ROS 2 migration plan (Phase 2)

When Phase 1 is done, each driver gets a thin node in `ros2_ws/src/`:

```
ros2_ws/src/
├── arm_msgs/                 # custom msg definitions (if needed)
├── accelerometer_node/
├── vision_node/
├── rangefinder_node/
├── pressure_node/
├── stepper_joint_node/       # one instance per joint
└── arm_bringup/              # launch files wiring it all together
```

Each node is maybe 50 lines: a class inheriting from `rclpy.node.Node` that
constructs the driver, ticks a timer, and publishes to a topic. The driver
class is what does the real work.

## Topic conventions (forward-looking)

```
/arm/accel            sensor_msgs/Imu
/arm/range/<id>       sensor_msgs/Range
/arm/pressure/<id>    std_msgs/Float32   (or custom)
/arm/camera/image_raw sensor_msgs/Image
/arm/joint_states     sensor_msgs/JointState
/arm/joint_cmd        trajectory_msgs/JointTrajectory
```

Using stock `sensor_msgs` wherever possible means tools like RViz2, `rqt`,
and MoveIt 2 work out of the box.
