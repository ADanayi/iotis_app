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
from .._UserGate import UserGate
from .._classes.__classes import Response

from typing import Optional


class ModuleBase:
    def __init__(self, module_name: str, server_url: str, loc_prefix: str = '/v1/modules'):
        self.__name = module_name
        self.__server_url = server_url
        self.__loc_prefix = loc_prefix
        self.__gate_url = server_url + loc_prefix + '/' + module_name
        self.__gate = None
        self.__use_mode = None

    def use_device_creds(self, uid: str, pkey_file_path: str):
        self.__gate = DeviceGate(uid, pkey_file_path, self.__gate_url)
        self.__use_mode = 'device'

    def use_owner_creds(self, owner_username: str, pkey_file_path: str):
        self.__gate = UserGate(owner_username, pkey_file_path, self.__gate_url)
        self.__use_mode = 'owner'

    def _pingPong(self, ftype: str, args: dict, TargetClass=Response, uid: Optional[str] = None) -> Response:
        if self.__use_mode is None:
            raise Exception(
                'Please call either use_device_creds or use_owner_creds first')
        if self.__use_mode == 'device':
            if uid != None and uid != self.__gate.uid:
                raise Exception('Can not use another uid in device_creds mode')
            return self.__gate._pingPong(ftype, args, TargetClass)
        else:
            if uid == None:
                raise Exception('UID can not be left None in owner_creds mode')
            return self.__gate._pingPong(ftype, args, TargetClass, {'uid': uid})

    @property
    def name(self) -> str:
        return self.__name
