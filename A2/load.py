#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import os
import json
import record
from pprint import pprint

class Load():
    
    def __init__(self, fpath, fname):
        with open(os.path.join(fpath, 'digest')) as data_file:    
            data = json.load(data_file)
            data_file.close()
        pprint(data)     
        if fname in data:
            print(data['testOutput.txt'][0][0])  
        
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
if __name__ == '__main__':
    Load(os.getcwd(),'testOutput.txt')
