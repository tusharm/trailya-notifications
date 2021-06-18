import itertools
from typing import Optional

from google.cloud import firestore

from utils.datetime import parse_to_utc, as_string
from storage.site import Site


class SitesStore:
    def __init__(self):
        self.db = firestore.Client()

    def last_updated_on(self) -> Optional[str]:
        stream = self.db.collection(u'exposure_sites').stream()
        docs = [doc.id for doc in stream]
        docs.sort(reverse=True)
        return None if len(docs) == 0 else docs[0]

    def save(self, sites: [Site]):
        grouped = itertools.groupby(sites, key=lambda s: as_string(s.added_time))

        sites_ref = self.db.collection(u'exposure_sites')
        for date, daily_sites in grouped:
            sites_list = list(daily_sites)

            date_doc_ref = sites_ref.document(date)
            for site in sites_list:
                date_doc_ref.collection(u'sites').add(site.to_dict())

            if date_doc_ref.get().exists:
                date_doc_ref.update({'count': firestore.Increment(len(sites_list))})
            else:
                date_doc_ref.set({'count': len(sites_list)})


if __name__ == '__main__':
    exposure_sites = SitesStore()
    sites = [
        Site(
            'Maidstone',
            'Arcare Maidstone Aged Care (Entire Facility)',
            '31 Hampstead Road',
            'VIC',
            3012,
            parse_to_utc('2021-05-26T00:00:00+10:00'),
            parse_to_utc('2021-05-26T11:59:00+10:00'),
            parse_to_utc('2021-05-28T16:15:00+10:00'),
        ),
        Site(
            'Melbourne',
            'Woolworths Metro Little Collins St',
            '360 Little Collins St',
            'VIC',
            3000,
            parse_to_utc('2021-06-03T12:10:00+10:00'),
            parse_to_utc('2021-06-03T12:50:00+10:00'),
            parse_to_utc('2021-06-05T12:00:00+10:00'),
        )
    ]
    print(sites)
    exposure_sites.save(sites)
    print(exposure_sites.last_updated_on())
