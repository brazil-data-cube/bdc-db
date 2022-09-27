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

"""Define models of the package demo_app."""

from jsonschema import draft7_format_checker

from bdc_db.db import db
from bdc_db.sqltypes import JSONB


class FakeModel(db.Model):
    """Define a simple table to store names."""

    __table_name__ = 'fake_model'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    properties = db.Column(JSONB('dummy-jsonschema.json', draft_checker=draft7_format_checker))
    counter = db.Column(db.Integer, default=0)
