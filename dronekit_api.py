import dronekit_sitl

# Import DroneKit-Python
from dronekit import connect, VehicleMode

class dronekit_api:
    def connect_vehicle(self, connection_string):
        # Connect to the Vehicle.
        print("Connecting to vehicle on: %s" % (connection_string,))
        self.vehicle = connect(connection_string, wait_ready=True)
        '''
        # Get some vehicle attributes (state)
        print "Get some vehicle attribute values:"
        print " GPS: %s" % vehicle.gps_0
        print " Battery: %s" % vehicle.battery
        print " Last Heartbeat: %s" % vehicle.last_heartbeat
        print " Is Armable?: %s" % vehicle.is_armable
        print " System status: %s" % vehicle.system_status.state
        print " Mode: %s" % vehicle.mode.name    # settable
        '''        