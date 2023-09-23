#!/usr/bin/env python3

import numpy as np

# --------------------------------------------------
# Config
MOVE_COUNT = 50
INPUT_MOVE_COUNT = True    # Overwrite MOVE_COUNT from stdin?
DEBUG_MATRIX = False

# --------------------------------------------------
# Helpers
dimensionCount = 24
rollChance = [x / 36 for x in [1,2,3,4,5,6,5,4,3,2,1]]
zeroChance = [0] * len(rollChance)

def unitVector(n):
    v = np.zeros(dimensionCount)
    v[n] = 1
    return v
def generateStartState():
    return unitVector(0)
def tripleChance(state):
    return state[-1]
def generateTransitionMatrix():
    """ Generate MC transition matrix for rolling any number 3 times in a row

    [ 0- 1): Start state (no previous symbol)
    [ 1-12): Previous symbol was a 2/.../12. First of its kind.
    [12-23): Previous symbol was a 2/.../12. Second of its kind.
    [23-24): The previous symbol already contained a group of three.
    """
    assert(dimensionCount == 24)
    M = np.zeros([dimensionCount, dimensionCount])

    # The start state always transitions to 1-in-a-row
    startMap = M[:,0]
    np.copyto(startMap, np.array([0] + rollChance + zeroChance + [0]))

    # The 1-chain transitions to the 2-chain if the same number rolls again
    chain1 = M[:, 1:12]
    # TODO This could be formulated in matrix notation as well
    for roll in range(11): # The rolled number, representing 2-12
        # Transit to 2-chain when rolling roll. Transit to 1-chain else.
        newChainChance            = rollChance.copy()
        newChainChance     [roll] = zeroChance[roll] 
        continueChainChance       = zeroChance.copy()
        continueChainChance[roll] = rollChance[roll]
        subchain = chain1[:, roll] # The transitions after chaining a single roll
        np.copyto(subchain, np.array([0] + newChainChance + continueChainChance + [0]))
#        print("Chain1, roll={} (number={})".format(roll, roll+2))
#        print("subchain:", subchain)

    # The 2-chain transtition into the success case if same number rolls again
    chain2 = M[:, 12:23]
    for roll in range(11): 
        # Transition into success case with probability rollChance[roll]
        newChainChance            = rollChance.copy()
        newChainChance     [roll] = zeroChance[roll] 
        subchain = chain2[:, roll] 
        np.copyto(subchain, np.array([0] + newChainChance + zeroChance + [rollChance[roll]]))
#        print("Chain2, roll={} (number={})".format(roll, roll+2))
#        print("subchain:", subchain)

    # The success state is retained
    successMap = M[:,23]
    np.copyto(successMap, np.array([0] + zeroChance + zeroChance + [1]))

    if DEBUG_MATRIX:
        print("StartMap", startMap.shape, startMap)
        print("chain1:", chain1.shape, chain1)
        print("chain2:", chain2.shape, chain2)
        print("successMap", successMap.shape, successMap)
        print("M", M.shape, M)
        for row in range(M.shape[1]):
            sum = np.sum(M[:,row])
            print("Row {}: sum={}".format(row, sum))

    return M

# --------------------------------------------------
# main
if __name__ == "__main__":

    if INPUT_MOVE_COUNT:
        moveCount = int(input("Input move count: "))
    else:
        moveCount = MOVE_COUNT

    state = generateStartState()
    A = generateTransitionMatrix()
    print("Starting MC with\nstart=\n{},\nA=\n{}".format(state, A))
    for i in range(1, moveCount+1):
        state = A.dot(state)
        print(i, "->", tripleChance(state))

    quit()
