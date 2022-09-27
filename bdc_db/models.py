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

"""Define the models associated with BDC-DB."""

from sqlalchemy import Column, Integer, String

from .db import db


class SpatialRefSys(db.Model):
    """Auxiliary model for the PostGIS spatial_ref_sys table.

    Note:
        This model is set to be excluded automatically in alembic generation
        on BDC-DB initialization using ``ALEMBIC_EXCLUDE_TABLES``.
    """

    __tablename__ = 'spatial_ref_sys'
    __table_args__ = ({"schema": "public"})

    srid = Column(Integer, primary_key=True)
    auth_name = Column(String)
    auth_srid = Column(String)
    srtext = Column(String)
    proj4text = Column(String)
