#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Database Management for Brazil Data Cube Applications and Services."""

from flask import Flask

from .db import db
from .ext import BrazilDataCubeDB
from .models import SpatialRefSys
from .sqltypes import JSONB
from .version import __version__


def create_app(config):
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
