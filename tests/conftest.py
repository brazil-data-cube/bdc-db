#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test configuration."""

import pytest
from flask import Flask

from bdc_db import BrazilDataCubeDB, db


@pytest.fixture
def app():
    """Flask application fixture."""
    app = Flask(__name__)

    with app.app_context():
        yield app
