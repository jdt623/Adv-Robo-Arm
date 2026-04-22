# ROS 2 workspace (Phase 2+)

Empty until Phase 1 drivers are validated. When that time comes:

```bash
# on the Pi
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions
source /opt/ros/jazzy/setup.bash

cd ros2_ws
colcon build --symlink-install
source install/setup.bash
```

One package per driver under `src/`, each importing the corresponding
``robo_arm.drivers.*`` class from the Phase 1 code.
