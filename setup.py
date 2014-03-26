#!/usr/bin/env python

from distutils.core import setup

setup(name='adpil',
      version='1.0',
      description='This module provides a link between numpy arrays and PIL, Python Imaging Library, images. Its functions perform image file I/O (in formats supported by PIL) and displaying of images represented as numpy arrays. The layout of these numpy arrays follows the rules of the adimage toolbox images.',
      url='http://adessowiki.fee.unicamp.br/adesso/wiki/main/adpil/view/',
      packages=['adpil']
     )
