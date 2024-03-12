# IMPORTS #
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def get_data(path_to_dir, fname, delim):
    data = pd.read_csv(path_to_dir+fname, delimiter=',',index_col=0)
    return data

def normalise_data(dataframe):
    ys = dataframe[dataframe.columns[0]]
    sigmas = dataframe[dataframe.columns[1]].multiply(1E-3)
    norm_ys = normalise(ys)
    norm_factor = norm_ys / ys

    norm_sigmas = sigmas.multiply(norm_factor)


    return pd.concat([norm_ys, norm_sigmas],axis=1)

def normalise(column):
    return (column - column.min()) / (column.max() - column.min())

def G(x,h,x0,sigma):
    """
    h: height
    x0: centre-pointy
    sigma: std dev
    """
    return h*np.exp(-(x-x0)**2/(2*sigma**2))

def get_fit(xs, ys):
    
    # Initialise optimisation params #
    h_i = max(ys)
    mask = [ y==h_i for y in ys]
    x0_i = xs[mask][0]
    sigma_i = np.std(xs)

    coeffs, _ = curve_fit(G, xs, ys, p0=(h_i,x0_i,sigma_i))
    return G(xs, *coeffs), coeffs

def get_e_squared_range(xs, ys):
    """Returns the lower and upper bounds of the 1/e^2 range"""
    peak = max(ys)
    e_squared_factor = peak/np.e**2

    mask = [ y>e_squared_factor for y in ys ]
    e_squared_region = xs[mask]
    return e_squared_region[0], e_squared_region[-1]

def plot_results(dataframe, title):# {{{
    xs = dataframe.index.values * 1E-3
    ys = dataframe[dataframe.columns[0]]
    sigmas = dataframe[dataframe.columns[1]]

    fit_ys, coeffs = get_fit(xs, ys)
    lower_bound, upper_bound = get_e_squared_range(xs, fit_ys)
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

def plot_beam_profile(data, title):
    xs = data["Displacement (um)"] * 1E-3 # um -> mm
    ys = normalise(data["Power (W)"])

    fit_ys, coeffs = get_fit(xs, ys)
    lower_bound, upper_bound = get_e_squared_range(xs, fit_ys)
    waist_size = upper_bound - lower_bound

    fig, ax = plt.subplots(1)
    ax.set_title(title)
    ax.set_xlabel("Pinhole Position, x, [mm]")
    ax.set_ylabel("Normalised Power")
    ax.annotate('', xy=(lower_bound,0.05), xytext=(upper_bound, 0.05), arrowprops=dict(arrowstyle="<->"))
    ax.annotate('', xy=(lower_bound,0.05), xytext=(upper_bound, 0.05), arrowprops=dict(arrowstyle="|-|"))
    bbox=dict(fc="white", ec="none")
    ax.text(lower_bound+waist_size/2, 0.05, f"Spot Size: \n{waist_size}mm", ha="center", va="center", bbox=bbox)

    line_lb = ax.vlines(lower_bound, 0 ,1, linestyle="dotted",color='k')
    line_ub = ax.vlines(upper_bound, 0, 1, linestyle="dotted",color='k')
    line_data = ax.plot(xs, ys, marker='.', linestyle='', c="blue")
    line_model = ax.plot(xs, fit_ys, linestyle='--', c="red", linewidth=2)

    return line_model, line_data


def beam_radius(z, w0):

    zR = (np.pi * w0**2)/1550E-3
    w = w0*np.sqrt(1 + (z/zR)**2)
    return w

def plot_parametric(zs, ws):
    coeffs, _ = curve_fit(beam_radius, zs, ws)
    fit_zs = np.linspace(0, zs[-1] + 100E-3, 100)
    fit_ws =  beam_radius(fit_zs, coeffs[0])
    print("w0 is:", coeffs)

    fig, ax = plt.subplots(1)
    ax.plot(fit_zs, fit_ws)
    plt.show()
