#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Mon Sep 04 2023
#
# Copyright (c) 2023 Abolfazl Danayi
# adanayidet@gmail.com
#

from .__ModuleBase import ModuleBase
from .Responses.__camera import CaptureResponse, CapturedResponse, ImageResponse, SetFlasherResponse

from typing import Optional


class Camera(ModuleBase):
    def __init__(self, server_url: str):
        ModuleBase.__init__(self, 'camera', server_url)

    def capture(self, flasher: bool = True, uid: Optional[str] = None) -> CaptureResponse:
        return self._pingPong('capture', {
            'flasher': flasher
        }, CaptureResponse, uid)

    def captured(self, uid: Optional[str] = None) -> CapturedResponse:
        return self._pingPong('captured', {}, CapturedResponse, uid)

    def image(self, uid: Optional[str] = None) -> ImageResponse:
        return self._pingPong('image', {}, ImageResponse, uid)

    def set_flasher(self, flasher: bool, uid: Optional[str] = None) -> SetFlasherResponse:
        return self._pingPong('set_flasher', {'flasher': flasher}, SetFlasherResponse, uid)
