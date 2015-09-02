#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import os
import hashlib
import argparse
import filecmp
import shutil
import sys
import json

IGNORE = ['Thumbs.db']

def json_test(json_obj):
    with open('data.json', 'a+') as f:
        json.dump(json_obj, f)
    
def sha256(fname, blocksize = 65536):
    hash = hashlib.sha256()
    with open(fname) as f:
        for chunk in iter(lambda: f.read(blocksize), ""):
            hash.update(chunk.encode('utf-8'))
    return hash.hexdigest()

def md5(fname, blocksize = 65536):
    hash = hashlib.md5()
    with open(fname) as f:
        for chunk in iter(lambda: f.read(blocksize), ""):
            hash.update(chunk.encode('utf-8'))
    return hash.hexdigest()            

def sync_files(src, dest, ignore=IGNORE):
    if os.path.isfile(src) or os.path.isfile(dest):
        print('只能对文件夹进行同步, 请正确输入源文件夹和目标文件夹...')
        return
    dir_cmp = filecmp.dircmp(src, dest, ignore=IGNORE)
    sync(dir_cmp)
    print('同步完成!')
          
def Main():
    parse = argparse.ArgumentParser()
    parse.add_argument("xPath", help="Source folder path",type = str)
    parse.add_argument("dPath", help="Destination folder path ",type = str)
    args = parse.parse_args()
    print('Source Folder:      %s\nDestination Folder: %s'% (args.xPath, args.dPath))
    if os.path.isfile(args.xPath) or os.path.isfile(args.dPath):
        
    print('='*50 + '\nStart to sync...' + '\n' + '='*50)
    src = sha256(args.xPath)
    dest = sha256(args.dPath)
    print('Source File SHA265: %s' % str(src))
    print('Source File SHA265: %s' % str(dest))
    print('\n' + '='*50 + '\nCompleted the sync' + '\n' + '='*50)
    json_obj = dict()
    json_obj(args.xPath) = src
    print(json_obj(args.xPath))
    
            
if __name__ == '__main__':
    Main()