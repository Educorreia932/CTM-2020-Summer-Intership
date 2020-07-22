import sys

if((len(sys.argv) == 3 and sys.argv[1] == "--connect") == False):
    sys.exit("Usage: python3 main.py --connect <ip:port>")

connection_string = sys.argv[2]

from dronekit_api import *

from utils import *

faps = []

mcs_index_folder = "MCS Index/"
faps_info_folder = "FAPs Info/"

# get UAV config from user input
bandwidth, spatial_streams, guard_interval = get_UAV_config()

snr_filename = mcs_index_folder + str(bandwidth) + "_" + str(spatial_streams) + ".csv"


dronekit_api = dronekit_api()
dronekit_api.connect_vehicle(connection_string)

exit = False
menu_text = "Menu Commands:\n'gwp' to start UAV simulation, it will simulate a real scenario by reading FAPs information from files and changing its position according to this information\n'exit' to shutdown vehicle\nOption: "
while(exit == False):
    option = input(menu_text)
    if(option == "gwp"):
        UAV_simulation(dronekit_api, faps, faps_info_folder, snr_filename, guard_interval)
    elif(option == "exit"):
        # close vehicle
        dronekit_api.vehicle.close()
        print("Complete")
        exit = True
    else:
        print("Invalid Option")