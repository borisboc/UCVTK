# -*- coding: utf-8 -*-
"""
Printing images in the console using matplotlib in "inline" backend.

@author: Boris Bocquet <borisboc@free.fr>
@license: LGPL V3.0
"""

# %%

import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib as mpl
import IPython as ip
import datetime
from ucvtk.utils.img_channels import is_single_channel, splitable_in_3
from ucvtk.utils.matplotlib_backend import set_backend, set_backend_inline 



def print_image(image: np.ndarray, cmap:mpl.colors.Colormap = None, convert_3ch_image: bool = True, convert: int = cv2.COLOR_BGR2RGB, title: str =''):
    """
    Print the given image into the console, using matplotlib.
    This will force matplotlib's inline.

    Parameters
    ----------
    image : numpy.ndarray
        The image, coming from opencv for instance.
    cmap : matplotlib.colors.Colormap, optional
        Colormap. The default is None. See matplotlib documentation.
    convert_3ch_image : bool, optional
        If you want to enable an opencv convertion. The default is True.
    convert : int, optional
        The convertion to apply on the input image. See opencv cv2.cvtColor
        documentation. The default is cv2.COLOR_BGR2RGB.
    title : str, optional
        The title do display on the image. The default is ''.
        If '', then a timestamp will be displayed.

    Returns
    -------
    None.

    """
    rollback, back_prev = set_backend_inline()

    if(type(image) is list):
        for i in range(0,len(image),1):
            _print_one_image(image[i], cmap, convert_3ch_image, convert, title)
    else:
        _print_one_image(image, cmap, convert_3ch_image, convert, title)

    if(rollback):
        set_backend(back_prev)


def _print_one_image(myImg, cmap = None, convert_3ch_image = True, convert = cv2.COLOR_BGR2RGB, title='') :
    if(convert_3ch_image
       and splitable_in_3(myImg)):
        plt.imshow(cv2.cvtColor(myImg, convert))
    else:
        if(cmap is None and is_single_channel(myImg)):
            cmap = 'gray'
        plt.imshow(myImg, cmap)

    if(title != ''):
        title = title + '\n'

    plt.title(title + "{1}x{2} {3} {0}".format(datetime.datetime.now(), myImg.shape[0], myImg.shape[1], myImg.dtype))
    plt.show()