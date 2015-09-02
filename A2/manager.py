#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import os
import json
import record
from pprint import pprint

class FileManager():
    
    def __init__(self, fpath):
        # w+ = overwrite, a+ = append     
        with open(os.path.join(fpath, 'digest'),'w+') as f:    
            data = json.load(f)
            f.close()
        #pprint(data) 
    
    def maintain(self, fpath, fname):
        if fname in self.data:
            print(data['testOutput.txt'][0][0])
        else:
            new_record = record.Record(name, time.ctime(os.path.getctime(os.path.join(root, name))), sha256(os.path.join(root, name)))
            new_record.digest(root, name)
    
        
    def peek(self):
        return self.records[0]
    
    def insert(self, mtime, uid):
        self.records.insert(0, [mtime, uid])
        
    def exists(self, encode_string):
        if encode_string in self.records:
            return true
        return false
        
    def digest(self, fpath, fname):
        json_obj = dict()
        json_obj[fname] = self.records
        # w+ = overwrite, a+ = append
        name = '%s.json' % fname
        with open(os.path.join(fpath, name), 'w+') as f:
            json.dump(json_obj, f)
            f.close() 
            
    def sha256(fname, blocksize = 65536):
        hash = hashlib.sha256()
        with open(fname) as f:
            for chunk in iter(lambda: f.read(blocksize), ""):
                hash.update(chunk.encode('utf-8'))
        return hash.hexdigest()
