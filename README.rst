Producrs.ZopeScanner
====================

ZopeScanner is a tool that provides valuable assistance with maintenance,
troubleshooting, development, research and much more. It allows users to take a
detailed look inside all parts of the Zope server via an easy to use web
interface.


WARNING
-------

The software poses certain risks, as it allows access to otherwise hidden parts
of the server. For this reason, great care is taken to ensure that it can only
ever perform read-only access. Access is also restricted to the "Manager" role,
i.e. the main administrator of the Zope server. ZopeScanner reports the
administrator’s existence in the Zope server's log file.

ZopeScanner circumvents Zope security mechanisms and allows access to protected
objects as well as to files on the server's file system. Therefore, as a
general rule:

**ONLY INSTALL THIS PRODUCT WHEN NEEDED AND REMOVE AFTERWARDS**

It is intended for use within a development environment for debugging and
analysis purpose only!


Audience
--------

ZopeScanner is a tool for development, administration, forensics,
troubleshooting, research and much more, which provides insights into the inner
workings of the Zope server. It is extremely easy to use. Various entry points
are provided, such as the directory tree or the server configuration. Links on
these web forms allow you to access deeper-level objects. Each object is
analysed in detail and the results presented in a structured manner.


Installation
------------

ZopeScanner is released as a Product – a standard extension for Zope – and
installs itself automatically into the Control Panel. It can also be removed
without leaving any traces. For security reasons, ZopeScanner logs its presence
in the log file. Furthermore, all access is explicitly restricted to the
"Manager" role – the main administrator of the Zope server – and cannot be
modified.

The ZopeScanner is designed to work seamlessly with all versions of Zope and
Python. Where possible, newer features are incorporated, whilst traditional
programming techniques ensure that the programme remains reliably available for
all versions. The original compatibility with very early versions of Zope
running on Python 1.5.2 on 32-bit operating systems is currently being
reviewed. ZopeScanner only depends one the standard Python library and Zope
components.

TLDR: To install ZopeScanner, unpack the archive into the Zope instance's
Products directory and restart the server. ZopeScanner will install itself into
Zope's Control Panel at startup. To deinstall, remove the ZopeScanner directory
from the Product directory.


Usage
-----

The ZopeScanner provides six different entry points from which users can
descend deeper into the details of the Zope server. These six entry points are
"System", "Products", "Objects", "Modules", "Sources", and "Log Files".


System
^^^^^^

System information encompasses all global settings of Zope, Python, the OS
(operating system), and the host machine itself.


Products
^^^^^^^^

Product software packages are plugins, that may register Base Classes, which
can be added through Zope's OFS in the object database (ZODB). This includes
basic content types, such as Folders and Documents (web pages), functional
types, such as user portals, as well as custom built applications.


Objects
^^^^^^^

The object scanner provides comprehensive reports on any object, identified by
path. It recognizes OFS object and extends the report with respective
information. It starts at the root of Zope's OFS directory tree, allowing users
to browse the OFS objects stored within.


Modules
^^^^^^^

Directory for all imported modules, including the Python standard library, the
Zope server, and any other installed package. Packages may consist of a single
module or contain any number of sub-modules.


Sources
^^^^^^^

Web based file browser of the Zope server and the Python programming language.
Access to files outside these root paths is impossible. File display adapts to
the file type.


Log Files
^^^^^^^^^

The Log File Scanner detects all log files managed by Zope and allows them to
be displayed in real time. ZopeScanner supports all versions of the modules
used, Python’s logging and Zope’s zLOG.


Copyright
---------

Copyright (c) 2009 - 2026, Sebastian Lühnsdorf.

This software is not based on or uses parts of a release by a third party.


License
-------

This product is published under the Zope Public License 2.1 (ZPL). A copy of the license can be found in the Product's directory.


More Information
----------------

Please visit `www.zope.love`_ and `www.github.com`_ for for more and current information.

.. _www.zope.love: https://www.zope.love/zopescanner
.. _www.github.com: https://github.com/sfluehnsdorf/ZopeScanner
