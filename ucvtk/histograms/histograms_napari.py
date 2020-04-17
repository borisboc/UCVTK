# -*- coding: utf-8 -*-
"""
Interactive histograms within ROI
using napari viewer.

@author: Boris Bocquet <b.bocquet@akeoplus.com>
@license: LGPL V3.0
"""

# %%
import napari
import numpy as numpy
from ucvtk.utils.img_channels import is_single_channel, splitable_in_3, convert_BGR2RGB
from ucvtk.roi.draw_roi_napari import _layer_rect
import datetime

from typing import Callable
import cv2

# %%

MODE_DRAG = "drag"
_mode = None
_func_info = None


def open_interactive_histogram(img, convert_3ch_image = True, convert = cv2.COLOR_BGR2RGB, title = None):

    imgconv = convert_BGR2RGB(img, convert_3ch_image, convert)

    with napari.gui_qt():
        viewer = napari.view_image(imgconv)
        viewer.title = 'Interactive histogram'

        roi_layer = _layer_rect(imgconv, viewer)
        roi_layer.mode = 'select'

        #does not work : it looks like this is disconnecting the napari events (so unable to move the rectangle)        
        #roi_layer.on_mouse_release = _mouse_release
        #roi_layer.on_mouse_move = _mouse_move

        #TODO LATER : use roi_layer.to_masks
        
        @roi_layer.mouse_drag_callbacks.append
        def mouse_drag(layer, event):
            print("mouse_drag_callbacks {0}".format(datetime.datetime.now()))
            global _mode
            _mode = MODE_DRAG

        @roi_layer.mouse_move_callbacks.append
        def mouse_move(layer, event):
            global _mode
            if(_mode == MODE_DRAG):
                print("TODO STOP UPDATE {0}".format(datetime.datetime.now()))
            _mode = None            
        


def _mouse_release(event):
    #print("_mouse_release {0}".format(datetime.datetime.now()))
    global _mode
    _mode = None


def _mouse_move(event):
    global _mode
    #if(_mode == MODE_DRAG):
        #print("_mouse_move {0}".format(datetime.datetime.now()))

