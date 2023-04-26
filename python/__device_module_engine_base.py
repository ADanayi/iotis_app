# In the name of Allah

from .__tools import pingPongJson, FileToCPPHeaderConverter
from .__classes import Response
from .__UTAEndpoint import UTAEndpoint

import os

class _DeviceModuleEngineBase:
    def __init__(self, uid: str, iotis_gate_url: str):
        self.__uid = uid
        self.__iotis_gate_url = iotis_gate_url
        self.__mode = None
    
    def auth_by_device(self, node_key_file_path: str):
        with open(node_key_file_path, 'r') as file:
            pkey = file.read()
        self.__uta = UTAEndpoint(self.__uid, pkey)
        self.__mode = 'd'

    def auth_by_auser(self, username: str, auser_key_file_path: str):
        self.__auser = username
        with open(auser_key_file_path, 'r') as file:
            pkey = file.read()
        self.__uta = UTAEndpoint(self.__auser, pkey)
        self.__mode = 'a'

    def pingPong(self, ftype: str, args: dict) -> Response:
        if self.__mode is None:
            raise Exception('First call one of auth_... methods to initialize')
        signature = self.__uta.sign()
        req = {
            'type': ftype,
            'args': args,
            'uid': self.__uid,
            'signature': signature
        }
        if self.__mode == 'a':
            req['username'] = self.__auser
        # print(req)
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
