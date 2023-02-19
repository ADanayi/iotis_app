# In the name of Allah

from .__tools import pingPongJson, FileToCPPHeaderConverter
from .__classes import Response
from .__UTAEndpoint import UTAEndpoint

import os

class _DeviceModuleEngineBase:
    def __init__(self, uid: str, node_key_file_path: str, iotis_gate_url: str):
        self.__node_key_file_path = node_key_file_path
        self.__uid = uid
        self.__iotis_gate_url = iotis_gate_url
        with open(self.__node_key_file_path, 'r') as file:
            pkey = file.read()
        self.__uta = UTAEndpoint(self.__uid, pkey)

    def pingPong(self, ftype: str, args: dict) -> Response:
        signature = self.__uta.sign()
        req = {
            "type": ftype,
            "uid": self.__uid,
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
