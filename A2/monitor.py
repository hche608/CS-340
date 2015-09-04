#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import os
import json
import time
import hashlib
from pprint import pprint

class Monitor():
    
    def __init__(self, root, files, sync, verbose = False):
        self.verbose = verbose
        self.sync = sync
        # load digest if it exists and it has data
        self.local_digest = self.load_digest(root)
        for fname in files:
            # Skip hide files
            if not fname.startswith('.') and not fname.endswith('~') and not fname == self.sync:
                mtime = time.strftime('%Y-%m-%d %H:%M:%S %z',time.localtime(os.path.getmtime(os.path.join(root, fname))))
                # mtime = time.ctime(os.path.getmtime(os.path.join(root, fname)))
                uid = self.sha256(os.path.join(root, fname))
                # Update exist file in sync
                if self.local_digest and fname in self.local_digest:
                    tmp_list = self.local_digest[fname]
                    # format = {'file name':[[mtime, uid],[mtime, uid]]}
                    if not uid == tmp_list[0][1] or not mtime == tmp_list[0][0]:
                    # if not self.exists(uid, tmp_list) or not self.exists(mtime, tmp_list):
                        tmp_list.insert(0, [mtime, uid])
                        self.local_digest[fname] = tmp_list
                # append a new file into the sync
                else:
                    # format = {'file name':[[mtime, uid]]}
                    self.local_digest[fname] = ([[mtime, uid]])
        if (self.local_digest):
            self.check_deletion(files)
        self.write_digest(root, self.local_digest, verbose)      
    
    def check_deletion(self, files):        
        for key in self.local_digest.keys():
            if not key in files and not self.local_digest[key][0][1] == 'deleted':
                mtime = time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime(time.time()))
                #mtime = time.strftime('%Y-%m-%d %H:%M:%S %z', time.gmtime())
                print('Deletion: %s' % key)
                tmp_list = self.local_digest[key]
                tmp_list.insert(0, [mtime, 'deleted'])
                self.local_digest[key] = tmp_list    	
    
    def load_digest(self, root):
		# w+ = overwrite, a+ = append
        load_buffer = dict()
        if os.path.exists(os.path.join(root, self.sync)) and os.stat(os.path.join(root, self.sync)).st_size > 0:
            with open(os.path.join(root, self.sync)) as f:

                load_buffer = json.load(f)
        return load_buffer

    def write_digest(self, root, json_obj, verbose = False):
        # w+ = overwrite, a+ = append
        # load or create a sync file
        if verbose:
            pprint(json_obj)
        with open(os.path.join(root, self.sync), 'w+') as f:
            json.dump(json_obj, f, indent=4)
    
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
