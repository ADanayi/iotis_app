#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Sun Sep 03 2023
#
# Copyright (c) 2023 Abolfazl Danayi
# adanayidet@gmail.com
#

from ._GateBase import GateBase


class DeviceGate(GateBase):
    def __init__(self, uid: str, pkey_file_path: str, gate_url: str):
        GateBase.__init__(self, 'uid', uid, pkey_file_path, gate_url)
        self.__uid = uid

    @property
    def uid(self) -> str:
        return self.__uid
