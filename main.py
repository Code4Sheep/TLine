from coolFuncs import Node, customReturn, reRoll, initNodeMatrix,contourCalc
import math
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import matplotlib.pyplot as plt



#test for git
wd = float(input("enter wd: "))
bd = float(input("enter bd: "))
aw = float(input("enter aw: "))
na = int(input("enter na: "))
nb = int(input("enter nb: "))
Er = float(input("enter Er: "))
customRelax = str(input("custom relaxation parameter? (True/False): "))
print(customRelax)
if customRelax == "True":
    relaxation = float(input("enter relaxation: "))
else:
    relaxation = 2 * (1 - (math.pi / math.sqrt(2)) * math.sqrt((1 / math.pow(na, 2)) + (1 / math.pow(nb, 2))))
grab = initNodeMatrix(wd,bd,aw,na,nb)
nodes = grab.getMat()

alpha = grab.getAdditional1()
temp = grab.getAdditional2()
stripThreshX = temp.getAdditional1()
interfaceY = temp.getAdditional2()

print("relaxation: " + str(relaxation))
resMax = 100
itER = 0
itAIR = 0
#interface y is zero indexed but strip x isnt

while resMax > pow(10, -5) and itER < 10000:
    resMax = 0
    ret = reRoll(nodes, na, nb, resMax, alpha, relaxation, Er)
    nodesEr = ret.getMat()
    resMax = ret.getAdditional1()
    itER = itER + 1
    if (itER % 100 == 0):
        print(str(itER))
        print("resMax: " + str(resMax))

grab = initNodeMatrix(wd, bd, aw, na, nb)
nodes = grab.getMat()
resMax = 100
print("LOOK")
while resMax > pow(10, -5) and itAIR < 10000:
#while itAIR < 6:
    resMax = 0
    ret = reRoll(nodes, na, nb, resMax, alpha, relaxation, 1)
    nodesAir = ret.getMat()
    resMax = ret.getAdditional1()
    itAIR = itAIR + 1


AirX = []
AirY = []
AirZ = []

for row in range(0, nb):
    temp = ""
    for col in range(0, na):
        temp = temp + " | " + nodesEr[row][col].nodePrint()

    print(temp + " |")
print("ER: " + str(itER))

for row in range(0, nb):
    temp = ""
    for col in range(0, na):
        temp = temp + " | " + nodesAir[row][col].nodePrint()
        AirX.append(col)
        AirY.append(row)
        AirZ.append(nodesAir[row][col].getPot())
    print(temp + " |")

print("Air: " + str(itAIR))


print(str(len(AirX)))
print(str(len(AirY)))
print(str(len(AirZ)))

AirZ1D = np.array(AirZ)

AirZ = [AirZ, AirZ]

print(str(AirX))
print(str(AirY))
print(str(AirZ))

AirXnp = np.array(AirX)
AirYnp = np.array(AirY)
AirZnp = np.array(AirZ)
CEoAir = contourCalc(nodesAir,stripThreshX,interfaceY,na,nb,alpha,1)
CEoEr = contourCalc(nodesEr,stripThreshX,interfaceY,na,nb,alpha,Er)

Eo = float(8.854*pow(10,-12))
CAir = CEoAir*Eo*-1
CEr = CEoEr*Eo*-1

print(str(AirZnp))
print("C/Eo air: " +str(CEoAir))
print("C/Eo Er: " +str(CEoEr))
print(str(CAir))
print(str(CEr))

fig = plt.figure()
ax = fig.add_subplot(111, projection ='3d')
ax.set_xlim(na,0)
ax.set_ylim(nb,0)
ax.set_xlabel('na')
ax.set_ylabel('nb')
ax.set_zlabel('pot')
ax.plot_trisurf(AirXnp,AirYnp,AirZ1D)
#ax.plot_wireframe(AirXnp,AirYnp,AirZnp,rstride=3,cstride=3)
plt.show()