from unittest import mock

import pytest
from pkg_resources import EntryPoint
from werkzeug.utils import import_string

from bdc_db import BrazilDataCubeDB
from tests.utils import mock_entry_points


class FakeNamespaceEntryPoint(EntryPoint):
    """Mock an Python Entrypoint."""

    def load(self):
        """Overwrite a dynamic loading of Entry point."""
        return None


def mock_entry_point_invalid_namespace(name):
    data = {
        'bdc_db.namespaces': [
            FakeNamespaceEntryPoint('demo_app', 'demo_app', attrs=()),
        ]
    }

    names = data.keys() if name is None else [name]
    for key in names:
        for entry_point in data.get(key, []):
            yield entry_point


class TestBDCExtension:
    """Test the BrazilDataCube Extension."""

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
    def test_load_provider_through_entrypoint(self, app):
        """Test the dynamic entry point loading."""
        ext = BrazilDataCubeDB(app)

        assert len(ext.namespaces) == 1
        assert ext.namespaces[0] == 'myapp'
        # Assert JSONSchema loaded
        schema = ext.schemas.get_schema('dummy-jsonschema.json')
        assert schema

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_point_invalid_namespace)
    def test_invalid_namespace(self, app):
        """Test the dynamic entry point loading."""
        with pytest.raises(RuntimeError):
            _ = BrazilDataCubeDB(app)
