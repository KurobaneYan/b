#! /usr/bin/env python3

import argparse
import json
from numpy import array, add, append, zeros
from math import inf


def solve(stoks, consumers, cost):
    stoks, consumers, cost = balancing(stoks, consumers, cost)
    plan, basis = get_start_plan(stoks, consumers)

    counter = 1
    while True:
        counter += 1
        u, v = get_u_and_v(*stoks.shape, *consumers.shape, basis, cost)
        spending_matrix, max_mark, i_0, j_0 = get_spending_matrix(basis, cost, u, v)

        if max_mark <= 0:
            print('Counter: ', counter)
            return plan, add.reduce(plan * cost, axis=(0, 1))

        cycle = find_cycle(i_0, j_0, basis)
        theta, i_to_remove, j_to_remove = get_theta(cycle, plan)

        for (i, j), is_add in cycle:
            plan[i, j] += theta * (1 if is_add else -1)

        basis.discard((i_to_remove, j_to_remove))
        basis.add((i_0, j_0))


def balancing(stoks, consumers, cost):
    in_stoks, needs = add.reduce(stoks), add.reduce(consumers)

    if needs > in_stoks:
        raise ValueError('needs > in_stoks')
    elif needs < in_stoks:
        return (stoks,
                append(consumers, array([in_stoks - needs])),
                append(cost, zeros((len(stoks), 1)), axis=1))
    else:
        return stoks, consumers, cost


def get_start_plan(stoks, consumers):
    plan = zeros((len(stoks), len(consumers)))
    stok_values = array(stoks, copy=True)
    basis = set()
    stok_index = 0
    inserted_values_count = 0

    for j, consumer_value in enumerate(consumers):
        i = stok_index
        while consumer_value > 0:
            basis.add((i, j))
            plan[i, j] = min(consumer_value, stok_values[i])
            consumer_value -= plan[i, j]
            stok_values[i] -= plan[i, j]
            if stok_values[i] == 0 and consumer_value > 0:
                stok_index += 1
            i += 1
            inserted_values_count += 1

    if inserted_values_count != len(stoks) + len(consumers) - 1:
        raise ValueError('n + m - 1')

    return plan, basis


def get_spending_matrix(basis, cost, u, v):
    spending_matrix = zeros(cost.shape)
    max_mark, i_0, j_0 = -inf, -1, -1
    i_size, j_size = spending_matrix.shape

    for i in range(i_size):
        for j in range(j_size):
            if (i, j) in basis:
                spending_matrix[i, j] = cost[i, j]
            else:
                spending_matrix[i, j] = u[i] + v[j] - cost[i, j]
                if max_mark < spending_matrix[i, j]:
                    max_mark, i_0, j_0 = spending_matrix[i, j], i, j

    return spending_matrix, max_mark, i_0, j_0


def get_u_and_v(u_size, v_size, basis, cost):
    u = zeros(u_size)
    v = zeros(v_size)
    calculated_v_indices = set((v_size - 1,))
    calculated_u_indices = set()

    while len(calculated_u_indices) != u_size or len(calculated_v_indices) != v_size:
        for i in range(u_size):
            for j in range(v_size):
                if (i, j) in basis:
                    if i not in calculated_u_indices and j in calculated_v_indices:
                        u[i] = cost[i, j] - v[j]
                        calculated_u_indices.add(i)
                    if i in calculated_u_indices and j not in calculated_v_indices:
                        v[j] = cost[i, j] - u[i]
                        calculated_v_indices.add(j)

    return u, v


def find_cycle(i_0, j_0, basis):

    def _find_cycle(previous_cell, trace, marked_trace, extended_basis, can_vertical):
        trace.add(previous_cell)
        marked_trace.append((previous_cell, not can_vertical))
        dimension = 1 if can_vertical else 0
        result = None

        cells_to_visit = (cell for cell in extended_basis
                          if cell[dimension] == previous_cell[dimension]
                             and cell not in trace)

        for cell in cells_to_visit:
            result = _find_cycle(cell,
                                 set(trace),
                                 list(marked_trace),
                                 extended_basis,
                                 not can_vertical)
            if result:
                return result

        i, j = previous_cell
        if (i == i_0 or j == j_0) and len(trace) >= 4 and len(trace) % 2 == 0:
            return marked_trace


    basis_copy = set(basis)
    basis_copy.add((i_0, j_0))
    return _find_cycle((i_0, j_0), set(), [], basis_copy, False)


def get_theta(cycle, plan):
    theta, i_to_remove, j_to_remove = inf, -1, -1
    for (i, j), _ in (item for item in cycle if not item[1]):
        if plan[i, j] < theta:
            theta, i_to_remove, j_to_remove= plan[i, j], i, j

    return theta, i_to_remove, j_to_remove


def map_input_to_numpy_arrays(input_data):
    return (array(input_data['stoks']),
            array(input_data['consumers']),
            array(input_data['cost']))


def _parse_args():
    parser = argparse.ArgumentParser(description='Matrix transport problem solver.')
    parser.add_argument('input', type=str, help='Name of file with input')

    return parser.parse_args()


def main():
    args = _parse_args();

    with open(args.input) as input_file:
        input_data = json.load(input_file)

    solution = solve(*map_input_to_numpy_arrays(input_data))
    print(solution)


if __name__ == '__main__':
    main()
