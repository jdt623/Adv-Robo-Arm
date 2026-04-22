# Development Setup

## One-time Pi setup

Assumes Ubuntu 24.04 already installed on a Raspberry Pi 5.

```bash
# System packages
sudo apt update
sudo apt install -y git python3-venv python3-dev python3-pip \
                    i2c-tools build-essential

# Enable I2C / SPI (if not already on)
# Add your user to hardware groups so you don't need sudo for GPIO/I2C
sudo usermod -aG gpio,i2c,spi,dialout $USER
# Log out and back in for group changes to take effect.
```

## Clone and install

```bash
cd ~
git clone https://github.com/jdt623/Adv-Robo-Arm.git
cd Adv-Robo-Arm
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install -e .
```

## Verify install

```bash
python -m robo_arm.drivers.accelerometer   # Ctrl+C to stop
pytest                                      # runs non-hardware tests
pytest -m hardware                          # runs hardware tests (skipped in CI)
```

## VS Code Remote-SSH

Host entry (see `~/.ssh/config` on your dev machine):

```
Host robotarm
    HostName <pi-ip-or-hostname>
    User <pi-username>
    IdentityFile ~/.ssh/id_ed25519_robotarm
```

In VS Code: `F1` → `Remote-SSH: Connect to Host` → `robotarm` → open the
`~/Adv-Robo-Arm` folder.

## Typical dev loop

```bash
# on Pi (via Remote-SSH terminal)
source .venv/bin/activate
git checkout -b feat/accelerometer
# …edit code…
python -m robo_arm.drivers.accelerometer
pytest
git commit -am "Accelerometer: LIS3DH support"
git push -u origin feat/accelerometer
# open a PR on GitHub, merge to main
```
