class FAP:
    def __init__(self, line, snr_file, guard_interval):
        self.id = line[0]
        self.x = line[1]
        self.y = line[2]
        self.z = line[3]
        self.traffic = line[4]
        self.snr = getSnr(self.traffic, snr_file, guard_interval)

def getSnr(traffic, snr_file, guard_interval):
    if(guard_interval == 800):
        traffic_index = 0
    elif(guard_interval == 400):
        traffic_index = 1

    snr_file = open(snr_file, "r")
    for line in snr_file.readlines():
        fields = line.split(',') # Traffic (800ns), Traffic (400ns), Minimum SNR
        if(float(traffic) <= float(fields[traffic_index])):
            snr = int(fields[2])
            break
    snr_file.close()
    return snr