# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Administration interface for Invenio.

Invenio-Admin provides an administration interface for Invenio based on
Flask-Admin.

Initialization
--------------

First create a Flask application (Flask-CLI is not needed for Flask version
1.0+):

>>> from flask import Flask
>>> from flask_cli import FlaskCLI
>>> app = Flask('myapp')
>>> app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
>>> ext_cli = FlaskCLI(app)

You initialize Invenio-Admin like a normal Flask extension, however
Invenio-Admin is dependent on Invenio-DB so you need to initialize both
extensions:

>>> from invenio_db import InvenioDB
>>> from invenio_admin import InvenioAdmin
>>> ext_db = InvenioDB(app)
>>> ext_admin = InvenioAdmin(app)

In order for the following examples to work, you need to work within an Flask
application context so let's push one:

>>> ctx = app.app_context()
>>> ctx.push()

Also, for the examples to work we need to create the database and tables (note,
in this example we use an in-memory SQLite database):

>>> from invenio_db import db
>>> db.create_all()

Configuration
~~~~~~~~~~~~~

Registering view
----------------

Entry point loading
~~~~~~~~~~~~~~~~~~~

Authorization and permissions
-----------------------------

"""

from __future__ import absolute_import, print_function

from .ext import InvenioAdmin
from .version import __version__

__all__ = ('__version__', 'InvenioAdmin')
