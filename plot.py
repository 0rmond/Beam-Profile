import matplotlib.pyplot as plt
import numpy as np

import analyse

def draw_dimension_lines(ax, bounds):
    lower_bound, upper_bound = bounds
    waist = upper_bound - lower_bound

    ax.annotate('', xy=(lower_bound,0.05), xytext=(upper_bound, 0.05), arrowprops=dict(arrowstyle="<->"))
    ax.annotate('', xy=(lower_bound,0.05), xytext=(upper_bound, 0.05), arrowprops=dict(arrowstyle="|-|"))
    bbox=dict(fc="white", ec="none")
    ax.text(lower_bound+waist/2, 0.05, f"Spot Size: \n{waist}mm", ha="center", va="center", bbox=bbox)

def plot_beam_profile(data, title):
    xs = data["Displacement (um)"] * 1E-3 # um -> mm
    ys = analyse.normalise(data["Power (W)"])

    fit_ys, coeffs = analyse.get_fit(xs, ys)
    lower_bound, upper_bound = analyse.get_e_squared_range(xs, fit_ys)

    fig, ax = plt.subplots(1)
    ax.set_title(title)
    ax.set_xlabel("Pinhole Position, x, [mm]")
    ax.set_ylabel("Normalised Power")
    draw_dimension_lines(ax, [lower_bound, upper_bound])

    line_lb = ax.vlines(lower_bound, 0 ,1, linestyle="dotted",color='k')
    line_ub = ax.vlines(upper_bound, 0, 1, linestyle="dotted",color='k')
    line_data = ax.plot(xs, ys, marker='.', linestyle='', c="blue")
    line_model = ax.plot(xs, fit_ys, linestyle='--', c="red", linewidth=3)

    return line_model, line_data

def plot_parametric(zs, ws):
    coeffs, _ = analyse.curve_fit(analyse.beam_radius, zs, ws)
    fit_zs = np.linspace(0, 1, 100)
    fit_ws =  analyse.beam_radius(fit_zs, coeffs[0])
    print("w0 is:", coeffs)

    fig, ax = plt.subplots(1)
    ax.plot(fit_zs, fit_ws)
    ax.plot(zs, ws, marker='x', color='red', linestyle='')
    plt.show()

def plot_results(dataframe, title):# {{{
    """Legacy plotting function that I cannot be bothered to get rid of. Used in the Manual-Beam-Profile notebook
    """
    xs = dataframe.index.values * 1E-3
    ys = dataframe[dataframe.columns[0]]
    sigmas = dataframe[dataframe.columns[1]]

    fit_ys, coeffs = analyse.get_fit(xs, ys)
    lower_bound, upper_bound = analyse.get_e_squared_range(xs, fit_ys)
    waist_size = upper_bound - lower_bound

    fig, ax = plt.subplots(1)
    ax.set_title(title)
    ax.set_xlabel("Pinhole Position, x, [mm]")
    ax.set_ylabel("Measured Power [uW]")
    ax.annotate('', xy=(lower_bound,0.05), xytext=(upper_bound, 0.05), arrowprops=dict(arrowstyle="<->"))
    ax.annotate('', xy=(lower_bound,0.05), xytext=(upper_bound, 0.05), arrowprops=dict(arrowstyle="|-|"))
    bbox=dict(fc="white", ec="none")
    ax.text(lower_bound+waist_size/2, 0.05, f"Spot Size: \n{waist_size}mm", ha="center", va="center", bbox=bbox)

    line_lb = ax.vlines(lower_bound, 0 , max(ys), linestyle="dotted",color='k')
    line_ub = ax.vlines(upper_bound, 0, max(ys), linestyle="dotted",color='k')
    line_data = ax.errorbar(xs, ys, yerr=sigmas/2, xerr=[5E-3 for x in xs], marker='x', linestyle='', c="blue")
    line_model = ax.plot(xs, fit_ys, linestyle='--', c="red")

    return line_model, line_data# }}}

