*bump* is a program for updating the version number of your project.  It uses 
`semantic versioning <https://semver.org>`_ and will also update the release 
date if desired.  It is unique in that it updates both the version number and 
the release date, whereas most other versioning utilities only update the 
version number.


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

Edit the configuration file to add the files than must be updated when the 
version changes and the name of the variables to change.  You can enter as many 
files as you want.  For example, to update the src/__init__.py file, you could 
add the following to the configuration file::

    files:
        src/__init__.py:
            date: __released__
            version: __version__

A typical configuration file looks like::

    major: 1
    minor: 6
    patch: 1
    revision: 0
    type: release
    style: semver
    files:
        src/__init__.py:
            date: __released__
            version: __version__
        pyproject.toml:
            version: version

It is a `NestedText <nestedtext.org>`_ file. With this configuration, two files 
will be updated upon a release.  The first, *src/__init__.py*, contains 
assignments to variables named *__released* and *__version__*.
The right-hand side of both should be strings, the first containing the date in 
the form YYYY-M-D and the second in the form 
*<major>.<minor>.<patch>[-<type>.<revision>]*.  For example::

    ...
    __version__ = "1.6.1"
    __released__ = '2021-01-27'
    ...

The second file, *pyproject.toml*,  contains only a version.  In this case the 
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
updated.  The lowest available level is *patch* post-release and *revision* 
pre-release.

You can output the current version using::

    bump version

Pre-releases and post-releases are also supported.  There are 5 kinds, *dev*, 
*alpha*, *beta*, *rc*, and *post*.  They have the following meanings:

*dev*:
    Development version: not intended for general use.

*alpha*:
    First step in release process, suitable for internal testing.

*beta*:
    Second step in release process, suitable for external testing.

*rc*:
    Release candidate: the final step in release process, believed ready for 
    release.

*post*:
    Post release version.  A post release corrects some address minor errors in 
    a final release that do not affect the distributed software, such as a fix 
    of the release notes.

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

You transition to a formal release using::

    bump release              ⟪2.2.0-beta.0 → 2.2.0⟫

Then you can do a post release:

    bump post                 ⟪2.2.0 → 2.2.0-post.0⟫

And another:

    bump post                 ⟪2.2.0-post.0 → 2.2.0-post.1⟫

Styles
------

*bump* supports two versioning styles, both variations of Semantic Versioning.  
The default style is *python* as specified in `PEP 440 
<https://peps.python.org/pep-0440>`_.  The second is *semver* as specified in 
`semver.org <https://semver.org>`_.  The *python* style is more concise of the 
two and takes the following forms::

    0.9
    1.0.dev0
    1.0.dev1
    1.0.dev2
    1.0.dev3
    1.0a0
    1.0a1
    1.0b0
    1.0b1
    1.0rc0
    1.0rc1
    1.0
    1.0.post0
    1.1.dev0

The *semver* style takes the following forms::

    0.9
    1.0-dev.1
    1.0-dev.2
    1.0-dev.3
    1.0-dev.4
    1.0-alpha.0
    1.0-alpha.1
    1.0-beta.0
    1.0-beta.1
    1.0-rc.0
    1.0-rc.1
    1.0
    1.0-post.0
    1.1-dev.0

You declare the style when you first initialize *bump*::

    bump initialize semver

or::

    bump initialize python

If you wish to change the style later, simply edit the configuration file.
