#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

import os
import json
import record
from pprint import pprint

class Load():
    
    def __init__(self, root, fname):
        # w+ = overwrite, a+ = append          
        with open(os.path.join(root, 'digest')) as f:           
            #data = []
            #for line in f:
            #    data.append(json.loads(line))                
            load_buffer = json.load(f)
            f.close() 
            pprint('Buffer: %s' % load_buffer['file1_1.txt'][0][1])
if __name__ == '__main__':
    Load(os.getcwd(),'testOutput.txt')
