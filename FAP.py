class FAP:
    def __init__(self, line):
        self.id = line[0]
        self.x = line[1]
        self.y = line[2]
        self.z = line[3]
        self.traffic = line[4]
        self.snr = getSnr(self.traffic)

def getSnr(traffic):
    snr_file = open("snr.csv", "r")
    snr_file.readline() # read first line
    for line in snr_file.readlines():
        fields = line.split(',') # Data Rate, Minimum SNR
        if(float(traffic) <= float(fields[0])):
            snr = int(fields[1])
            break
    snr_file.close()
    return snr