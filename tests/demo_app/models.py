#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Define models of the package demo_app."""

from jsonschema import draft7_format_checker

from bdc_db.db import db
from bdc_db.sqltypes import JSONB


class FakeModel(db.Model):
    """Define a simple table to store names."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    properties = db.Column(JSONB('dummy-jsonschema.json', draft_checker=draft7_format_checker))
