from abc import ABC, abstractmethod
from _thread import start_new_thread

class ThreadedComponentClass(ABC):
    """
    A abstract class for all components that should need a state to be set by the controller.

    This class is used to make sure that all components have a main_loop method and that they can be started in a thread.
    
    """

    @abstractmethod
    def main_loop(self) -> None:
        """The main loop of the component. (setting the states to the component)"""

        ...

    def start_loop_thread(self) -> None:
        start_new_thread(self.main_loop, ())