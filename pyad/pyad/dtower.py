'''
Created on Jul 12, 2010

@author: johnsalvatier
'''

import numpy
    
class LinearMap:
    
    _function = None 
    
    def __init__(self, function):
        self._function = function
    
    def __add__(self, other):
        return LinearMap(lambda a: self.map(a) + other.map(a))
    
    def __neg__(self):
        return LinearMap(lambda a: -self.map(a))
        
    def map(self, a ):
        return self.function(a)
    
ZeroVector = LinearMap(lambda a: 0)

class DTower: 
    
    _value = None
    value = property (lambda self : self._value) 
    
    _lmap = None 
    lmap = property(lambda self : self._lmap)
    
    
    def __init__(self, value, lmap):
        self._value = value 
        self._lmap= lmap
       
    def __add__(self, other):
        return DTower(self.value + other.value, self.lmap + other.lmap) 
    
    def __mul__(self, other):
        return DTower(self.value * other.value,
                      
                      lambda da : self.lmap(da) + other.lmap(da))
        
    
        
def dConst(value):
    return DTower(value, dZero)
        
def dZero():
    return dConst(ZeroVector())
        
def LinearD(function, value):
    return DTower(function(value), lambda du: dConst(function(du))  )

def Id(value):
    return LinearD(lambda x: x, value)


class dfunction:
    _function = None 
    _lmap = None 
    
    def __init__(self, function):
        self._function = function 
        
    def __call__(self, a):
        return DTower(self._function(a.value), self._lmap)
    
    def set_lmap(self, df2):
        self._lmap = LinearMap (lambda da : f2(u) * u.lmap(da))
    

exp = dfunction(numpy.exp)
exp.set_lmap(exp)


