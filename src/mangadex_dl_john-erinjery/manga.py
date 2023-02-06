'''
MangaDex-dl CLI

This Command Line Client uses the ManagDex API to download manga
and store it in image or PDF format.

You can choose whether to have the software merge all the chapters
downloaded into a single PDF, or have it in Chapterwise PDFs

If you choose to download manga in image format, you can choose
whether to save it in chapterwise folders or as a single large folder.
- this option is made to make it more convinient for readers to scroll
  through and read manga
- another feature is that if the files are named in a format that
  Andriod phones and PC's will be able to sort easily.
- it names files in the format aaa-1.jpg, aab-2.jpg...ect.
  if not, the file order will be quite messed up

This software is completely open source.
Feel free to use it as you like!

'''

import mangadex
from PIL import Image, UnidentifiedImageError
import os
from random import randint
from shutil import rmtree, copyfileobj
from PyPDF2 import PdfMerger, PdfReader
import requests
api = mangadex.Api()
merger = PdfMerger()
abc = 'abcdefghijklmnopqrstuvwxyz'
def make_sortable(stack):
    lenght = len(stack)
    prefixes = name_gen(lenght)
    result_stack = []
    for i in range(lenght):
        result_stack.append(prefixes[i] + '-' + str(stack[i]))
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
def ret_float_or_int(num):
    if '.' in num:
        if (num.split('.')[1] != '0') and (num.split('.')[1] != '00'):
            return float(num) 
        else:
            return int(num.split('.')[0])
    else:
        return int(num)

def path_prettify(path:str):
    new_path = path.replace('/', '\\')
    return new_path

'''
MangaDex-dl CLI manga downloader function

This function serves as the core of the software
'''

def manga_downloader(args_dict):

    manga_url = args_dict['manga_url']
    chapter_url = args_dict['chapter_url']
    range_ = args_dict['range']
    pdf = args_dict['pdf']
    img = args_dict['img']
    merge = args_dict['merge']
    single_folder = args_dict['single_folder']

    if manga_url != None:
        manga_id = manga_url.split('/')[-2]
        print('Starting download of \'{}\''.format(api.view_manga_by_id(manga_id=manga_id).title['en']))
        print('\ngetting chapters and volumes..')
        mangadict = api.get_manga_volumes_and_chapters(manga_id=manga_id, translatedLanguage=['en'])

        unsorted_chap_dict = {}
        chap_dict = {}
        d1 = {}
        for i in mangadict.keys():
            d1.update(mangadict[i]['chapters'])
        for i in d1:
            if ret_float_or_int(i) >= range_[0] and ret_float_or_int(i) <= range_[1]:
                unsorted_chap_dict[ret_float_or_int(i)] = d1[i]['id']
        for i in sorted(unsorted_chap_dict):
            chap_dict[i] = unsorted_chap_dict[i]

        ch_image = {}
        for i in chap_dict:
            r = requests.get(url='https://api.mangadex.org/at-home/server/' + chap_dict[i])
            data = r.json()
            ch_img_list = []
            baseurl = data['baseUrl']
            hash = data['chapter']['hash']
            url = baseurl + '/data-saver/' + hash + '/'
            for j in data['chapter']['dataSaver']:
                ch_img_list.append(url + j)
            ch_image[i] = ch_img_list

        output_folder = os.getcwd() + ''
        folder_random_id = randint(10000, 99999)
        rel_folder_name = 'manga' + str(folder_random_id)
        folder_name = path_prettify(output_folder + '/' + rel_folder_name)
        os.mkdir(folder_name)
        os.chdir(folder_name)
        print('Created root folder at : ' + folder_name)
        os.mkdir(folder_name + '\\' + 'pdf')
        all_images = []
        for i in ch_image:
            print('\ndownloading images for chapter {}..'.format(i))
            os.mkdir(str(i))
            n = 1
            image_list = []
            img_obj_list = []

            for j in ch_image[i]:
                r = requests.get(j, stream=True)
                with open((str(i) + '/' + str(n) + j[-4:]), 'wb') as f:
                    r.raw.decode_content = True
                    copyfileobj(r.raw, f)
                image_list.append(str(i) + '/' + str(n) + j[-4:])
                n += 1
            all_images.extend(image_list)
            if pdf:
                try:
                    for k in image_list:
                        img_obj_list.append(Image.open(str(k)).convert('RGB'))
                    print('converting chapter {} into pdf..'.format(i))
                except UnidentifiedImageError:
                    print(UnidentifiedImageError.errno, 'Unidentified Image Error : ', UnidentifiedImageError.strerror)

                try:
                    img_obj_list[0].save(folder_name + '/' + 'pdf/' + str(i) + '.pdf', save_all=True, append_images=img_obj_list[1:])
                except UnidentifiedImageError:
                    print(UnidentifiedImageError.errno, 'Unidentified Image Error : ', UnidentifiedImageError.strerror)
                
                if merge:
                    merger.append(PdfReader(folder_name + '/' + 'pdf/' + str(i) + '.pdf', 'rb'))
            else:
                pass
        
        if not pdf:
            if os.path.exists('pdf'):
                rmtree('pdf')
            os.mkdir('../imgs')
            dir = os.listdir('.')
            dir_ = []
            for i in dir:
                dir_.append(ret_float_or_int(i))
            dir_.sort()
            overlap = name_gen(len(dir))
            print('organising image folders..')
            if not single_folder:
                for i in range(len(dir_)):
                    os.rename(str(dir_[i]), ('../imgs/' + overlap[i] + '-' + str(dir_[i])))
            else:
                dir = os.listdir('.')
                total_imgs = len(all_images)
                over_lap = name_gen(total_imgs)
                for i in range(total_imgs):
                    os.rename(all_images[i], ('../imgs/' + over_lap[i] + '-' + str(i + 1) + all_images[i][-4:] ))
        else:
            os.rename('pdf', '../pdf')
        if merge:
            print('\nmerging chapters {} to {}'.format(range_[0], range_[1]))
            merger.write('../Chapter {}-{}.pdf'.format(range_[0], range_[1]))
            print('merge complete')
        os.chdir('..')
        print('deleting ' + folder_name)
        rmtree(folder_name)
    else:
        pass