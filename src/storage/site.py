import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from utils.dateutils import to_epoch_millis


@dataclass
class Site:
    suburb: str
    title: str
    street_address: str
    state: str
    postcode: Optional[int]
    exposure_start_time: datetime
    exposure_end_time: datetime
    added_time: datetime
    latitude: Optional[float]
    longitude: Optional[float]
    geocode: dict
    data_errors: []

    def id(self):
        hash_fn = hashlib.blake2b(digest_size=15)
        start_ms = to_epoch_millis(self.exposure_start_time)
        end_ms = to_epoch_millis(self.exposure_end_time)

        as_bytes = bytes(f'${self.latitude}_${self.longitude}_${start_ms}_${end_ms}', 'UTF-8')
        hash_fn.update(as_bytes)
        return hash_fn.hexdigest()

    def to_dict(self):
        result = {
            'suburb': self.suburb,
            'title': self.title,
            'street_address': self.street_address,
            'state': self.state,
            'exposure_start_time': self.exposure_start_time,
            'exposure_end_time': self.exposure_end_time,
            'added_time': self.added_time,
            'geocode': self.geocode,
            'data_errors': self.data_errors,
        }
        if self.postcode:
            result['postcode'] = self.postcode

        if self.latitude:
            result['latitude'] = self.latitude

        if self.longitude:
            result['longitude'] = self.longitude

        return result

    def full_address(self) -> str:
        return f'{self.title}, {self.street_address}, {self.suburb}, {self.state} {self.postcode}'

    def set_geocode(self, geo: dict):
        self.geocode = geo
        self.latitude = geo['geometry']['location']['lat']
        self.longitude = geo['geometry']['location']['lng']

    def __str__(self) -> str:
        return f"""Site(
            suburb: {self.suburb},
            title: {self.title},
            street_address: {self.street_address},
            state: {self.state},
            postcode: {self.postcode},
            exposure_start_time: {self.exposure_start_time},
            exposure_end_time: {self.exposure_end_time},
            added_time: {self.added_time}
            latitude: {self.latitude}
            longitude: {self.longitude}
            data_errors: {self.data_errors}
        )
        """
