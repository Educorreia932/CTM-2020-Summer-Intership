#!/bin/bash
# exit when any command fails
set -e

MASTER="tcp:127.0.0.1:5760"
SITL="127.0.0.1:5501"
OUT1="127.0.0.1:14550"
OUT2="127.0.0.1:14551"

gnome-terminal -- /bin/bash -c "cd ../../ardupilot/ArduCopter; ../Tools/autotest/sim_vehicle.py --console --map"
gnome-terminal -- /bin/bash -c "python3 main.py --connect $OUT1; exec bash"