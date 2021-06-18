from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dateutils import parse_to_utc, build_isoformat_string


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

    def to_dict(self):
        result = {
            'suburb': self.suburb,
            'title': self.title,
            'street_address': self.street_address,
            'state': self.state,
            'exposure_start_time': self.exposure_start_time,
            'exposure_end_time': self.exposure_end_time,
            'added_time': self.added_time
        }
        if self.postcode:
            result['postcode'] = int(self.postcode)

        return result

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
        )
        """

    @staticmethod
    def from_dict(data: dict):
        return Site(
            data['Suburb'],
            data['Site_title'],
            data['Site_streetaddress'],
            data['Site_state'],
            int(data['Site_postcode']) if data['Site_postcode'] else None,
            parse_to_utc(build_isoformat_string(data['Exposure_date_dtm'], data['Exposure_time_start_24'])),
            parse_to_utc(build_isoformat_string(data['Exposure_date_dtm'], data['Exposure_time_end_24'])),
            parse_to_utc(build_isoformat_string(data['Added_date_dtm'], data['Added_time'])),
        )


