#!/usr/bin/python3
# -*- coding: utf-8 -*-

from functools import wraps
import time

from prometheus_client import Gauge

@wraps
def time_elapsed(funcs):
    '''
    time_elapsed is a decorator that calculates the time elapsed for a function to run
    '''
    def wrapper(*args, **kwargs):
        start = time.time()
        result = funcs(*args, **kwargs)
        end = time.time()
        print(f"Time elapsed | {funcs.__name__}| {end - start} seconds")
        return result
    
    return wrapper


acc_simplemodel = Gauge("acc_simplemodel", "Simple Model Accuracy")

def record_acc_simplemodel(accuracy):
    acc_simplemodel.set(accuracy)


