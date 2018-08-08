from itertools import chain


def flatten(list_of_lists, n=0):
    result = chain.from_iterable(list_of_lists)
    for i in range(0, n):
        print(list(result))
        result = chain.from_iterable(result)
        print(list(result))
    return list(result)
