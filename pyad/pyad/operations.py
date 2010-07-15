'''
Created on Jul 10, 2010

@author: johnsalvatier
'''
from Node import *
from utilities.meta import find_element, bind_method, find_operator_method, getcallargs
from utilities.doc import parameter_list
import numpy


generic = ['abs', 'exp', 'log', 'sqrt','expm1', 'log1p']
trig = ['sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan']
hyp_trig = ['sinh', 'cosh', 'tanh', 'arcsinh', 'arccosh', 'arctanh']
transformation_deterministics = generic + trig + hyp_trig

__all__ = transformation_deterministics


#def bind_factory_to_unary_operation(op_name, klass, derivatives = None):
#    """
#    Creates a new univariate special method, such as A.__neg__() <=> -A,
#    for target class. The method is called __op_name__.
#    """
#
#    op_function_base = find_operator_method(op_name)
#    #many such functions do not take keyword arguments, so we need to wrap them 
#    def op_function(self):
#        return op_function_base(self)
#        
#    
#    def operator_method(self):
#        return DependentNode(op_function + ' ' + self.name,
#                    parents = {'self':self},
#                    derivatives = derivatives)
#    
#    bind_method(klass,op_name, operator_method)
  
 
#def bind_factory_to_rlbinary_operation(op_name, klass, derivatives = None):
#    """
#    Creates a new univariate special method, such as A.__neg__() <=> -A,
#    for target class. The method is called __op_name__.
#    """
#
#    op_function_base = find_operator_method(op_name)
#    #many such functions do not take keyword arguments, so we need to wrap them 
#    def op_function(a, b):
#        return op_function_base(a, b)   
#    
#    for prefix in ['r','']:
#        
#        def operator_method(self, other):
#            other = as_node(other)
#            
#            if prefix == 'r':
#                parents = {'a':other, 'b':self}
#            else:
#                parents = {'a':self, 'b':other}
#            
#            
#            name = "(" + parents['a'].name + ' ' + op_name + ' ' + parents['b'].name + ")" 
#            return DependentNode(name,
#                        parents = parents,
#                        function = op_function,
#                        derivatives = derivatives)
#    
#        bind_method(klass,op_name, operator_method)
#
#
#
#
#
#
#for op in ['neg','pos','abs','invert','index']:
#    bind_factory_to_unary_operation(op, Node, derivatives = find_element([op+"_derivatives"],[locals()])  )
#    
#for op in ['div', 'truediv','pow']:
#    bind_factory_to_rlbinary_operation(op, Node, derivatives=  find_element([op+"_derivatives"],[locals()])  )
#
#for op in ['add', 'mul', 'sub']:
#    bind_factory_to_rlbinary_operation(op, Node, derivatives=  find_element([op+"_derivatives"],[locals()])  )


def neg(self):
    if self is ZeroNode: return ZeroNode
    
    return PrefixUnaryNode(self, '-',
                           function =           lambda a : -a,
                           derivatives = {'a' : lambda a : -1 })

def add(self, other):
        if self  is ZeroNode: return other
        if other is ZeroNode: return self
        
        return InfixNode(self, '+', other,
                         function =           lambda a, b: a + b,
                         derivatives = {'a' : lambda a, b: 1,
                                        'b' : lambda a, b: 1})

def sub(self, other):
    if self  is ZeroNode: return -other
    if other is ZeroNode: return self
    
    return InfixNode(self, '-', other,
                     function =           lambda a, b: a - b,
                     derivatives = {'a' : lambda a, b: 1,
                                    'b' : lambda a, b: -1})

def mul(self, other):
    if self  is UnityNode: return other
    if other is UnityNode: return self
    
    if self is ZeroNode or other is ZeroNode: return ZeroNode

    return InfixNode(self, '*', other,
                     function =           lambda a, b: a * b,
                     derivatives = {'a' : lambda a, b: b,
                                    'b' : lambda a, b: a})

def div(self, other):
    if self  is ZeroNode : return ZeroNode
    if other is UnityNode: return self
    
    if other is ZeroNode: raise ZeroDivisionError("division by ZeroNode")
    
    return InfixNode(self, '/', other,
                     function =           lambda a, b: a / b,
                     derivatives = {'a' : lambda a, b: 1 / b,
                                    'b' : lambda a, b:-a / b**2  })
    
def pow(self, other):
    if self  is ZeroNode : return ZeroNode
    if other is UnityNode: return self
    
    if other is ZeroNode: raise ZeroDivisionError("division by ZeroNode")
    
    return InfixNode(self, '**', other,
                     function =           lambda a, b: a ** b,
                     derivatives ={'a' : lambda a, b: b * a**(b - 1),
                                   'b' : lambda a, b: log(a) * a**b   } )
    
numpy_operators = {'neg' : neg,
                   'add' : add,
                   'sub' : sub,
                   'mul' : mul,
                   'div' : div,
                   'pow' : pow}

Node.operators['numpy'] = numpy_operators
Node.operator_set = 'numpy'
        
    
abs_jacobians = {'x' : lambda x : sign(x) }
exp_jacobians = {'x' : lambda x : exp(x)  }
log_jacobians = {'x' : lambda x : 1.0/x      }
sqrt_jacobians = {'x': lambda x : .5    * x **-.5}
hypot_jacobians = {'x1' : lambda x1, x2 : (x1**2 + x2**2)**-.5 * x1,
                   'x2' : lambda x1, x2 : (x1**2 + x2**2)**-.5 * x2}
expm1_jacobians = exp_jacobians
log1p_jacobians = {'x' : lambda x : 1.0/(1.0 + x)}

sin_jacobians = {'x' : lambda x :  cos(x)  }
cos_jacobians = {'x' : lambda x : -sin(x) }
tan_jacobians = {'x' : lambda x : 1 + np.tan(x)**2}

arcsin_jacobians = {'x' : lambda x :  (1.0-x**2)**-.5}
arccos_jacobians = {'x' : lambda x : -(1.0-x**2)**-.5}
arctan_jacobians = {'x' : lambda x :  1.0/(1.0+x**2) }

arctan2_jacobians = {'x1' : lambda x1, x2 :  x2/ (x2**2 + x1**2),
                     'x2' : lambda x1, x2 : -x1/ (x2**2 + x1**2)}
# found in www.math.smith.edu/phyllo/Assets/pdf/findcenter.pdf p21

sinh_jacobians = {'x' : lambda x : cosh(x)}
cosh_jacobians = {'x' : lambda x : sinh(x)}
tanh_jacobians = {'x' : lambda x : 1.0 - tanh(x)**2}

arcsinh_jacobians = {'x' : lambda x : (1+x**2)**-.5}
arccosh_jacobians = {'x' : lambda x : (x+1)**-.5*(x-1.0)**-.5}
arctanh_jacobians = {'x' : lambda x : 1.0/(1-x**2) }

def wrap(func):
    def wrapped(x):
        return func(x)
    wrapped.__name__ = func.__name__
    return wrapped

for function_name in transformation_deterministics:
    func = find_element(function_name, numpy, error_on_fail = True)
    
    
    
    jacobians = find_element(function_name + "_jacobians", locals(), error_on_fail = True)
    
    locals()[function_name] = FunctionNodeFactory(function_name, 
                                                  wrap(func), 
                                                  jacobians,
                                                  transformation_map)