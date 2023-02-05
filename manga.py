import mangadex
from PIL import Image, UnidentifiedImageError
import subprocess
import os
from random import randint
from shutil import rmtree
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
    for i in ch_image:
        print('Starting Image conversion for Chapter {}'.format(i))
        os.mkdir(str(i))
        n = 1
        image_list = []
        img_obj_list = []
        for j in ch_image[i]:
            subprocess.run(['wget', j, '-O', (str(i) + '/' + str(n) + j[-4:])], capture_output=True)
            image_list.append(str(i) + '/' + str(n) + j[-4:])
            n += 1
"""
 try:
            for k in image_list:
                img_obj_list.append(Image.open(k).convert('RGB'))
            print('Pdf Conversion and Merge appending underway on Chapter {}'.format(i))
        except UnidentifiedImageError:
            print('there was an unidentified image error')
        try:
            img_obj_list[0].save(output_folder + '/' + folder_name + '/' + 'pdf/' + str(i) + '.pdf', save_all=True, append_images=img_obj_list[1:])
        except UnidentifiedImageError:
            print('there was an unidentified image error')
"""

        # merger.append(PdfReader(output_folder + '/' + folder_name + '/' + 'pdf/' + str(i) + '.pdf', 'rb'))

    # merger.write('../Chapter {}-{}.pdf'.format(rangee[0], rangee[1]))
    #print('Successfully Saved Chapter {}-{}.pdf'.format(rangee[0], rangee[1]))
    #os.chdir(output_folder)
    # rmtree(folder_name)