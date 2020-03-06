import sys
import os
import pytest
sys.path.append(os.path.abspath("."))

from easy_exceptions import EasyException, bind_parent
from easy_exceptions.easy_exceptions import reset_module

@pytest.fixture(autouse=True) 
def reset_exception_module():
    reset_module()

def test_typical():
    try: 
        raise EasyException(name='NamedException') 
    except EasyException(name='NamedException'):
        assert True 
    except:
        assert False

def test_raise_with_name_as_arg():
    try:
        raise EasyException('NamedException') 
    except EasyException('NamedException'):
        assert True 
    except:
        assert False

def test_reject_nonalphanum_exception_name():
    try:
        EasyException("Test!Symbol") 
        assert False 
    except ValueError:
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
    class ParentException(Exception):
        def test(self):
            return 'TEST'

    class OtherParentException(Exception):
        def test(self):
            return 'FAIL'

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
    class ParentException(Exception):
        def test(self):
            return 'TEST'

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

    #assert that using different definitions yields different EasyExceptions
    assert EasyException(name='Test', parent=first_definition) != EasyException(name='Test', parent=second_definition)

    assert EasyException(name='Test', parent=first_definition) == EasyException(name='Test', parent=first_definition)
    assert EasyException(name='Test', parent=second_definition) == EasyException(name='Test', parent=second_definition)

def test_bind_parent():
    class ParentException(Exception):
        def test(self):
            return 'TEST'

    bind_parent(ParentException)

    try:
        raise EasyException('NamedException') 
    except ParentException:
        assert True 
    except:
        assert False

    try:
        raise EasyException('NamedException') 
    except EasyException('NamedException'):
        assert True 
    except:
        assert False

    try:
        raise EasyException('NamedException', parent=Exception)
    except EasyException('NamedException'):
        assert False 
    except EasyException('NamedException', parent=Exception):
        assert True 
    except:
        assert False

def test_nameless_exception():
    assert EasyException() == Exception
