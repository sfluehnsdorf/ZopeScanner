ZopeScanner

  The ZopeScanner is an introspective tool for developers and administrators of
  Zope2 servers. It allows users to analyze attributes and methods of Zope
  objects, browse the source code or read the log files. It installs itself into
  Zope's Control Panel and uninstalls itself completely without any traces.

  WARNING

    This Product may be considered a high security risk as it circumvents Zope
    security mechanisms and allows access to protected objects as well as to
    files on the server's file system. As a general rule:

    NEVER INSTALL THIS PRODUCT ON A PUBLICALLY ACCESSIBLE ZOPE SERVER!

    It is intended for use within a development environment for debugging and
    analysis purpose only!

  Audience

    The ZopeScanner is primarily intended for developers and administrators. It
    can be used to debug, analyze, inspect or research the Zope server's
    architechture, components and extensions.

  Features

    The ZopeScanner's management interface provides seven screens with different
    displays of the Zope server's internals. These are "Config", "Servers",
    "Products", "Objects", "Modules", "Sources" and "Log Files". Further
    information about these screens can be found in the *Usage* section below.

    All values and attributes displayed are formatted for human readability.

  Installation

    To install ZopeScanner, unpack the archive into the Zope instance's Products
    directory, activate the Zope server's debug mode in the configuration file
    (etc/zope.conf) and restart the server. ZopeScanner will install itself into
    Zope's Control Panel at startup.

    NOTE: ZopeScanner will not run unless the debug mode is activated, even if
    properly installed. The idea behind this is to prevent an accidentally
    installed ZopeScanner on a production server to allow access to the Zope
    server's internals.

  Deinstallation

    Either deactivate the debug mode or remove the ZopeScanner directory from
    the Product directory.

  Usage

    The ZopeScanner provides seven different introspective views in the Zope
    server's management interface. Below is a description for each of these
    screens.

    Config

      Here you can browse the attributes (key, value) contained in Zope's
      configuration object.

      Links are provided to views of objects of all types, providing further
      information (see *Objects* screen below).

    Servers

      List of all active servers gathered from asyncore's socket_map. Each
      server is listed with file number, server type, hostname, ip address,
      port and class. 

      Links are provided to views of objects of all types, providing further
      information (see *Objects* screen below).

    Products

      This screen displays two lists. The first is the list of all disk based
      Products and their respective Base Classes. The second is an alphabetical
      list of all the Base Classes.

      By clicking on the linked name of a Base Classe in the first list you
      reach the respective entry in the second list. Each entry in the second
      list contains the Base Class' registration information.

      Links are provided to views of objects of all types, providing further
      information (see *Objects* screen below).

    Objects

      The Object scanner displays extensive information for a specific object
      of arbitrary type. The scanner defaults to a scan of the Zope server's
      PhysicalRoot object. This screen contains several sub sections:

      Path Info

        A breadcrumb trail starting with the respective root. When linked to
        from another scanner, the root object may differ from the Zope
        server's PhysicalRoot object.

      Object Info

        Standard Python and Zope attributes of the scanned object including
        its representation, type, module, Zope Id, title property, absolute
        URL and more.

      Sub Objects

        Sub objects contained within the scanned object for Zope Folders.

      Management Options

        The object's ZMI management options mapping object.

      Properties

        The object's properties.

      Permissions

        Alphabetical list of permissions associated with the object and the
        list of mapped roles.

        See Roles section below.

      Roles

        Alphabetical list of roles associated with the object and the list of
        mapped permissions.

        See Permissions section above.

      Ownership

        Ownership information of the object.

      Undoable Transactions

        List of undoable transactions of the object.

      Historic Revisions

        List of historical revisions of the object.

      Form & Image Objects

        List of attributes of the object of the type DTMLFile, HTMLFile, HTML,
        MessageDialog and ImageFile. 

      Callable Objects (Functions, Methods, etc.)

        List of callable attributes of the object. 

      Sequence Items

        List of items when the object is accessed as a sequence object.

      Mapping Items

        List of items when the object is accessed as a mapping object.

      Attributes (__dict__)

        List of object attributes found in the __dict__ mapping.

      Attributes (dir)

        List of object attributes identified by the dir function.

    Modules

      List of all modules found in the modules mapping of Python's sys module.
      This list includes both Zope specific and generic Python modules.

      Links are provided to views of objects of all types, providing further
      information (see *Objects* section above).

    Sources

      The source file scanner is a file system browser for Zope related source
      repositories. Files are displayed either in plain text, as images or
      hexdumps. The following directories are available:

      Instance

        The Zope instance's base directory (INSTANCE_HOME).

      Software

        The Zope server's source code directory (SOFTWARE_HOME).

      Zope

        The Zope server's base directory including the Zope server's source
        code directory (ZOPE_HOME).

      Python

        The Python module library (PYTHON_HOME's Lib sub directory).

    Log Files

      Dump of the Zope server's log files, specifically the access log, error
      log and the event log.

  Copyright

    Copyright (c) 2009 - 2012, Sebastian Lühnsdorf - Web-Solutions

    Idea, design and code by Sebastian Lühnsdorf.
    Web: www.luehnsdorf.com
    Email: info@luehnsdorf.com

  License

    This product is published under the Zope Public License 2.1 (ZPL). A copy
    of the license can be found in the Product's directory.

  Credits

    This software is not based on or uses parts of a release by a third party.

  More Information

    Please visit www.zope.biz/scanner for more information.
