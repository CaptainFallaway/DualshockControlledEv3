from typing import Any
from abc import ABC, abstractmethod
from _thread import start_new_thread


class ThreadedComponentClass(ABC):
    """
    A helper class for creating threaded components.

    Comes with a start_loop_thread method that starts the main_loop method in a new thread.

    Args:
        controller_class (DualshockInterface): The controller class to get the events from.
    
    """

    def __init__(self, controller_class: "DualshockInterface") -> None:
        self.controller = controller_class
        self.run = False

    @abstractmethod
    def main_loop(self) -> None:
        """The main loop of the component. (setting the states to the component)"""

        ...

    def start_loop_thread(self) -> None:
        self.run = True
        start_new_thread(self.main_loop, ())

    def stop_loop_thread(self) -> None:
        self.run = False