import pandas as pd
import numpy as np
from functools import reduce

def get_data(fname):
    raw = pd.read_csv(fname, skiprows=14, usecols=[2,3], index_col=0 )
    times = [ t.strip() for t in raw.index.values ]
    timestamps = pd.to_datetime(times, format="%H:%M:%S.%f", origin="unix")

    data = pd.DataFrame(raw[raw.columns[0]].values, columns=["Power (W)"], index=timestamps)
    return data

def reindex_timestamps_with_times(timestamped_data):
    timestamps = timestamped_data.index
    t0 = timestamp_to_seconds(timestamps[0])
    timestamped_data.index = timestamps.map(lambda t: abs(timestamp_to_seconds(t) - t0))
    return timestamped_data

def calculate_displacement(timed_data, velocity):
    times = timed_data.index
    timed_data["Displacement (m)"] = list(map(lambda t: t * velocity["value"], times.values))
    return timed_data

def get_distances(displacement_data):
    displacements = displacement_data["Displacement (m)"]
    displacement_data["Distances (m)"] = [0, *np.diff(displacements)]
    return displacement_data

def calculate_distances_error(displacement_data, velocity):
    distances = displacement_data["Distances (m)"].values
    displacement_data["Displacement Error (m)"] =  distances * np.sqrt((velocity["error"] / velocity["value"]))
    return displacement_data


def percent_diff(a, b):
    return 100 * abs( a - b ) / (a + b)

def get_rows_with_known_displacement(data, known_powers):
    percentage_differences = map(
        lambda power: percent_diff( data["Power (W)"].values, power),
        known_powers
    )
    rows_close_to_known_powers = map(lambda p_diff: data.loc[ p_diff <= 1 ], percentage_differences)

    well_defined_data = pd.concat(list(rows_close_to_known_powers))
    return well_defined_data

def characterise_velocity(well_defined_data, known_positions):
    del_t = abs(well_defined_data.index[1] - well_defined_data.index[0])

    um_per_second = abs(known_positions[1] - known_positions[0]) / (timestamp_to_seconds(del_t))

    return um_per_second

def timestamp_to_seconds(timestamp):
    return timestamp.value * 1E-9

def convert_time_to_displacement(data, well_defined_data, um_per_second ):
    matched_times = well_defined_data.index.map(
        lambda time: timestamp_to_seconds(time)
    )

    ds = data.index.map(
        lambda time: (timestamp_to_seconds(time) - matched_times[0]) * um_per_second
    ).values

    data["Displacement (um)"] = ds
    return data
