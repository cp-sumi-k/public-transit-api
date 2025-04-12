import pandas as pd
import os


class GTFSLoader:
    def __init__(self, root_data_dir: str = "data"):
        self.root_data_dir = root_data_dir
        self.modes = ["subways", "buses", "railroads"]
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
