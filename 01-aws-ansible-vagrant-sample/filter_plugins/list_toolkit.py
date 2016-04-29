

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import math
import collections
from ansible import errors



def lst_slice(lst,a,b):
    if isinstance(a,int) and isinstance(b,int):
        # c = set(a) & set(b)
    # else:
        # c = unique(filter(lambda x: x in b, a))
        return lst[a:b]

class FilterModule(object):
    ''' Ansible math jinja2 filters '''

    def filters(self):
        return {
            # general math

            'lst_slice' : lst_slice,

        }