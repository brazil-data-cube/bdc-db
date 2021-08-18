#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Define utility functions for unittests."""

from pkg_resources import EntryPoint
from werkzeug.utils import import_string


class MockEntryPoint(EntryPoint):
    """Mock an Python Entrypoint."""

    def load(self):
        """Overwrite a dynamic loading of Entry point."""
        if self.name == 'importfail':
            raise ImportError()
        else:
            _module = import_string(self.module_name)
            return _module.SCHEMA if getattr(_module, 'SCHEMA', None) else _module


def mock_entry_points(name):
    """Represent general mock entrypoint function to simulate a dynamic setup.py module loading."""
    data = {
        'bdc_db.namespaces': [
            MockEntryPoint('demo_app', 'demo_app', attrs=('SCHEMA',)),
        ],
        'bdc_db.models': [
            MockEntryPoint('demo_app', 'demo_app.models', attrs=(),),
        ],
        'bdc.schemas': [
            MockEntryPoint('demo_app', 'demo_app.jsonschemas', attrs=(),)
        ],
        'bdc_db.triggers': [
            MockEntryPoint('demo_app', 'demo_app.triggers', attrs=(), )
        ],
        'bdc_db.scripts': [
            MockEntryPoint('demo_app', 'demo_app.scripts', attrs=(), )
        ]
    }
    names = data.keys() if name is None else [name]
    for key in names:
        for entry_point in data.get(key, []):
            yield entry_point