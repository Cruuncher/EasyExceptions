generated_exceptions = {}
bound_parent = Exception

def reset_module():
    global generated_exceptions, bound_parent 
    generated_exceptions = {} 
    bound_parent = Exception

def bind_parent(parent):
    global bound_parent
    bound_parent = parent

def EasyException(name=None, parent=None):
    if not name:
        return Exception

    if not name.isalnum():
        raise ValueError("Exception name {} is not alphanueric".format(name))

    if not parent:
        parent = bound_parent
        
    exc_class = generated_exceptions.get((name, parent))
    if exc_class:
        return exc_class 
    else:
        exec("class {}(parent):\n    pass".format(name)) 
        generated_exceptions[(name, parent)] = locals()[name]
        return generated_exceptions[(name, parent)]
