#!/bin/bash
# exit when any command fails
set -e

MASTER="tcp:127.0.0.1:5760"
SITL="127.0.0.1:5501"
OUT1="127.0.0.1:14550"
OUT2="127.0.0.1:14551"
HOME_LOCATION="41.177942,-8.596081,0,0" # latitude, longitude, altitude, heading (FEUP)

echo "Press ENTER to start ArduPilot: "
read VAR
gnome-terminal -- /bin/bash -c "ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter --custom-location=$HOME_LOCATION --console --map"

echo "Press ENTER to start the program (to avoid timeout errors do this only when the map from ArduPilot is loaded): "
read VAR
gnome-terminal -- /bin/bash -c "python3 src/main.py --connect $OUT1 --home $HOME_LOCATION; exec bash"