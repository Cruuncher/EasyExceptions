[![CircleCI](https://circleci.com/gh/Cruuncher/EasyExceptions/tree/master.svg?style=shield)](https://circleci.com/gh/Cruuncher/EasyExceptions/tree/master) 
[![Coverage Status](https://coveralls.io/repos/github/Cruuncher/EasyExceptions/badge.svg?branch=master)](https://coveralls.io/github/Cruuncher/EasyExceptions?branch=master)
[![PyPi](https://img.shields.io/badge/pypi-v1.0.2-blue)](https://pypi.org/project/easy-exceptions/1.0.2/)

# EasyExceptions
Throw and catch named exceptions without creating a class first. The goal of this project is to make working with named exceptions simpler. It's often a huge overhead of work to create named exceptions in a separate file before being able to throw them to nicely be caught. 

## Installation 

    pip install easy-exceptions

## Usage
    from easy_exceptions import EasyException
    try:
        raise EasyException('NamedException')('TEST MESSAGE')
    except EasyException('NamedException') as e:
        print("Caught this specific exception without having to define it!")

EasyExceptions even supports using a custom parent class instead of the base Exception. This is because APIs often use a custom exception class for rendering error messages. All you have to do in this case is pass that parent class to EasyException and instantiate it the way you always would. For example: 

    from easy_exceptions import EasyException 
    from api.exceptions import BaseException # Your custom base exception
    try:
        # you can pass whatever special args here that you usually do to BaseException
        raise EasyException('NamedException', parent=BaseException)(...)
    except EasyException('NamedException', parent=BaseException):
        print("Caught the specific exception!") 
    # This exception can still be caught by referencing the BaseException with regular syntax 
    except BaseException:
        print("This would be called if the above exception handler wasn't there")

This can be further simplified by binding the BaseException during application startup using the bind_parent

    from easy_exceptions import EasyException, bind_parent 
    from api.exceptions import BaseException

    bind_parent(BaseException)
    try:
        raise EasyException('NamedException') 
    except BaseException: #Could alse use EasyException('NamedException') to target the named exception only
        print("Exceptions are always of type BaseException now")
