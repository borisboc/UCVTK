# -*- coding: utf-8 -*-
"""
Examples showing how to use the ucvtk.histograms module

@author: Boris Bocquet <b.bocquet@akeoplus.com>
@license: LGPL V3.0
"""

# %%

import cv2
import matplotlib.pyplot as plt
import sys
import napari 

from ucvtk.histograms.histograms_napari import open_interactive_histogram

# %%


# Load an color image in grayscale using opencv
imgPath = r"D:\GIT\UCVTK\rgb_circles.png"
img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
imgHeigh, imgWidth, imgNbChannels = img.shape[:3]
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Load using matplotlib
imgMatplotlib = plt.imread(imgPath)

# %%

# Most basic usage is below.
open_interactive_histogram(img)
