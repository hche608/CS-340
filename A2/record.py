#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import os
import json
import hashlib
import time

class Record():
    
    def __init__(self, root, fname):
        ctime = time.strftime("%Y-%m-%d %H:%M:%S %z",time.localtime(os.path.getctime(os.path.join(root, fname))))
        #self.records = [[time.ctime(os.path.getctime(os.path.join(root, fname))), self.sha256(os.path.join(root, fname))]]      
        self.records = [[ctime, self.sha256(os.path.join(root, fname))]] 
        
    def peek(self):
        return self.records[0]
    
    def insert(self, root, fname):
        self.records.insert(0, [time.mtime(os.path.getmtime(os.path.join(root, fname))), self.sha256(os.path.join(root, fname))])

    def exists(self, searching_key):
        return searching_key in [elem for sublist in self.records for elem in sublist]
        
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
