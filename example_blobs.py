# -*- coding: utf-8 -*-
"""
Drawing Region Of Interest (ROI) on images
using napari viewer

@author: Boris Bocquet <b.bocquet@akeoplus.com>
@license: LGPL V3.0
"""

# %%

import cv2
from matplotlib import pyplot as plt
from ucvtk.blobs.blob_management_napari import open_blob_management, stats_dict_to_str

# %%a

# Load an color image in grayscale using opencv
imgPath = 'sand.jpg'
img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
imgHeigh, imgWidth, imgNbChannels = img.shape[:3]
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Load using matplotlib
imgMatplotlib = plt.imread(imgPath)

# %%

# The goal of open_blob_management is to display a napari viewer,
# where you will be able to get some infos on the blobs you click (work ongoing).
# And also to select some blobs by clicking on it.
# By blob, is meant "connected components on segmented 2d images".

# So lets start to trheshold the image grayvals and compute the blobs (connected components)
ret, imgThres = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY)
retval, labels = cv2.connectedComponents(imgThres)

# Then open the viewer to get some infos on the blobs, and select blobs you click on.
# Press 's' (for 'stats') to get some informations on the blob you click onto.
# Press 'a' (for 'adding') to add the blobs you click on to a selection (see return).
# Press 'r' (for 'removing') to remove a blob you have previously selected.
selected_blobs = open_blob_management(imgThres, labels)

# selected_blobs is the new label image (numpry.ndarray) of the blobs you have selected.

# Display your selection on a new blob management viewer.
again = open_blob_management(imgThres, selected_blobs)


# %%

# If you are not aligned with the default blob statistics,
# you can pass your own function.
# For example the function below will return the main moments (the diagonal).

def custom_stats_on_blob(binarySingleBlobImg):

    statsretval, clickedlabels, blobstats, blobcentroids = cv2.connectedComponentsWithStats(binarySingleBlobImg, connectivity=8)
    outDict = {}

    if(statsretval >= 2):
        # index 0 is background
        allMoments = cv2.moments(clickedlabels, binaryImage=True)
        outDict = dict((k,allMoments[k]) for k in ('m00','m11') if k in allMoments)
        return stats_dict_to_str(outDict)
    else:
        return f'stats_on_blob returned {statsretval}'


# This function is passed to the blob management gui.
open_blob_management(imgThres, labels, funcInfoBlobs=custom_stats_on_blob)
