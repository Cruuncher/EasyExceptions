import sys
import os
sys.path.append(os.path.abspath("."))

from easy_exceptions import EasyException 

class ParentException(Exception):
    def test(self):
        return 'TEST'

class OtherParentException(Exception):
    def test(self):
        return 'FAIL'

def test_typical():
    try: 
        raise EasyException(name='NamedException') 
    except EasyException(name='NamedException'):
        assert True 
    except:
        assert False

def test_exception_message_persists():
    try:
        raise EasyException(name='NamedException')('TEST MESSAGE') 
    except EasyException(name='NamedException') as e:
        assert str(e) == 'TEST MESSAGE'

def test_other_named_exception():
    try:
        raise EasyException(name='OtherException') 
    except EasyException(name='NamedException'):
        assert False 
    except EasyException(name='OtherException'):
        assert True 
    except:
        assert False 

def test_parent_exception_differentiated():
    try:
        raise EasyException(name='NamedException', parent=ParentException) 
    except EasyException(name='NamedException'):
        assert False 
    except EasyException(name='NamedException', parent=OtherParentException):
        assert False 
    except EasyException(name='OtherException'):
        assert False 
    except EasyException(name='OtherException', parent=OtherParentException):
        assert False 
    except EasyException(name='OtherException', parent=ParentException):
        assert False 
    except EasyException(name='NamedException', parent=ParentException) as e:
        assert e.test() == 'TEST'
    except:
        assert False

def test_catch_using_parent_exception():
    try:
        raise EasyException(name='NamedException', parent=ParentException) 
    except ParentException as e:
        assert e.test() == 'TEST'
    except:
        assert False

def test_proper_referential_integrity_of_exception_parents():
    class NewException(Exception):
        pass 
    first_definition = NewException 

    class NewException(Exception):
        pass 
    second_definition = NewException 
    assert first_definition != second_definition

    # The following try block is to demonstrate that python sees the two definitions of NewException differently 
    # When assessing what the type of the exception is. 
    try:
        raise first_definition 
    except second_definition:
        assert False 
    except first_definition:
        assert True 
    except:
        assert False

    # TODO: This test currently passes, but represents a bug. If an exception class is redefined elsewhere with the same name
    # as a parent used for another exception, these parent classes will not be differentiated. Need a way of nailing down 
    # what makes a parent class actually unique.
    # This issue is considered fixed once the following assertion fails (at which time it should be swapped to an !=)
    # Also, this is a potentially breaking change and should be associated with a major version bump
    assert EasyException(name='Test', parent=first_definition) == EasyException(name='Test', parent=second_definition)
