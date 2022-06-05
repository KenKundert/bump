*bump* is a program for updating the version number of your project.  It uses 
`semantic versioning <https://semver.org>`_ and will also update the release 
date if desired.


Installation
------------

Install using

    pip3 install .


Configuration
-------------

To create initial version of configuration file:

    bump initialize

Configuration file is ``.bump.cfg.nt``.  It is a `NestedText <nestedtext.org>` 
file.

Set initial values for version number components and indicate the variables that 
should be updated upon release.

A typical configuration file looks like::

    major: 1
    minor: 6
    patch: 1
    iteration: 0
    type: release
    files:
        teneya/__init__.py:
            date: __released__
            version: __version__
        setup.py:
            version: version

It is a `NestedText <nestedtext.org>`_ file. With this configuration, two files 
will be updated upon a release.  The first, *teneya/__init__.py*, contains 
assignments to variables named *__released* and *__version__*.
The right-hand side of both should be strings, the first containing the date in 
the form YYYY-M-D and the second in the form 
*<major>.<minor>.<patch>[-<type>.<iteration>]*.  For example::

    ...
    __version__ = "1.6.1"
    __released__ = '2021-01-27'
    ...

The second file, *setup.py*,  contains only a version.  In this case the 
assignment takes the form of a named function argument::

    ...
    version = '1.6.1',
    ...

It could also take the form of a dictionary value::

    ...
    "version": '1.6.1',
    ...


Use
---

To demonstrate the use of the tool, a series of actions will be shown along  
with the corresponding changes to the version.  Assume that the initial version 
is 1.6.1.

Update the major level with::

    bump major      ⟪1.6.1 → 2.0.0⟫

Update the minor level with::

    bump minor      ⟪2.0.0 → 2.1.0⟫

Update the patch level with::

    bump patch      ⟪2.1.0 → 2.1.1⟫

or simply::

    bump            ⟪2.1.1 → 2.1.2⟫

Without an indication of which level to update, the lowest available level is 
updated.  The lowest available level is *patch* post-release and *iteration* 
pre-release.

You can output the current version using::

    bump version

Pre-releases are also supported.  There are 4 kinds, *dev*, *alpha*, *beta* and 
*rc*.  They have the following meanings:

*dev*:
    Development version: not intended for general use.

*alpha*:
    First step in release process, suitable for internal testing.

*beta*:
    Second step in release process, suitable for external testing.

*rc*:
    Release candidate: the final step in release process, believed ready for 
    release.

*release*: A released version.

For example, consider a project that has just done a minor release, say 1.2, and 
is now commencing the development of a new feature.  The initial subsequent 
release would not be intended for general use and so would be marked as a *dev* 
release.  Once the new version becomes feature complete and seems to be working, 
it transitions to the alpha phase.  During this phase the code is only used 
internally while the tests and documentation are filled out.  Once it is ready 
for external users the code transitions to the beta phase.  After others have 
had a chance to try out the new code and comment on it and their feedback has 
been addressed, it transitions to the release candidate phase.  Finally, once 
all concerns about the code are addressed and the code appears stable, it goes 
to formal release.  Typically, this is the version that is published to general 
distribution sites like `PyPI <pypi.org>`_.

To continue our example, assume that our project is entering a phase where 
a substantial new feature is being developed that will lead to a minor release::

    bump minor dev            ⟪2.1.2 → 2.2.0-dev.0⟫

You can indicate new development versions either with::

    bump dev                  ⟪2.2.0-dev.0 → 2.2.0-dev.1⟫

or simply with::

    bump                      ⟪2.2.0-dev.1 → 2.2.0-dev.2⟫

You transition to a new phase with::

    bump beta                 ⟪2.2.0-dev.2 → 2.2.0-beta.0⟫

Notice that the phase jumped from *dev* to *beta*, bypassing *alpha*.  It is not 
necessary to go through all the phases, but you should go through them in the 
proper order.

Finally, you transition to a formal release using::

    bump release              ⟪2.2.0-beta.0 → 2.2.0⟫

