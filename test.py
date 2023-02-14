melds = []
dice = [None]*6
def fooyoh(tableDice, amount):
    global melds
    sorted_nums = tableDice.copy()
    sorted_nums.sort()
    phdTable = sorted_nums.copy()
    phdScore = 0
    melds = []  # type, dice id, amount, pts, emoji
    for i in range(6):
        if tableDice.count(i) == 6:
            return (True, 3000)
    if sorted_nums == list(range(6)):
        return (True, 2500)
    for i in range(6):
        if tableDice.count(i) >= 5:
            melds += [(i, 5, 2000, dice[i])]
            if i in phdTable:
                while i in phdTable:
                    phdTable.remove(i)
                phdScore += 2000
    if amount == 6 and tableDice[0] == tableDice[1] and tableDice[2] == tableDice[3] and tableDice[
        4] == tableDice[5]:
        return (True, 1500)
    if tableDice.count(0) >= 3:
        melds += [(0, 3, 1000, dice[0])]
        if 0 in phdTable:
            while 0 in phdTable:
                phdTable.remove(0)
            phdScore += 1100 if tableDice.count(0) == 4 else 1000
    for i in range(6):
        if tableDice.count(i) >= 4:
            melds += [(i, 4, 1000, dice[i])]
            if i in phdTable:
                while i in phdTable:
                    phdTable.remove(i)
                phdScore += 1000
    for i in range(1, 6):
        if tableDice.count(i) >= 3:
            melds += [(i, 3, i * 100 + 100, dice[i])]
            if i in phdTable:
                while i in phdTable:
                    phdTable.remove(i)
                phdScore += i * 100 + 100
    if 0 in tableDice:
        melds += [(0, 1, 100, dice[0])]
        phdScore += phdTable.count(0) * 100
        while 0 in phdTable:
            phdTable.remove(0)
    if 4 in tableDice:
        melds += [(4, 1, 50, dice[0])]
        phdScore += phdTable.count(4) * 50
        while 4 in phdTable:
            phdTable.remove(4)
    
    if phdTable == []:
        melds = []
        return (True, phdScore)
    else:
        return (False, melds)

print(fooyoh([0, 4], 2))