import servo
import analyse
import plot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def waist_from_measurements(data, measurements):
    known_xs = measurements["Displacement (m)"].values
    known_ps = measurements["Power (W)"].values

    
    well_defined_data = servo.get_rows_with_known_displacement(data, known_ps)
    speed = servo.characterise_speed(well_defined_data, known_xs)
    print("Speed: ", speed)
    data = servo.convert_time_to_displacement(data, well_defined_data, speed)
    waist, _, __ = plot.plot_beam_profile(data, "")
    return waist

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

import servo
import analyse
import plot

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def timestamps_to_displacement(timestamped_data, velocity):

    data = (timestamped_data
            .pipe(servo.reindex_timestamps_with_times)
            .pipe(servo.calculate_displacement, velocity)
           )
    displacement_data = data.set_index("Displacement (m)")

    
    return displacement_data
    

def plot_knife_edge_method(ax, dataset):
    xs = dataset.index.values*1E3 # in mm
    ys = dataset["Power (W)"].values*1E6 # in uW
    
    coeffs, coeff_errs = analyse.fit_erf(xs, ys)
    fit_ys = analyse.erf(xs, *coeffs)

    gauss_ys = analyse.G(xs, 2*coeffs[0], coeffs[1], coeffs[2]/np.sqrt(2))

    lower_bound, upper_bound = analyse.get_e_squared_range(xs, gauss_ys)

    ax.set_xlabel("Displacement [mm]")
    
    ax.plot(xs, ys, marker='.', linestyle='', color="tab:blue", label="meas")
    ax.plot(xs, fit_ys,linestyle='--', linewidth=3, color="tab:red", label="erf fit")
    ax.plot(xs, gauss_ys, linestyle='--', linewidth=3, color="tab:purple", label="gauss fit")
    
    plot.draw_dimension_lines(ax, upper_bound, lower_bound)
    ax.vlines(lower_bound, 0, max(ys), linestyle=':', linewidth=2, color="black")
    ax.vlines(upper_bound, 0, max(ys), linestyle=':',  linewidth=2, color="black")

    return upper_bound - lower_bound

def plot_result(files, velocity):
    timestamped_knife_measurements = map(servo.get_data, files)
    displacement_data = map(
        lambda m: timestamps_to_displacement(m, velocity),
        timestamped_knife_measurements
    )
    fig, axes = plt.subplots(1,len(files), dpi=250, sharey=True)
    axes = [axes]
    axes[0].set_ylabel("Power (uW)")
    diameters = np.array([
        plot_knife_edge_method(ax, data) for ax, data in zip(axes, [*displacement_data])
    ])
    mean_diam = diameters.mean()
    mean_diam_err = diameters.std()/np.sqrt(len(diameters))
    fig.suptitle(f"Mean Beam Diameter: {round(mean_diam, 3)} +/- {round(mean_diam_err, 3)}")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center')
    plt.tight_layout()
    return mean_diam, mean_diam_err
def main():

    slow_v_data = [5.44824, 4.96972, 5.16894, 5.32715, 5.16797, 5.09668, 4.79297, 5.17773, 5.03418, 5.12597, 4.8164, 5.02929, 5.52637, 5.20703, 5.01758, 5.28613, 5.13086, 5.14453, 4.86523, 5.04883, 5.05566, 4.93652, 5.34277, 5.39453, 5.08789, 5.03808, 5.00683, 5.07031, 5.23437, 4.77929, 5.11719, 5.12402]
    slow_v_df = pd.DataFrame({"times": slow_v_data})

    slow_v = (slow_v_df
                  .pipe(analyse.get_std_of_times)
                  .pipe(analyse.get_velocity)
                  .pipe(analyse.get_velocity_std)
                  .pipe(analyse.get_velocity_and_error)
                   )
    file = ["Data/knife-edge/single/1.csv"]
    plot_result(file, slow_v)
    plt.show()


if __name__ == "__main__":
    main()
