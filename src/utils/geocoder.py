import googlemaps


class Geocoder:
    def __init__(self, key: str):
        self.maps = googlemaps.Client(key=key)

    def get_geocode(self, address: str):
        result = self.maps.geocode(address)
        if len(result) == 0:
            return {}

        return {
            'formatted_address': result[0]['formatted_address'],
            'geometry': result[0]['geometry'],
            'place_id': result[0]['place_id'],
            'types': result[0]['types']
        }

