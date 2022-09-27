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