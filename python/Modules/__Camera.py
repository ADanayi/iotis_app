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

class Camera(ModuleBase):
    def __init__(self, uid: str, pkey_file_path: str, server_url: str):
        ModuleBase.__init__(self, 'camera', uid, pkey_file_path, server_url)

    def capture(self, flasher: bool = True) -> CaptureResponse:
        return self._pingPong('capture', {
            'flasher': flasher
        }, CaptureResponse)

    def captured(self) -> CapturedResponse:
        return self._pingPong('captured', {}, CapturedResponse)

    def image(self) -> ImageResponse:
        return self._pingPong('image', {}, ImageResponse)

    def set_flasher(self, flasher: bool) -> SetFlasherResponse:
        return self._pingPong('set_flasher', {'flasher': flasher}, SetFlasherResponse)
