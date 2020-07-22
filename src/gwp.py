from gekko import GEKKO
from math import log10, pi

def solve_equation(PT, faps):
    K = -20 * log10((4 * pi) / (3 * 10 ** 8)) - 20 * log10(5250 * 10 ** 6) - (-85) 
    
    m = GEKKO(remote = False)
    
    x = m.Var()
    y = m.Var()
    z = m.Var()

    for fap in faps:
        x_term = (x - fap.x) ** 2
        y_term = (y - fap.y) ** 2
        z_term = (z - fap.z) ** 2
               
        radius_term = (10 ** ((K + PT - fap.snr) / 20)) ** 2
        
        m.Equation(x_term + y_term + z_term <= radius_term)
 
    try:
        m.solve(disp = False)
        solution = (x.value[0], y.value[0], z.value[0])
        
    except:
        solution = None
        
    return solution
                
def gwp(faps):
    #  Transmission Power (dBm)
    PT = 0
    
    while True:
        solution = solve_equation(PT, faps)
        
        if solution != None:
            return PT, solution
        
        else:
            PT += 1