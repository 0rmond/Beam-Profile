import servo
import analyse
import plot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def waist_from_pre_char_speed(timestamped_data, velocity):

    displacement_data = (timestamped_data
                         .pipe(servo.reindex_timestamps_with_times)
                         .pipe(servo.calculate_displacement, velocity)
                         .pipe(servo.calculate_displacement_error, velocity)
                        )
    print(displacement_data)
    waist, _, __ = plot.plot_beam_profile(displacement_data, "")
    plt.show()
    return 5
def main():
    """
    POWERS = [86.38E-6, 148.8E-6]
    DISTANCES = [2200, 3800]
    """

    speed_3_data = pd.DataFrame({
        "times": [1.85449, 1.92676, 1.88867, 1.90918, 1.88672, 1.93359, 1.92383, 1.84668, 1.87012, 1.96777, 1.92969, 1.94433, 1.85351, 1.87109, 1.93652, 2.00976, 1.74121, 1.94922, 1.92285, 1.92383, 1.95215, 1.88086, 1.91113, 1.88086, 1.93164, 1.87695, 1.80859, 1.93164, 1.90625, 2.00683],    
    })
    speed_4_data = pd.DataFrame({
        "times": [1.4082, 1.36133, 1.35059, 1.37695, 1.41113, 1.3584, 1.37305, 1.39062, 1.39062, 1.36426, 1.38574, 1.41797, 1.3584, 1.44141, 1.30762, 1.38281, 1.31738, 1.47558, 1.36035, 1.39844, 1.43652, 1.34668, 1.36816, 1.37695, 1.39258, 1.44043, 1.37402, 1.38965, 1.41992, 1.27148, 1.46484, 1.37207, 1.32519, 1.44043, 1.39941],
    })
    v = (speed_3_data
         .pipe(analyse.get_std_of_times)
         .pipe(analyse.get_velocity)
         .pipe(analyse.get_velocity_std)
         .pipe(analyse.get_velocity_and_error)
    )
    data0 = servo.get_data("Data/1.csv")
    waist_from_pre_char_speed(data0, v)


if __name__ == "__main__":
    main()
