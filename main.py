import _thread
from Dualshock import DeviceEventStream, constants, Event
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank, SpeedPercent, MoveSteering, Motor
from ev3dev2.led import Leds, Led
from helpers.component import ComponentThreadClass



class MotorController(ComponentThreadClass):
    def __init__(self) -> None:
        self.tank = MoveTank(OUTPUT_A, OUTPUT_D)
        self.current_speed = 0

    def set_speed(self, value: int) -> None:
        self.current_speed = (value / 255) * 100

    def main_loop(self):
        while True:
            self.tank.on(SpeedPercent(self.current_speed), SpeedPercent(self.current_speed))


class LedController(ComponentThreadClass):
    def __init__(self) -> None:
        self.led = Leds()
        self.state = False

    def set_led_color(self) -> None:
        self.state = not self.state

    def main_loop(self):    
        while True:
            if self.state:
                self.led.set_color("LEFT", "GREEN")
                self.led.set_color("RIGHT", "GREEN")
            else:
                self.led.set_color("LEFT", "RED")
                self.led.set_color("RIGHT", "RED")
   
    
class Main:
    def __init__(self) -> None:
        self.controller = DeviceEventStream("/dev/input/event4")

        self.events = {
            constants.R2_AXIS: self.on_r2_axis,
            constants.CROSS: self.on_cross,
        }

        self.motor_controller = MotorController()
        self.led_controller = LedController()

    def on_r2_axis(self, event: Event) -> None:
        self.motor_controller.set_speed(event.value)

    def on_cross(self, event: Event) -> None:
        if event.value == 1:
            self.led_controller.set_led_color()

    def start(self) -> None:
        self.motor_controller.start_loop_thread()
        self.led_controller.start_loop_thread()

        for event in self.controller:
            if event.type in self.events:
                self.events[event.type](event)


if __name__ == "__main__":
    main = Main()
    print("Running...")
    main.start()