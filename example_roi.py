# -*- coding: utf-8 -*-
"""
Examples showing how to use the ucvtk.draw module

@author: Boris Bocquet <b.bocquet@akeoplus.com>
@license: LGPL V3.0
"""

# %%

import cv2
import matplotlib.pyplot as plt

from ucvtk.roi.draw_roi_napari import draw_point, draw_rectangle

# %%

# Load an color image in grayscale using opencv
imgPath = 'sand.jpg'
img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
imgHeigh, imgWidth, imgNbChannels = img.shape[:3]
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Load using matplotlib
imgMatplotlib = plt.imread(imgPath)

# %%

# Basic usage to draw a point.
point = draw_point(img)
# Returns numpy.ndarray, that are the coordinates of the point.
# The shape is (1,2)
# point[0,0] is row coordinate
# point[0,1] is column coordinate
# See documentation of draw_point

# %%

# Basic usage to draw a rectangle.
rect = draw_rectangle(img)
# Returns numpy.ndarray, that are the coordinates of the corners.
# See documentation of draw_rectangle (the ordering of the corners depends
# on the angle of the rectangle).

# %%

# Concerning the color convertion, and grayscale, the functions
# of uctk.roi are similare to uctk.print
# Indeed, by default, we expect you to work with opencv color image,
# .i.e BGR images.
# But if you load from matplotlib (or other) you can convert before printing.
# If you don't, the channels will be wrongly displayed

# So here is how to convert.
rect_again = draw_rectangle(imgMatplotlib, convert=False)

# %%
# Of course, grayscale / single channel is handled
rect_grayscale = draw_rectangle(imgGray)


# %%
# If you have noted in the napari, we split the channels of the color image.
# So that you can they display/hide each channel separatly.
# The drawback is that the viewer takes more time to appear,
# and it flickers a bit.
# But you can disable this splitting. See below.
rect_no_split = draw_rectangle(img, split_channels=False)
