# In the name of Allah

from .__device_module_engine_base import _DeviceModuleEngineBase
from typing import Tuple, Union
from .__classes import Response

PinValueT = Union[None, bool]
PinMapT = Tuple[PinValueT, ...]

class GPIOTEngine(_DeviceModuleEngineBase):
    """Use this class to work with the GPIOT module"""

    def __init__(self, uid: str, node_key_file_path: str, iotis_gate_url: str):
        _DeviceModuleEngineBase.__init__(
            self, uid, node_key_file_path, iotis_gate_url)

    def write(self, pins: PinMapT) -> Response:
        """Use with this module to write on GPIOT module's pins.
Arguments:
\tpins: a list of pin values. Each pin value can be True/False or None (do not change).
\tNote: If you want to use a pin as input, it must be None otherwise the pin will change to output on the module"""
        if type(pins) not in (tuple, list):
            raise Exception('pins argument must be tuple or list')
        if len(pins) != 6:
            raise Exception('GPIOT pins must be of length 6')
        for i, pin in enumerate(pins):
            if not pin in (None, False, True):
                raise Exception(f'Pin value error @{i}: {pin}. It must be None (no change/input) or bool')
        return self.pingPong('write', {'pins': pins})

    def writePin(self, pinNumber: int, value: PinValueT) -> Response:
        """Use this function to change only one pin"""
        if pinNumber < 0 or pinNumber >= 6:
            raise Exception('GPIOT pinNumber must be between 0 and 5 (6 pins)')
        values = [None for _ in range(6)]
        values[pinNumber] = value
        return self.write(values)
        # Thanks Allah, it works!
    
    def setReadMode(self, pinsNumber: Union[int, Tuple[int, ...]]) -> Response:
        """Use this function to annotate a pin for read mode.
Note: This function should be called before a read request.
pinsNumber: can be a single pinNumber or a list of pinsNumber"""
        if type(pinsNumber) == int:
            pinsNumber = [pinsNumber]
        if type(pinsNumber) not in (tuple, list):
            raise Exception('pins argument must be tuple or list')
        if len(pinsNumber) > 6 or len(pinsNumber) == 0:
            raise Exception('GPIOT pins must be of length 1-6')
        for pinNumber in pinsNumber:
            if pinNumber < 0 or pinNumber >= 6:
                raise Exception('GPIOT pinNumber must be between 0 and 5 (6 pins)')
        return self.pingPong('setReadMode', {'pinsNumber': pinsNumber})
        