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
