#
# This file is part of BDC-DB.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

from unittest import mock

import jsonschema
import pytest
from demo_app.models import FakeModel
from sqlalchemy.exc import StatementError
from utils import mock_entry_points

from bdc_db import BrazilDataCubeDB
from bdc_db.db import db


@mock.patch('bdc_db.ext.entry_points', mock_entry_points)
@mock.patch('importlib_metadata.entry_points', mock_entry_points)
def test_validate_jsonschema_type(app):
    BrazilDataCubeDB(app)

    db.create_all()

    with db.session.begin_nested():
        model = FakeModel()
        model.name = 'MyModel'
        model.properties = {"fieldStringRequired": "FakeData"}
        db.session.add(model)
    db.session.commit()

    assert model.id > 0

    model.properties = None
    db.session.commit()

    with pytest.raises(StatementError) as e:
        model.properties = dict()  # Expect the key fieldStringRequired
        db.session.add(model)
        db.session.commit()

    assert isinstance(e.value.orig, jsonschema.ValidationError)
    assert e.value.orig.message == "'fieldStringRequired' is a required property"
