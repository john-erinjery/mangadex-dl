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

def ret_float_or_int(num):
    if '.' in num:
        if (num.split('.')[1] != '0') and (num.split('.')[1] != '00'):
            return float(num) 
        else:
            return int(num.split('.')[0])
    else:
        return int(num)

'''
MangaDex-dl CLI manga downloader function

This function serves as the core of the software
'''
def manga_downloader(manga_id:str, download_range:list, output=''):
    print('Title :', api.view_manga_by_id(manga_id=manga_id).title['en'])
    print('Getting chapters and volumes list...')
    mangadict = api.get_manga_volumes_and_chapters(manga_id=manga_id, translatedLanguage=['en'])
    unsorted_chap_dict = {}
    chap_dict = {}
    rangee = download_range
    d1 = {}
    for i in mangadict.keys():
        d1.update(mangadict[i]['chapters'])
    for i in d1:
        if ret_float_or_int(i) >= rangee[0] and ret_float_or_int(i) <= rangee[1]:
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
    output_folder = os.getcwd() + output
    folder_random_id = randint(10000, 99999)
    folder_name = 'manga' + str(folder_random_id)
    os.mkdir(output_folder + '/' + folder_name)
    os.mkdir(output_folder + '/' + folder_name + '/' + 'pdf')
    os.chdir(output_folder + '/' + folder_name)
    print('Created root folder at ' + output_folder + '/' + folder_name)
    try:
        for i in ch_image:
            print('Starting Image conversion for Chapter {}'.format(i))
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
            try:
                for k in image_list:
                    img_obj_list.append(Image.open(str(k)).convert('RGB'))
                print('Pdf Conversion and Merge appending underway on Chapter {}'.format(i))
            except UnidentifiedImageError:
                print(UnidentifiedImageError.errno, 'Unidentified Image Error : ', UnidentifiedImageError.strerror)
            try:
                img_obj_list[0].save(output_folder + '/' + folder_name + '/' + 'pdf/' + str(i) + '.pdf', save_all=True, append_images=img_obj_list[1:])
            except UnidentifiedImageError:
                print(UnidentifiedImageError.errno, 'Unidentified Image Error : ', UnidentifiedImageError.strerror)
            merger.append(PdfReader(output_folder + '/' + folder_name + '/' + 'pdf/' + str(i) + '.pdf', 'rb'))
    except UnidentifiedImageError:
        print(UnidentifiedImageError.errno, 'Unidentified Image Error : ', UnidentifiedImageError.strerror)
    merger.write('../Chapter {}-{}.pdf'.format(rangee[0], rangee[1]))
    print('Successfully Saved Chapter {}-{}.pdf'.format(rangee[0], rangee[1]))
    os.chdir(output_folder)
    rmtree(folder_name)