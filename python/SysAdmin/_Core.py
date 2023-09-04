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

import json


class Core(UserGate):
    def __init__(self, username: str, pkey_path: str, server_url: str, gate_address: str = '/v1/core'):
        """Note: server_location points to the root url of server; includes http or https at the beginning."""
        UserGate.__init__(self, username, pkey_path, server_url + gate_address)

    def __prepare_message(self, message: MessageType) -> str:
        if type(message) not in (dict, str, bytes):
            raise Exception(
                'Bad message type. Only dict, str and bytes are allowed.')
        if type(message) == dict:
            return json.dumps(message)
        return message

    def send_message_to_node(self, uid: str, message: MessageType) -> Response:
        return self._pingPong('send_message', {
            'uid': uid,
            'message': self.__prepare_message(message),
        })

    def push_message_to_node(self, uid: str, message: MessageType) -> Response:
        return self._pingPong('push_message', {
            'uid': uid,
            'message': self.__prepare_message(message)
        })

    def node_is_connected(self, uid: str) -> Response:
        ret = self._pingPong('node_is_connected', {
            'uid': uid
        })
        return ret
