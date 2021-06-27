from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
