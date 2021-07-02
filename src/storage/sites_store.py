import itertools

from google.cloud import firestore

from config.config import Config
from storage.site import Site
from utils.dateutils import as_string
from utils.geocoder import Geocoder

"""
This class writes data to Firestore.

Note that our datasets are a full snapshot, so this class discards 
previous state, where applicable and writes afresh 
"""


class SitesStore:
    def __init__(self, geocoder: Geocoder, location: str):
        self.geocoder = geocoder
        self.location = location
        self.fs_client = firestore.Client()

    def update(self, sites: [Site]):
        location_col_ref = self.fs_client.collection(self.location)

        grouped_by_date = itertools.groupby(sites, key=lambda s: as_string(s.added_time))
        for date, daily_sites in grouped_by_date:
            sites_as_list = list(daily_sites)
            date_doc_ref = location_col_ref.document(date)

            # delete doc if it exists
            date_doc_ref.delete()

            self.batch_write(date_doc_ref, sites_as_list)
            date_doc_ref.set({'count': len(sites_as_list)})

    def batch_write(self, doc, sites: [Site]):
        batch = self.fs_client.batch()
        for site in sites:
            if not site.latitude:
                site.set_geocode(self.geocoder.get_geocode(site.full_address()))

            site_doc_ref = doc.collection(f'{self.location}_sites').document(site.id())
            batch.set(site_doc_ref, site.to_dict())

        batch.commit()
