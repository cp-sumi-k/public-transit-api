import requests

GOOGLE_MAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


class GeocodingService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def reverse_geocode(self, lat: float, lon: float) -> str:
        try:
            params = {
                'latlng': f"{lat},{lon}",
                'key': self.api_key
            }

            response = requests.get(GOOGLE_MAPS_BASE_URL, params=params)
            response.raise_for_status()

            result = response.json()

            if result['status'] != 'OK' or not result['results']:
                return ""

            return result['results'][0]['formatted_address']

        except Exception as e:
            print(f"Error in reverse geocoding: {str(e)}")
            return None
