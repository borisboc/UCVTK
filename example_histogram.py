# -*- coding: utf-8 -*-
"""
Examples showing how to use the ucvtk.histograms module

@author: Boris Bocquet <borisboc@free.fr>
@license: LGPL V3.0
"""

# %%

import cv2
import matplotlib.pyplot as plt
import numpy as np

from ucvtk.histograms.histograms_napari import open_interactive_histogram


# %%


# Load an color image in grayscale using opencv
imgPath = r"D:\GIT\UCVTK\rgb_circles.png"
img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
imgHeigh, imgWidth, imgNbChannels = img.shape[:3]
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Load using matplotlib
imgMatplotlib = plt.imread(imgPath)
if imgMatplotlib.dtype == np.float32:
    # sometimes (if you are not using pillow), reading png returns normalized float
    imgMatplotlib = np.asarray(imgMatplotlib*255, dtype=np.uint8)


# %%

# The goal of this tool is for analysing the grayvalue distribution
# thanks to an interactive rectangle you can move on the image.
# This is usefull when you want to check the contrasts and estimate
# local threshold values (i.e. for color segementation, edges etc.)

# Most basic usage is below.
open_interactive_histogram(img)


# By default, we expect you to work with opencv color image,
# .i.e BGR images.
# But if you load from matplotlib (or other) you can convert calling histograms

# If you don't, the channels will be wrongly displayed
open_interactive_histogram(imgMatplotlib, convert_3ch_image=False)


# It also works with gray images
open_interactive_histogram(imgGray)
