'''
Created on Jul 13, 2010

@author: johnsalvatier
'''
def parameter_list(args, kwargs):
    l = []
    for arg in args:
        l.append(str(arg))
        l.append(',')
    
    for parameter, arg in kwargs.iteritems():
        l.append(parameter + '=' + str(arg) )
        l.append(',')
    l.pop()
    return "".join(l)