#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import os
import argparse
import sys
import monitor
import ants
import multiprocessing


SYNC = '.sync'
FORMAT = '%Y-%m-%d %H:%M:%S %z'


def mover(local_root, remote_root):
    if args.verbose:
        print('From %s ===> %s.' % (local_root, remote_root))
    for root, dirs, files in os.walk(local_root):
        files_worker = ants.Ants(
            root,
            files,
            root.replace(
                local_root,
                remote_root,
                1),
            SYNC,
            FORMAT,
            args.verbose)


def update(local_path, remote_path):
    p1 = multiprocessing.Process(target=walker(local_path, remote_path))
    p2 = multiprocessing.Process(target=walker(remote_path, local_path))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def walker(local_root, remote_root):
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(local_root):
        if args.verbose:
            print('Current path: %s' % root)
        files_monitor = monitor.Monitor(
            root, files, SYNC, FORMAT, args.verbose)
        if args.verbose and dirs:
            print('dirs: %s' % dirs)
        for name in dirs:
            if not os.path.exists(os.path.join(
                    root.replace(local_root, remote_root, 1), name)):
                # if folder does not exist then create it
                os.makedirs(
                    os.path.join(
                        root.replace(
                            local_root,
                            remote_root,
                            1),
                        name))
                if args.verbose:
                    print(
                        'Make Folder: %s' %
                        os.path.join(
                            root.replace(
                                local_root,
                                remote_root,
                                1),
                            name))
                    print('%s, %s' % (local_root, name))


def Main(local_path, remote_path):
    if args.verbose:
        print(
            '*' *
            80 +
            '\n' +
            '*' *
            80 +
            '\n' +
            ' ' *
            10 +
            '......Scan Files......' +
            '\n' +
            '=' *
            50)
    if args.multi:
        if args.verbose:
            print(
                ' ' *
                10 +
                '......Multiprocessing Mode.....' +
                '\n' +
                '=' *
                50)
        update(local_path, remote_path)
    else:
        if args.verbose:
            print(
                ' ' *
                10 +
                '......Single processing Mode......' +
                '\n' +
                '=' *
                50)
        walker(local_path, remote_path)
        walker(remote_path, local_path)
    if args.verbose:
        print(
            '=' *
            50 +
            '\n' +
            ' ' *
            10 +
            '......Scan Completed' +
            '\n' +
            '=' *
            50 +
            '\n' +
            ' ' *
            10 +
            '......Sync Files......' +
            '\n' +
            '=' *
            50)

    if args.multi:
        p1 = multiprocessing.Process(target=mover(local_path, remote_path))
        p2 = multiprocessing.Process(target=mover(remote_path, local_path))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    else:
        mover(local_path, remote_path)
        if args.verbose:
            print('=' * 50)
        mover(remote_path, local_path)
    if args.verbose:
        print(
            '=' *
            50 +
            '\n' +
            ' ' *
            10 +
            '......Update Sync......' +
            '\n' +
            '=' *
            50)
    if args.multi:
        update(local_path, remote_path)
    else:
        walker(local_path, remote_path)
        walker(remote_path, local_path)
    if args.verbose:
        print(
            '=' *
            50 +
            '\n' +
            ' ' *
            10 +
            '......Update Sync Completed......' +
            '\n' +
            '=' *
            50 +
            '\n' +
            ' ' *
            10 +
            '......Completed the sync......' +
            '\n' +
            '*' *
            80)


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("dir_1", help="Folder path 1", type=str)
    parse.add_argument("dir_2", help="Folder path 2", type=str)
    parse.add_argument(
        '-m',
        "--multi",
        help="multiprocess mode",
        action="store_true")
    parse.add_argument(
        '-v',
        "--verbose",
        help="increase output verbosity",
        action="store_true")
    args = parse.parse_args()
    if args.verbose:
        print('*' * 50)
    local_path, remote_path = args.dir_1, args.dir_2
    if not os.path.exists(local_path) and not os.path.exists(remote_path):
        raise Exception('input dirs are invalid')
    if args.verbose:
        print('%s\n%s' % (local_path, remote_path))
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    if not os.path.exists(remote_path):
        os.makedirs(remote_path)
    Main(local_path, remote_path)
