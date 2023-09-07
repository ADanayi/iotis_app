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

from typing import Optional, List

from .._classes.__classes import Response, CommandResponse


class IOController(ModuleBase):
    def __init__(self, OuputPortSize: int, server_url: str):
        ModuleBase.__init__(self, 'iocontroller', server_url)
        self.__osize = OuputPortSize

    def write_output_port(self, port: List[bool], uid: Optional[str] = None) -> CommandResponse:
        pass
        # if type(port) not in (tuple, list):
        #     raise Exception('Port must be tuple or list')
        # if len(port) != self.__osize:
        #     raise Exception('Port size mismatch')
        # return self._pingPong('capture', {
        #     'flasher': flasher
        # }, CommandResponse, uid)

    def write_output_pin(self, pin: int, value: bool, uid: Optional[str] = None) -> CommandResponse:
        if pin < 0 or pin >= self.__osize:
            raise Exception('Bad pin number value')
        return self._pingPong('write_output_pin', {
            'pin': int(pin),
            'value': bool(value)
        }, CommandResponse, uid)
