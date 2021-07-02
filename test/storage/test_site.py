from datetime import datetime

from storage.site import Site


def test_geocode_added_to_site():
    s = Site(
        suburb='asdas',
        title='adsfs',
        street_address='asdf',
        state='NSW',
        postcode=None,
        exposure_start_time=datetime.now(),
        exposure_end_time=datetime.now(),
        added_time=datetime.now(),
        latitude=None,
        longitude=None,
        geocode={},
        data_errors=[],
    )
    s.set_geocode({
        'geometry': {
            'location': {
                'lat': 123.4,
                'lng': 432.1
            }
        }
    })

    assert s.latitude == 123.4
    assert s.longitude == 432.1
