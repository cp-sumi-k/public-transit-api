import unittest
from datetime import datetime
import pytz
from utils import convert_times


class TestTimeConversion(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.timezone = "Asia/Kolkata"
        self.local_tz = pytz.timezone(self.timezone)

    def test_invalid_time_format(self):
        """Test invalid time formats"""
        self.assertIsNone(convert_times("25:00:00", self.timezone))
        self.assertIsNone(convert_times("14:60:00", self.timezone))
        self.assertIsNone(convert_times("14:30", self.timezone))
        self.assertIsNone(convert_times("not a time", self.timezone))
        self.assertIsNone(convert_times("", self.timezone))
        self.assertIsNone(convert_times(None, self.timezone))

    def test_valid_time_conversion(self):
        """Test valid time string"""
        result = convert_times("14:30:00", self.timezone)

        today = datetime.now(self.local_tz).date()
        expected = self.local_tz.localize(
            datetime.combine(today, datetime.strptime(
                "14:30:00", "%H:%M:%S").time())
        ).isoformat()

        self.assertEqual(result, expected)

    def test_different_timezone(self):
        """Test different timezone"""
        ny_time = convert_times("14:30:00", "America/New_York")
        self.assertIsNotNone(ny_time)
        self.assertTrue(
            '-04:00' in ny_time or '-05:00' in ny_time)


if __name__ == '__main__':
    unittest.main()
