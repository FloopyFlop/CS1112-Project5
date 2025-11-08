"""
Functions to draw rectangle and disk

The shape is added to the current plot if a figure window is active. Otherwise,
a new figure window will open.
"""


import matplotlib.pyplot as plt 
import numpy as np


def draw_rect(a, b, w, h, c):
    """
    Adds a rectangle to the plot.

    The rectangle has vertices (a,b), (a+w,b), (a+w,b+h), and (a,b+h) 
    and color c where c is one of 'r', 'g', 'y', etc.

    Parameters:
        a (float): The x-coordinate of the lower left corner of the rectangle
        b (float): The y-coordinate of the lower left corner of the rectangle
        w (float): The width of the rectangle
        h (float): The height of the rectangle
        c (str): The color of the rectangle
    """
    x= [a, a+w, a+w, a]
    y= [b, b, b+h, b+h]
    plt.fill(x, y, color=c)
    
    
def draw_disk(xc, yc, r, c):
    """
    Adds a circular disk to the plot.

    The disk has radius r, center (xc,yc), and 
    color c where c is one of 'r', 'g', 'y', etc.

    Parameters:
        xc (float): The x-coordinate of the center of the disk
        yc (float): The y-coordinate of the center of the disk
        r (float): The radius of the disk
        c (str): The color of the disk
    """
    theta= np.linspace(0, 2*np.pi, 100)
    cosines= np.cos(theta)
    sines= np.sin(theta)
    plt.fill(xc + r*cosines, yc + r*sines, color=c)