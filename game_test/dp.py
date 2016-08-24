import math

input = [
    [8, 1, 6, 3, 5, 7, 4, 9, 2],
    [2, 7, 6, 9, 5, 1, 4, 3, 8],
    [3, 5, 7, 8, 1, 6, 4, 9, 2],
    [8, 1, 6, 7, 5, 3, 4, 9, 2],
    [7,12,1,14,2,13,8,11,16,3,10,5,9,6,15,4],
    [12,1,14,7,13,8,11,2,3,10,5,16,6,15,4,9],
    [4,14,15,1,9,7,6,12,5,11,10,8,16,2,3,13],
    [11,24,7,20,3,4,12,25,8,16,17,5,13,21,9,10,18,1,14,22,23,6,19,2,15],
]


def horizontal(val, sz, sum):

    for x in range(sz):
        total = 0
        for y in range(sz):
            total += val[x*sz+y]
        if (total != sum):
            return False

    return True

def vertical(val, sz, sum):

    for x in range(sz):
        total = 0
        for y in range(sz):
            total += val[x+y*sz]
        if (total != sum):
            return False

    return True

def diagonal(val, sz, sum):

    total = 0
    for x in range(sz):
        total += val[x*sz+x]
    if (total != sum):
        return False

    total = 0
    for x in range(sz):
        total += val[sz-1+x*sz-x]
    if (total != sum):
        return False

    return True

def verify(val):

    sz = int(math.sqrt(len(val)))
    sum = sz*(sz*sz+1)/2

    if not horizontal(val, sz, sum) or not vertical(val, sz, sum) or not diagonal(val, sz, sum):
        return 'false'

    return 'true'

for i in input:
    print (i, verify(i))