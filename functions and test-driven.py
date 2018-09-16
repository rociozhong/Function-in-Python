def alternate_case(s: str, upper_first=True) -> str:
    """Given an arbitrary string, convert every odd character to
    upper case and even to lower-case (or vice-versa)
    :param s: a string to start with
    :param upper_first: defaults to uppers first, set False for opposite
    :return: the altered string
    >>> alternate_case('abcdefg')
    'AbCdEfG'
    >>> alternate_case('abcdefg', upper_first=False)
    'aBcDeFg'
    >>> alternate_case('The Three-Body Problem, by Cixin Liu')
    'ThE ThReE-BoDy pRoBlEm, By cIxIn lIu'
    """
    result = []
    if upper_first:
        for i, char in enumerate(s):
            if i % 2 == 0:
                result.append(str.upper(char))
            else:
                result.append(str.lower(char))

    else:
        for i, char in enumerate(s):
            if i % 2 == 0:
                result.append(str.lower(char))
            else:
                result.append(str.upper(char))

    return ''.join(result)






def get_every_number(mixed_list: list) -> list:
    """Create a new list from a mixed-type list, keeping only the number type items.
    In other words, it ignores strings, tuples, sublists, dictionaries, etc.
    :param mixed_list: a 1-dimensional list containing various types of data
    :return: a new list containing only the items that are number types
    >>> get_every_number(['abc', 42, 3.14159, 2 * 4, '9'])
    [42, 3.14159, 8]
    >>> get_every_number([75, 101010101, 0xC0ffee, 'java'])
    [75, 101010101, 12648430]
    """

    return [ele for ele in mixed_list if type(ele) == int or type(ele) == float]





def back_words(s: str) -> str:
    """Rearrange a string so that every word gets spelled backwards but the
    sequence of words and any punctuation stays the same.
    :param s: any string
    :return: a string with words in the same order but each word spelled backwards.
    >>> back_words('even yellow apples are not bananas.')
    'neve wolley selppa era ton sananab.'
    >>> back_words('to be or not to be, that is the question.')
    'ot eb ro ton ot eb, taht si eht noitseuq.'
    """
    import re

    new_s = re.findall(r'\w+|\S+', s)
    return ' '.join(w[::-1] for w in new_s[: -1]) + new_s[-1]





def flatten_list(nested_list: list) -> list:
    """Given a list contains other lists nested to any depth,
    compute a new 1-dimensional list containing all the original non-list
    values in the same order. Non-list collections are kept as-is, not flattened,
    even if they contain other lists.
    :param nested_list: A list that contains other lists, to any depth.
    :return: a 1-dimensional list with all the original non-list values in the same order.
    >>> flatten_list([[[[[1, 2], 3]], 4, 5], 6])
    [1, 2, 3, 4, 5, 6]
    >>> flatten_list(['abc', 2, ['x', 'y'], ['a', 'b'], [[[[[[[[[[['z']]]]]]]]]]]])
    ['abc', 2, 'x', 'y', 'a', 'b', 'z']
    >>> flatten_list([1, 2, (3, [4, 5]), ['cat', 'in', 'the', 'hat']])
    [1, 2, (3, [4, 5]), 'cat', 'in', 'the', 'hat']
    >>> flatten_list(['this list', 'is', 'not', 'nested'])
    Traceback (most recent call last):
    ...
    ValueError: nested_list parameter was already 1-dimensional.
    """

    nonlist = len([i for i in nested_list if type(i) != type([])])
    if nonlist == len(nested_list):
        raise ValueError("nested_list parameter was already 1-dimensional.")
    result = []
    def helper(nested_list, result):
        for i in nested_list:
            if type(i) == type([]):
                helper(i, result)
            else:
                result.append(i)
    helper(nested_list, result)
    return result


def sum_list_numbers(x: list) -> float:
    """Given any list of mixed data types, possibly nested with other lists,
    compute the arithmetic sum of all the numeric values contained in it.
    Supports integers, floats, decimals, and lists thereof. Ignores values 
    contained in non-list collections.
    :param x: a list of mixed data types, possibly nested with other lists.
    :return: the sum of all numeric values contained in list x.
    >>> sum_list_numbers([5, 2, 3])
    10.0
    >>> sum_list_numbers([[[2, 5], 4]])
    11.0
    >>> sum_list_numbers([['number 5', [[25.2]]], 0.9, 'x', [4]])
    30.1
    >>> sum_list_numbers([34, 2, (5, 1)])
    36.0
    >>> sum_list_numbers([{45: 5, 100: -200}])
    0.0
    """
    flatten = flatten_list(x)
    return round(sum(i for i in flatten if isinstance(i, (int, float))),1)


import numpy as np


def find_max_subcube(a: np.ndarray, show_intermediate_results=True) -> np.ndarray:
    """Given a cubical ndarray, search all subcubes (all proper
    and the improper one), to find which one has the maximum sum.
    Since there are negative numbers in the values, there's no
    way to predict where it will be, and there's no theoretical
    advantage for largest subcubes vs medium ones.
    :param a: the whole array to search
    :param show_intermediate_results: whether to print results per subcube size
    :return: the subcube ndarray that had max sum
    >>> cube = np.load(file='A4_cube_size5_example.npy', allow_pickle=False, mmap_mode=None)
    >>> cube[4,4,4]
    -97.094082653629087
    >>> m = find_max_subcube(cube)
    searching cube of width 5
    checking all subcubes of width  1, of which     125 exist.  Highest sum    95.15 found at position (3, 4, 2)
    checking all subcubes of width  2, of which      64 exist.  Highest sum   355.41 found at position (1, 3, 3)
    checking all subcubes of width  3, of which      27 exist.  Highest sum   433.42 found at position (0, 0, 1)
    checking all subcubes of width  4, of which       8 exist.  Highest sum   310.35 found at position (0, 1, 1)
    checking all subcubes of width  5, of which       1 exist.  Highest sum   -38.25 found at position (0, 0, 0)
    <BLANKLINE>
    Total number of subcubes checked: 225
    Highest sum found was 433.415033731 in a subcube of width 3 at position (0, 0, 1)
    """
    global_max = -np.inf
    global_result = (0, 0, 0)
    global_k = 1
    dim = a.shape
    n = dim[0]
    total_num = 0
    for k in range(1, n + 1):
        local_max = -np.inf
        local_result = (0, 0, 0)
        num_cubes = (n - k + 1) ** 3
        total_num += num_cubes
        for i in range(n - k + 1):
            for j in range(n - k + 1):
                for l in range(n - k + 1):
                    temp = np.sum(a[i:(i + k), j:(j + k), l:(l + k)])
                    if temp > local_max:
                        local_max = temp
                        local_result = (i, j, l)
        if local_max > global_max:
            global_max = local_max
            global_result = local_result
            global_k = k

        if show_intermediate_results:
            print("checking all subcubes of width {0}".format(k), ", of which {0}".format(num_cubes),
                  "exist. Highest sum {0: 0.2f}".format(local_max), "found at position {0}\n".format(local_result))

    print("Total number of subcubes checked {0}".format(total_num), "Highest sum found was {0}".format(global_max),
          "in a subcube of width {0}".format(global_k), "at position {0}".format(global_result))

    i, j, l = global_result

    return a[i:(i + global_k), j:(j + global_k), l:(l + global_k)]



