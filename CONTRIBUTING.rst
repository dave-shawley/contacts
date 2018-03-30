Contributing to contacts
========================

**Thank you for even considering!**

There are a few things that need to happen before you should create that pull
request though.  You need to make sure that your changes are documented and
tested.

Before you make your changes
----------------------------
This project use Python 3 so create a new Python virtual environment right at
the root of the directory::

   $ python3 -mvenv env

Next, install the package::

   $ env/bin/pip install -e .

Finally, run the tests to make sure that your environment is set up correctly.
The tests in master should always pass::

   $ env/bin/python -munittest
   .
   ----------------------------------------------------------------------
   Ran 1 test in 0.384s

   OK

Now you can make your changes.

Making changes
--------------
If you haven't forked the repository, do that first.  Then create a new branch
for your work and start changing code.  Here are a few things that will make
your pull request more likely to get merged.

- favor small commits where each commit contains a single logical change, the
  associated tests, and documentation changes (if any)
- update tests and documentation
- write docstrings for public functions and methods
- follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ for formatting
  conventions

Once your changes are finished, submit them as a pull request.
