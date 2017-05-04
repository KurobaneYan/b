# -*- coding: utf-8 -*-

from goto import goto
import numpy as np

def setDate(a, b_smal, b_big, d, x_first, j_op, j_star):
    a[0, 0] = 1
    a[0, 1] = 2
    a[0, 2] = 0
    a[0, 3] = 1
    a[0, 4] = 0
    a[0, 5] = 4
    a[0, 6] = -1
    a[0, 7] = -3

    a[1, 0] = 1
    a[1, 1] = 3
    a[1, 2] = 0
    a[1, 3] = 0
    a[1, 4] = 1
    a[1, 5] = -1
    a[1, 6] = -1
    a[1, 7] = 2

    a[2, 0] = 1
    a[2, 1] = 4
    a[2, 2] = 1
    a[2, 3] = 0
    a[2, 4] = 0
    a[2, 5] = 2
    a[2, 6] = -2
    a[2, 7] = 0
    
    b_smal[0] = 4
    b_smal[1] = 5
    b_smal[2] = 6

    b_big[0, 0] = 1
    b_big[0, 1] = 1
    b_big[0, 2] = -1
    b_big[0, 3] = 0
    b_big[0, 4] = 3
    b_big[0, 5] = 4
    b_big[0, 6] = -2
    b_big[0, 7] = 1

    b_big[1, 0] = 2
    b_big[1, 1] = 6
    b_big[1, 2] = 0
    b_big[1, 3] = 0
    b_big[1, 4] = 1
    b_big[1, 5] = -5
    b_big[1, 6] = 0
    b_big[1, 7] = -1

    b_big[2, 0] = -1
    b_big[2, 1] = 2
    b_big[2, 2] = 0
    b_big[2, 3] = 0
    b_big[2, 4] = -1
    b_big[2, 5] = 1
    b_big[2, 6] = 1
    b_big[2, 7] = 1

    d[0] = 7
    d[1] = 3
    d[2] = 3

    x_first[0] = 0
    x_first[1] = 0
    x_first[2] = 6
    x_first[3] = 4
    x_first[4] = 5
    x_first[5] = 0
    x_first[6] = 0
    x_first[7] = 0

    j_op[0] = 3 - 1
    j_op[1] = 4 - 1
    j_op[2] = 5 - 1

    j_star[0] = 3 - 1
    j_star[1] = 4 - 1
    j_star[2] = 5 - 1
    
def createMatrix(b_big, d):
    d_big = np.zeros((n, n), dtype=float)
    c = np.zeros(n, dtype=float)
    d_big = np.dot(b_big.transpose(), b_big)
    c = np.dot(-d, b_big)
    return d_big, c

