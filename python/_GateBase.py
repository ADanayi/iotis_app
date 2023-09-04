#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Sun Sep 03 2023
#
# Copyright (c) 2023 Abolfazl Danayi
# adanayidet@gmail.com
#

from ._classes.__tools import pingPongJson
from ._classes.__classes import Response
from ._classes.__UTAEndpoint import UTAEndpoint

import json
from urllib.parse import urlparse


class GateBase:
    def __init__(self, identifier_kw: str, identifier_value: str, pkey_file_path: str, gate_url: str):
        try:
            result = urlparse(gate_url)
        except:
            raise Exception('Bad url %s' % (gate_url))
        if not all([result.scheme, result.netloc]):
            raise Exception('Bad url %s' % (gate_url))
        self.__identifier_kw = identifier_kw
        self.__identifier_value = identifier_value
        self.__gate_url = gate_url
        with open(pkey_file_path, 'r') as file:
            pkey = file.read()
        self.__uta = UTAEndpoint(identifier_value, pkey)

    def _pingPong(self, ftype: str, args: dict, TargetClass=Response) -> Response:
        signature = self.__uta.sign()
        req = {
            "type": ftype,
            "signature": signature,
            "args": args
        }
        req[self.__identifier_kw] = self.__identifier_value
        try:
            jresp = pingPongJson(self.__gate_url, req)
        except KeyboardInterrupt:
            exit(1)
        except:
            jresp = {
                'status': 'error',
                'result': {
                    'error': '#-1'
                }
            }
        return TargetClass(jresp)
