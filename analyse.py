# IMPORTS #
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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

def beam_radius(z, w0):

    zR = (np.pi * (w0**2))/1550E-9
    w = w0*np.sqrt(1 + ((z/zR)**2))
    return w

