import sys
from dronekit_api import *
from utils import *

# Verify command line arguments
if ((len(sys.argv) == 5 and sys.argv[1] == "--connect" and sys.argv[3] == "--home") == False):
    sys.exit("Usage: python3 main.py --connect <ip:port> --home <lat>,<lon>,<alt>,<heading>")

connection_string = sys.argv[2]
home_location = [float(i) for i in sys.argv[4].split(",")]

# Folders location
mcs_index_folder = "MCS Index/"
faps_info_folder = "FAPs Info/"

# get UAV config from user input: [bandwidth, spatial streams, guard interval]
uav_config = get_UAV_config()

snr_filename = mcs_index_folder + str(uav_config["bandwidth"]) + "_" + str(uav_config["spatial_streams"]) + ".csv"

dronekit_api = dronekit_api(home_location)
dronekit_api.connect_vehicle(connection_string)

exit = False

menu_text = "\nMenu Commands:\n'gwp' to start UAV simulation, it will simulate a real scenario by reading FAPs information from files and changing its position according to this information\n'exit' to shutdown vehicle\nOption: "

while (exit == False):
    option = input(menu_text)
    
    if option == "gwp":
        UAV_simulation(dronekit_api, faps_info_folder, snr_filename, uav_config)
    
    elif option == "exit":
        # Close vehicle
        dronekit_api.vehicle.close()
        print("Complete")
        exit = True
        
    else:
        print("Invalid Option")
        