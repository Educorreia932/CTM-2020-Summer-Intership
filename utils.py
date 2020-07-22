import os
import csv
from FAP import FAP
from gwp import gwp

# simulates a real scenario where FAPs change their positions and traffic demand,
# and the UAV also changes its position to support this changes
def UAV_simulation(dronekit_api, faps, faps_info_folder, snr_filename, guard_interval):

    dronekit_api.arm_and_takeoff(10)

    for filename in sorted(os.listdir(faps_info_folder)):
        if filename.endswith(".csv"): 
            
            input("Press ENTER to get new FAPs information (filename " + filename + "): ")

            updateFAPs(faps, faps_info_folder + filename, snr_filename, guard_interval)
            
            # execute the GWP algorithm and print the power transmission needed for the GW UAV and its position
            PT, location = gwp(faps)
            print(PT, location)

            dronekit_api.goto(location)

    input("Press ENTER to return to launch position: ")
    dronekit_api.land()

# read new FAPs info from input_filename and updates faps list
def updateFAPs(faps, input_filename, snr_filename, guard_interval):
    
    faps.clear()

    #  Open input file with the FAPs data
    with open(input_filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0
        
        for line in csv_reader:
            if line_count != 0:
                fap = FAP(line, snr_filename, guard_interval)
            
                faps.append(fap)
                        
            line_count += 1

# returns bandwidth, spatial streams and guard interval specified by the user
def get_UAV_config():

    # ask the user for the bandwidth
    while(True):
        try:
            bandwidth = int(input("Bandwith (20, 40, 80 or 160 MHz): "))
            if(bandwidth in [20, 40, 80, 160]):
                break
            else:
                print("Invalid Option")
        except ValueError:
            print("Invalid Option")

    # ask the user for the number of spatial streams
    while(True):
        try:
            spatial_streams = int(input("Spatial Streams (1, 2 or 3): "))
            if(spatial_streams in [1,2,3]):
                break
            else:
                print("Invalid Option")
        except ValueError:
            print("Invalid Option")

    # ask the user for the Guard Interval to be used
    while(True):
        try:
            guard_interval = int(input("Guard Interval (400 or 800ns): "))
            if(guard_interval in [400, 800]):
                break
            else:
                print("Invalid Option")
        except ValueError:
            print("Invalid Option")

    return bandwidth, spatial_streams, guard_interval