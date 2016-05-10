============
Installation
============

Get OBB
========

Using the mel script
---------------------
- Download the package from the github repo http://github.com/chrisdevito/OBB.git and click Download Zip.
- After extraction, drag and drop the setup.mel script into any open maya window.
- This will install it into your maya/scripts directory and add a shelf button to your current shelf.

Pip not on Windows
------------------
::

    $ pip install OBB_Maya

Pip on Windows
---------------
::
	// We need to install these versions of numpy/scipy for it work against Maya in Windows!
    $ pip install -i https://pypi.anaconda.org/carlkl/simple numpy
    $ pip install -i https://pypi.anaconda.org/carlkl/simple scipy
    $ pip install OBB_Maya

Git not on Windows
--------------------
::

    $ git clone https://github.com/chrisdevito/OBB
    $ cd OBB
    $ python setup.py install

Git on Windows
---------------
::

    $ git clone https://github.com/chrisdevito/OBB
    $ cd OBB
    $ python setup.py install
