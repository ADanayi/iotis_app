#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Mon Sep 04 2023
#
# Copyright (c) 2023 Abolfazl Danayi
# adanayidet@gmail.com
#

from .__base import ProductBase
from ..Modules import Camera, IOController


class GenericCam(ProductBase):
    def __init__(self, server_url: str):
        mods = [
            (Camera, {}),
            (IOController, {'OuputPortSize': 1})
        ]
        ProductBase.__init__(self, 'generic_cam', mods, server_url)

    @property
    def camera(self) -> Camera:
        return self['camera']

    @property
    def iocontroller(self) -> IOController:
        return self['iocontroller']
