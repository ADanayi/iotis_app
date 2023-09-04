#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Mon Sep 04 2023
#
# Copyright (c) 2023 Abolfazl Danayi
# adanayidet@gmail.com
#

from .._DeviceGate import DeviceGate


class ModuleBase(DeviceGate):
    def __init__(self, module_name: str, uid: str, pkey_file_path: str, server_url: str, loc_prefix: str = '/v1/modules'):
        DeviceGate.__init__(self, uid, pkey_file_path,
                            server_url + loc_prefix + '/' + module_name)
        self.__name = module_name

    @property
    def name(self) -> str:
        return self.__name
