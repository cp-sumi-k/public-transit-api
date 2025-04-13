import unittest
import pandas as pd
from gtfs_loader import GTFSLoader
from unittest.mock import patch


class TestGTFSLoader(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.loader = GTFSLoader(root_data_dir="test_data")

        # Sample test data
        self.sample_stops = pd.DataFrame({
            'stop_id': ['S1', 'S2', 'S3'],
            'stop_name': ['Stop 1', 'Stop 2', 'Stop 3'],
            'stop_lat': [40.7128, 40.7589, 40.7505],
            'stop_lon': [-74.0060, -73.9851, -73.9934],
            'transit_mode': ['buses'] * 3
        })

        self.sample_stop_times = pd.DataFrame({
            'trip_id': ['T1', 'T1', 'T2', 'T2'],
            'stop_id': ['S1', 'S2', 'S1', 'S3'],
            'arrival_time': ['08:00:00', '08:30:00', '09:00:00', '09:30:00'],
            'transit_mode': ['buses'] * 4
        })

    @patch('pandas.read_csv')
    def test_load_all(self, mock_read_csv):
        """Test loading all GTFS data"""
        mock_read_csv.side_effect = [
            self.sample_stops,
            self.sample_stop_times
        ] * len(self.loader.modes)

        result = self.loader.load_all()

        self.assertFalse(self.loader.stops_df.empty)
        self.assertFalse(self.loader.stop_times_df.empty)

        self.assertIn('stops', result)
        self.assertIn('stop_times', result)

    def test_get_closest_stop(self):
        """Test getting stop name by ID"""
        self.loader.stops_df = self.sample_stops

        # Test valid stop ID
        result = self.loader.get_closest_stop('S1')
        self.assertEqual(result, 'Stop 1')

        # Test with different type stop ID
        result = self.loader.get_closest_stop(str('S2'))
        self.assertEqual(result, 'Stop 2')

    def test_get_stop_id_from_coordinates(self):
        """Test finding nearest stop ID from coordinates"""
        self.loader.stops_df = self.sample_stops

        # Test coordinates near Stop 1
        result = self.loader.get_stop_id_from_coordinates(40.7128, -74.0060)
        self.assertEqual(result, 'S1')

        # Test coordinates somewhere between stops
        result = self.loader.get_stop_id_from_coordinates(40.7500, -73.9900)
        self.assertIn(result, self.sample_stops['stop_id'].values)

    def test_get_schedule(self):
        """Test getting schedule between two stops"""
        self.loader.stop_times_df = self.sample_stop_times

        result = self.loader.get_schedule('S1', 'S2')
        self.assertFalse(result.empty)
        self.assertEqual(len(result), 1)

        # Test invalid stop pair
        result = self.loader.get_schedule('S1', 'S4')
        self.assertTrue(result.empty)

        # Test same stop
        result = self.loader.get_schedule('S1', 'S1')
        self.assertTrue(result.empty)

    def test_load_data_with_empty_df(self):
        """Test error handling scenarios"""
        empty_loader = GTFSLoader()

        closest_stop = empty_loader.get_closest_stop('S1')
        self.assertTrue(closest_stop == "")

        result = empty_loader.get_schedule('S1', 'S2')
        self.assertTrue(result.empty)


if __name__ == '__main__':
    unittest.main()
