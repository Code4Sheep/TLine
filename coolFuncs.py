import math

class Node:
    #   a representation of Nodes
    #   holds some additonal usefull info
    def __init__(self,pot,res,interface,strip):
        self.pot = float(pot)
        self.res = float(res)
        self.interface = bool(interface)
        self.strip = bool(strip)

    def getPot(self):
        return self.pot
    def getRes(self):
        return self.res
    def setInterface(self,B):
        self.interface = B
    def isInterface(self):
        return self.interface
    def isStrip(self):
        return self.strip
    def nodePrint(self):
        return "p: " + str.format('{0:1.4f}', self.pot) + ", r: " + str.format('{0:1.4f}', math.fabs(self.res)) + ", i: " + str.format('{0:1.1f}',int(self.interface))


class customReturn:
    #custom return function returns a matrix and additonal value

    def __init__(self, mat, additional1, additional2):
        self.mat = mat
        self.additional1 = additional1
        self.additional2 = additional2
    def getMat(self):
        return self.mat
    def getAdditional1(self):
        return self.additional1
    def getAdditional2(self):
        return self.additional2

def initNodeMatrix (wd,bd,aw,na,nb):
    #   makes the initial matrix, how nice
    #   assume a = 1 and derive the rest of the values
    a = 1
    w = float(a / aw)
    d = float(w / wd)
    b = float(d * bd)

    #derive h and k values, usefull to check if a node is on the strip or not
    k = float(b/(nb-1))
    h = float(a/(na-1))

    #   calc where strip is relative to top left as well as calc how long the strip is in terms of nodes
    ind = float(b - d)
    interfaceY = math.floor(ind/k)
    stripThreshX = math.floor(w/h)
    #   generate matrix skeleton
    nodes = [[Node(0, 0, False, False) for j in range(na)] for i in range(nb)]

    #   apply values to special cases, strip and
    for x in range(0, na):
        if x <= stripThreshX:
            nodes[interfaceY][x] = Node(1, 0, True, True)
        else:
            nodes[interfaceY][x] = Node(0, 0, True, False)

    shell = customReturn([],stripThreshX,interfaceY)
    ret = customReturn(nodes, float(h/k),shell)
    return ret

def calcNode(mat, row, col, alpha, relaxation, Er):
    #   Calculates a new node from the old node
    #   handles both potential and residual

    #   if the node is the strip then just pass over it
    if mat[row][col].isStrip():
        return mat[row][col]

    top = mat[row - 1][col]
    bottom = mat[row + 1][col]
    right = mat[row][col + 1]
    left = Node(0, 0, False, False)
    if col == 0:
        left = right
    else:
        left = mat[row][col - 1]

    #check interface condition
    if mat[row][col].isInterface():
        E = Er
    else:
        E = 1

    a2 = float(alpha*alpha)
    A = 1 / (2 * (1 + a2))
    B = left.getPot() + right.getPot()
    C = (2*a2)/(1+E)
    D = top.getPot() + E*bottom.getPot()

    #implement sor algo
    Res = A * (B + C*D) - mat[row][col].getPot()
    newPot = mat[row][col].getPot() + relaxation*Res
    ret = Node(newPot, Res, mat[row][col].isInterface(), mat[row][col].isStrip())
    return ret

def reRoll(mat,na,nb,resMax, alpha , relaxation, Er):
    #   snake iteration starting from bottom left ignoring top, bottom and right sides
    #   as these sides will always be zero
    check = (nb) % 2
    for row in range(nb - 2, 0, -1):
        if row % 2 == check:
            for col in range(0, na-1):
                mat[row][col] = calcNode(mat, row, col, alpha, relaxation, Er)
                if mat[row][col].getRes() > resMax:
                    resMax = mat[row][col].getRes()
        else:
            for col in range(na - 2, -1, -1):
                mat[row][col] = calcNode(mat, row, col, alpha, relaxation, Er)
                if mat[row][col].getRes() > resMax:
                    resMax = mat[row][col].getRes()

    ret = customReturn(mat,resMax,0)
    return ret

def contourCalc(mat,stripthreshX,interfaceY,na,nb,alpha,Er):
    sumtopbot = 0;
    sumtop = 0;
    sumbot = 0;
    sumRT = 0
    sumRB = 0
    offsetTop = 1
    offsetBot = 1
    offsetRight = 1


    topoffset = interfaceY - offsetTop
    botoffset = interfaceY + offsetBot
    rightoffset = stripthreshX + offsetRight


    #sum bottom and top leg
    for col in range(0, rightoffset+1):
        tempbot = Er*(mat[botoffset+1][col].getPot() -
                      mat[botoffset-1][col].getPot())
        temptop = (mat[topoffset-1][col].getPot() -
                   mat[topoffset+1][col].getPot())

        if (col == 0 or col == rightoffset):
            sumtop = sumtop + (1/2)*temptop
            sumbot = sumbot + (1 / 2) * tempbot
            sumtopbot = sumtopbot + (1/2)*(temptop + tempbot)
        else:
            sumtop = sumtop + temptop
            sumbot = sumbot + tempbot
            sumtopbot = sumtopbot + (temptop + tempbot)

    for row in range(topoffset,interfaceY+1):
        tempRT = (mat[row][rightoffset+1].getPot() -
                      mat[row][rightoffset-1].getPot())
        if (row == topoffset or row == interfaceY):
            sumRT = sumRT + (1/2)*tempRT
        else:
            sumRT = sumRT + tempRT

    for row in range(interfaceY,botoffset+1):
        tempRB =Er*(mat[row][rightoffset+1].getPot() -
                      mat[row][rightoffset-1].getPot())
        if (row == interfaceY or row == botoffset):
            sumRB = sumRB + (1/2)*tempRB
        else:
            sumRB = sumRB + tempRB

    negCEo = alpha*sumtopbot + (1/alpha)*(sumRT+sumRB)
    return negCEo



























