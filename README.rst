Orchester.io
============

Abstract
--------

Orchester.io is a cloud solution providing these main functionalities:

- VM / Bare metal provisionning
- Web apps hosting
- One-time code execution

Actually under heavy developpement.


Installation
------------

I recommend installing a virtualenv, especially for developpement, this
is however not mandatory::

    pip install virtualenv
    virtualenv /my/venv/path
    source /my/venv/path/bin/activate

Then just install the packages by running this command::

    python setup.py install

Or if you want your system to use symlinks to your repo instead
(wich is useful for developpement)::

    python setup.py develop

You also need to have mongodb installed and running on your localhost.


Usage
-----

You can run the tests with::

    python setup.py test

And you can run the master with::

    ./bin/orchester-master.py

And the node with::

    ./bin/orchester-node.py

