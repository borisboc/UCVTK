# -*- coding: utf-8 -*-
"""
Examples showing how to use the ucvtk.print module

@author: Boris Bocquet <borisboc@free.fr>
@license: LGPL V3.0
"""

# %%

import cv2
import matplotlib.pyplot as plt

from ucvtk.print.print_image_matplotlib import print_image

# %%

# Load an color image in grayscale using opencv
imgPath = 'sand.jpg'
img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
imgHeigh, imgWidth, imgNbChannels = img.shape[:3]
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Load using matplotlib
imgMatplotlib = plt.imread(imgPath)

# %%

# Most basic usage is below.
print("Printing BGR image loaded with openCV")
print_image(img)

# %%

# By default, if you pass no title, a timestamp will be displayed on the image.
# But of this is wised to give a name to track where the print was invoked
print_image(img, title='My BGR image')

# %%

# By default, we expect you to work with opencv color image,
# .i.e BGR images.
# But if you load from matplotlib (or other) you can convert before printing.

# If you don't, the channels will be wrongly displayed
print_image(imgMatplotlib, title='from matplotlib imread')

# So here is how to convert.
print_image(imgMatplotlib, convert_3ch_image=False,
            title='matplotlib no convert')

# %%

# Of course, grayscale / single channel is handled
print("Printing grayscal image")
print_image(imgGray, title='grayscale')

# %%

# And you can provide your matplotlib colormap as well
print_image(imgGray, cmap='plasma', title='colormap')
