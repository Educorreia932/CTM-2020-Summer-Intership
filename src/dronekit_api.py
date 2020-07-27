import dronekit_sitl

# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal

import time
import math

class dronekit_api:
    def __init__(self, home_location):
        lat = home_location[0]
        lon = home_location[1]
        self.global_home_location = LocationGlobal(lat, lon)

    def connect_vehicle(self, connection_string):
        # Connect to the Vehicle.
        print("Connecting to vehicle on: %s" % (connection_string,))
        self.vehicle = connect(connection_string, wait_ready=True)

    # arms vehicle and fly to target_altitude
    def arm_and_takeoff(self, target_altitude):

        print("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        print("Arming motors")
        # Copter should arm in GUIDED mode
        mode = "GUIDED"
        self.vehicle.mode = VehicleMode(mode)
        while self.vehicle.mode.name != mode:
            print(" Waiting for mode change (current = " + self.vehicle.mode.name + ", expected = " + mode + ")...")
            time.sleep(1)

        if self.vehicle.armed == True:
            was_disarmed = False
        else:
            was_disarmed = True

        self.vehicle.armed = True
        # Confirm vehicle armed before attempting to take off
        while not self.vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        # if vehicle was disarmed it means it was on the ground so it has to takeoff
        if(was_disarmed):
            print("Taking off!")
            self.vehicle.simple_takeoff(target_altitude)  # Take off to target altitude

            # Wait until the vehicle reaches a safe height before processing the goto
            #  (otherwise the command after Vehicle.simple_takeoff will execute
            #   immediately).
            while True:
                print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
                # Break and return from function just below target altitude.
                if self.vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
                    print("Reached target altitude")
                    break
                time.sleep(1)
        else:
            if self.vehicle.location.global_relative_frame.alt < target_altitude * 0.95:
                print("Going up to " + str(target_altitude) + " meters of altitude!")
                lat = self.vehicle.location.global_relative_frame.lat
                lon = self.vehicle.location.global_relative_frame.lon
                location = LocationGlobalRelative(lat, lon, target_altitude)
                self.vehicle.simple_goto(location)  # Go up to target altitude

                # Wait until the vehicle reaches a safe height before processing the goto
                #  (otherwise the command after Vehicle.simple_takeoff will execute
                #   immediately).
                while True:
                    print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
                    # Break and return from function just below target altitude.
                    if self.vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
                        print("Reached target altitude")
                        break
                    
                    time.sleep(1)

    def land(self):
        print("Returning to Launch")
        self.vehicle.mode = VehicleMode("RTL")

    def goto(self, location):

        airspeed = 10
        print("Set default/target airspeed to " + str(airspeed))
        self.vehicle.airspeed = airspeed

        print("Going towards the optimal position ...")
        # X position is North, Y position is East
        # get target_location relative to home location
        x = location[0]
        y = location[1]
        target_location = self.get_location_metres(self.global_home_location, x, y)
        target_location.alt = location[2]
        self.vehicle.simple_goto(target_location)
        
    def get_location_metres(self, original_location, dNorth, dEast):
        """
        Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
        specified `original_location`. The returned LocationGlobal has the same `alt` value
        as `original_location`.
        The function is useful when you want to move the vehicle around specifying locations relative to 
        the current vehicle position.
        The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
        For more information see:
        http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
        """
        earth_radius = 6378137.0 #Radius of "spherical" earth
        
        #Coordinate offsets in radians
        dLat = dNorth / earth_radius
        dLon = dEast / (earth_radius*math.cos(math.pi * original_location.lat / 180))

        #New position in decimal degrees
        newlat = original_location.lat + (dLat * 180 / math.pi)
        newlon = original_location.lon + (dLon * 180 / math.pi)
        
        if type(original_location) is LocationGlobal:
            targetlocation=LocationGlobal(newlat, newlon,original_location.alt)
        
        elif type(original_location) is LocationGlobalRelative:
            targetlocation=LocationGlobalRelative(newlat, newlon, original_location.alt)
        
        else:
            raise Exception("Invalid Location object passed")
            
        return targetlocation
