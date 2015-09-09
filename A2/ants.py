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
    
    def __init__(self, local_root, local_files, remote_root, SYNC, TIME_FORMAT, verbose = False):
        self.SYNC = SYNC
        self.TIME_FORMAT = TIME_FORMAT
        self.verbose = verbose        
        local_data = self.load_digest(local_root)
        remote_data = self.load_digest(remote_root)        
        # Determine the items that exist in both directories
        if os.path.exists(local_root) and os.path.exists(remote_root):
            d1 = set(os.listdir(local_root))        
            d2 = set(os.listdir(remote_root))
            common_files = list(filter(lambda f: not f.startswith('.') and not f.endswith('~') and not f == self.SYNC and os.path.isfile(os.path.join(local_root, f)), list( d1 & d2)))
            # Determine the items that only exist in left directory
            only = list(filter(lambda f: not f.startswith('.') and not f.endswith('~') and not f == self.SYNC and os.path.isfile(os.path.join(local_root, f)), list( d1 - d2 )))
            
            # Compare the directories
            match, mismatch, errors = filecmp.cmpfiles(local_root, remote_root, common_files,shallow=False)
            if self.verbose:
                print('Match:', match) # No copy
                print('Mismatch:', mismatch)
                print('Only:',only)
                print('Errors:', errors)
            
            # check mismatch and only
            working_list = []
            if len(list(set(mismatch) | set(only))) > 0:
                for fname in list(set(mismatch) | set(only)):
                    if self.needs_copy(fname,local_data,remote_data):
                        working_list.append(fname)
                        if self.verbose:
                            print('Added: %s' % fname)        
            
            # delete file in only list
            for fname in list(set(only) - set(working_list)):
                os.remove(os.path.join(local_root,fname))
                if self.verbose:
                    print('%s deleted' % fname)
        
            if len(working_list) > 0:
                if self.verbose:
                    print('Task: %s' % working_list)
                for fname in working_list:
                    shutil.copy2(os.path.join(local_root,fname), os.path.join(remote_root,fname)) 
                    if self.verbose:
                        print('Copy2 %s .........' % fname) 

    
    def needs_copy(self, fname, local_info, remote_info):
        result = False
        # check mismatch or deleted in only
        if fname in remote_info:
            # format = {'file name':[[mtime, uid]]}
            local_mtime = time.strptime(local_info[fname][0][0], self.TIME_FORMAT)
            local_uid = local_info[fname][0][1]
            remote_mtime = time.strptime(remote_info[fname][0][0], self.TIME_FORMAT)
            remote_uid = remote_info[fname][0][1]
            if self.verbose:
                print('Fname: ', fname)
                print('L Uid: ', local_uid)
                print('R Uid: ', remote_uid)
                print('L Time: ', time.strftime(self.TIME_FORMAT,local_mtime))
                print('R Time: ', time.strftime(self.TIME_FORMAT,remote_mtime))
                print('L > R: ', local_mtime > remote_mtime )

            if local_mtime > remote_mtime and remote_info[fname][0][1] == 'deleted':
                 result = True
            elif local_mtime == remote_mtime and local_uid != remote_uid:
                if remote_info[fname][0][1] in [j for i in local_info[fname] for j in i]:
                    if self.verbose:
                        print('Old version in Re')
                    result = True
            elif local_uid == remote_uid and local_mtime < remote_mtime: # Case 1: same UID, DIff Mtime => Earliest time apply
                result = True 
            elif local_uid != remote_uid and local_mtime > remote_mtime: # Case 2: diff UID, DIff Mtime => latest time apply
                # current remote uid exists in past loacl uids 
                #if remote_info[fname][0][1] in [j for i in local_info[fname] for j in i]:
                #    if self.verbose:
                #        print('Old version')
                #    result = True
                #else:
                #    if self.verbose:
                #        print('Tow diff files')
                result = True          
        # check only
        else:
            if self.verbose:
                print('New File: ', fname)
            result = True
        return result            
            
            
    def load_digest(self, root):
		# w+ = overwrite, a+ = append
        if os.path.exists(os.path.join(root, self.SYNC)) and os.stat(os.path.join(root, self.SYNC)).st_size > 0:
            with open(os.path.join(root, self.SYNC)) as f:
                load_buffer = json.load(f)
            f.close()
            return load_buffer            
           
    

