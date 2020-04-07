# -*- coding: utf-8 -*-
"""
Drawing Region Of Interest (ROI) on images
using napari viewer

@author: Boris Bocquet <b.bocquet@akeoplus.com>
@license: LGPL V3.0
"""

# %%
import napari
import numpy as numpy
from ucvtk.utils.img_channels import is_single_channel, splitable_in_3, convert_BGR2RGB
from typing import Callable

# %%

ADDING_BLOBS = "ADDING BLOBS !!"
REMOVING_BLOBS = "REMOVING BLOBS !!"
INFO_BLOBS = "BLOB INFO : "

MODE_ADD = "add"
MODE_REMOVE = "remove"
MODE_INFO = "info"
selected_labels_layer = None
mode = None

def open_blob_management(img: numpy.ndarray, labels: numpy.ndarray, funcInfoBlobs: Callable[[],str]=None) -> numpy.ndarray:
    """
    Open a napari viewer where the blobs are displayed.
    The viewer is an interactive GUI where you can click on the blobs.
    Depending if you are in "add" mode ('a') or "remove" ('r'),
    this will add or remove the clicked blobs on the 'selected_labels_layer' layer.
    That will be output.
    
    Press 'i' (for 'info') to get some informations on the blob you click onto.
    Press 'a' (for 'adding') to add the blobs you click on to a selection (see return).
    Press 'r' (for 'removing') to remove a blob you have previously selected.

    TODO : blob info 'i'

    Parameters
    ----------
    img : numpy.ndarray
        The background image. E.g., the image where the blobs come from.
    labels : numpy.ndarray
        The blobs / connected components. As 'label image'.
        E.g. coming from cv2.connectedComponents
    funcInfoBlobs : Callable[[],str], optional
        A function called on the clicked blob.
        It will return some informations on the blob as string output.
        This string is displayed on the napari 'status' (bottom left).
        The default is None.

    Returns
    -------
    numpy.ndarray
        The selected blobs / connected components (clicked by user).
        As 'label image'.

    """

    global mode
    mode = None

    with napari.gui_qt():
        viewer = napari.view_image(img)
        viewer.title = 'Blob analysis and selection'

        # add the labels
        global selected_labels_layer
        selected_labels = numpy.copy(labels)
        selected_labels[:] = 0
        selected_labels_layer = viewer.add_labels(selected_labels, name='selected blobs', visible=True)

        labels_layer = viewer.add_labels(labels, name='blobs')

        @viewer.bind_key('a')
        def add_blob(viewer):
            global mode
            mode = MODE_ADD
            viewer.title = ADDING_BLOBS

        @viewer.bind_key('r')
        def remove_blob(viewer):
            global mode
            mode = MODE_REMOVE
            viewer.title = REMOVING_BLOBS

        @viewer.bind_key('i')
        def info_blob(viewer):
            global mode
            mode = MODE_INFO
            viewer.title = INFO_BLOBS

        @labels_layer.mouse_drag_callbacks.append
        def get_connected_component_shape(layer, event):
            cords = numpy.round(layer.coordinates).astype(int)
            val = layer.get_value()
            msg = ''
            if val is None:
                return
            if val != 0:
                data = layer.data
                binary = data == val

                global selected_labels_layer
                selected_labels = selected_labels_layer.data

                if(mode == MODE_ADD):
                    selected_labels[binary] = data[binary]
                    msg = f'clicked at {cords} on blob {val}'
                elif(mode == MODE_REMOVE):
                    selected_labels[binary] = 0
                    msg = f'clicked at {cords} on blob {val}'

                selected_labels_layer.data = selected_labels

            else:
                msg = f'clicked at {cords} on background which is ignored'
            layer.status = msg

    return selected_labels_layer.data
