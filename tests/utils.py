#
# This file is part of BDC-DB.
# Copyright (C) 2023 INPE.
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

from importlib.metadata import EntryPoint

from werkzeug.utils import import_string


class MockEntryPoint(EntryPoint):
    """Mock a Python Entrypoint."""

    def load(self):
        """Overwrite a dynamic loading of Entry point."""
        if self.name == 'importfail':
            raise ImportError()
        else:
            _module = import_string(self.value)
            return _module.SCHEMA if getattr(_module, 'SCHEMA', None) else _module


def mock_entry_points(group=None, **kwargs):
    """Represent general mock entrypoint function to simulate a dynamic setup.py module loading."""
    data = {
        'bdc_db.namespaces': [
            MockEntryPoint(name='demo_app', group=None, value='demo_app:SCHEMA'),
        ],
        'bdc_db.models': [
            MockEntryPoint(name='demo_app', group=None, value='demo_app.models'),
        ],
        'bdc.schemas': [
            MockEntryPoint(name='demo_app', group=None, value='demo_app.jsonschemas')
        ],
        'bdc_db.triggers': [
            MockEntryPoint(name='demo_app', group=None, value='demo_app.triggers')
        ],
        'bdc_db.scripts': [
            MockEntryPoint(name='demo_app', group=None, value='demo_app.scripts')
        ]
    }
    names = data.keys() if group is None else [group]
    for key in names:
        for entry_point in data.get(key, []):
            yield entry_point