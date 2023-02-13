# In the name of Allah

from .__tools import pingPongJson, FileToCPPHeaderConverter
from .__classes import Response
from .__UTAEndpoint import UTAEndpoint

import os

class FactoryEngine:
    def __init__(self, username: str, public_key_file_path: str, iotis_gate_url: str):
        self.__public_key_file_path = public_key_file_path
        self.__username = username
        self.__iotis_gate_url = iotis_gate_url
        with open(self.__public_key_file_path, 'r') as file:
            pkey = file.read()
        self.__uta = UTAEndpoint(self.__username, pkey)

    def _pingPong(self, ftype: str, args: dict) -> Response:
        signature = self.__uta.sign()
        req = {
            "type": ftype,
            "username": self.__username,
            "signature": signature,
            "args": args
        }
        try:
            jresp = pingPongJson(self.__iotis_gate_url, req)
        except KeyboardInterrupt:
            exit(1)
        except:
            jresp = {
                'status': 'error',
                'result': {
                    'error': '#-1'
                }
            }
        return Response(jresp)

    def generate_device(self, device_model: str, owners: list = [], save_to_path: str = None) -> Response:
        r = self._pingPong('generate_device', {
            'device_model': device_model,
            'owners': owners
        })
        if not r:
            return r
        if save_to_path is not None:
            self.__save(path, **r.result)
        return r

    def save_device(self, uid: str, path: str) -> bool:
        pkey_resp = self.get_pkey(uid)
        if not pkey_resp:
            return False
        self.__save(path, uid, pkey_resp.result['pkey'])
        return True

    def __save(self, path: str, uid: str, pkey: str):
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

""".format(uid)
    )
        key_pub_path = os.path.join(path, 'pkey.pub')
        key_h_path = os.path.join(path, 'pkey.h')
        with open(key_pub_path, 'w') as pkey_pub_file:
            pkey_pub_file.write(pkey)
        FileToCPPHeaderConverter.convert(
            key_pub_path, key_h_path, 'pkey', namespace='li', define_length=False)
        os.remove(key_pub_path)
    
    def ack_code_upload(self, uid: str, code_version: str, app_code_version: str) -> Response:
        return self._pingPong('ack_code_upload', {
            'code_version': code_version,
            'app_code_version': app_code_version
        })

    def ack_code_reupload(self, uid: str, code_version: str, app_code_version: str) -> Response:
        return self._pingPong('ack_code_reupload', {
            'code_version': code_version,
            'app_code_version': app_code_version
        })
    
    def lock_device(self, uid: str) -> Response:
        return self._pingPong('lock_device', {'uid': uid})
    
    def unlock_device(self, uid: str) -> Response:
        return self._pingPong('unlock_device', {'uid': uid})
    
    def get_pkey(self, uid: str) -> Response:
        return self._pingPong('get_pkey', {'uid': uid})