@goto
def cycles():
    global x_first
    global j_star
    global j_op
    m_new = m

    """PART 1"""
    label .bbb
    d_big, c = createMatrix(b_big, d)
    c_x_first = np.dot(d_big, x_first) + c
    a_op = np.zeros((m, m), dtype=float)
    c_x_first_op = np.zeros(m, dtype=float)
    count = 0
    for item_i in xrange(n):
        if item_i == j_op[count]:
            c_x_first_op[count] = c_x_first[item_i]
            count += 1
            if count == m:
                break
    for item_i in xrange(m):
        count = 0
        for item_j in xrange(n):
            if item_j == j_op[count]:
                a_op[item_i, count] = a[item_i, item_j]
                count += 1
                if count == m:
                    break
    vector_potenc = np.dot(-c_x_first_op, np.linalg.inv(a_op))
    vector_ocenc = np.dot(vector_potenc, a) + c_x_first
    """PART 2"""
    count = 0
    j0 = 99999
    vector_ocenc_min = 99999
    for item_j in xrange(n):
        if item_j != j_star[count]:
            if vector_ocenc[item_j] < -epsilon:
                if vector_ocenc_min > vector_ocenc[item_j]:
                    vector_ocenc_min = vector_ocenc[item_j]
                    j0 = item_j
        else:
            count += 1
            if count == m_new:
                count -= 1
    if j0 == 99999:
        c_with_sh = np.dot(-d, b_big)
        res = np.dot(c_with_sh, x_first) + 0.5 * np.dot(np.dot(x_first, d_big), x_first)
        return "Optimal plan х0 = " + str(x_first) + "\nc'x0 + 0.5x0'Dx0=" + str(res) 
    """PART 3"""
    label .bbb_three
    l = np.zeros(n, dtype=float)
    l[j0] = 1
    h_big = np.zeros((m_new + m, m_new + m), dtype=float)
    count_i = 0
    for item_i in xrange(n):
        if item_i == j_star[count_i]:
            count_j = 0
            for item_j in xrange(n):
                if item_j == j_star[count_j]:
                    h_big[count_i, count_j] = d_big[item_i, item_j]
                    count_j += 1
                    if count_j == m_new:
                        break
            count_i += 1
            if count_i == m_new:
                break
    h_dop = np.zeros((m, m_new), dtype=float)
    for item_i in xrange(m):
        count_j = 0
        for item_j in xrange(n):
            if item_j == j_star[count_j]:
                h_dop[item_i, count_j] = a[item_i, item_j]
                count_j += 1
                if count_j == m_new:
                    break
    h_dop = h_dop.transpose()
    for item_i in xrange(m_new):
        for item_j in xrange(m):
            h_big[item_i, item_j + m_new] = h_dop[item_i, item_j]
    for item_i in xrange(m):
        count_j = 0
        for item_j in xrange(n):
            if item_j == j_star[count_j]:
                h_big[item_i + m_new, count_j] = a[item_i, item_j]
                count_j += 1
                if count_j == m_new:
                    break
    bb = np.zeros(m_new + m, dtype=float)
    count = 0
    for item_i in xrange(n):
        if item_i == j_star[count]:
            bb[count] = d_big[item_i, j0]
            count += 1
            if count == m_new:
                break
    count = 0
    for item_i in xrange(n):
        bb[count + m] = a[item_i, j0]
        count += 1
        if count == m:
            break
    l_dop = np.dot(-np.linalg.inv(h_big), bb.transpose())
    count = 0
    for item_i in xrange(n):
        if item_i == j_star[count]:
            l[item_i] = l_dop[count]
            count += 1
            if count == m_new:
                break
    """PART 4"""
    teta = np.zeros(n, dtype=float)
    for item_i in xrange(n):
        teta[item_i] = 99999
    count = 0
    for item_i in xrange(n):
        if item_i == j_star[count]:
            if l[item_i] >= -epsilon:
                teta[item_i] = 99999
            else:
                teta[item_i] = -x_first[item_i] / l[item_i]
            count += 1
            if count == m_new:
                break
    bi = np.dot(np.dot(l.transpose(), d_big), l)
    if bi == 0:
        teta[j0] = 99999
    elif bi > 0:
        teta[j0] = abs(vector_ocenc[j0]) / bi
    j_small_star = 99999
    teta_min = 99999
    for item_i in xrange(n):
        if teta[item_i] < teta_min:
            teta_min = teta[item_i]
            j_small_star = item_i
    """PART 5"""
    x_first = x_first + np.dot(teta_min, l)
    """PART 6"""
    """1"""
    if j_small_star == j0:
        j_star_new_new = np.zeros(m_new + 1, dtype=float)
        for item_i in xrange(m_new):
            j_star_new_new[item_i] = j_star[item_i]
        j_star_new_new[m_new] = j0;
        j_star_new_new.sort()
        m_new = m_new + 1
        j_star = j_star_new_new
        goto .bbb
    """2"""
    if j_small_star in j_star:
        if j_small_star in j_op:
            print
        else:
            j_star_new_new = np.zeros(m_new - 1, dtype=float)
            coooount = 0
            for item_i in xrange(m_new):
                if j_star[item_i] != j_small_star:
                    j_star_new_new[coooount] = j_star[item_i]
                    coooount += 1
            m_new = m_new - 1
            print j_star
            j_star = j_star_new_new
            print j_star
            print vector_ocenc[j0]
            vector_ocenc[j0] += teta_min * bi
            print vector_ocenc[j0]
            goto .bbb_three
    """3"""
    s_dop = 0
    if j_small_star in j_op:
        for item_i in xrange(m):
            if j_small_star == j_op[item_i]:
                s_dop = item_i
        for item_i in xrange(n):
            if item_i in j_star:
                if item_i in j_op:
                    print
                else:
                    e_dop = np.zeros(m, dtype=float)
                    e_dop[s_dop] = 1
                    a_j_plus = np.zeros(m, dtype=float)
                    for item_j in xrange(m):
                        a_j_plus[item_j] = a[item_i, item_j]
                    if np.dot(np.dot(e_dop.transpose(), np.linalg.inv(a_op)), a_j_plus) != 0:
                        j_op_new_new = np.zeros(m, dtype=float)
                        coooount = 0
                        for item_i in xrange(m):
                            if j_op[item_i] != j_small_star:
                                j_op_new_new[coooount] = j_op[item_i]
                                coooount += 1
                        j_op_new_new[m] = item_j
                        j_op = j_op_new_new
                        j_op.sort()

                        j_star_new_new = np.zeros(m_new - 1, dtype=float)
                        coooount = 0
                        for item_i in xrange(m_new):
                            if j_star[item_i] != j_small_star:
                                j_star_new_new[coooount] = j_star[item_i]
                                coooount += 1
                        m_new = m_new - 1
                        j_star = j_star_new_new
                        vector_ocenc[j0] += teta_min * bi
                        goto .bbb_three
        """4"""
        j_op_new_new = np.zeros(m, dtype=float)
        coooount = 0
        for item_i in xrange(m):
            if j_op[item_i] != j_small_star:
                j_op_new_new[coooount] = j_op[item_i]
                coooount += 1
        j_op_new_new[m] = j0
        j_op = j_op_new_new
        j_op.sort()

        j_star_new_new = np.zeros(m_new, dtype=float)
        coooount = 0
        for item_i in xrange(m_new):
            if j_star[item_i] != j_small_star:
                j_star_new_new[coooount] = j_star[item_i]
                coooount += 1
        j_star_new_new[m_new] = j0
        j_star = j_star_new_new
        j_star.sort()
        goto .bbb
        
    return "Error"

m = 3
n = 8
a = np.zeros((m, n), dtype=float)
b_smal = np.zeros(m, dtype=float)
b_big = np.zeros((m, n), dtype=float)
d = np.zeros(m, dtype=float)
x_first = np.zeros(n, dtype=float)
j_op = np.zeros(m, dtype=float)
j_star = np.zeros(m, dtype=float)
epsilon = 0.001
setDate(a, b_smal, b_big, d, x_first, j_op, j_star)
print(cycles())

