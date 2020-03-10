nodes = [[0 for j in range(5)] for i in range(6)]
d = 3
cthresh = 3
rows = 6
cols = 5
for r in range(0, rows):
    temp = ""
    for c in range(0, cols):
        if not(r == d and c <= cthresh):
            nodes[r][c] = 9

        temp = temp + " | " +  str(nodes[r][c])
    print(temp + " |")

for x in range (0,10):
    print(str(x))
print