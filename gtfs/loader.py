import pandas as pd
import os
from utils import convert_times


class GTFSLoader:
    def __init__(self, root_data_dir: str = "data"):
        self.root_data_dir = root_data_dir
        self.modes = ["buses", "railroads"]
        self.stops_df = pd.DataFrame()
        self.stop_times_df = pd.DataFrame()
        self.trips_df = pd.DataFrame()
        self.routes_df = pd.DataFrame()

    def load_all(self):
        for mode in self.modes:
            mode_dir = os.path.join(self.root_data_dir, mode)
            print(f"Loading GTFS data for: {mode}")

            stops = pd.read_csv(os.path.join(mode_dir, "stops.txt"))
            stop_times = pd.read_csv(os.path.join(mode_dir, "stop_times.txt"))
            trips = pd.read_csv(os.path.join(mode_dir, "trips.txt"))
            routes = pd.read_csv(os.path.join(mode_dir, "routes.txt"))

            # Add transit mode label for traceability
            stops["transit_mode"] = mode
            stop_times["transit_mode"] = mode
            trips["transit_mode"] = mode
            routes["transit_mode"] = mode

            self.stops_df = pd.concat(
                [self.stops_df, stops], ignore_index=True)

            self.stop_times_df = pd.concat(
                [self.stop_times_df, stop_times], ignore_index=True)
            self.stop_times_df["transit_mode"] = mode

            self.trips_df = pd.concat(
                [self.trips_df, trips], ignore_index=True)
            self.routes_df = pd.concat(
                [self.routes_df, routes], ignore_index=True)

        print("All modes loaded successfully.")

        return {
            "stops": self.stops_df,
            "stop_times": self.stop_times_df,
            "trips": self.trips_df,
            "routes": self.routes_df
        }

    def get_schedule(self, origin_stop_id: str, destination_stop_id: str):
        # Convert stop IDs to string
        stop_times = self.stop_times_df.copy()
        stop_times['stop_id'] = stop_times['stop_id'].astype(str)

        # Get all relevant trips
        is_present = stop_times['stop_id'].isin(
            [origin_stop_id, destination_stop_id])
        relevant_stops = stop_times[is_present]

        # Count occurrences of each trip_id
        trip_counts = relevant_stops.groupby('trip_id').size()
        valid_trip_ids = trip_counts[trip_counts == 2].index

        if len(valid_trip_ids) == 0:
            return pd.DataFrame()

        # Filter for valid trips
        valid_stops = relevant_stops[relevant_stops['trip_id'].isin(
            valid_trip_ids)]

        schedule = valid_stops.pivot(
            index='trip_id',
            columns='stop_id',
            values=['arrival_time', 'transit_mode']
        )

        result = pd.DataFrame({
            'trip_id': schedule.index,
            'transit_mode': schedule[('transit_mode', origin_stop_id)],
            'eta_origin': schedule[('arrival_time', origin_stop_id)].apply(convert_times),
            'eta_destination': schedule[('arrival_time', destination_stop_id)].apply(convert_times)
        })

        return result.sort_values('eta_origin').reset_index(drop=True)
