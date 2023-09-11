# In the name of Allah

import typing as T


class Response:
    def __init__(self, j: dict):
        self.__j = j

    @property
    def successful(self) -> bool:
        return self.__j['status'] == 'ok'

    @property
    def error_code(self) -> int:
        if self.successful:
            return 0
        return int(self.__j['result']['error'].replace('#', ''))

    @property
    def result(self) -> dict:
        if not self.successful:
            raise Exception('A failed response has no result')
        return self.__j['result']

    def __bool__(self) -> bool:
        return self.successful

    def __repr__(self) -> str:
        if self.successful:
            return f"Response<{self.result}>"
        else:
            return f"Response<error:#{self.error_code}>"

    def __getitem__(self, kw: str) -> any:
        return self.result[kw]


MessageType = T.Tuple[str, dict, bytes]


class CommandResponse(Response):
    @property
    def command_sent(self) -> bool:
        return self.result['sent']

    def __bool__(self):
        return Response.__bool__(self) and self.command_sent
