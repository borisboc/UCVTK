# -*- coding: utf-8 -*-

"""
Interactive histograms within ROI
using napari viewer.

@author: Boris Bocquet <borisboc@free.fr>
@license: LGPL V3.0
"""

# %%
import napari
import numpy as np
from ucvtk.utils.img_channels import splitable_in_3, convert_BGR2RGB, convert_RGB2BGR
from ucvtk.roi.draw_roi_napari import _layer_rect
from ucvtk.utils.matplotlib_backend import set_backend_qt, set_backend, NOT_IMPLEMENTED
import cv2
import matplotlib.pyplot as plt
import mplcursors

# %%

_fig = None
_axs = None
_nbChannels = 0
_roi_layer = None
_img_layer = None
_lines = None


def _init_global():
    global _fig, _axs, _nbChannels, _roi_layer, _img_layer, _lines
    _fig = None
    _axs = None
    _nbChannels = 0
    _roi_layer = None
    _img_layer = None
    _lines = None


def open_interactive_histogram(img: np.ndarray, convert_3ch_image: bool = True, convert: int = cv2.COLOR_BGR2RGB):
    """
    The goal of this tool is for analysing the grayvalue distribution
    thanks to an interactive rectangle you can move on the image.
    This is usefull when you want to check the contrasts and estimate
    local threshold values (i.e. for color segementation, edges etc.)

    This function opens a napari viewer with an interactive rectangle.
    In parallel, there is a matplotlib figure showing, with 1 or 3 graphs(depending on the number of channels).
    The histogram(s) of the grayvalues inside the rectangle are printed in the graph(s).
    Resize and move the rectangle in the regions where you want to study the grayvalues distributions.

    Parameters
    ----------
    img : np.ndarray
        The RGB image, or the BGR image (convert_3ch_image == True, convert == cv2.COLOR_BGR2RGB),
        or the grayscale image.
    convert_3ch_image : bool, optional
        If you want to enable an opencv convertion. The default is True.
    convert : int, optional
        The convertion to apply on the input image. See opencv cv2.cvtColor
        documentation. The default is cv2.COLOR_BGR2RGB.

    Returns
    -------
    None.

    """

    _init_global()

    img_rgb = convert_BGR2RGB(img, convert_3ch_image, convert)

    global _nbChannels
    if(splitable_in_3(img_rgb)):
        _nbChannels = 3
    else:
        _nbChannels = 1

    rollback, back_prev = set_backend_qt()

    global _fig, _axs
    _fig, _axs = plt.subplots(1, _nbChannels, figsize=(15, 5), sharey=True)

    if(_nbChannels == 1):
        _axs = [_axs]

    _fig.suptitle('Grayvalues histograms.You can click somewhere on a line. Right-click to deselect.')

    if(rollback and back_prev != NOT_IMPLEMENTED):
        set_backend(back_prev)

    viewer = napari.Viewer()

    global _img_layer
    _img_layer = viewer.add_image(img_rgb)
    viewer.title = 'Interactive histogram'

    global _roi_layer
    _roi_layer = _layer_rect(img_rgb, viewer)
    _roi_layer.mode = 'select'

    _update_bars_with_roi()

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
            # print('drag end')
            _update_bars_with_roi()
        # else:
            # print('clicked!')

    viewer.show(block=True)
    plt.close(_fig)


def _update_bars_with_roi():
    global _roi_layer, _img_layer
    if((_roi_layer is not None) and (_img_layer is not None)):
        mask_shape = (_img_layer.data.shape[0], _img_layer.data.shape[1])
        ms = _roi_layer.to_masks(mask_shape=mask_shape)[0, :, :]
        ms_conv = ms.astype(np.uint8)
        _update_bars(_img_layer.data, ms_conv)


def _update_bars(img_rgb, mask=None):

    global _nbChannels, _axs, _fig, _lines

    if(_lines is None):
        first_time = True
        _lines = []
    else:
        first_time = False

    for c in range(0, _nbChannels):
        # hist_full = cv2.calcHist([img_rgb],[c],mask,[256],[0,255]) #not working properly ... I probably do something wrong

        if(_nbChannels == 1):
            hist_full = cv2.calcHist([img_rgb], [0], mask, [256], [0, 256])
        else:
            hist_full = cv2.calcHist([img_rgb[:, :, c]], [0], mask, [256], [0, 256])

        hist_sum = hist_full.sum()

        if(hist_sum.size != 0):
            hist_full = hist_full / hist_sum

        if(c % 3 == 0):
            colr = 'r'
        elif(c % 3 == 1):
            colr = 'g'
        elif(c % 3 == 2):
            colr = 'b'

        if(first_time):
            l, = _axs[c].plot(hist_full, color=colr)
            _lines.append(l)
            _axs[c].set_title("Channel {0}".format(c))
            _axs[c].set_ylim([-0.1, 1.1])
            mplcursors.cursor(_axs[c], multiple=True)
            plt.show()

        else:
            _lines[c].set_ydata(hist_full)
            _fig.canvas.draw()
            _fig.canvas.flush_events()
