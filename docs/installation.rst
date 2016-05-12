============
Installation
============

Get OBB for Maya
==================

Using the MEL setup script
---------------------------
- Download the package from the github repo http://github.com/chrisdevito/OBB.git and click Download Zip.
- After extraction, drag and drop the setup.mel (found in the OBB directory) into any open maya window.
- This will install it into your maya/scripts directory and add the OBB Shelf.

Using Pip
----------
::

    $ pip install OBB_Maya

Git
-----
::

    $ git clone https://github.com/chrisdevito/OBB
    $ cd OBB
    $ python setup.py install

Installing the shelf
=====================

After installation through whatever means, just type in the python script editor:

::
	import OBB.shelf


Installing numpy/scipy (**Optional**)
===================================
You do not have to install numpy/scipy to get this to work.
It currently just doesn't allow you to use the from_hull method in the api.

Using Pip
----------
Windows (Maya requires libraries compiled against MSVC2010:
::

    $ pip install -i https://pypi.anaconda.org/carlkl/simple numpy
    $ pip install -i https://pypi.anaconda.org/carlkl/simple scipy

Non-Windows:
::

    $ pip install numpy
    $ pip install scipy
