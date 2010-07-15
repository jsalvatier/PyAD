from __future__ import division
from collections import defaultdict
from utilities.meta import  getcallargs
from utilities.doc import parameter_list
'''
Created on Jul 10, 2010

@author: johnsalvatier

Nodes are nodes of a computation graph which is a directed acyclic graph
the parents of node are specific and named 
a node does not keep track of its children 
computation should be lazy whenever possible
'''



class Node: 
    
    
    name = None 
    parents = None
    
    def __init__(self, name, parents):
        self.name = name
        
        self.parents = {}
        for name, value in parents.iteritems():
            self.parents[name] = as_node(value)
        
    _value = None
    def _set_value(self, value):
        self._value = value 

    def _get_value(self):
        return self._value
    
    value = property(_get_value)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    
    d = None
    
    operator_set = None
    operators = {}
    
    @staticmethod
    def unary_operator(a , operator):
        a = as_node(a)

        return Node.operators[Node.operator_set][operator](a)
    @staticmethod
    def binary_operator(a , operator,b):
        a = as_node(a)
        b = as_node(b)

        return Node.operators[Node.operator_set][operator](a, b)

    def __neg__(self):
        return Node.unary_operator(self, 'neg')
    def __add__(self, other):
        return Node.binary_operator(self,'add', other)
    def __radd__(self,other):
        return Node.binary_operator(other,'add', self)
    
    
    def __sub__(self, other):
        return Node.binary_operator(self,'sub', other)
    def __rsub__(self,other):
        return Node.binary_operator(other,'sub', self)

    def __mul__(self, other):
        return Node.binary_operator(self,'mul', other)   
    def __rmul__(self,other):
        return Node.binary_operator(other,'mul', self)
    
    def __div__(self, other):
        return Node.binary_operator(self,'div', other)
    def __rdiv__(self,other):
        return Node.binary_operator(other,'div', self)
    
    def __pow__(self, other):
        return Node.binary_operator(self,'pow', other)
    def __rpow__(self,other):
        return Node.binary_operator(other,'pow', self)
    


class IndependentNode (Node):
    
    def __init__(self, name, initial_value = None):
        Node.__init__(self, name , {})
        self._set_value(initial_value)

    value = property(Node._get_value, Node._set_value) 
    
    _derivatives = {}
    def _d(self):
        if not self._derivatives:
            self._derivatives = {self.name : UnityNode }
        return self._derivatives
    d = property(_d)
    
    
        
class ConstantNode(Node):
    def __init__(self, name, value):
        Node.__init__(self, name, {})
        
        self._set_value(value)
    
    _derivatives = {}
    def _d(self):
        if not self._derivatives:
            self._derivatives = {self.name : ZeroNode}
        return self._derivatives
    d = property(_d)
        
def as_node(x):
    if isinstance(x, Node):
        return x
    else :
        if x is 0:
            return ZeroNode
        if x is 1:
            return UnityNode
        
        return ConstantNode(str(x), x)

ZeroNode = ConstantNode("0", 0)
UnityNode = ConstantNode("1", 1)
    
        
class DependentNode (Node):
    
    function = None 
    derivative_functions = None
    mapping_function = None
    
    def __init__(self, name, parents, function, derivatives = None, mapping_function = None):
        
        Node.__init__(self, name, parents)
        self.function = function
        self.derivative_functions = derivatives
        self.mapping_function = mapping_function
    
    def _get_value(self):
        self._set_value(self.function(**get_value_dict(self.parents)))
        
        return Node._get_value(self)
    value = property(_get_value)
    
    _derivatives = None
    def _d(self):
        if not self._derivatives: 
            self._derivatives = defaultdict(lambda : ZeroNode)
            for function_parent, parent_node in self.parents.iteritems():
                for independent, parent_derivative_node in parent_node.d.iteritems():

                    derivative_node = self.derivative_functions[function_parent](**self.parents)

                    self._derivatives[independent] += self.mapping_function(derivative_node, parent_derivative_node)
        return self._derivatives
    
    d = property(_d)
    
class InfixNode(DependentNode):
    def __init__(self, a, infix, b,  function, derivatives):
        DependentNode.__init__(self,
                               name = "(" + a.name + ' ' + infix + ' ' + b.name + ")",
                               parents = {'a' : a, 'b' : b},
                               function = function,
                               derivatives = derivatives,
                               mapping_function = transformation_map)
        
class PrefixUnaryNode(DependentNode):
    def __init__(self, a, prefix, function, derivatives):
        DependentNode.__init__(self,
                             name = prefix + ' ' + a.name ,
                             parents = {'a' : a},
                             function = function,
                             derivatives = derivatives,
                             mapping_function = transformation_map)

def transformation_map(da , db):
    return da * db

class FunctionNodeFactory:
    def __init__(self, function_name, function, derivatives, mapping_function):
        self.function_name = function_name 
        self.function = function 
        self.derivatives = derivatives
        self.mapping_function = mapping_function
        
        
    def __call__(self, *args, **kwargs):
        
        parents = getcallargs(self.function, *args, **kwargs)[0]

        return DependentNode(self.function_name+"(" +parameter_list(args,kwargs) +")",
                    parents,
                    self.function,
                    self.derivatives,
                    self.mapping_function)
        

"x = IndependentNode('x', .5)"

    
def get_value_dict(parents):
    value_dict = {}
    for name, parent in parents.iteritems():
        value_dict[name] = parent.value
    return value_dict

