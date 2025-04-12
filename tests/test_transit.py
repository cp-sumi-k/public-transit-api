import unittest
import os
import pandas as pd
from transit import get_next_transit_schedules
from model import TransitScheduleInput, Coordinates
from gtfs_loader import GTFSLoader
from geocoding import GeocodingService
from fastapi import HTTPException


class TestTransit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are reused across all tests"""
        # Initialize services with test data
        cls.test_data_dir = os.path.join(
            os.path.dirname(__file__), "test_data")
        cls.setup_test_data()

        # Initialize services
        cls.gtfs_loader = GTFSLoader(root_data_dir=cls.test_data_dir)
        cls.geocoding_service = GeocodingService(
            api_key=os.getenv('GOOGLE_MAPS_API_KEY', 'test_key'))

        # Create state object
        class TestState:
            def __init__(self, loader, geocoding):
                self.gtfs_loader = loader
                self.geocoding_service = geocoding

        cls.state = TestState(cls.gtfs_loader, cls.geocoding_service)

        # Load GTFS data
        cls.gtfs_loader.load_all()

    @classmethod
    def setup_test_data(cls):
        """Create test GTFS data files"""
        # Create test directories
        os.makedirs(os.path.join(cls.test_data_dir, "buses"), exist_ok=True)

        # Create stops.txt
        stops_df = pd.DataFrame({
            'stop_id': ['S1', 'S2', 'S3'],
            'stop_name': ['Times Square', 'Grand Central', 'Penn Station'],
            'stop_lat': [40.7580, 40.7527, 40.7505],
            'stop_lon': [-73.9855, -73.9772, -73.9934],
            'stop_desc': ['', '', '']
        })
        stops_df.to_csv(os.path.join(cls.test_data_dir,
                        "buses", "stops.txt"), index=False)

        # Create stop_times.txt
        stop_times_df = pd.DataFrame({
            'trip_id': ['T1', 'T1', 'T2', 'T2'],
            'arrival_time': ['08:00:00', '08:30:00', '09:00:00', '09:30:00'],
            'departure_time': ['08:00:00', '08:30:00', '09:00:00', '09:30:00'],
            'stop_id': ['S1', 'S2', 'S1', 'S3'],
            'stop_sequence': [1, 2, 1, 2]
        })
        stop_times_df.to_csv(os.path.join(
            cls.test_data_dir, "buses", "stop_times.txt"), index=False)

        # Create trips.txt
        trips_df = pd.DataFrame({
            'route_id': ['R1', 'R2'],
            'service_id': ['WK', 'WK'],
            'trip_id': ['T1', 'T2'],
            'trip_headsign': ['Downtown', 'Uptown'],
            'direction_id': [0, 1]
        })
        trips_df.to_csv(os.path.join(cls.test_data_dir,
                        "buses", "trips.txt"), index=False)

        # Create routes.txt
        routes_df = pd.DataFrame({
            'route_id': ['R1', 'R2'],
            'route_short_name': ['1', '2'],
            'route_long_name': ['Downtown Route', 'Uptown Route'],
            'route_type': [3, 3]
        })
        routes_df.to_csv(os.path.join(cls.test_data_dir,
                         "buses", "routes.txt"), index=False)

    def test_schedule_by_station_id(self):
        """Test getting schedule using station IDs"""
        input_data = TransitScheduleInput(
            origin_station_id="S1",
            destination_station_id="S2"
        )

        response = get_next_transit_schedules(self.state, input_data)

        self.assertGreater(len(response.next_schedules), 0)
        self.assertEqual(response.closest_stop, "Times Square")

    def test_schedule_by_coordinates(self):
        """Test getting schedule using coordinates"""
        input_data = TransitScheduleInput(
            coordinates=Coordinates(
                latitude=40.7580,
                longitude=-73.9855
            ),
            destination_station_id="S2"
        )

        response = get_next_transit_schedules(self.state, input_data)

        self.assertGreater(len(response.next_schedules), 0)
        self.assertIsNotNone(response.closest_stop)

    def test_invalid_station(self):
        """Test handling of invalid station IDs"""
        input_data = TransitScheduleInput(
            origin_station_id="INVALID",
            destination_station_id="S2"
        )

        with self.assertRaises(HTTPException):
            get_next_transit_schedules(self.state, input_data)

    @classmethod
    def tearDownClass(cls):
        """Clean up test data"""
        import shutil
        if os.path.exists(cls.test_data_dir):
            shutil.rmtree(cls.test_data_dir)


if __name__ == '__main__':
    unittest.main()
