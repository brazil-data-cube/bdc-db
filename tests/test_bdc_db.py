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

"""Unit-test for BrazilDataCubeExtension."""

from click.testing import CliRunner
from flask.cli import ScriptInfo
from sqlalchemy import inspect
from sqlalchemy_utils.functions import database_exists

import bdc_db.cli as bdc_cli
from bdc_db import BrazilDataCubeDB, create_app
from bdc_db.config import SQLALCHEMY_DATABASE_URI
from bdc_db.db import db


def test_cli(app):
    """Test database creation."""
    BrazilDataCubeDB(app=app)

    runner = app.test_cli_runner()

    # Test package initialization
    _ = create_app()

    # Create minimal db
    if not database_exists(SQLALCHEMY_DATABASE_URI):
        result = runner.invoke(bdc_cli.init, [])
        assert result.exit_code == 0

    assert database_exists(SQLALCHEMY_DATABASE_URI)

    result = runner.invoke(bdc_cli.create_extension_postgis, [])
    assert result.exit_code == 0
    with app.app_context():
        inspector = inspect(db.engine)
        assert inspector.has_table('spatial_ref_sys', schema='public')


if __name__ == '__main__':
    import pytest
    pytest.main(['--color=auto', '--no-cov'])