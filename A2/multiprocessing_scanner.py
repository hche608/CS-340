#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import multiprocessing
import manager


class Multiprocessing_scanner():

    def worker(dir_path):
        print('Root path: %s' % (dir_path))
        # traverse root directory, and list directories as dirs and files as
        # files
        for root, dirs, files in os.walk(dir_path):
            print('Current path: %s' % root)
            files_manager = manager.FileManager(root, files)
            for name in dirs:
                print(os.path.join(root, name))
        return
