generated_exceptions = {}

def EasyException(name=None, parent=None):
    if not name:
        return Exception

    if not parent:
        parent = Exception
        
    exc_class = generated_exceptions.get((name, parent.__name__))
    if exc_class:
        return exc_class 
    else:
        exec("class {}(parent):\n    pass".format(name)) 
        generated_exceptions[(name, parent.__name__)] = locals()[name]
        return generated_exceptions[(name, parent.__name__)]
