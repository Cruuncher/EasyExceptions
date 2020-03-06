from distutils.core import setup
import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

# read the contents of your README file
from os import path
import setuptools

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'easy_exceptions',
  packages = ['easy_exceptions'],
  version = '1.0.2',
  license='MIT',
  description = 'Throw and catch named exceptions without creating a class first',
  long_description_content_type='text/markdown',
  long_description=long_description,
  author = 'Patrick Robertshaw',
  author_email = 'patrick.robertshaw1@gmail.com',
  url = 'https://github.com/Cruuncher/EasyExceptions',
  download_url = 'https://github.com/Cruuncher/EasyExceptions/archive/1.0.2.tar.gz',
  keywords = ['exceptions'],  
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',   
  ],
)
