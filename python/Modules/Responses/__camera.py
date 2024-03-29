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


CaptureResponse = CommandResponse


class CapturedResponse(Response):
    @property
    def captured(self) -> bool:
        if self.result['captured'] is None:
            return False
        else:
            return self.result['captured']

    def __bool__(self) -> bool:
        return Response.__bool__(self) and self.captured


class ImageResponse(Response):
    @property
    def timestamp(self) -> str:
        return self.result['img']['time']

    @property
    def data(self) -> bytes:
        return b64decode(
            self.result['img']['data']
        )

    def save(self, parent_folder: str) -> str:
        """Saves the file and returns the filename"""
        os.makedirs(parent_folder, exist_ok=True)
        ts = self.timestamp
        for ch in ('/ ,:*?|'):
            ts = ts.replace(ch, '_')
        filename = f"{ts}.jpeg"
        with open(os.path.join(parent_folder, filename), 'wb') as file:
            file.write(self.data)
        return filename

    def __bool__(self):
        return Response.__bool__(self) and self.result


SetFlasherResponse = CommandResponse
