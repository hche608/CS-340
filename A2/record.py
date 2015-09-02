#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Created by Hao CHEN
# UPI: 8476927

class record():
    
    def __init__(self, name, time, encode_string):
        self.records = [[time, encode_string]]
        self.name = name        
        
    def peek(self):
        return self.records[0]
    
    def insert(self, time, encode_string):
        self.records.insert(0, encode_string)
        self.records.insert(0, time)
        
    def exists(self, encode_string):
        if encode_string in self.records:
            return true
        return false
        
    def get
    