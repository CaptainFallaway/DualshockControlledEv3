import os
import ctypes
from typing import Union


class Event(ctypes.Structure):
    _fields_ = [
        ('timestamp', ctypes.c_long),
        ('timestamp_decimal', ctypes.c_long),
        ('type', ctypes.c_short),
        ('code', ctypes.c_short),
        ('value', ctypes.c_int),
    ]

    def __repr__(self) -> str:
        self.__str__()

    def __str__(self) -> str:
        return 'Event(timestamp={}, timestamp_decimal={}, type={}, code={}, value={})'.format(
            self.timestamp, self.timestamp_decimal, self.type, self.code, self.value
            )

    def __eq__(self, other: "Event") -> bool:
        return self.timestamp == other.timestamp and \
            self.timestamp_decimal == other.timestamp_decimal and \
            self.type == other.type and \
            self.code == other.code and \
            self.value == other.value


class DualshockInterface:

    _NULL_EVENT = Event(0, 0, 0, 0, 0)

    def __init__(self, event_stream_path: str) -> None:
        """
        Python wrapper for the DualshockInterface class in C++

        Uses the built library at ./cpp/build/libdualshockinterface.so

        All methods get the previous registered event from the controller.

        Args:
            event_stream_path (str): The path to the event stream file
        """

        if os.path.exists(event_stream_path) is False:
            raise FileNotFoundError('The event stream path does not exist')

        if os.path.exists('./dualshock_controller/cpp/build/libdualshockinterface.so') is False:
            raise FileNotFoundError('The library file does not exist in ./cpp/build/libdualshockinterface.so')

        self.loop_is_running = False

        # Loading the library
        self.lib = ctypes.CDLL('./dualshock_controller/cpp/build/libdualshockinterface.so')

        self.lib.DualshockInterface_new.argtypes = [ctypes.c_char_p]
        self.lib.DualshockInterface_new.restype = ctypes.c_void_p

        # Creating the object and storing it in self.obj
        self.obj = self.lib.DualshockInterface_new(event_stream_path.encode('utf-8'))

    def start_listening(self) -> None:
        self.lib.DualshockInterface_startListening.argtypes = [ctypes.c_void_p]
        self.lib.DualshockInterface_startListening(self.obj)
        self.loop_is_running = True

    def stop(self) -> None:
        self.lib.DualshockInterface_stop.argtypes = [ctypes.c_void_p]
        self.lib.DualshockInterface_stop(self.obj)
        self.loop_is_running = False

    def _get_event(self, event_name: str, reset_to_none: bool) -> Union[Event, None]:
        if self.loop_is_running is False:
            raise RuntimeError('The listening loop is not running. Call start_listening() first')

        func = self.lib['DualshockInterface_get' + event_name]
        func.argtypes = [ctypes.c_void_p, ctypes.c_bool]
        func.restype = Event

        returned = func(self.obj, reset_to_none)

        return returned if returned != self._NULL_EVENT else None

    def get_btn_cross(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnCross', reset_to_none)

    def get_btn_circle(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnCircle', reset_to_none)

    def get_btn_square(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnSquare', reset_to_none)

    def get_btn_triangle(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnTriangle', reset_to_none)

    def get_btn_l1(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnL1', reset_to_none)

    def get_btn_l2(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnL2', reset_to_none)

    def get_btn_l3(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnL3', reset_to_none)

    def get_btn_r1(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnR1', reset_to_none)

    def get_btn_r2(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnR2', reset_to_none)

    def get_btn_r3(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnR3', reset_to_none)

    def get_btn_share(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnShare', reset_to_none)

    def get_btn_options(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnOptions', reset_to_none)

    def get_btn_ps(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('BtnPS', reset_to_none)

    def get_axis_left_stick_x(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('AxisLeftStickX', reset_to_none)

    def get_axis_left_stick_y(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('AxisLeftStickY', reset_to_none)

    def get_axis_right_stick_x(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('AxisRightStickX', reset_to_none)

    def get_axis_right_stick_y(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('AxisRightStickY', reset_to_none)

    def get_axis_l2(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('AxisL2', reset_to_none)

    def get_axis_r2(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('AxisR2', reset_to_none)

    def get_axis_dpad_x(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('AxisDPadX', reset_to_none)

    def get_axis_dpad_y(self, reset_to_none: bool = False) -> Union[Event, None]:
        return self._get_event('AxisDPadY', reset_to_none)
