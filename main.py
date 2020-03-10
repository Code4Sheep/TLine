from coolFuncs import Node, customReturn, reRoll, initNodeMatrix,contourCalc
import math

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

while resMax > pow(10, -5) and itER < 1000:
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
while resMax > pow(10, -5) and itAIR < 1000:
#while itAIR < 6:
    resMax = 0
    ret = reRoll(nodes, na, nb, resMax, alpha, relaxation, 1)
    nodesAir = ret.getMat()
    resMax = ret.getAdditional1()
    itAIR = itAIR + 1


for x in range(0, nb):
    temp = ""
    for y in range(0, na):
        temp = temp + " | " + nodesEr[x][y].nodePrint()
    print(temp + " |")
print("ER: " + str(itER))

for x in range(0, nb):
    temp = ""
    for y in range(0, na):
        temp = temp + " | " + nodesAir[x][y].nodePrint()
    print(temp + " |")

print("Air: " + str(itAIR))


CEoAir = contourCalc(nodesAir,stripThreshX,interfaceY,na,nb,alpha,1)
CEoEr = contourCalc(nodesEr,stripThreshX,interfaceY,na,nb,alpha,Er)

Eo = float(8.854*pow(10,-12))
CAir = CEoAir*Eo*-1
CEr = CEoEr*Eo*-1

print("C/Eo air: " +str(CEoAir))
print("C/Eo Er: " +str(CEoEr))
print(str(CAir))
print(str(CEr))