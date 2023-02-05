from sys import argv
from manga import ret_float_or_int, manga_downloader
args = argv
VERSION = '1.0'

# Loading the help dictionary
with open('help-dict.txt') as f:
    help_dict = eval(f.read())
    help_dict_ops = []
    help_dict_all_ops = []
    for i in help_dict.keys():
        help_dict_ops.append(i.split(','))
        for j in i.split(','):
            if j != '':
                help_dict_all_ops.append(j)

'''
MangaDex-dl CLI help function

handles all help details
(yet to add help <option> help)
'''
def help(func='general'):
    if func not in help_dict_all_ops:
        print('ERROR : Invalid Option')
    else:
        for i in help_dict_ops:
            if func in i:
                print(help_dict[list(help_dict.keys())[help_dict_ops.index(i)]])

# An helper function to parse the args           
def obj_at_next_index(obj, stack, steps=1):
    index = stack.index(obj) + 1
    if steps==1:
        return stack[index]
    else:
        return stack[index: index + steps]

'''
MangaDex-dl CLI argument collector function

collects all the arguments from input and categorises them,
error raised if invalid args given, else arg dict returned
'''
def get_arguments(args):
    manga_url = None
    chapter_url = None
    range_ = []
    range_1 = []
    pdf = True
    img = False
    merge = False
    single_folder = False
    if len(args) == 1:
        help()
        return None
    elif len(args) == 2:
        if args[-1] == '-V' or args[-1] == '--version':
            help('-V')
        elif args[-1] == '-h' or args[-1] == '--help':
            help()
        else:
            print('ERROR: Invalid Syntax')
        return None
    else:
        for i in args[1:]:
            if i == '-t' or i == '--manga-url':
                manga_url = obj_at_next_index(i, args)
            elif i == '-c' or i == '--chapter-url':
                chapter_url = obj_at_next_index(i, args)
            elif i == '-r' or i == '--range':
                range_1 = obj_at_next_index(i, args, 2)
                for i in range_1:
                    range_.append(ret_float_or_int(i))
            elif i == '-pdf':
                continue
            elif i == '-img':
                pdf = False
                img = True
            elif i == '-m' or i == '--merge-pdf':
                merge = True
            elif i == '-s' or i == '--single-folder':
                single_folder = True
            elif i in range_1:
                continue
            elif i == manga_url or i == chapter_url:
                continue
            else:
                print('ERROR: Invalid Option', i)
                return None
    return {'manga_url' : manga_url, 'chapter_url' : chapter_url, 'range' : range_, 'pdf' : pdf, 'img' : img, 'merge' : merge, 'single_folder' : single_folder}

'''
MangaDex-dl CLI argument analyzer

goes through the argument dictionary to find sematic errors
'''
def check_ok(arg_dict):
    if arg_dict == None:
        return False
    
    manga_url = arg_dict['manga_url']
    chapter_url = arg_dict['chapter_url']
    range_ = arg_dict['range']
    pdf = arg_dict['pdf']
    img = arg_dict['img']
    merge = arg_dict['merge']
    single_folder = arg_dict['single_folder']
    
    if manga_url == chapter_url == None:
        print('ERROR: manga url or chapter must be provided')
        return False
    elif manga_url != None and chapter_url != None:
        print('ERROR: both manga and chapter urls should not be provided')
        return False
    elif manga_url != None and range_ == []:
        print('ERROR: Range must be provided for manga urls')
        return False
    elif chapter_url != None and range_ != []:
        print('ERROR: Range should not be provided for chapter urls')
        return False
    elif pdf and img:
        print('ERROR: Manga cannot be stored as both image and pdf')
        return False
    elif merge and single_folder:
        print('ERROR: Cannot merge and single folder')
        return False
    elif pdf and single_folder:
        print('ERROR: Cannot be both pdf and single folder')
        return False
    elif img and merge:
        print('ERROR: Cannot be both img and merge')
        return False
    else:
        return True

arg_dict = get_arguments(args)

if check_ok(arg_dict):
    manga_downloader(arg_dict)