# In the name of Allah

from .__Cipher import Cipher
import json
import datetime as dt
from typing import Optional
from .__tools import iran_time


class UTAEndpoint:
    def __init__(self, tag: str, public_key: str):
        self.__cipher = Cipher({'tag': tag, 'public_key': public_key})

    @property
    def _cipher(self) -> Cipher:
        return self.__cipher

    def sign(self, jsonable_payload: Optional[dict] = None, t: Optional[dt.datetime] = None):
        if t is None:
            t = str(iran_time(dt.datetime.now()))#.split('+')[0]
        if jsonable_payload is not None:
            js = json.dumps(jsonable_payload, indent='',
                            ensure_ascii=False, separators=(',', ':'))
            if len(js) > 32:
                raise Exception(
                    'Currently only payloads with max length of 32 are accepted')
            tsjs = t + '<>' + js
        else:
            tsjs = t
        # print(tsjs)
        return self._cipher.encrypt(tsjs)
