#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Database management extension configuration."""

import os

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI',
                                    'postgresql://postgres:postgres@localhost:5432/bdc')

SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', False)

JSONSCHEMAS_HOST = os.getenv('JSONSCHEMAS_HOST', 'brazildatacube.org')
"""Define the hostname for any JSONSchemas supported by Brazil Data Cube."""
