import csv
from gekko import GEKKO
from math import log10, pi

faps = []

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

#  Open input file with the FAPs data
with open("input.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    line_count = 0
    
    for line in csv_reader:
        if line_count != 0:
            fap = FAP(line)
        
            faps.append(fap)
                       
        line_count += 1
              
def solve_equation(PT):
    K = -20 * log10((4 * pi) / (3 * 10 ** 8)) - 20 * log10(5250 * 10 ** 6) - (-85) 
    
    m = GEKKO(remote = False)
    
    x = m.Var()
    y = m.Var()
    z = m.Var()

    for fap in faps:
        x_term = (x - fap.x) ** 2
        y_term = (y - fap.y) ** 2
        z_term = (z - fap.z) ** 2
        
        print(fap.snr)
               
        radius_term = (10 ** ((K + PT - fap.snr) / 20)) ** 2
        
        m.Equation(x_term + y_term + z_term <= radius_term)
 
    try:
        m.solve(disp = False)
        solution = (x.value, y.value, z.value)
        
    except:
        solution = None
        
    return solution
                
def gwp():
    #  Transmission Power (dBm)
    PT = 0
    
    while True:
        solution = solve_equation(PT)
        
        if solution != None:
            return PT, solution
        
        else:
            PT += 1
            
print(gwp())