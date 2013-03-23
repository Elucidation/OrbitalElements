from __future__ import division
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
cos = np.cos
sin = np.sin
pi = np.pi

def plotOrbit(semi_major_axis, eccentricity):
    "Draws orbit around an earth in units of kilometers."

    fig = plt.figure(figsize=plt.figaspect(1))  # Square figure
    ax = fig.add_subplot(111, projection='3d')

    #### Draw Earth
    Earth_radius = 6371 # km
    
    # Coefficients in a0/c x**2 + a1/c y**2 + a2/c z**2 = 1 
    coefs = (1, 1, 1)  

    # Radii corresponding to the coefficients:
    rx, ry, rz = [Earth_radius/np.sqrt(coef) for coef in coefs]

    # Set of all spherical angles:
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    # Cartesian coordinates that correspond to the spherical angles:
    # (this is the equation of an ellipsoid):
    x = rx * np.outer(np.cos(u), np.sin(v))
    y = ry * np.outer(np.sin(u), np.sin(v))
    z = rz * np.outer(np.ones_like(u), np.cos(v))

    # Plot:
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='g')

    ### Draw orbit
    theta = np.linspace(0,2*pi, 360)
    r = (semi_major_axis * (1-eccentricity**2)) / (1 + eccentricity*cos(theta))

    plt.plot(r*cos(theta),r*sin(theta))


    # Adjustment of the axes, so that they all have the same span:
    max_radius = max(rx, ry, rz, max(r))
    for axis in 'xyz':
        getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))

    # Draw figure
    plt.show()