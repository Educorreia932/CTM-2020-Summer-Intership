import os
import csv
from FAP import FAP
from gwp import gwp

# simulates a real scenario where FAPs change their position and traffic demand,
# and the UAV adjusts its position according to the FAPs
def UAV_simulation(dronekit_api, faps_info_folder, snr_filename, uav_config):

    faps = []

    dronekit_api.arm_and_takeoff(10)

    for filename in sorted(os.listdir(faps_info_folder)):
        if filename.endswith(".csv"): 

            faps_info_filename = faps_info_folder + filename
            
            input("\nPress ENTER to get new FAPs information (filename " + faps_info_filename + "): ")

            # updateFAPs returns true if the UAV can handle the FAPs traffic, false otherwise
            if(updateFAPs(faps, faps_info_filename, snr_filename, uav_config["guard_interval"]) == True):

                # execute the GWP algorithm and print the power transmission needed for the GW UAV and its position
                PT, location = gwp(faps)
                print("\nPT: " + str(PT))
                print("Location:")
                print(" x: " + str(location[0]))
                print(" y: " + str(location[1]))
                print(" z: " + str(location[2]))

                dronekit_api.goto(location)
            else:
                print("\nUAV Configuration:")
                print(" Bandwidth: " + str(uav_config["bandwidth"]) + "MHz")
                print(" Spatial Streams: " + str(uav_config["spatial_streams"]))
                print(" Guard Interval: " + str(uav_config["guard_interval"]) + "ns")
                print("Error: This UAV configuration can't handle the FAPs traffic from file " + faps_info_filename + ". Please change the FAPs information in this file or the UAV configuration.")


    input("\nPress ENTER to return to launch position: ")
    dronekit_api.land()

# from a FAP traffic get the corresponding SNR value from a file that contains MCS Index values
def getSnr(traffic, guard_interval, snr_file):
    snr = None
    
    if(guard_interval == 800):
        traffic_index = 0
    elif(guard_interval == 400):
        traffic_index = 1

    snr_file = open(snr_file, "r")
    for line in snr_file.readlines():
        fields = line.split(',') # Traffic (800ns), Traffic (400ns), Minimum SNR
        if fields[traffic_index] == "N/A":
            continue
        if(float(traffic) <= float(fields[traffic_index])):
            snr = int(fields[2])
            break
    snr_file.close()
    return snr

# read new FAPs info from input_filename and updates faps list
def updateFAPs(faps, input_filename, snr_filename, guard_interval):
    
    faps.clear()

    #  Open input file with the FAPs data
    with open(input_filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0
        
        for line in csv_reader:
            if line_count != 0:
                fap_id = line[0]
                x = line[1]
                y = line[2]
                z = line[3]
                traffic = line[4]

                snr = getSnr(traffic, guard_interval, snr_filename)
                if snr == None:
                    return False

                fap = FAP(fap_id, x, y, z, traffic, snr)
            
                faps.append(fap)
                        
            line_count += 1

    return True

# returns bandwidth, spatial streams and guard interval specified by the user
def get_UAV_config():

    # ask the user for the bandwidth
    while(True):
        try:
            bandwidth = int(input("Bandwidth (20, 40, 80 or 160 MHz): "))
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

    return {"bandwidth": bandwidth, "spatial_streams": spatial_streams, "guard_interval": guard_interval}