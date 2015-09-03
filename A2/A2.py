#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import os
import argparse
import sys
import manager
import multiprocessing

#IGNORE = ['Thumbs.db', '~', '.DS_Store', 'digest']

def sync_dir(local_files, remote_sync):
    #dir_cmp = filecmp.dircmp(local_root, remote_root, ignore = IGNORE, hide = None)
    if args.verbose:
        #print('sync_dir: %s' % dir_cmp.left_list)
        print('L: %s, R: %s' % (local_files,remote_sync))


def walker(local_root, remote_root):
    if args.verbose:
        print('Local Root path: %s'% (local_root))
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(local_root):
        if args.verbose:
            print('Current path: %s'% root)
        files_manager = manager.FileManager(root, files, args.verbose)
        files_manager.sync_file(root,files,root.replace(local_root,remote_root))
        for name in dirs:
            if not os.path.exists(os.path.join(root.replace(local_root,remote_root), name)):
                if args.verbose:
                    print('R-Folder does not exist')
                os.makedirs(os.path.join(root.replace(local_root,remote_root), name))             

def Main(local_path, remote_path):
    if args.verbose:
        print('='*50 + '\nStart to sync...' + '\n' + '='*50)
    #walker(os.getcwd())
    p1 = multiprocessing.Process(target=walker(local_path, remote_path))
    #p2 = multiprocessing.Process(target=walker(dir_right))
    p1.start()
    #p2.start()
    p1.join()
    #p2.join()
    #walker(dir_left)
    #sync_dir(local_path, remote_path) 
    if args.verbose:
        print('\n')
    #walker(dir_right)
        print('\n' + '='*50 + '\nCompleted the sync' + '\n' + '='*50)
    
            

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("dir_1", help="Folder path 1",type = str)
    parse.add_argument("dir_2", help="Folder path 2",type = str)
    parse.add_argument('-v', "--verbose", help="increase output verbosity", action="store_true")
    args = parse.parse_args()
    if args.verbose:
        print('*'*50)
    local_path, remote_path = args.dir_1, args.dir_2
    if not os.path.exists(local_path) and not os.path.exists(remote_path):
        raise Exception('input dirs are invalid')
    if args.verbose:
        print('%s\n%s'% (local_path, remote_path))
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    if not os.path.exists(remote_path):
        os.makedirs(remote_path)
    Main(local_path, remote_path)
