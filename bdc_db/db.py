#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Database instance using Flask-SQLAlchemy extension."""

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import MetaData as _MetaData

metadata = _MetaData()
"""Default database metadata object holding associated schema constructs."""


db = _SQLAlchemy(metadata=metadata)
"""Shared database instance using Flask-SQLAlchemy extension."""