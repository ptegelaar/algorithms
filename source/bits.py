#!/usr/bin/env python2.7
"""Helper module for representing sets as integers"""

import doctest

def delete_city(int_cities, j):
    """ (int, int) -> int

    Take a set of cities (represented by an int) and delete the j-th
    city (index starting at 0). If not present, then ignore and return
    the original set.

    NB int_cities = 1 represents city 0 is present.

    >>> delete_city(1,0) # 1 = 1
    0
    >>> delete_city(10,0) # 10 = 1010
    10
    >>> delete_city(5,2) # 5 = 101
    1

    Keyword arguments:
    int_cities -- integer representation of a set of cities
    j          -- city id
    """

    j_bin = 1 << j

    if int_cities & j_bin: # j in int_cities
        return int_cities^j_bin
    else: # j not in int_cities, so nothing to delete
        return int_cities

def combinations_with_0(n, k):
    """ (int, int) -> [ints]

    Generate combinations of k items from a set of n items, that
    includes item 0. Return a list of integer representations of
    these combinations.

    >>> list(combinations_with_0(2, 1))
    [1]
    >>> list(combinations_with_0(4, 2))
    [3, 5, 9]
    >>> list(combinations_with_0(4, 3))
    [7, 11, 13]
    """

    assert 1 <= k <= n, ("Parameter k should be (inclusively)"
                         "between 1 and n.")

    # So the limit will be set equal to the # of cities (25 in our
    # case). We reserve the prefix 5 bits for our j: j << n.
    limit = 1 << n
    x = (1 << k) - 1

    while x < limit:
        if x & 1: # the set should include item 0
            yield x

        # Gosper's hack:
        y = x & -x
        c = x + y
        x = (((c^x) >> 2) / y) | c

# TODO change representation to (cities,destination)
def generate_index(int_cities, city_count, destination):
    """ (int, int, int) -> [int]

    Takes a set of cities (represented by an int), the total number of
    cities, and a destination city. Returns an int representation of
    the combination (destination, cities). This allows us to use a
    single int instead of two, which matters a lot for memory
    consumption with large hash tables with 32-bit integer keys.

    >>> generate_index(3, 2, 1)
    11
    >>> generate_index(22, 5, 3)
    150
    """

    # check if most significant bit is less than the total number of
    # cities
    assert len(bin(int_cities)[2:])-1 < city_count
    assert destination < city_count

    return int_cities + ((destination+1) << city_count)

# http://stackoverflow.com/questions/8898807/pythonic-way-to-iterate-over-bits-of-integer
def bits(n):
    """ int -> [int]

    Get the index numbers (starting at 0) of 1's out of the binary
    representation of an int (without having to iterate over all the
    intervening 0s).

    >>> bits(0)
    []
    >>> bits(5)
    [0, 2]
    >>> bits(83)
    [0, 1, 4, 6]
    """

    items = []

    while n:
        b = n & -n
        highbit = b
        item = 0

        while highbit != 1:
            highbit >>= 1
            item += 1

        items.append(item)
        n ^= b

    return items

if __name__ == '__main__':
    doctest.testmod()
