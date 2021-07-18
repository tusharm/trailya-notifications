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

    def update(self, sites: [Site]) -> int:
        """
        Updates Firestore collection with new sites

        Args:
            sites: list of Site objects

        Returns:
            No of documents updated in this run

        """
        total_sites_updated = 0
        grouped_by_date = itertools.groupby(sorted(sites, key=_grouping_key), key=_grouping_key)

        location_col_ref = self.fs_client.collection(self.location)

        for date, daily_sites in grouped_by_date:
            sites_as_list = list(daily_sites)

            date_doc_count = 0
            date_doc_ref = location_col_ref.document(date)
            if date_doc_ref.get().exists:
                date_doc_count = int(date_doc_ref.get().to_dict()['count'])

            if date_doc_count != len(sites_as_list):
                # this means no of sites on this date has updated

                # ideally, we should check for existence of each doc in the subcollection
                # but that's too much complexity for our use case. so, just delete/recreate the doc
                date_doc_ref.delete()

                self.batch_write(date_doc_ref, sites_as_list)
                date_doc_ref.set({'count': len(sites_as_list)})

                updated_sites = len(sites_as_list) - date_doc_count
                total_sites_updated += updated_sites
                print(f'{updated_sites} new sites found for date {date}')

        return total_sites_updated

    def batch_write(self, doc, sites: [Site]):
        batch = self.fs_client.batch()
        for site in sites:
            if not site.latitude:
                site.set_geocode(self.geocoder.get_geocode(site.full_address()))

            site_doc_ref = doc.collection(f'{self.location}_sites').document(site.id())
            batch.set(site_doc_ref, site.to_dict())

        batch.commit()


def _grouping_key(site: Site):
    return as_string(site.added_time)
