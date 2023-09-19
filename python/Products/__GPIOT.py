#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Wed Sep 13 2023
#
# Copyright (c) 2023 Abolfazl Danayi
# adanayidet@gmail.com
#

from .__base import ProductBase
from ..Modules import Camera, IOController


class GPIOT(ProductBase):
    def __init__(self, server_url: str):
        mods = [
            (IOController, {'OutputPortSize': 8})
        ]
        ProductBase.__init__(self, 'gpiot', mods, server_url)

    @property
    def iocontroller(self) -> IOController:
        return self['iocontroller']
