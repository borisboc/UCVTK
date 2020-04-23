# -*- coding: utf-8 -*-
"""
Handling  matplotlib "inline" / QT backend.

@author: Boris Bocquet <b.bocquet@akeoplus.com>
@license: LGPL V3.0
"""

# %%

import matplotlib as mpl
import IPython as ip

_backend = ''
NOT_IMPLEMENTED = 'not implemented'

# %%

def _debug_print(*message):
    #print(message)
    return None

# %%

def update_backend():
    global _backend
    _backend = mpl.backends.matplotlib.backends.backend.title()
    _debug_print('update_backend returns ', _backend)

def set_backend_inline():
    update_backend()
    if(_backend.count('Inline') > 0):
        _debug_print('no need to set Inline backend')
        return False, _backend
    else:
        if(_backend.count('Qt')):
            backend_prev = 'qt'
        else:
            backend_prev = NOT_IMPLEMENTED

        _debug_print('force backend inline, because current is ', backend_prev)
        set_backend('inline')
        return True, backend_prev
    
def set_backend_qt():
    update_backend()
    if(_backend.count('Qt') > 0):
        _debug_print('no need to set Qt backend')
        return False, _backend
    else:
        if(_backend.count('inline')):
            backend_prev = 'inline'
        else:
            backend_prev = NOT_IMPLEMENTED

        _debug_print('force backend Qt, because current is ', backend_prev)
        set_backend('qt')
        return True, backend_prev

def set_backend(backn):
    ip.get_ipython().run_line_magic('matplotlib', backn)
    update_backend()

