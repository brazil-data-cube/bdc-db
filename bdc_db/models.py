#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
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
