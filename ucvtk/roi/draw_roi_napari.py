# -*- coding: utf-8 -*-
"""
Drawing Region Of Interest (ROI) on images
using napari viewer

@author: Boris Bocquet <b.bocquet@akeoplus.com>
@license: LGPL V3.0
"""

# %%
import napari
import numpy as np
import cv2
from ucvtk.utils.img_channels import is_single_channel, splitable_in_3, convert_BGR2RGB


# %%

def _draw_shape(img, func_layer, convert_3ch_image = True, convert = cv2.COLOR_BGR2RGB, split_channels = True, title = None):
    imgconv = convert_BGR2RGB(img, convert_3ch_image, convert)
    layer = None
    
    viewer = napari.Viewer()
    viewer.add_image(imgconv)

    if title is None:
        viewer.title = title
    else:
        viewer.title = 'Drawing ROI (Region Of Interest)'

    if(splitable_in_3(img) and split_channels):
        ch0, ch1, ch2 = cv2.split(img)
        viewer.add_image(ch0, name='channel 0', visible=False)
        viewer.add_image(ch1, name='channel 1', visible=False)
        viewer.add_image(ch2, name='channel 2', visible=False)

    layer = func_layer(img, viewer)
    layer.mode = 'select'

    viewer.show(block=True)
    
    if(type(layer.data) is list):
        return layer.data[0]
    else:
        return layer.data


def _layer_rect(img, viewer):
    # add rectangle
    rect = np.array([[img.shape[0]/4, img.shape[1]/4], [img.shape[0]*3/4, img.shape[1]*3/4]])
    layer = viewer.add_shapes(
        rect,
        shape_type='rectangle',
        edge_width=1,
        name='rectangle',
        opacity=0.1
    )
    return layer

def draw_rectangle(img: np.ndarray, convert_3ch_image: bool = True, convert: int = cv2.COLOR_BGR2RGB, split_channels: bool = True, title: str = "Draw rectangle") -> np.ndarray:
    """
    Open a napari viewer with an interactive rectangle ROI.

    Parameters
    ----------
    img : numpy.ndarray
        Image to display as background.
    convert_3ch_image : bool, optional
        If you want to enable an opencv convertion. The default is True.
    convert : int, optional
        The convertion to apply on the input image. See opencv cv2.cvtColor
        documentation. The default is cv2.COLOR_BGR2RGB.
    split_channels : bool, optional
        If you want the image channels to be splitted and
        displayed as different available layers on the napari viewer.
        The default is True.
    title : str, optional
        Title to display on he viewer. The default is "Draw rectangle".

    Returns
    -------
    numpy.ndarray
        The coordinates of the rectangle.
        The shape is (4,2).
        The ordering depens is always w.r.t the angle of the rectangle.
        NOT w.r.t the image.
        So if you rotate the rectangle with an angle ]-90, 90[ the ordering will be :
        rect[0,:] : Top left corner (row, column)
        rect[1,:] : Bottom left corner (row, column)
        rect[2,:] : Bottom right corner (row, column)
        rect[3,:] : Top right corner (row, column)

        You can help yourself using the "lever" (or joystick) on the rectangle
        of the napari viewer.
        It is has shown in the drawing bellow.

                        0
                        |
    rect[0,:]           |             rect[3,:]
        --------------------------------
        |                              |
        |                              |
        |                              |
        --------------------------------
    rect[1,:]                         rect[2,:]

    """
    return _draw_shape(img, _layer_rect, convert_3ch_image, convert, split_channels, title)

def _layer_point(img, viewer):
    # add rectangle
    pt = np.array([[img.shape[0]/2, img.shape[1]/2]])
    layer = viewer.add_points(
        pt
    )
    return layer

def draw_point(img: np.ndarray, convert_3ch_image: bool = True, convert: int = cv2.COLOR_BGR2RGB, split_channels: bool = True, title: str = "Draw point") -> np.ndarray:
    """
    Open a napari viewer with an interactive point ROI.

    Parameters
    ----------
    img : numpy.ndarray
        Image to display as background.
    convert_3ch_image : bool, optional
        If you want to enable an opencv convertion. The default is True.
    convert : int, optional
        The convertion to apply on the input image. See opencv cv2.cvtColor
        documentation. The default is cv2.COLOR_BGR2RGB.
    split_channels : bool, optional
        If you want the image channels to be splitted and
        displayed as different available layers on the napari viewer.
        The default is True.
    title : str, optional
        Title to display on he viewer. The default is "Draw point".

    Returns
    -------
    numpy.ndarray
        The coordinates of the point.
        The shape is (1,2)
        point[0,0] is row coordinate
        point[0,1] is column coordinate
    """
    return _draw_shape(img, _layer_point, convert_3ch_image, convert, split_channels, title)
