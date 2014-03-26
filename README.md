# adpil

This is a simple python package containing only the adpil module from pymorph.

## Original authors
Copyright 2003, Roberto A. Lotufo, UNICAMP-University of Campinas; CenPRA-Renato Archer Research Center, Rubens C. Machado.

`adpil.py` was downloaded from [adessowiki](http://adessowiki.fee.unicamp.br/adesso/wiki/main/adpil/view/)

## Introduction

The adpil module provides a link between numpy arrays and Python Imaging Library (PIL) images. Its functions perform image file I/O (in formats supported by PIL) and displaying of images represented as numpy arrays. The layout of these numpy arrays follows the rules of the mmorph toolbox images.

The module is part of the "SDC Morphology Toolbox for Python" and is imported by the Adessowiki execution sandbox. In the Adessowiki execution context, some functions of the adpil module are overriden in order to operate in the web environment.

## Install

Download and run:

    python setup.py install

## Usage

    from adpil import *
