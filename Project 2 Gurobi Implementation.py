# Rohan Bhagat
# ISYE 3133
# Project 2
# Studio Section MW1
# GTID: 903657424

from gurobipy import GRB,Model
import numpy as np
m = Model('Project 2')
m.setParam('OutputFlag', False)

with open('staffing_requirements.csv') as f:
    rows = f.read().split('\n')
types = []
for row in rows[1:len(rows) - 1]:
    row = row.split(',')
    intRow = []
    for element in row:
        intRow.append(int(element))
    types.append(intRow)

with open('pay.csv') as f:
    rows = f.read().split('\n')
salaries = []
for row in rows[1:len(rows) - 1]:
    row = row.split(',')
    numberRow = []
    for element in row:
        numberRow.append(int(float((element))))
    salaries.append(tuple(numberRow))

# problem-specific variables
with open('total_shifts.csv') as f:
    s = int(f.read().split('\n')[1])

k = len(types)
n = len(types[1]) - 1



# pay scale vectors
x_reg = np.array([np.array(row) for row in salaries])[:, 1]
x_ot = np.array([np.array(row) for row in salaries])[:, 2]

# staffing requirements matrix
reqs = np.array([np.array(row) for row in types])[:,1:]
A = m.addMVar((k,n), vtype=GRB.INTEGER, name = 'Non-Overtime Employee Starting Shifts')
B = m.addMVar((k,n), vtype=GRB.INTEGER, name = 'Overtime Employee Starting Shifts')
m.addConstrs((A[(i-3)%12, :] +
                A[(i-2)%12, :] +
                A[(i-1)%12, :] +
                A[i, :] +
                B[(i-4)%12, :] +
                B[(i-3)%12, :] +
                B[(i-2)%12, :] +
                B[(i-1)%12, :] +
                B[i, :] >= reqs[i] for i in range(k)), name='c1')
m.setObjective(sum((A @ x_reg) + (B @ x_reg) + (B @ x_ot)), GRB.MINIMIZE)
m.optimize() 
if m.status == 2:
    print("The solution found is optimal.")
    print(f"The optimal objective value is {m.objVal}")
    totalEmployees = 0
    totalOT = 0
    for j in range(n):
        employees = 0
        ot = 0
        for i in range(k):
            otToAdd = B[i,j].x
            ot += otToAdd
            employees += (A[i, j].x + otToAdd)
        print(f"The required number of employees (regular and overtime) of type {j} is {employees}.")
    print(f"{ot/employees} of our employees will work an overtime shift.")
else:
    print("The solution found is not optimal.")
