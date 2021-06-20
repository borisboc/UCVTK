# -*- coding: utf-8 -*-
"""
Utils functions to handle the image channels.

@author: Boris Bocquet <b.bocquet@akeoplus.com>
@license: LGPL V3.0
"""

# %%

import numpy as np
import cv2

# %%

def _convert(img: np.ndarray, convert_3ch_image: bool = True, convert: int = cv2.COLOR_BGR2RGB) -> np.ndarray:
    if(convert_3ch_image
       and type(img) == np.ndarray
       and img.ndim == 3
       and img.shape[2] == 3):
        imgConv = cv2.cvtColor(img, convert)
    else:
        imgConv = img
    return imgConv

def convert_BGR2RGB(img: np.ndarray, convert_3ch_image: bool = True, convert: int = cv2.COLOR_BGR2RGB) -> np.ndarray:
    return _convert(img, convert_3ch_image=convert_3ch_image, convert=convert)

def convert_RGB2BGR(img: np.ndarray, convert_3ch_image: bool = True, convert: int = cv2.COLOR_RGB2BGR) -> np.ndarray:
    return _convert(img, convert_3ch_image=convert_3ch_image, convert=convert)

def split_image(img: np.ndarray, channel_num: int) -> np.ndarray:
    if(splitable_in_3(img)):
        ch0, ch1, ch2 = cv2.split(img)
        if(channel_num == 0):
            return ch0
        elif(channel_num == 1):
            return ch1
        elif(channel_num == 2):
            return ch2
        else:
            return img
    else:
        return img

def splitable_in_3(img: np.ndarray) -> bool:
    if(type(img) == np.ndarray
       and img.ndim == 3
       and img.shape[2] == 3):
        return True
    else:
        return False

def is_single_channel(img: np.ndarray) -> bool:
    if(type(img) == np.ndarray
       and img.ndim == 2
       or (img.ndim == 3 and img.shape[2] == 1)):
        return True
    else:
        return False
