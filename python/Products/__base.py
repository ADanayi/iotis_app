#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Mon Sep 04 2023
#
# Copyright (c) 2023 Abolfazl Danayi
# adanayidet@gmail.com
#

from ..Modules.__ModuleBase import ModuleBase
from ..Modules import DevTools 
import typing as T


class ProductBase:
    def __init__(self, product_name: str, ModuleClasses: T.List[list], server_url: str):
        self.__product_name = product_name
        self.__mods = {}
        for ModuleCls, kwargs in ModuleClasses:
            kwargs['server_url'] = server_url
            mod = ModuleCls(**kwargs)
            self.__mods[mod.name] = mod
        if not 'devtools' in self.__mods:
            self.__mods['devtools'] = DevTools(server_url)
        
    def __getitem__(self, kw: str):
        return self.__mods[kw]

    def use_device_creds(self, uid: str, pkey_file_path: str):
        for mod in self.__mods.values():
            mod.use_device_creds(uid, pkey_file_path)

    def use_owner_creds(self, owner_username: str, pkey_file_path: str):
        for mod in self.__mods.values():
            mod.use_owner_creds(owner_username, pkey_file_path)

    @property
    def product_name(self) -> str:
        return self.__product_name

    @property
    def devtools(self) -> DevTools:
        return self['devtools']

    @property
    def connected(self) -> bool:
        """Checks if the node is connected or not?
Note: If you're using this class in owner_creds mode, use uid_is_connected(uid) method, instead of this property!"""
        return self.devtools.is_connected().connected
    
    def uid_is_connected(self, uid: str) -> bool:
        return self.devtools.is_connected(uid=uid).connected

    @property
    def creds_mode(self) -> T.Optional[str]:
        """Returns either None, 'device' or 'owner' based on the use_x_creds function called!"""
        return self.devtools.creds_mode
    
    def __bool__(self) -> bool:
        if self.creds_mode != 'device':
            raise Exception('Can not use __bool__ method is non-device creds mode')
        return self.connected
