from collections import defaultdict

from instructies import *

test="""push 999
push x
push -3
add
jmpos 2
ret
ret
push 123
ret"""

def evalBlockje(aInst, x, y, z):
    # run stack machine program in aInst
    pc = 0
    stack = []
    while True:
        inst = aInst[pc]
        ops = inst.split(' ')
        op = ops[0]
        if op == "push": # I'm running Python 3.9, so no match/case :-(
            if (ops[1].lower() == 'x'):
                stack.append(x)
            elif (ops[1].lower() == 'y'):
                stack.append(y)
            elif (ops[1].lower() == 'z'):
                stack.append(z)
            else:
                stack.append(int(ops[1]))
        elif op == "add":
            assert(len(stack) >= 2)
            stack.append(stack.pop() + stack.pop())
        elif op == "jmpos":
            if stack.pop() >= 0:
                pc += int(ops[1])
        elif op == "ret":
            return stack.pop()
        else:
            assert(False)
        pc += 1

# print(evalBlockje(test.split('\n'), 7, 0, 0))

def sneeuwtotaal(inst):
    # first part

    aInst = inst.split('\n')
    som = 0
    for x in range(0,30):
        for y in range(0,30):
            for z in range(0,30):
                som += evalBlockje(aInst, x, y, z)
    return som
        
# print(f"sneeuwtotaal = {sneeuwtotaal(test)}")
# print(f"sneeuwtotaal = {sneeuwtotaal(instructies)}")


def root(blockjes, xyz):
    # follow the linked list of connected blockjes and return root (points at self)

    assert(xyz in blockjes) # should only call on cloudy blocks
    xyzNext = blockjes[xyz]
    while xyzNext != xyz:
        xyz = xyzNext
        xyzNext = blockjes[xyz]

    # better performance by "collapsing" lists to root, not needed for this small case

    return xyz

def connectWolken(blockjes, xyz0, xyz1):
    # connect two groups by pointing one's root at the other's root

    xyzRoot0 = root(blockjes, xyz0)
    xyzRoot1 = root(blockjes, xyz1)
    blockjes[xyzRoot0] = xyzRoot1

def wolkentotaal(inst):
    aInst = inst.split('\n')
    
    blockjes = {} # 3d array in dict -- if there were a LOT more blockjes, I'd maybe use numpy

    for x in range(0,30):
        for y in range(0,30):
            for z in range(0,30):
                if evalBlockje(aInst, x, y, z) <= 0:
                    continue

                # add self as cloud
                blockjes[(x,y,z)] = (x,y,z)

                # connect to adjacent clouds
                if x > 0 and (x-1,y,z) in blockjes:
                    connectWolken(blockjes, (x,y,z), (x-1,y,z))
                if y > 0 and (x,y-1,z) in blockjes:
                    connectWolken(blockjes, (x,y,z), (x,y-1,z))
                if z > 0 and (x,y,z-1) in blockjes:
                    connectWolken(blockjes, (x,y,z), (x,y,z-1))

    # build set of unique cloud roots

    wolken = set()
    for x in range(0,30):
        for y in range(0,30):
            for z in range(0,30):
                if (x,y,z) in blockjes:
                    wolken.add(root(blockjes, (x,y,z)))

    return len(wolken)


print(f"wolkentotaal = {wolkentotaal(instructies)}")
