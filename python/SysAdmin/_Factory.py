#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Sun Sep 03 2023
#
# Copyright (c) 2023 Abolfazl Danayi
# adanayidet@gmail.com
#

from .._UserGate import UserGate
from .._classes.__classes import MessageType
from .._classes.__classes import Response
from .._classes.__tools import FileToCPPHeaderConverter

import json
import os


class Factory(UserGate):
    def __init__(self, username: str, pkey_path: str, server_url: str, gate_address: str = '/v1/modules/factory'):
        """Note: server_location points to the root url of server; includes http or https at the beginning."""
        UserGate.__init__(self, username, pkey_path, server_url + gate_address)

    def generate_device(self, device_model: str, owners: list = [], modules: list = []) -> 'GenerateDeviceResponse':
        r = self._pingPong('generate_device', {
            'device_model': device_model,
            'owners': owners,
            'modules': modules
        }, GenerateDeviceResponse)
        return r

    def save_device(self, uid: str, path: str) -> bool:
        pkey_resp = self.get_pkey(uid)
        if not pkey_resp:
            return False
        self.__save(path, uid, pkey_resp.result['pkey'])
        return True

    def ack_code_upload(self, uid: str, code_version: str, app_code_version: str) -> Response:
        return self._pingPong('ack_code_upload', {
            'code_version': code_version,
            'app_code_version': app_code_version,
            'uid': uid
        })

    def ack_code_reupload(self, uid: str, code_version: str, app_code_version: str) -> Response:
        return self._pingPong('ack_code_reupload', {
            'code_version': code_version,
            'app_code_version': app_code_version,
            'uid': uid
        })

    def lock_device(self, uid: str) -> Response:
        return self._pingPong('lock_device', {'uid': uid})

    def unlock_device(self, uid: str) -> Response:
        return self._pingPong('unlock_device', {'uid': uid})

    def get_pkey(self, uid: str) -> Response:
        return self._pingPong('get_pkey', {'uid': uid})


###############
class GenerateDeviceResponse(Response):
    @property
    def uid(self) -> str:
        return self['uid']

    @property
    def pkey(self) -> str:
        return self['pkey']

    def save(self, path: str):
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, 'uid.h'), 'w') as uid_file:
            uid_file.write(
                """// In the name of Allah

#ifndef __LI_UID_H
#define __LI_UID_H

namespace li
{{
const char *const uid = "{}";
}}

#endif

""".format(self.uid)
            )
        key_pub_path = os.path.join(path, 'pkey.pub')
        key_h_path = os.path.join(path, 'pkey.h')
        with open(key_pub_path, 'w') as pkey_pub_file:
            pkey_pub_file.write(self.pkey)
        FileToCPPHeaderConverter.convert(
            key_pub_path, key_h_path, 'pkey', namespace='li', define_length=False)
        os.remove(key_pub_path)
