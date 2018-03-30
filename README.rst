========
Contacts
========

Simple web application for managing your contact information.

+---------------+------------------------------------------+
| Source        | https://github.com/dave-shawley/contacts |
+---------------+------------------------------------------+
| Documentation | https://pythonhosted.org/contacts        |
+---------------+------------------------------------------+
| Download      | https://pypi.org/projects/contacts       |
+---------------+------------------------------------------+

Installing and running
======================
The contacts service is simple to install::

   $ pip install contacts

Installing the package creates a command-line utility that runs the service
in the foreground listening on port 8,000.  The foreground process forks
multiple children to handle the request velocity.
::

   $ contacts-api
   I[sprockets@34085 correlation_id="" logger="Runner" process="37916" line="93" function="start_server" module="runner"] starting processes on port 8000
   I[sprockets@34085 correlation_id="" logger="tornado.general" process="37916" line="133" function="fork_processes" module="process"] Starting 8 processes

You can kill the process by sending either a termination or an interrupt
signal to the process group::

   $ kill -INT -37916

Note that the signal is sent to the process group and not simply the parent
process.

Running in development
======================
The application can also be run using the **httprun** *setup.py* command::

   $ ./setup.py httprun -a contacts.app:Application
   running httprun
   running <class 'contacts.app.Application'>
   I[sprockets@34085 correlation_id="" logger="Runner" process="38326" line="93" function="start_server" module="runner"] starting processes on port 8000
   I[sprockets@34085 correlation_id="" logger="tornado.general" process="38326" line="133" function="fork_processes" module="process"] Starting 8 processes

