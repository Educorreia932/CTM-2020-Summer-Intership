import sys

if((len(sys.argv) == 3 and sys.argv[1] == "--connect") == False):
    sys.exit("Usage: python3 main.py --connect <ip:port>")

connection_string = sys.argv[2]

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
PT, location = gwp(faps)
print(PT, location)

# connect vehicle
dronekit_api = dronekit_api()
dronekit_api.connect_vehicle(connection_string)

exit = False
menu_text = "Menu Commands:\n'gwp' to move the UAV to its optimal position\n'exit' to shutdown vehicle\nOption: "
while(exit == False):
    option = input(menu_text)
    if(option == "gwp"):
        dronekit_api.goto(location)
    elif(option == "exit"):
        # close vehicle
        dronekit_api.vehicle.close()
        print("Complete")
        exit = True
    else:
        print("Invalid Option")