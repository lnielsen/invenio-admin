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


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import shutil
import tempfile

import pytest
from flask import request as flask_request
from flask import Flask, current_app
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from flask_cli import FlaskCLI
from flask_login import LoginManager, UserMixin, current_user, login_user
from flask_principal import Identity, Principal, UserNeed, identity_changed, \
    identity_loaded
from invenio_db import InvenioDB, db
from sqlalchemy_utils.functions import create_database, database_exists, \
    drop_database

from invenio_admin import InvenioAdmin
from invenio_admin.permissions import action_admin_access
from invenio_admin.views import protected_adminview_factory


class TestModel(db.Model):
    """Test model with just one column."""

    id = db.Column(db.Integer, primary_key=True)
    """Id of the model."""


class TestModelView(ModelView):
    """AdminModelView of the TestModel."""


class TestUser(UserMixin):
    """Test user class."""

    def __init__(self, user_id):
        """Constructor of the user."""
        self.id = int(user_id)

    @classmethod
    def get(cls, user_id):
        """Getter of the TestUser."""
        return cls(user_id)


@pytest.fixture()
def app(request):
    """Flask application fixture."""
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)
    app.config.update(
        TESTING=True,
        SECRET_KEY='SECRET_KEY',
        ADMIN_LOGIN_ENDPOINT='login',
    )
    Babel(app)
    FlaskCLI(app)
    InvenioDB(app)
    Principal(app)
    LoginManager(app)

    # Install login and access loading.
    @app.login_manager.user_loader
    def load_user(user_id):
        return TestUser.get(user_id)

    @app.route('/login/')
    def login():
        user = TestUser.get(flask_request.args.get('user', 1))
        login_user(user)
        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id))
        return "Logged In"

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        identity.provides.add(UserNeed(current_user.id))
        if current_user.id == 1:
            identity.provides.add(action_admin_access)

    # Register admin view
    app.admin_app = InvenioAdmin(app)
    protected_view = protected_adminview_factory(TestModelView)
    app.admin_app.admin.add_view(protected_view(TestModel, db.session))

    # Create database
    with app.app_context():
        if not database_exists(str(db.engine.url)):
            create_database(str(db.engine.url))
        db.drop_all()
        db.create_all()

    def teardown():
        with app.app_context():
            drop_database(str(db.engine.url))
        shutil.rmtree(instance_path)

    request.addfinalizer(teardown)
    return app
