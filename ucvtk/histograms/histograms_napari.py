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
from ucvtk.utils.matplotlib_backend import set_backend_qt, set_backend, NOT_IMPLEMENTED
import datetime
from typing import Callable
import cv2
import matplotlib.pyplot as plt
import mplcursors


# %%

MODE_DRAG = "drag"
_mode = None
_func_info = None
_fig = None
_axs = None
_nbChannels = 0

def open_interactive_histogram(img, convert_3ch_image = True, convert = cv2.COLOR_BGR2RGB, title = None):


    imgconv = convert_BGR2RGB(img, convert_3ch_image, convert)

    global _nbChannels
    if(splitable_in_3(imgconv)):
        _nbChannels = 3
    else:
        _nbChannels = 1
            
    rollback, back_prev = set_backend_qt()


    global _fig, _axs
    _fig, _axs = plt.subplots(1, _nbChannels, figsize=(9, 3), sharey=True)
    _fig.suptitle('Grayvalues histograms.You can click somewhere on a line. Right-click to deselect.')

    _update_bars(imgconv)
    # hist_full = cv2.calcHist([imgconv],[0],None,[256],[0,256])
    # _axs[0].plot(hist_full)
    # mplcursors.cursor(_axs[0])

    
        
    if(rollback and back_prev != NOT_IMPLEMENTED):
        set_backend(back_prev)
            
    with napari.gui_qt():
        viewer = napari.view_image(imgconv)
        viewer.title = 'Interactive histogram'

        roi_layer = _layer_rect(imgconv, viewer)
        roi_layer.mode = 'select'


        #TODO LATER : use roi_layer.to_masks
        
        @roi_layer.mouse_drag_callbacks.append
        def mouse_drag(layer, event):
            print("mouse_drag_callbacks {0}".format(datetime.datetime.now()))
            global _mode
            _mode = MODE_DRAG
            roi_layer.mouse_move_callbacks.append(_mouse_move)

    plt.close(_fig);


def _mouse_move(layer, event):
    global _mode
    if(_mode == MODE_DRAG):
        print("TODO STOP UPDATE {0}".format(datetime.datetime.now()))
        layer.mouse_move_callbacks.remove(_mouse_move)
    _mode = None            

def _update_bars(img):
    
    global _nbChannels, _axs
    for c in range(0,_nbChannels):
        hist_full = cv2.calcHist([img],[c],None,[256],[0,256])
        if(c % 3 == 0):
            colr = 'r'
        elif(c % 3 == 1):
            colr = 'g'
        elif(c % 3 == 2):
            colr = 'b'

        _axs[c].plot(hist_full, color=colr)
        _axs[c].set_title("Channel {0}".format(c))
        mplcursors.cursor(_axs[c], multiple=True)