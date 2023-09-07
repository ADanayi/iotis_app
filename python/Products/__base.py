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
import typing as T


class ProductBase:
    def __init__(self, product_name: str, ModuleClasses: T.List[list], server_url: str):
        self.__product_name = product_name
        self.__mods = {}
        for ModuleCls, kwargs in ModuleClasses:
            kwargs['server_url'] = server_url
            mod = ModuleCls(**kwargs)
            self.__mods[mod.name] = mod
        
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
