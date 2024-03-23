#!/usr/bin/env python3

help = '''
PyDownloader by ZhaoymOvO
ver 0.1.0
Function: Specify the download file of the thread.
Syntax: python main.py [parameters] <URL>
        or ./main.py [parameters] <URL>
Usage: python main.py -t16 -d'./download' -o'new' -e'img' -y https://example.org/examplt.img
Parameters:
    -t[count]           Specify the number of download threads
    -d'[directory]'     Specify the directory where the file is stored
    -o'[filename]'      Specify the file name when outputting the file (excluding extension)
    -e'[extension]'     Specify the file extension when output
    -y                  Let the script not ultimately confirm whether the user actually needs to download
'''

# get argv, if no argv, exit and print help
import sys, re
if not sys.argv[1:]:
    print(f'[-] !Syntax error: no argv\n{help}')
    sys.exit()

# import downloadkit, if no, print error and exit
try:
    from DownloadKit import DownloadKit
except:
    print(f'''[-] !Dependency error: DownloadKit package does not exist
    To solve this problem: use the command `pip install DownloadKit`''')
    sys.exit()

# Define the default value of the function option as the variable below
threads = 4
targetDirectory = None
sourceFileURL = None
outputName = None
outputExtenditionName = None
noConfirm = False

# Iterate over argv
for i in sys.argv[1:]:
    
    # print help
    if i.startswith('--help'):
        print(help)
        sys.exit()
    
    # define thread count
    elif i.startswith('-t'):
        try:
            threads = int(i[2:])
        except:
            print(f'[-] !Syntax error: unexpected thread count {i[2:]}')
            sys.exit()
    
    # define target directory
    elif i.startswith('-d'):
        if not i[2:]:
            print(f'[-] !Syntax error: unexpected target directory')
            sys.exit()
        try:
            targetDirectory = i[2:]
        except:
            print(f'[-] !Syntax error: unexpected target directory {i[2:]}')
            sys.exit()
    
    # define target file name
    elif i.startswith('-o'):
        if not i[2:]:
            print(f'[-] !Syntax error: unexpected target file name')
        outputName = i[2:]
        
    # define target extendition name
    elif i.startswith('-e'):
        if not i[2:]:
            print(f'[-] !Syntax error: unexpected target file name')
        outputExtenditionName = i[2:]
        
    # define confirm
    elif i.startswith('-y'):
        noConfirm = True
        
    # define source url
    else:
        isURL = re.fullmatch(r'[a-z]+://.+', i)
        if not isURL:
            print(f'[-] !Syntax error: unexpected source url {i}')
            sys.exit()
        else:
            sourceFileURL = i

# if there's no source url, exit
if not sourceFileURL:
    print('[-] !Syntax error: where is the source URL?')

# thie final confirm
if not noConfirm:
    while True:
        downloadRequest = input(f'''The finally ask:
The source URL is: {sourceFileURL}
The parameters are:
    threads: {threads}
    targetDirectory: {targetDirectory}
    sourceFileURL: {sourceFileURL}
    outputName: {outputName}
    outputExtenditionName: {outputExtenditionName}
Are you sure to download?
(y|n)''').strip().lower()
        if downloadRequest == 'n':
            sys.exit()
        elif downloadRequest == 'y':
            break
        else:
            continue

# download file
downloader = DownloadKit(targetDirectory, threads, file_exists='rename')
downloader.download(sourceFileURL, targetDirectory, outputName, outputExtenditionName, file_exists='rename')
downloader.wait()
