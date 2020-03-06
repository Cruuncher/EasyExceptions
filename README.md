
# EasyExceptions
Throw and catch named exceptions without creating a class first. The goal of this project is to make working with named exceptions simpler. It's often a huge overhead of work to create named exceptions in a separate file before being able to throw them to nicely be caught. 

## Usage
    from easy_exceptions import EasyException
    try:
        raise EasyException(name='NamedException')('TEST MESSAGE')
    except EasyException(name='NamedException') as e:
        print("Caught this specific exception without having to define it!")

EasyExceptions even supports using a custom parent class instead of the base Exception. This is because APIs often use a custom exception class for rendering error messages. All you have to do in this case is pass that parent class to EasyException and instantiate it the way you always would. For example: 

    from easy_exceptions import EasyException 
    from api.exceptions import BaseException # Your custom base exception
    try:
        # you can pass whatever special args here that you usually do to BaseException
        raise EasyException(name='NamedException', parent=BaseException)(...)
    except EasyException(name='NamedException', parent=BaseException):
        print("Caught the specific exception!") 
    # This exception can still be caught by referencing the BaseException with regular syntax 
    except BaseException:
        print("This would be called if the above exception handler wasn't there")
