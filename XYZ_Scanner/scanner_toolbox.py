#! /usr/bin/env python
# -*- coding: utf-8 -*-

#####################################
#                                   #
# Dev: Mickael Rigault              #
# (mrigault@physik.hu0-berlin.de)   #
#
# = Computing and Math tools        #
#
#####################################
import numpy as N

def kwargs_update(default,**kwargs):
    """
    """
    k = default.copy()
    for key,val in kwargs.iteritems():
        k[key] = val
        
    return k

def Make_Me_Iterable(A):
    """
    """
    if hasattr(A, '__iter__'):
        return A
    return [A]

def relativepercent_to_value(percent,object_range):
    """
    (N.max(object_range) - N.min(object_range)) * percent / 100. + N.min(object_range)
    """
    return (N.max(object_range) - N.min(object_range)) * percent / 100. + N.min(object_range)
            
def value_in_micron(value,unit):
    """
    """
    known_units = N.asarray(["m","cm","dm","mm","mim"])
    if unit not in known_units:
        raise ValueError("The given unit is not known %s"%unit)
    
    if unit == "m":
        return value * 1e6
    if unit == "dm":
        return value * 1e5
    if unit == "cm":
        return value * 1e4
    if unit == "mm":
        return value * 1e3
    if unit == "mim":
        return value * 1
    
