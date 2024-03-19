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
    x0: centre-pointy
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

def fit_err(xs, ys):
    coeffs, errs = curve_fit(erf, xs, ys)
    return coeffs, errs

def get_e_squared_range(xs, ys):
    """Returns the lower and upper bounds of the 1/e^2 range"""
    peak = max(ys)
    e_squared_factor = peak/np.e**2

    mask = [ y>e_squared_factor for y in ys ]
    e_squared_region = xs[mask].values
    return e_squared_region[0], e_squared_region[-1]

def beam_radius(z, w0):

    zR = (np.pi * (w0**2))/1550E-9
    w = w0*np.sqrt(1 + ((z/zR)**2))
    return w


def get_std_of_times(v_char_data):
    v_char_data["times std"] = v_char_data["times"].std()
    return v_char_data

def get_velocity(v_char_data):
    v_char_data["velocity"] = 200E-6 / v_char_data["times"]
    return v_char_data

def get_velocity_std(v_char_data):
    v_char_data["velocity err"] = v_char_data["velocity"] * np.sqrt((v_char_data["times std"] / v_char_data["times"]))
    return v_char_data

def get_velocity_and_error(v_char_data):
    return {"value": v_char_data["velocity"].mean(), "error": v_char_data["velocity err"].mean()/np.sqrt(len(v_char_data))}

