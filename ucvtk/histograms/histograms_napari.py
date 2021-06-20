# -*- coding: utf-8 -*-
"""
Interactive histograms within ROI
using napari viewer.

@author: Boris Bocquet <b.bocquet@akeoplus.com>
@license: LGPL V3.0
"""

# %%
import napari
import numpy as np
from ucvtk.utils.img_channels import is_single_channel, splitable_in_3, convert_BGR2RGB
from ucvtk.roi.draw_roi_napari import _layer_rect
from ucvtk.utils.matplotlib_backend import set_backend_qt, set_backend, NOT_IMPLEMENTED
import datetime
from typing import Callable
import cv2
import matplotlib.pyplot as plt
import mplcursors
from ucvtk.print.print_image_matplotlib import print_image

# %%

MODE_DRAG = "drag"
_mode = None
_func_info = None
_fig = None
_axs = None
_nbChannels = 0
_roi_layer = None
_imgconv = None
_img_layer = None
_lines = None


def open_interactive_histogram(img, convert_3ch_image = True, convert = cv2.COLOR_BGR2RGB, title = None):

    global _imgconv
    _imgconv = convert_BGR2RGB(img, convert_3ch_image, convert)

    global _nbChannels
    if(splitable_in_3(_imgconv)):
        _nbChannels = 3
    else:
        _nbChannels = 1
            
    rollback, back_prev = set_backend_qt()


    global _fig, _axs
    _fig, _axs = plt.subplots(1, _nbChannels, figsize=(9, 3), sharey=True)
    _fig.suptitle('Grayvalues histograms.You can click somewhere on a line. Right-click to deselect.')

    # _update_bars(imgconv)
    # mplcursors.cursor(_axs[0])

    
        
    if(rollback and back_prev != NOT_IMPLEMENTED):
        set_backend(back_prev)
    
    viewer = napari.Viewer()
    global _img_layer 
    _img_layer = viewer.add_image(_imgconv)
    viewer.title = 'Interactive histogram'

    global _roi_layer
    _roi_layer = _layer_rect(_imgconv, viewer)
    _roi_layer.mode = 'select'

    _update_bars_with_roi()

    # TODO LATER : use roi_layer.to_masks
    
    @_roi_layer.mouse_drag_callbacks.append
    def click_drag(layer, event):
        # print('mouse down')
        dragged = False
        yield
        # on move
        while event.type == 'mouse_move':
            # print(event.position)
            dragged = True
            yield
        # on release
        if dragged:
            print('drag end')
            _update_bars_with_roi()
        # else:
            # print('clicked!')
    
    # @_roi_layer.mouse_drag_callbacks.append
    # def mouse_drag(layer, event):
    #     print("mouse_drag_callbacks {0}".format(datetime.datetime.now()))
    #     # _update_bars_with_roi()
            
        
    #     global _mode
    #     _mode = MODE_DRAG
    #     _roi_layer.mouse_move_callbacks.append(_mouse_move)
        

    viewer.show(block = True)
    print("after run")
    plt.close(_fig);


def _update_bars_with_roi():
    global _roi_layer
    if(_roi_layer != None):
        print(_img_layer.data.shape)
        print(_imgconv.shape)
        mask_shape = (_img_layer.data.shape[0], _img_layer.data.shape[1])
        print(mask_shape)
        ms = _roi_layer.to_masks(mask_shape = mask_shape)[0,:,:]
        ms_conv =  ms.astype(np.uint8)
        print("count 0 = ", np.count_nonzero(ms_conv == 0))
        print("count 1 = ", np.count_nonzero(ms_conv == 1))
        print("sum == ", np.count_nonzero(ms_conv == 0) + np.count_nonzero(ms_conv == 1))
        print("shape ", mask_shape[0] * mask_shape[1])
        # print(type(ms_conv))
        # print(ms_conv.shape)
        # print(ms_conv.dtype)
        # print(ms_conv)
        _update_bars(_imgconv, ms_conv)

def _mouse_move(layer, event):
    print("mouse move")
    global _mode
    if(_mode == MODE_DRAG):
        print("TODO STOP UPDATE {0}".format(datetime.datetime.now()))
        layer.mouse_move_callbacks.remove(_mouse_move)
    _mode = None            

    
def _update_bars(img, mask = None):
    
    global _nbChannels, _axs, _fig, _lines
    
    
    if(_lines is None):
        first_time = True
        _lines = []
    else:
        first_time = False
         
    
    
    
    for c in range(0,_nbChannels):
        # hist_full = cv2.calcHist([img],[c],mask,[256],[0,255]) #not working properly ... I probably do something wrong
        hist_full = cv2.calcHist([img[:,:,c]],[0],mask,[256],[0,256])
        
        hist_sum = hist_full.sum()
        if(hist_sum.size != 0):
            hist_full = hist_full / hist_sum
        
        if(c % 3 == 0):
            colr = 'r'
        elif(c % 3 == 1):
            colr = 'g'
        elif(c % 3 == 2):
            colr = 'b'
        
        print("hist full {0} has mean value {1}".format(colr, hist_full.mean()))
        print("hist full size {0}".format(hist_full.size))
        
        if(first_time) :
            l, = _axs[c].plot(hist_full, color=colr)
            _lines.append(l)
            _axs[c].set_title("Channel {0}".format(c))
            mplcursors.cursor(_axs[c], multiple=True)
            plt.show()

        else :
            _lines[c].set_ydata(hist_full)
            _fig.canvas.draw()
            _fig.canvas.flush_events()
