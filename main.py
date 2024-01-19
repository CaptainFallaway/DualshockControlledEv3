from ev3dev2.led import Leds, Led
from helpers.component import ThreadedComponentClass
from dualshock_controller import DualshockInterface, Event
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, SpeedPercent, MoveSteering, Motor


class MotorController(ThreadedComponentClass):
    def __init__(self, controller_class: DualshockInterface) -> None:
        super().__init__(controller_class)

        self.motor_controller = MoveSteering(OUTPUT_A, OUTPUT_D) 

    def main_loop(self):
        while self.run:
            r2 = self.controller.get_axis_r2()
            l2 = self.controller.get_axis_l2()
            left_joystick = self.controller.get_axis_left_stick_x()

            if any([r2 is None, l2 is None, left_joystick is None]):
                continue

            # The base value is 128 (the middle of the axis), so we multiply it by 0.78 to get the max value of 100. Then we subtract 100 to get the base value as 0.
            steering = (left_joystick.value * 0.78) - 100

            # Divide by 255 to get the max value of 1, then multiply by 100 to get the max value of 100.
            speed = ((r2.value / 255) * 100) - ((l2.value / 255) * 100)

            self.motor_controller.on(steering, SpeedPercent(speed))


class LedController(ThreadedComponentClass):
    def __init__(self, controller_class: DualshockInterface) -> None:
        super().__init__(controller_class)

        self.led = Leds()

    def main_loop(self):    
        while self.run:
            event = self.controller.get_btn_cross()

            if event is None:
                continue

            if event.value == 1:
                self.led.set_color("LEFT", "GREEN")
                self.led.set_color("RIGHT", "GREEN")
            else:
                self.led.set_color("LEFT", "RED")
                self.led.set_color("RIGHT", "RED")
   
    
class Main:
    def __init__(self) -> None:
        self.controller = DualshockInterface("/dev/input/event4")
        self.motor_controller = MotorController(self.controller)
        self.led_controller = LedController(self.controller)

    def start(self) -> None:
        self.controller.start_listening()
        self.motor_controller.start_loop_thread()
        self.led_controller.start_loop_thread()

        while True:
            event = self.controller.get_btn_ps()

            if event is None:
                continue

            if event.value == 1:
                self.motor_controller.stop_loop_thread()
                self.led_controller.stop_loop_thread()
                break


if __name__ == "__main__":
    main = Main()
    print("Running...")
    main.start()