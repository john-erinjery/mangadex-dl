from sys import argv
from manga import ret_float_or_int, manga_downloader
args = argv
print("""
MangaDex CLI
""")
url = None
download_range = []
output = ''
for i in args:
    if i == '-l':
        index = args.index(i) + 1
        url = args[index]
    elif i == '-r':
        index = args.index('-r') + 1
        download_range_str = args[index:index+2]
        for i in download_range_str:
            download_range.append(ret_float_or_int(i))
    elif i == '-o':
        index = args.index('-o') + 1
        output = args[index]
id = url.split('/')[-2]

manga_downloader(id, download_range, output)