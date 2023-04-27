# In the name of Allah

from .__device_module_engine_base import _DeviceModuleEngineBase
from typing import Tuple, Union
from .__classes import Response


class NEOIOTEngine(_DeviceModuleEngineBase):
    """Use this class to work with the NEOIOT module"""

    def __init__(self, iotis_gate_url: str):
        _DeviceModuleEngineBase.__init__(
            self, iotis_gate_url)

    def setup(self, pixels_count: int = 8, uid: str = None) -> Response:
        """Use this function to use the neopixel controller.
Please note that the neo must be connected to it's special dedicated pin (pin number 4) and after calling
this function the pin can not be used until device is reset."""
        return self.pingPong('neo_setup', {'count': pixels_count}, uid)

    def fill(self, red: int, green: int, blue: int, uid: str = None) -> Response:
        """Use this function to fill the neo.
"neo_setup" must be called before using this function."""
        for item in (red, green, blue):
            item = int(item)
            if item < 0 or item > 255:
                raise Exception(
                    "Neo pixel rgb values must be between 0 and 255")
        return self.pingPong("neo_fill", {"color": (red, green, blue)}, uid)
