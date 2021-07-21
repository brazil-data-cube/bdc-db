from unittest import mock

import jsonschema
import pytest
from demo_app.models import FakeModel
from sqlalchemy.exc import StatementError
from utils import mock_entry_points

from bdc_db import BrazilDataCubeDB
from bdc_db.db import db


@mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
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
