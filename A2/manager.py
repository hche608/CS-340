#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import os
import json
import record
import time
import hashlib
from pprint import pprint

class FileManager():
    
    def __init__(self, root, files):
        self.local_digest = dict()
        # load digest if it exists and it has data
        if os.path.exists(os.path.join(root, 'digest')) and os.stat(os.path.join(root, 'digest')).st_size > 0:
            self.local_digest = self.load_digest(root, self.local_digest)
        for fname in files:
            # Skip hide files
            if not fname.startswith('.') and not fname.endswith('~') and not fname == 'digest':
                mtime = time.strftime("%Y-%m-%d %H:%M:%S %z",time.localtime(os.path.getmtime(os.path.join(root, fname))))
                #mtime = time.ctime(os.path.getmtime(os.path.join(root, fname)))
                uid = self.sha256(os.path.join(root, fname))
                # Update exist file in sync
                if fname in self.local_digest:
                    tmp_list = self.local_digest[fname]
                    # format = {'file name':[[mtime, uid],[mtime, uid]]}
                    if not self.exists(uid, tmp_list) or not self.exists(mtime, tmp_list):
                        tmp_list.insert(0,[mtime, uid])
                        self.local_digest[fname] = tmp_list
                # append a new file into the sync
                else:
                    self.local_digest[fname] = ([[mtime, uid]])
                
                # Create a new sync file if sync is not exist or len == 0
                #if not os.path.exists(os.path.join(root, 'digest')) or os.stat(os.path.join(root, 'digest')).st_size == 0:
                #    self.local_digest[fname] = ([[mtime, uid]])
                #    pprint(self.local_digest)
                #else:
                #    # Update exist file in sync
                #    if fname in self.local_digest:
                #        tmp_list = self.local_digest[fname]
                #        # format = {'file name':[[mtime, uid],[mtime, uid]]}
                #        if not self.exists(uid, tmp_list) or not self.exists(mtime, tmp_list):
                #            tmp_list.insert(0,[mtime, uid])
                #            self.local_digest[fname] = tmp_list
                #    # append a new file into the sync
                #    else:
                #        self.local_digest[fname] = ([[mtime, uid]])

        pprint(self.local_digest)
        self.write_digest(root, self.local_digest)
		
    def load_digest(self, root, load_buffer):
		# w+ = overwrite, a+ = append          
        with open(os.path.join(root, 'digest')) as f:                          
            load_buffer = json.load(f)
            f.close() 
        return load_buffer
                   
    def write_digest(self, root, json_obj):
        # w+ = overwrite, a+ = append
        # only if the json_obj is not empty
        if bool(json_obj):
            with open(os.path.join(root, 'digest'), 'w+') as f:
                json.dump(json_obj, f)
                f.close() 

    def exists(self, searching_key, working_list):
        return searching_key in [elem for sublist in working_list for elem in sublist]
        
    def get_records(self):
        if len(self.records) > 1:
            return self.records.sort(key=lambda x: x[1], reverse=True)
        else:
            return self.records
             
    def sha256(self, fname, blocksize = 65536):
        hash = hashlib.sha256()
        with open(fname) as f:
            for chunk in iter(lambda: f.read(blocksize), ""):
                hash.update(chunk.encode('utf-8'))
        return hash.hexdigest()
        
    def md5(self, fname, blocksize = 65536):
        hash = hashlib.md5()
        with open(fname) as f:
            for chunk in iter(lambda: f.read(blocksize), ""):
                hash.update(chunk.encode('utf-8'))
        return hash.hexdigest()
