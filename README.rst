About
-----
**elticket** is a command line tool that sets up a new JIRA ticket within the
E+L JIRA environment (https://eljira.els.local:8443) and inserts default
information into various field, including templates for the ticket
description and the underlying environment. The user then must only insert
the specific information for this ticket. The goal is to make filing a ticket
less of hassle and also enabling to establish a standardized form for the
ticket description.

Both Google Chrome and Mozilla Firefox can be used.
Other browsers are currently not supported.

Prerequisites
-------------
* Python 3.6 or higher must be installed (https://www.python.org/downloads/)
* Either Chrome or Firefox browser must be installed
* geckodriver must be installed to use this script with **Firefox** (https://github.com/mozilla/geckodriver/releases)
* chromedriver must be installed to use this script with **Chrome** (http://chromedriver.chromium.org/)
* Linux only: gedit must be installed (``sudo apt install gedit``)

Compatibility chart
-------------------
Generally, use the latest chromedriver when using Chrome (or geckodriver
for Firefox). If unexpected errors occur, please try one of the following
configuration:

+---------------+-----------------------+
| Chromedriver  | Chrome                |
+===============+=======================+
| 2.38          | 70.0                  |
+---------------+-----------------------+
| 2.45          | 71.0                  |
+---------------+-----------------------+
| 75.0.3770.90  | 75.0.3770.100         |
+---------------+-----------------------+

Please see http://chromedriver.chromium.org/ for latest compatibility information

+---------------+-----------------------+
| Geckodriver   | Firefox               |
+===============+=======================+
| 0.21.0        | 56.0.1                |
+---------------+-----------------------+
| 0.23.0        | 64.0                  |
+---------------+-----------------------+
| 0.24.0        | 67.0.4                |
+---------------+-----------------------+

Firefox version 53.0 or higher is required

Installation
------------
**1. Check python installation**

Before the installation, make sure that the ``python`` CLI command is referring to your Python 3 installation,
since this is the environment, this package is supposed to be installed in.

After installing Python, see if the ``python`` and the ``pip`` (Python's package manager)
are referring to the correct installation::

    python --version
    which python
    which pip

Note that Windows users require to use ``where`` instead of ``which``.

If the version fits and both commands refer to the correct Python installation, proceed with the step 2.

Linux and OSX systems often have a pre-installed versions of Python 2 and 3, whereas Windows commonly does not.
If the ``python`` command referse to a Python 2 installation, check these::

    python3 --version
    which python3
    which pip3

If the version fits and both commands refer to the correct Python installation, proceed with the step 2.

If these commands don't refer to valid binaries, then these must be added manually to the system PATH variable.

For Windows:

If ``python`` refers to a Python 2 installation and ``python3`` isn't found, then do this little trick.
Go to your Python 3 installation directory (usually ``C:\Users\<yourusername>\AppData\Local\Programs\Python\Python3x\)``
and create a copy of ``python.exe`` and rename it ``python3.exe``. After restarting the
command line, when typing ``python3`` the Python 3.x console is launched.*

**2. Create a virtual environment**

It is highly recommended to create a new virtual environment for this package,
otherwise elticket and all depending packages are installed into your default
python environment::

    python3 -m venv </desired/path/to/my/virtual/environement>

Please note that ``pip3`` must be used if ``pip`` is part of an existing Python 2 installation.
Do not use `virtualenv`_ to create your virtual environment, as this alters required libraries.

Activate your virtual environment

on Windows::

    C:</path/to/your/virtual/env>/bin/activate

on Linux / OSX::

    source </path/to/your/virtual/env/>activate

You notice the (<virtual_environment_parent_pathname)
then install via pip::

    pip install elticket-<version>.tar.gz

Please note that while within a virtual environment, you don't need to use ``pip3`` and ``python3``
as ``python`` or ``pip`` always refer to the binaries of the virtual environment while it is activated.

To deactivate a virtual environment simply write::

    deactivate

.. _virtualenv: https://pypi.org/project/virtualenv/

**3. Install elticket**

Make sure your virtual environment is active. Then type::

    pip install elticket-<version>.tar.gz

This will install the package and all its dependencies.

Enabling the 'elticket' command
-------------------------------

**Method #1:** Use from activated virtualenv

Activate the virtualenv then run elticket::

    elticket --help

The virtual environment must be activated before script can be used

**Method #2:** Create a symlink of elticket in your global script directory

Create a symlink of elticket(.exe)

in Windows::

    mklink "<X:\my\python\virtual\env\dir>\elticket\bin\elticket.exe" "<X:\my\global\script\dir\>elticket.exe"

or on Linux / OSX::

    cd <my/global/script/dir>
    ln -s </my/python/virtual/env/dir>/elticket/bin/elticket elticket

Script can now be used *without* activating the virtual environment::

    elticket --help

Usage examples
--------------
Create a ticket (here: creates a bug ticket for OMS3)::

    elticket create -p oms3 -t bug

Set a new default assignee (here: for any OMS4 improvement ticket)::

    elticket set assignee -p oms4 -t improvement "John Doe"

Change a template (here: for OMS6 bug description)::

    elticket set template -p oms6 -t bug

Use ``--help`` option for more details.

Browser profiles
----------------
**Firefox**

You can define a Firefox profile to be used. It is recommended (see `here`_)
to use a clean profile for browser automation tasks to prevent browser plugins or
addons to break functionality or also to save space (since each ticket creation opens
a new browser instance) and increase performance.

Follow `these steps`_ to create a new profile for Firefox.

Add the new profile to the elticket settings by typing::

    elticket set firefox_profile "/path/to/firefox/profile/<some_code>.<profile_name>"

To find out your profile directory, type::

    about:profile

into your address bar and look for ``Root Directory`` of your designated profile.

Please note:

Before executing the script from a new profile, make sure to manually accept the
**security certificate** for E+L JIRA as each profile manages these independently.

**Chrome**

Using a separate profile is not required for Google Chrome, as the chromedriver
uses a browser instance using the default profile, which does not contain any
user installed extension or settings, that might temper with the browser automation.


.. _here: https://www.toolsqa.com/selenium-webdriver/custom-firefox-profile/#Why%20do%20I%20need%20New%20Profile
.. _these steps: https://support.mozilla.org/en-US/kb/profile-manager-create-and-remove-firefox-profiles
.. _instructions: https://support.google.com/chrome/answer/2364824?co=GENIE.Platform%3DDesktop&hl=en

Changelog
---------
**0.2** - *(2019-07-12)*

- Able to set individual JIRA login data
- Added support for Firefox
- Templates files are no longer overwritten when re-installing elticket

**0.1** - *(2019-01-07)*

- *Initial release*
- Support for products OMS3, OMS4 and OMS6
- Support for Chrome

Developers
----------
The source code of **elticket** can be found at::

    https://elscr.els.local/svn/inspection/inspection/Test/TestArne/elticket/

A new distribution is easily created using `setuptools`_
which is pre-installed for each Python environment (otherwise can be installed via pip).

To create a distribution, increase the __version__ variable in elticket.py,
then type::

    python setup.py sdist

A new target distribution file (\*.tar.gz) is now located at the ./dist directory.
Please see the setuptools `documentation`_ for further information.

.. _setuptools: https://pypi.org/project/setuptools/
.. _documentation: https://setuptools.readthedocs.io/en/latest/