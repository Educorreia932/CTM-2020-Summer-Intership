import csv
from math import *
from sympy.abc import x
from sympy import Poly
from sympy.solvers.inequalities import solve_poly_inequalities

faps = []

class FAP:
    def __init__(self, line):
        self.id = line[0]
        self.x = line[1]
        self.y = line[2]
        self.z = line[3]
        self.traffic = line[4]
    
#  Open input file with the FAPs data
with open("input.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    line_count = 0
    
    for line in csv_reader:
        if line_count != 0:
            fap = FAP(line)
        
            faps.append(fap)
                       
        line_count += 1
              
def solve_equation():
    K = -20 * log10((4 * pi) / (3 * 10 ^ 8)) - 20 * log10(5250 * 10 ^ 6) - (-85) 
    
    # equations = (
    #     (Poly(x - 10), ">"), 
    #     (Poly(-x + 1), ">")
    # )
    
    equations = []
    
    for fap in faps:
        equation = (Poly("x"), ">=")
        
        equations.append(equation)
    
    solution = solve_poly_inequalities(equations)
    
    return solution
                
# (𝑥𝑈𝐴𝑉 𝑟𝑒𝑙𝑎𝑦 −𝑥𝐹𝐴𝑃 𝑁) ^ 2
#  + (𝑦𝑈𝐴𝑉 𝑟𝑒𝑙𝑎𝑦 −𝑦𝐹𝐴𝑃 𝑁) ^ 2
#  + (𝑧𝑈𝐴𝑉 𝑟𝑒𝑙𝑎𝑦 −𝑧𝐹𝐴𝑃 𝑁) ^ 2
#  <= 10 ^
# K + PT − 𝑆𝑁𝑅𝐿𝑖𝑔𝑎ç𝑎𝑜 𝑁
# 20
# 2

def gwp():
    #  Transmission Power (dBm)
    PT = 0
    
    while True:
        solution = solve_equation()
        
        if solution != None:
            return PT, solution
        
        else:
            PT += 1
            
print(gwp())