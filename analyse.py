# IMPORTS #
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf as err_fun

def get_data(path_to_dir, fname):
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
    x0: centre-point
    sigma: std dev
    """
    return h*np.exp(-(x-x0)**2/(2*sigma**2))

def erf(x, a, mu, std, b):
    return a*err_fun((x-mu) / std) + b

def fit_gaussian(xs, ys):
    
    # Initialise optimisation params #
    h_i = max(ys)
    mask = [ y==h_i for y in ys]
    x0_i = xs[mask].values[0]
    sigma_i = np.std(xs)

    coeffs, _ = curve_fit(G, xs, ys, p0=(h_i,x0_i,sigma_i))
    return G(xs, *coeffs), coeffs

def fit_gauss(xs, ys):
    h_i = max(ys)
    mask = [ y == h_i for y in ys ]
    x0_i = xs[mask][0]
    sigma_i = np.std(xs)

    coeffs, pcov = curve_fit(G, xs, ys, p0 = (h_i, x0_i, sigma_i)) 
    errs = np.sqrt(np.diag(pcov))
    return coeffs, errs

def fit_erf(xs, ys):
    a_i = max(ys) * 1/2
    mu_i = xs.mean()
    std_i = xs.std()
    b_i = min(ys)
    initial_guess = (a_i, mu_i, std_i, b_i)

    coeffs, pcov = curve_fit(erf, xs, ys, p0=initial_guess)
    errs = np.sqrt(np.diag(pcov))
    return coeffs, errs

def get_e_squared_range(xs, ys):
    """Returns the lower and upper bounds of the 1/e^2 range"""
    peak = max(ys)
    e_squared_factor = peak/np.e**2

    mask = [ y > e_squared_factor for y in ys ]
    e_squared_region = xs[mask]
    return e_squared_region[0], e_squared_region[-1]

def beam_radius(z, w0, z0):
    # default z0 - 10.2E-3
    zR = (np.pi * (w0**2))/1550E-9
    w = w0*np.sqrt(1 + (((z-z0)/zR)**2))
    return w


def get_std_of_times(v_char_data):
    v_char_data["times std"] = v_char_data["times"].std()
    return v_char_data

def get_velocity(v_char_data, div_in_um):
    v_char_data["velocity"] = (div_in_um*1E-6) / v_char_data["times"]
    return v_char_data

def get_velocity_std(v_char_data):
    v_char_data["velocity err"] = v_char_data["velocity"] * np.sqrt((v_char_data["times std"] / v_char_data["times"]))
    return v_char_data

def get_velocity_and_error(v_char_data):
    return {"value": v_char_data["velocity"].mean(), "error": v_char_data["velocity err"].mean()/np.sqrt(len(v_char_data))}

def get_average_velocity(v_tracker_data):
    ts = np.array(v_tracker_data.dropna()["t"].values)
    del_ts = np.diff(ts)
    print(ts[20] - ts[0])
    vs = np.array(list(map(lambda t: 10E-6 / t, del_ts)))

    return { "value": vs.mean(), "err": vs.std() / np.sqrt(len(vs)) }
