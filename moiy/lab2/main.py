import numpy as np
def col(A, n):
    return [A[i][n] for i in range(0,len(A))]
def colSumm(A):
    newA = []
    for i in range(0,len(A)):
           newA.append(sum(col(A,i)))
    return newA
def rowSumm(A):
    newA = []
    for i in range(0,len(A)):
           newA.append(sum(A[i]))
    return newA
def DupleSimplexMethod(A, b, c, Y, Jb):
    iterations = 0
    stop_solved = True
    stop_nosolution = True
    stop_overflow = False
    n = len(A[0])
    m = len(A)
    X_prev = None
    Ab = []
    for j in Jb:
        Ab.append(col(A,j))
    Ab = np.transpose(Ab)
    B = np.linalg.inv(Ab)
    PseudoX = None
# 5 -9
# 1 -9
    while(True):
        np.seterr(all='raise')
        stop_solved = True
        stop_nosolution = True
        #stop_nosolution = False
        PseudoX = np.dot(B,b);
        s = -1
        for i in xrange(m) :
            if PseudoX[i]<=0:
                stop_solved = False
                s = i
        if stop_solved==True:
            stop_nosolution = False
            break
        es = np.eye(m);
        es = es[s]
        dy = np.dot(es , B)
        Jn = []
        mu = []
        for j in range(n):
            if j not in Jb:
                Jn.append(j)
                mu.append(np.dot(dy , col(A,j)))
            else:
                mu.append(None)
        for Mu in mu:
            if (Mu!=None) and Mu < 0:
                stop_nosolution = False
                break
        if stop_nosolution:
            break
        sigma0 = float('infinity')
        expr_res = []
        j0 = -1
        for j in range(0,n):
            if (j in Jn) and mu[j]<0:
                expr_res.append((c[j] - np.dot(col(A,j), Y)) / mu[j])
                if (expr_res[j] < sigma0):
                    sigma0 = expr_res[j]
                    j0 = j
            else:
                expr_res.append(None)
        # new plan
        new_y = Y + sigma0*dy
        Jb[s] = j0
        Y = new_y
        
        Ab = []
        for j in Jb:
            Ab.append(col(A,j))
        Ab = np.transpose(Ab)
        B = np.linalg.inv(Ab)
        iterations+=1
        print("iteration " + str(iterations) + "\n"),
    if stop_overflow:
        print("\n(OF) Optimal plan is:\nY= " + str(Y))
        print("Number of iterations: " + str(iterations))
    elif stop_solved:
        print("\nSolved! Optimal plan is:\nX= " + str(PseudoX))
        print("\nOptimal dual plan is:\nY= " + str(Y))
        print("Number of iterations: " + str(iterations))
    if stop_nosolution:
        print("\nThere is no solution. The target function is not limited from above")

A = [
    [-2,-1,1,-7,0,0,0,2],
    [4,2,1,0,1,5,-1,-5],
    [1,1,0,-1,0,3,-1,1]
]
b = [-2,4,3]
c = [2,2,1,-10,1,4,-2,-3]
Y0 = [1,1,1]
Jb = [1,4,6]
DupleSimplexMethod(A,b,c,Y0,Jb)

print("----------------------")

A = [
    [-2, -1, 1, -7, 0, 0, 0, 2],
    [4, 2, 1, 0, 1, 5, -1, -5],
    [1, 1, 0, -1, 0, 3, -1, 1]
]
b = [-2, -4, -2]
c = [5, 2, 3, -16, 1, 3, -3, -12]
Jb = [1, 2, 3]
Y0 = [1, 2, -1]
DupleSimplexMethod(A, b, c, Y0, Jb)
