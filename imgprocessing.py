import os
from manga import ret_float_or_int
import shutil
abc = 'abcdefghijklmnopqrstuvwxyz'
def make_sortable(stack):
    lenght = len(stack)
    prefixes = name_gen(lenght)
    result_stack = []
    for i in range(lenght):
        result_stack.append(prefixes[i] + '-' + stack[i])
    return result_stack
def name_gen(lenght):
    n1 = 0
    n2 = 0
    n3 = 0
    name_list = []
    while n1 < 26:
        while n2 < 26:
            while (n3 < 26) and (len(name_list) < lenght):
                name_list.append(abc[n1] + abc[n2] + abc[n3])
                n3 += 1
            n2 += 1
            n3 = 0
        n1 += 1
        n2 = 0
        n3 = 0
    return name_list


