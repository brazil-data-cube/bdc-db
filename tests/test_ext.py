from unittest import mock

from pkg_resources import EntryPoint
from werkzeug.utils import import_string

from bdc_db import BrazilDataCubeDB


class MockEntryPoint(EntryPoint):
    """Mock an Python Entrypoint."""

    def load(self):
        """Overwrite a dynamic loading of Entry point."""
        if self.name == 'importfail':
            raise ImportError()
        else:
            return import_string(self.module_name).SCHEMA


def _mock_entry_points(name):
    data = {
        'bdc_db.namespaces': [
            MockEntryPoint('demo_app', 'demo_app', attrs=('SCHEMA',)),
        ],
    }
    names = data.keys() if name is None else [name]
    for key in names:
        for entry_point in data.get(key, []):
            yield entry_point


class TestBDCExtension:
    """Test the BrazilDataCube Extension."""

    @mock.patch('pkg_resources.iter_entry_points', _mock_entry_points)
    def test_load_provider_through_entrypoint(self, app):
        """Test the dynamic entry point loading."""
        ext = BrazilDataCubeDB(app)

        assert len(ext.namespaces) == 1
        assert ext.namespaces[0] == 'myapp'
