import itertools
from typing import Optional

from google.cloud import firestore

from storage.site import Site
from utils.dateutils import as_string
from utils.geocoder import Geocoder


class SitesStore:
    def __init__(self, geocoder: Geocoder, location: str):
        self.geocoder = geocoder
        self.location = location
        self.db = firestore.Client()

    def last_updated_on(self) -> Optional[str]:
        stream = self.db.collection(self.location).stream()
        docs = [doc.id for doc in stream]
        docs.sort(reverse=True)
        return None if len(docs) == 0 else docs[0]

    def save(self, sites: [Site]):
        grouped = itertools.groupby(sites, key=lambda s: as_string(s.added_time))

        sites_ref = self.db.collection(self.location)
        for date, daily_sites in grouped:
            sites_list = list(daily_sites)

            date_doc_ref = sites_ref.document(date)
            for site in sites_list:
                site.geocode = self.geocoder.get_geocode(site.full_address())
                date_doc_ref.collection(f'{self.location}_sites').add(site.to_dict())

            if date_doc_ref.get().exists:
                date_doc_ref.update({'count': firestore.Increment(len(sites_list))})
            else:
                date_doc_ref.set({'count': len(sites_list)})

