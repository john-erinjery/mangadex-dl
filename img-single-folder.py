import os
from manga import ret_float_or_int
import shutil
abc = 'abcdefghijklmnopqrstuvwxyz'
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
manga_dir_list = os.listdir('manga')
os.chdir('manga')
os.mkdir('imgs')
for i in manga_dir_list:
    for j in os.listdir(i):
        if j != 'pdf':
            os.rename(src=f'{i}/{j}', dst=f'imgs/{j}')
os.chdir('imgs')
order_of_chapters = []
for i in os.listdir('.'):
    order_of_chapters.append(ret_float_or_int(i))
order_of_chapters.sort()
n = 1
j = len(order_of_chapters)
x = 0
big_d = {}
length = 0
for i in order_of_chapters:
    l1 = []
    l = []
    ext = []
    for q in os.listdir(str(i)):
        l1.append(ret_float_or_int(q[:-4]))
        ext.append(q[-4:])
    hjt = l1
    l1.sort()
    for s in l1:
        index = hjt.index(s)
        e = ext[index]
        l.append(str(s) + e)
    big_d[i] = l
    length += len(l)

name_list = name_gen(length)
n = 0
for i in big_d:
    l = big_d[i]
    for j in l:
        os.rename(f'{i}/{j}', (name_list[n] + '.' + j.split('.')[1]))
        n += 1
for i in big_d:
    shutil.rmtree(str(i))