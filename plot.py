import matplotlib.pyplot as plt
import numpy as np

import analyse

def draw_dimension_lines(axis, upper_bound, lower_bound):
    waist = upper_bound-lower_bound

    axis.annotate('', xy=(lower_bound,0), xytext=(upper_bound, 0), arrowprops=dict(arrowstyle="<->"))
    axis.annotate('', xy=(lower_bound,0), xytext=(upper_bound, 0), arrowprops=dict(arrowstyle="|-|"))
    bbox=dict(fc="white", ec="none")
    axis.text(lower_bound + waist/2, 0, f"{round(waist, 3)}mm", ha="center", va="center", bbox=bbox)

def plot_beam_profile(data, title):
    xs = data["Displacement (m)"] * 1E3 # um -> mm
    x_errs = data["Displacement Error (m)"] * 1E3
    ys = analyse.normalise(data["Power (W)"])

    fit_ys, coeffs = analyse.get_fit(xs, ys)
    lower_bound, upper_bound = analyse.get_e_squared_range(xs, fit_ys)
    lower_bound_err = x_errs.loc[xs == lower_bound].values[0]
    upper_bound_err = x_errs.loc[xs == upper_bound].values[0]

    waist = {
        "value": round(upper_bound - lower_bound, 3),
        "err": round(np.sqrt( upper_bound_err**2 + lower_bound_err**2), 3)
    }

    fig, ax = plt.subplots(1)
    ax.set_title(title)
    ax.set_xlabel("Pinhole Position, x, [mm]")
    ax.set_ylabel("Normalised Power")
    draw_dimension_lines(ax, [lower_bound, upper_bound], waist)

    line_lb = ax.vlines(lower_bound, 0 ,1, linestyle="dotted",color='k')
    line_ub = ax.vlines(upper_bound, 0, 1, linestyle="dotted",color='k')
    line_data = ax.errorbar(xs, ys, xerr=x_errs, marker='.', linestyle='', c="blue")
    line_model = ax.plot(xs, fit_ys, linestyle='--', c="red", linewidth=3, zorder=999)

    return waist, line_model, line_data

def plot_parametric(zs, ws):
    coeffs, _ = analyse.curve_fit(analyse.beam_radius, zs, ws)
    fit_ws =  analyse.beam_radius(zs, coeffs[0])
    fake_zs = np.linspace(0, zs[-1], 100)

    fig, ax = plt.subplots(1)
    ax.plot(zs, fit_ws, color = "blue", linestyle="--")
    ax.plot(zs, ws, marker='x', color='red', linestyle='')
    #ax.plot(fake_zs, list(map(lambda z: analyse.beam_radius(z, (2.27E-3) / 2), fake_zs)), color="black", linestyle = "--")
    ax.set_xlabel("Position on the Table (mm)")
    ax.set_ylabel("Beam Radius (mm)")

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

