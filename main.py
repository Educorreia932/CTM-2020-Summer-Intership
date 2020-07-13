import csv
from FAP import FAP
from gwp import gwp
from dronekit_api import *

faps = []

#  Open input file with the FAPs data
with open("input.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    line_count = 0
    
    for line in csv_reader:
        if line_count != 0:
            fap = FAP(line)
        
            faps.append(fap)
                       
        line_count += 1

# execute the GWP algorithm and print the power transmission needed for the GW UAV and its position
print(gwp(faps))

# initialize SITL
dronekit_api = dronekit_api()
dronekit_api.initialize_SITL()

dronekit_api.connect_vehicle()

# close vehicle and stop SITL
dronekit_api.stop_SITL()