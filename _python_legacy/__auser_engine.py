# In the name of Allah

from .__tools import pingPongJson, FileToCPPHeaderConverter
from .__classes import Response
from .__UTAEndpoint import UTAEndpoint

import os

class AUserEngine:
    def __init__(self, username: str, public_key_file_path: str, iotis_gate_url: str):
        self.__public_key_file_path = public_key_file_path
        self.__username = username
        self.__iotis_gate_url = iotis_gate_url
        with open(self.__public_key_file_path, 'r') as file:
            pkey = file.read()
        self.__uta = UTAEndpoint(self.__username, pkey)

    def pingPong(self, ftype: str, args: dict) -> Response:
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
