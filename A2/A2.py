#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import os
import argparse
import filecmp
import shutil
import sys
import json
import manager
import multiprocessing
import multiprocessing_scanner

IGNORE = ['Thumbs.db', '~', '.', 'json']

def sync_files(src, dest, ignore=IGNORE):
    if os.path.isfile(src) or os.path.isfile(dest):
        print('只能对文件夹进行同步, 请正确输入源文件夹和目标文件夹...')
        return
    dir_cmp = filecmp.dircmp(src, dest, ignore=IGNORE)
    sync(dir_cmp)
    json_obj = dict()
    json_obj[dir_left] = src
    print(json_obj)
    
    walker(os.getcwd())
    print('同步完成!')
          
def walker(dir_path):
    print('Root path: %s'% (dir_path))
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(dir_path):
        print('Current path: %s'% root)
        files_manager = manager.FileManager(root, files)
        for name in dirs:
            print(os.path.join(root, name))

            
def Main(dir_left, dir_right):
    print('='*50 + '\nStart to sync...' + '\n' + '='*50)
    #walker(os.getcwd())
    p1 = multiprocessing.Process(target=walker(dir_left))
    #p2 = multiprocessing.Process(target=walker(dir_right))
    p1.start()
    #p2.start()
    p1.join()
    #p2.join()
    #walker(dir_left)
    print('\n')
    #walker(dir_right)
    print('\n' + '='*50 + '\nCompleted the sync' + '\n' + '='*50)

    
            
if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("dir_1", help="Folder path 1",type = str)
    parse.add_argument("dir_2", help="Folder path 2",type = str)
    args = parse.parse_args()
    print('*'*50)
    dir_left, dir_right = args.dir_1, args.dir_2
    if not os.path.exists(dir_left) and not os.path.exists(dir_right):
        raise Exception('input dirs are invalid')
    print('%s\n%s'% (dir_left, dir_right))    
    if not os.path.exists(dir_left):
        os.makedirs(dir_left)
    if not os.path.exists(dir_right):
        os.makedirs(dir_right)
    Main(dir_left, dir_right)
