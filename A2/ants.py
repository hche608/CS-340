#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import os
import json
import time
import hashlib
import shutil
import filecmp
from pprint import pprint

class Ants():
    
    def __init__(self, local_root, local_files, remote_root, sync, verbose = False):
        self.verbose = verbose
        self.sync = sync
        local_data = self.load_digest(local_root)
        remote_data = self.load_digest(remote_root)
        working_list = []
        
        # Determine the items that exist in both directories
        d1_contents = set(os.listdir(local_root))
        d2_contents = set(os.listdir(remote_root))
        common = list(d1_contents & d2_contents)
        common_files = [ f for f in common if os.path.isfile(os.path.join(local_root, f))]
        print('Common files:', common_files)

        # Compare the directories
        match, mismatch, errors = filecmp.cmpfiles(local_root, remote_root, common_files,shallow=False)
        print('Match:', match)
        print('Mismatch:', mismatch)
        print('Errors:', errors)
        
        
        if bool(remote_data):
            for fname in local_files:
                if not fname.startswith('.') and not fname.endswith('~') and not fname == self.sync and not self.is_same(fname,local_data,remote_data):
                    working_list.append(fname)
                    print('Added: %s' % fname)

        if len(working_list) > 0:
            if self.verbose:
                print('Task: %s' % working_list)
            for fname in working_list:
                shutil.copy2(os.path.join(local_root,fname), os.path.join(remote_root,fname)) 
                if self.verbose:
                    print('Copy2 %s .........' % fname) 


    
    def is_same(self, fname, local_info, remote_info):
        result = False
        if fname in remote_info:
            # format = {'file name':[[mtime, uid]]}
            local_mtime = local_info[fname][0][0]
            local_uid = local_info[fname][0][1]
            remote_mtime = remote_info[fname][0][0]
            remote_uid = remote_info[fname][0][1]
            # if two files are same, or local file is older than remote one
            if local_mtime < remote_mtime or local_uid == remote_uid:
                result = True
        return result            
            
            
    def load_digest(self, root):
		# w+ = overwrite, a+ = append
        if os.path.exists(os.path.join(root, self.sync)) and os.stat(os.path.join(root, self.sync)).st_size > 0:
            with open(os.path.join(root, self.sync)) as f:
                load_buffer = json.load(f)
            f.close()
            return load_buffer            
           
    

