Contributor's guide
===================

Abstract
--------

If you're reading this README it means you're potentially interested
to contribute to orchester.io, so this README will really start with
these two words: Thank you ! 

This file describe the contribution guidelines (a.k.a. how to write
code for orchester). It explains all you need to contribute efficiently.

This README will cover:

- coding guidelines
- orchester code organization
- bug reporting
- how to write tests
- how to write documentation


Coding guidelines
-----------------

To be defined.


Orchester code organization
---------------------------

Plugins
```````

In order to not package all available plugins in one big package and to
allow other to write plugins easily, we separated the plugins from the
main codebase. 

It means all plugins must retain in separate repositories and PyPI
packages. We defined the plugins namespaces this way:

- orchester.node.plugins is the namespace to put your generic plugins.
- orchester.node.lb.plugins is the namespace to put your plugins that
  does not work for both instances and LB.
- orchester.node.instance.plugins is the namespaces to your instance
  related plugins.

For instance you may want to have a Docker plugin which is reusable for
both instances and LB, you then shoud put your code in
`orchester.node.plugins.docker` and then subclass this plugin in
`orchester.node.instance.plugins` and `orchester.node.lb.plugins`.


API
```

Orchester.io makes use of different API between the different parts, the
code is organized this way:

- common utilities go in the orchester.api module
- other API related code go to the convenient module


Tests
`````

To be defined.


Bug reporting
-------------

When reporting a bug, please consider the following points:


Global infos report
```````````````````

Always report versions of the software used, including:

- master version
- node version
- plugins used and their versions


Use case (a.k.a. how to reproduce)
``````````````````````````````````

Detail the cause of the crash as much as possible, include a traceback
will help !

A bug report saying "master crashed when IPv6 is used" is much more
interesting that "Does not work for me. lol."


Bonus 1: A test that reproduce the bug
``````````````````````````````````````

If you can, submitting a pull-request with a tet that reproduce the bug
will help us *a lot*.


Bonus 2: A pull-request that fix the bug
````````````````````````````````````````

If you can address it, feel free to submit a pull-request fixing the bug.
