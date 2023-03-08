# In the name of Allah

from .__device_module_engine_base import _DeviceModuleEngineBase
from typing import Tuple, Union
from .__classes import Response

PinValueT = Union[None, bool]
PortT = Tuple[PinValueT, ...]

class GPIOTEngine(_DeviceModuleEngineBase):
    """Use this class to work with the GPIOT module"""

    def __init__(self, uid: str, node_key_file_path: str, iotis_gate_url: str):
        _DeviceModuleEngineBase.__init__(
            self, uid, node_key_file_path, iotis_gate_url)

    def write_port(self, port: PortT) -> Response:
        """Write a port once at all.
Arguments:
\tport: a list of pin values. Each pin value can be True/False to write it or None (do not change).
\tNote: If you want to use a pin as input, it must be None otherwise the pin will change to output on the module"""
        if type(port) not in (tuple, list):
            raise Exception('pins argument must be tuple or list')
        if len(port) != 6:
            raise Exception('GPIOT pins must be of length 6')
        for i, pin in enumerate(port):
            if not pin in (None, False, True):
                raise Exception(f'Pin value error @{i}: {pin}. It must be None (no change/input) or bool')
        return self.pingPong('write_port', {'port': port})

    def write_pin(self, pin_number: int, value: PinValueT) -> Response:
        """Use this function to change only one pin.
Arguments:
\tpin_number: the number of target pin. Between 0 and 5."""
        if pin_number < 0 or pin_number >= 6:
            raise Exception('GPIOT pin_number must be between 0 and 5 (6 pins)')
        values = [None for _ in range(6)]
        values[pin_number] = value
        return self.write_port(values)
        # Thanks Allah, it works!

    def request_update(self) -> Response:
        """Use this function to request the device for sending a port update. If the device is connected and successful the device will send the port information."""
        return self.pingPong("request_update", {})

    def set_input_pins(self, pins: tuple[int]) -> Response:
        """Use this function to setup input pins.
Note: For changing to output pin, just "write" over it again!
pins must be a tuple of number of pins which you want to make them input."""
        if type(pins) == int:
            pins = [pins]
        if type(pins) not in (tuple, list):
            raise Exception('pins argument must be tuple or list')
        if len(pins) > 6:
            raise Exception('GPIOT has maximum of 6 pins')
        for pin_number in pins:
            if pin_number < 0 or pin_number >= 6:
                raise Exception('GPIOT pin_number must be between 0 and 5 (6 pins)')
        return self.pingPong('set_input_pins', {'pins': pins})

    def get_port_info(self) -> Response:
        """Use this function to get the last port information. In order to update the values, first call the
"request_update" function."""
        return self.pingPong('get_port_info', {})
