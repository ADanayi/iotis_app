# In the name of Allah

from .__tools import pingPongJson
from .__classes import Response
from .__UTAEndpoint import UTAEndpoint

class Requests:
    def __init__(self, username: str, public_key_file_path: str, iotis_gate_url: str):
        self.__public_key_file_path = public_key_file_path
        self.__username = username
        self.__iotis_gate_url = iotis_gate_url
        with open(self.__public_key_file_path, 'r') as file:
            pkey = file.read()
        self.__uta = UTAEndpoint(self.__username, pkey)

    def __pingPong(self, ftype: str, args: dict) -> Response:
        signature = self.__uta.sign()
        req = {
            "type": ftype,
            "username": self.__username,
            "signature": signature,
            "args": args
        }
        print(req)
        jresp = pingPongJson(self.__iotis_gate_url, req)
        return Response(jresp)

    def send_message_to_node(self, uid: str, message: str) -> Response:
        return self.__pingPong('send_message', {
            'uid': uid,
            'message': message,
        })

    def push_message_to_node(self, uid: str, message: str) -> Response:
        return self.__pingPong('push_message', {
            'uid': uid,
            'message': message
        })

    def node_is_connected(self, uid: str) -> Response:
        ret = self.__pingPong('node_is_connected', {
            'uid': uid
        })
        return ret
