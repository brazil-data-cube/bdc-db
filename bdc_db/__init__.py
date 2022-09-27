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

"""Database Management for Brazil Data Cube Applications and Services."""

from flask import Flask

from .db import db
from .ext import BrazilDataCubeDB
from .models import SpatialRefSys
from .sqltypes import JSONB
from .version import __version__


def create_app():
    """Flask application factory.

    Returns:
        Flask Application with BrazilDataCubeDB extension prepared.
    """
    app = Flask(__name__)

    BrazilDataCubeDB(app)

    return app


__all__ = (
    '__version__',
    'BrazilDataCubeDB',
    'JSONB',
    'SpatialRefSys',
    'create_app',
    'db',
)
