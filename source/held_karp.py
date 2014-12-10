#!/usr/bin/env python2.7
"""Implements the held-karp algorithm for calculating min-cost tours
for TSP."""

import numpy as np
import scipy.sparse as sparse
import sys
import time

import bits

# LESSONS LEARNED
# - NEVER assign default values for a key. If you can't find a key,
#   return a default value at invocation instead.
# - Sometimes it's a good idea to use two small dictionaries instead of
#   accumulating 1 massive one

# TODO
# - Dicts: how about deleting entries from the previous array when all
#   references to it have been made? This should free up memory.
# - Rewrite with numpy arrays
# - PyLint: still a lot of "Invalid argument name" convention mismatches.

def distance_matrix(cities):
    """ [points] -> [[int]]

    Accepts a list of cities of length n and returns the complete graph
    of pair-wise distances as an n x n matrix.

    Keyword arguments:
    cities -- list of points in a 2-D plane
    count  -- number of cities
    """

    return [[city1.distance(city2) for city2 in cities]
                                   for city1 in cities]

def choose(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke
    (contrib).
    """
    # http://stackoverflow.com/a/3025547/313967
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

def final_hop(count, final_set, last_iteration, distances):
    """
    Take the min-cost paths from 0 to j and add the final hop. Return
    the min-cost tour.
    """
    res = list()

    for j in range(1, count):
        cj0 = distances[j][0] # cost of final hop of tour
        # min-cost from 0 to j, visiting everybody once +
        index_j = bits.generate_index(final_set, count, j)
        res.append(last_iteration[index_j] + cj0)
    return min(res)

def final_hop2(count, final_set, last_iteration, distances):
    """
    Take the min-cost paths from 0 to j and add the final hop. Return
    the min-cost tour.
    """
    res = list()

    for j in range(1, count):
        res.append(last_iteration[final_set,j] + distances[j][0])
    return min(res)

def diagnostics_next_size(m, n):
    """ Diagnostics """
    print "========================================"
    print "Working through subsets of size     m = {m}".format(m=m)
    print "Number of subsets with that size:       {n}".format(n=n)
    print

def diagnostics_set(i, t, sA, sB):
    """ Diagnostics """
    print "Number of subsets processed so far:     {i}".format(i=i)
    print("Took: {t1} minutes and {t2} seconds"
          "".format(t1=int(t/60), t2=t%60))
    print "Size of current dictionary (in bytes):  {sA}".format(sA=sA)
    print "Size of previous dictionary (in bytes): {sB}".format(sB=sB)
    print "Total size (in bytes):                  {s}".format(s=sA+sB)
    print

# TODO Fill up the docstring with some examples
# TODO PyLint: Too many local variables (16/15) (too-many-locals)
def held_karp_dicts(cities, count, verbose=True):
    """ ([point],int,bool) -> float

    Calculate the min-cost TSP tour for a list of cities.

    Keyword arguments:
    cities  -- list of points in a 2-D plane
    count   -- number of cities
    verbose -- optional parameter for extra diagnostics
    """

    distances = distance_matrix(cities)

    # Only non-trivial base case; if not in the table then assume +Inf
    B = {1^(1<<count):0}

    if verbose:
        i = 0
        start = time.clock()

    for m in range(2, count+1):
        # Get all the cities subsets of size m that include city 0
        size_m_cities = bits.combinations_with_0(count, m)
        A = {}

        # subtract 1 b/c we ignore city 0
        if verbose:
            diagnostics_next_size(m, choose(count-1, m-1))

        for S in size_m_cities:
            if verbose:
                if i % 100000 == 0:
                    diagnostics_set(i, time.clock()-start, sys.getsizeof(A),
                                    sys.getsizeof(B))
                    start = time.clock()
                i += 1

            items = bits.bits(S)

            for j in items[1:]: # ignore city 0
                res = list()

                for k in items:
                    if k == j:
                        continue

                    index_k = bits.generate_index(bits.delete_city(S, j),
                                                  count, k)

                    if index_k in B:
                        # calculate A[S-{j},k] + ckj
                        res.append(B[index_k] + distances[k][j])

                # print res
                A[bits.generate_index(S, count, j)] = min(res)
        B = A

    final_set = list(bits.combinations_with_0(count, count))[0]

    return final_hop(count, final_set, B, distances)

# TODO Fill up the docstring with some examples
# TODO PyLint: Too many local variables (16/15) (too-many-locals)
def held_karp_scipy(cities, count, verbose=True):
    """ ([point],int,bool) -> float

    Calculate the min-cost TSP tour for a list of cities.

    Keyword arguments:
    cities  -- list of points in a 2-D plane
    count   -- number of cities
    verbose -- optional parameter for extra diagnostics
    """

    distances = distance_matrix(cities)

    # Only non-trivial base case; if not in the table then assume +Inf
    # B = {1^(1<<count):0}
    B = sparse.dok_matrix((2,1), dtype=np.float32) # or size 0?
    B[1,0] = 0 # Of B[0,1] = 0?

    if verbose:
        i = 0
        start = time.clock()

    # pdb.set_trace()

    for m in range(2, count+1):
        # Get all the cities subsets of size m that include city 0
        size_m_cities = bits.combinations_with_0(count, m)
        A = sparse.dok_matrix((1<<count,count), dtype=np.float32)

        # subtract 1 b/c we ignore city 0
        if verbose:
            diagnostics_next_size(m, choose(count-1, m-1))

        for S in size_m_cities:
            if verbose:
                if i % 100000 == 0:
                    diagnostics_set(i, time.clock()-start, sys.getsizeof(A),
                                    sys.getsizeof(B))
                    start = time.clock()
                i += 1

            items = bits.bits(S)

            for j in items[1:]: # ignore city 0
                res = list()

                for k in items:
                    if k == j:
                        continue

                    S_old = bits.delete_city(S, j)
                    if B[S_old,k] != 0 or S_old == 1:
                        # calculate A[S-{j},k] + ckj
                        res.append(B[S_old,k] + distances[k][j])

                A[S,j] = min(res)
        B = A

    final_set = list(bits.combinations_with_0(count, count))[0]

    return final_hop2(count, final_set, B, distances)
