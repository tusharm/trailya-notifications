from datetime import datetime, timezone
from unittest.mock import Mock, MagicMock, patch

from storage.sites_store import SitesStore


@patch('storage.sites_store.firestore')
def test_update_on_first_run(mock_firestore):
    geocoder = Mock()
    geocoder.get_geocode.return_value = {}

    mocked_client = MagicMock(name='FirestoreClient')
    mock_firestore.Client.return_value = mocked_client

    store = SitesStore(geocoder, location='X')
    store.update([
        _mocked_site(1, added=datetime(2021, 1, 1, 18, 0, 0).astimezone(timezone.utc)),
        _mocked_site(2, added=datetime(2021, 1, 2, 18, 0, 0).astimezone(timezone.utc)),
    ])

    mocked_client.collection.assert_called_with('X')
    # mocked_client.collection.return_value.document.assert_has_calls([
    #     call('2021-01-01'),
    #     call('2021-01-01'),
    # ])


def _mocked_site(id: int, added: datetime):
    site = Mock()
    site.id.return_value = id
    site.to_dict.return_value = {'id': id}
    site.added_time = added
    return site
