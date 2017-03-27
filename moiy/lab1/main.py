#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

def setDate(c, b, a, x_first, j_base):
    
    c[0] = -6
    c[1] = -9
    c[2] = -5
    c[3] = 2
    c[4] = -6
    c[5] = 0
    c[6] = 1
    c[7] = 3

    b[0] = 6
    b[1] = 1.5
    b[2] = 10

    a[0, 0] = 0
    a[0, 1] = -1
    a[0, 2] = 1
    a[0, 3] = 7.5
    a[0, 4] = 0
    a[0, 5] = 0
    a[0, 6] = 0
    a[0, 7] = 2
    
    a[1, 0] = 0
    a[1, 1] = 2
    a[1, 2] = 1
    a[1, 3] = 0
    a[1, 4] = -1
    a[1, 5] = 3
    a[1, 6] = -1.5
    a[1, 7] = 0
    
    a[2, 0] = 1
    a[2, 1] = -1
    a[2, 2] = 1
    a[2, 3] = -1
    a[2, 4] = 0
    a[2, 5] = 3
    a[2, 6] = 1
    a[2, 7] = 1
    
    x_first[0] = 4
    x_first[1] = 0
    x_first[2] = 6
    x_first[3] = 0
    x_first[4] = 4.5
    x_first[5] = 0
    x_first[6] = 0
    x_first[7] = 0

    j_base[0] = 1 - 1
    j_base[1] = 3 - 1
    j_base[2] = 5 - 1
    
def createMatrix(a, j_base, c, m, n):
    a_base = np.zeros((m, m), dtype=float)
    c_base = np.zeros(m, dtype=float)
    for item_i in range(m):
        count = 0
        for item_j in range(n):
            if item_j == j_base[count]:
                a_base[item_i, count] = a[item_i, item_j]
                count += 1
                if count == m:
                    break

    if np.linalg.det(a_base) != 0:
        a_base_obrat = np.linalg.inv(a_base)
    else:
        print("Матрица A является вырожденной, det(A)=0")
        return

    count = 0
    for item_i in range(n):
        if item_i == j_base[count]:
            c_base[count] = c[item_i]
            count += 1
            if count == m:
                break
    return a_base, a_base_obrat, c_base

def solve():
    while (True):
        a_base, a_base_obrat, c_base = createMatrix(a, j_base, c, m, n)
        u = np.dot(c_base, a_base_obrat)
        delta = np.dot(u, a) - c
        flag = False
        count = 0
        for item_i in range(n):
            if (delta[item_i] >= -epsilon) == False:
                if item_i != j_base[count]:
                    flag = True
                else:
                    count += 1
                    if count == m:
                        count = m -1 
        if flag == False:
            return "Оптимальный план задали x0 = " + str(x_first) + "\ncx0 = " + str(np.dot(c.transpose(), x_first))
        j0 = -1
        count = 0
        for item_i in range(n):
            if (delta[item_i] >= -epsilon) == False:
                if item_i != j_base[count]:
                    j0 = item_i
                    break
                else:
                    count += 1
                    if count == m:
                        count = m -1 
        a_j0 = np.zeros((m, 1), dtype=float)
        for item_i in range(m):
            a_j0[item_i, 0] = a[item_i, j0]
        z = np.dot(a_base_obrat, a_j0)
        flag = False
        for item_i in range(m):
            if (z[item_i] <= epsilon) == False:
                flag = True
        if flag == False:
            return "данная задача не имеет решения, т.к. ее целевая функция не ограничена на множестве планов."
        q0 = 10000000000000
        s = 10000000000000
        for item_i in range(m):
            if z[item_i] > 0:
                last_q0 = x_first[j_base[item_i]] / z[item_i]
                if q0 > last_q0:
                    q0 = last_q0
                    s = item_i
        count = 0
        for item_i in range(n):
            if item_i != j_base[count]:
                x_first[item_i] = 0
            else:
                count += 1
                if count == m:
                    count = m -1        
        x_first[j0] = q0
        count = 0
        for item_i in range(n):
            if item_i == j_base[count]:
                x_first[item_i] = x_first[item_i] - q0 * z[count]  
                count += 1
                if count == m:
                    break
            
        j_base[s] = j0
        j_base.sort()
    return "Error"


c = np.zeros(8, dtype=float)
b = np.zeros(3, dtype=float)
a = np.zeros((3, 8), dtype=float)
m = 3
n = 8
epsilon = 0.001

x_first = np.zeros(8, dtype=float)
j_base = np.zeros(3, dtype=int)
setDate(c, b, a, x_first, j_base)

print(solve())

