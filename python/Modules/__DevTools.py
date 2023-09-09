#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Thu Sep 07 2023
#
# Copyright (c) 2023 Abolfazl Danayi
# adanayidet@gmail.com
#

from .__ModuleBase import ModuleBase
from .._classes.__classes import CommandResponse, Response

from .Responses.__devTools import LoadTagResponse

from typing import Optional
import json
import traceback


class DevTools(ModuleBase):
    def __init__(self, server_url: str):
        ModuleBase.__init__(self, 'devtools', server_url)

    def restart_on_normal_mode(self, uid: Optional[str] = None) -> CommandResponse:
        return self._pingPong('restart', {'mode': 'normal'}, CommandResponse, uid)

    def restart_on_config_mode(self, uid: Optional[str] = None) -> CommandResponse:
        return self._pingPong('restart', {'mode': 'config'}, CommandResponse, uid)

    def save_tag(self, tag: dict, uid: Optional[str] = None) -> Response:
        """The tag can be used to save user information on IoTiS server for your own application development
The tag should be less than 10 KBytes (a jsonable dict)"""
        if type(tag) != dict:
            raise Exception('Tag should be a python dict (jsonable)')
        try:
            tag = json.loads(json.dumps(tag))
        except KeyboardInterrupt:
            exit(0)
        except:
            traceback.print_exc()
            raise Exception('Tag is not jsonable')
        if len(str(tag)) > 10*1024:
            raise Exception('Tag size must be less than 10 KBytes')
        return self._pingPong('save_tag', {'tag': tag}, Response, uid)

    def load_tag(self, uid: Optional[str] = None) -> LoadTagResponse:
        """The tag can be used to save user information on IoTiS server for your own application development
The tag should be less than 10 KBytes (a jsonable dict)"""
        return self._pingPong('load_tag', {}, LoadTagResponse, uid)
