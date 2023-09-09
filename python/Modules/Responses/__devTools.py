#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Mon Sep 04 2023
#
# Copyright (c) 2023 Abolfazl Danayi
# adanayidet@gmail.com
#

from ..._classes.__classes import Response, CommandResponse
import os
from base64 import b64decode


class LoadTagResponse(Response):
    @property
    def tag(self) -> dict:
        return self.result['tag']
    
    def __getitem__(self, key):
        # print('__getitem__', key)
        return self.tag[key]

    def __contains__(self, key):
        return key in self.tag
