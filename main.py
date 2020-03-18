from coolFuncs import Node, customReturn, reRoll, initNodeMatrix,contourCalc
import math
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import matplotlib.pyplot as plt

wd = float(input("enter wd: "))
bd = float(input("enter bd: "))
aw = float(input("enter aw: "))
na = int(input("enter na: "))
nb = int(input("enter nb: "))
Er = float(input("enter Er: "))
customRelax = str(input("custom relaxation parameter? (T/F): "))
if customRelax == "T":
    relaxation = float(input("enter relaxation: "))
else:
    relaxation = 2 * (1 - (math.pi / math.sqrt(2)) * math.sqrt((1 / math.pow(na, 2)) + (1 / math.pow(nb, 2))))
gr = str(input("3D graph? (T/F): "))
if gr == "T":
    print("1 for Air Line")
    print("2 for Substrate")
    print("3 for Both")
    choice = int(input())
else:
    choice = 0
grab = initNodeMatrix(wd,bd,aw,na,nb)
nodes = grab.getMat()
alpha = grab.getAdditional1()
temp = grab.getAdditional2()
stripThreshX = temp.getAdditional1()
interfaceY = temp.getAdditional2()
print()
print("relaxation: " + str.format('{0:1.4f}', relaxation))
print("alpha : " + str.format('{0:1.4f}', alpha))

#setup for potential calculation
resMax = 100
itER = 0
itAIR = 0
while resMax > pow(10, -5) and itER < 1000:
    resMax = 0
    ret = reRoll(nodes, na, nb, resMax, alpha, relaxation, Er)
    nodesEr = ret.getMat()
    resMax = ret.getAdditional1()
    itER = itER + 1

grab = initNodeMatrix(wd, bd, aw, na, nb)
nodes = grab.getMat()
resMax = 100
while resMax > pow(10, -5) and itAIR < 1000:
    resMax = 0
    ret = reRoll(nodes, na, nb, resMax, alpha, relaxation, 1)
    nodesAir = ret.getMat()
    resMax = ret.getAdditional1()
    itAIR = itAIR + 1

#these arrays are for the graphics
AirX = []
AirY = []
AirZ = []
ErX = []
ErY = []
ErZ = []

for row in range(0, nb):
    for col in range(0, na):
        ErX.append(col)
        ErY.append(row)
        ErZ.append(nodesEr[row][col].getPot())

for row in range(0, nb):
    for col in range(0, na):
        AirX.append(col)
        AirY.append(row)
        AirZ.append(nodesAir[row][col].getPot())

print("Iterations (Air): " + str(itAIR))
print("Iterations (Er): " + str(itER))

CEoAir = contourCalc(nodesAir,stripThreshX,interfaceY,na,nb,alpha,1)
CEoEr = contourCalc(nodesEr,stripThreshX,interfaceY,na,nb,alpha,Er)
Eo = float(pow(10, -9)/(36*math.pi))
CAir = CEoAir*Eo*-1
CEr = CEoEr*Eo*-1
print("C/Eo Air: " +str.format('{0:1.4f}', CEoAir))
print("C/Eo Er: " +str.format('{0:1.4f}', CEoEr))

if choice == 1 or choice == 3:
    AirXnp = np.array(AirX)
    AirYnp = np.array(AirY)
    AirZnp = np.array(AirZ)


    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection ='3d')

    ax1.title.set_text("Air Line")
    ax1.set_xlim(na,0)
    ax1.set_ylim(nb,0)
    ax1.set_xlabel('na')
    ax1.set_ylabel('nb')
    ax1.set_zlabel('potential')
    ax1.plot_trisurf(AirXnp,AirYnp,AirZnp)
    plt.show()

if choice == 2 or choice == 3:
    ErXnp = np.array(ErX)
    ErYnp = np.array(ErY)
    ErZnp = np.array(ErZ)

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, projection='3d')

    ax2.title.set_text("Er = " + str(Er))
    ax2.set_xlim(na, 0)
    ax2.set_ylim(nb, 0)
    ax2.set_xlabel('na')
    ax2.set_ylabel('nb')
    ax2.set_zlabel('potential')
    ax2.plot_trisurf(ErXnp, ErYnp, ErZnp)
    plt.show()