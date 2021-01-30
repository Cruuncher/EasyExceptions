import threading
from time import sleep

generated_exceptions = {}
bound_parent = Exception
update_mutex = threading.Lock()
TEST_PARALELLISM = False

def reset_module():
    # !!!! This function is intended for testing purposes. Using this in production code breaks 
    # thread safety guarantees
    global generated_exceptions, bound_parent, update_mutex
    generated_exceptions = {} 
    bound_parent = Exception
    update_mutex = threading.Lock()

def bind_parent(parent):
    global bound_parent
    acquired = update_mutex.acquire() 
    if not acquired:
        raise Exception("Lock acquire while binding parent failed")
    try: 
        bound_parent = parent
    finally:
        update_mutex.release()
    

def EasyException(name=None, parent=None):
    if not name:
        return Exception

    if not name.isalnum():
        raise ValueError("Exception name {} is not alphanumeric".format(name))

    # perform a check outside of a lock to allow full parallelism when exceptions have already been created
    exc_class = generated_exceptions.get((name, parent))
    if exc_class:
        return exc_class

    acquired = update_mutex.acquire()
    if not acquired:
        raise Exception("Lock acquire while generating exception failed")
    try:
        if not parent:
            parent = bound_parent
            
        # Now that we have a lock and are planning on creating a new exception, we have to recheck
        # if an exception has been generated since our last pull.
        exc_class = generated_exceptions.get((name, parent))

        if TEST_PARALELLISM:
            sleep(0.125) # this sleeps allows us to force a race condition to test the locking mechanism

        if exc_class:
            return exc_class 
        else:
            exec("class {}(parent):\n    pass".format(name)) 
            generated_exceptions[(name, parent)] = locals()[name]
            return generated_exceptions[(name, parent)]
    finally:
        update_mutex.release()