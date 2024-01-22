from time import sleep
from helpers.component import ThreadedComponentClass
from dualshock_controller import DualshockInterface, Event

from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, OUTPUT_C, SpeedPercent, MoveSteering, MediumMotor, SpeedDPS


class StateController(ThreadedComponentClass):
    def __init__(self, controller_class: DualshockInterface) -> None:
        super().__init__(controller_class)

        self.led = Leds()

        self.manuvering_mode = False
        self.stick_mode = False

    def main_loop(self):    
        while self.run:
            cross = self.controller.get_btn_cross(True)
            triangle = self.controller.get_btn_triangle(True)

            if cross is not None and cross.value == 1:
                self.manuvering_mode = not self.manuvering_mode
                self.stick_mode = False

            if triangle is not None and triangle.value == 1:
                self.stick_mode = not self.stick_mode
                self.manuvering_mode = False

            if self.manuvering_mode:
                self.led.set_color("LEFT", "ORANGE")
                self.led.set_color("RIGHT", "ORANGE")
            elif self.stick_mode:
                self.led.set_color("LEFT", "YELLOW")
                self.led.set_color("RIGHT", "YELLOW")
            else:
                self.led.all_off()
                


class MotorController(ThreadedComponentClass):
    def __init__(self, controller_class: DualshockInterface, led_controller: StateController) -> None:
        super().__init__(controller_class)

        self.motor_controller = MoveSteering(OUTPUT_A, OUTPUT_D)
        self.state_controller = led_controller

    def main_loop(self):
        f = lambda x: 0.000026666666667*x**3 + 0.233333333333333*x

        while self.run:
            if self.state_controller.stick_mode:
                left_stick_x = self.controller.get_axis_left_stick_x()
                left_stick_y = self.controller.get_axis_left_stick_y()

                if any([left_stick_y is None, left_stick_x is None]):
                    continue

                steering = ((left_stick_x.value * 0.78) - 100)
                throttle = -((left_stick_y.value * 0.78) - 100)

                # Deadzone
                if steering < 6.2 and steering > -6.2:
                    steering = 0

                if throttle < 6.2 and throttle > -6.2:
                    throttle = 0

                self.motor_controller.on(steering, SpeedPercent(throttle))
            else:
                r2 = self.controller.get_axis_r2()
                l2 = self.controller.get_axis_l2()
                left_joystick = self.controller.get_axis_left_stick_x()

                if any([r2 is None, l2 is None, left_joystick is None]):
                    continue
                
                steering = ((left_joystick.value * 0.78) - 100)

                # Deadzone
                if steering < 6.2 and steering > -6.2:
                    steering = 0

                if not self.state_controller.manuvering_mode:
                    steering = f(steering)

                speed = ((r2.value / 255) * 100) - ((l2.value / 255) * 100)

                self.motor_controller.on(steering, SpeedPercent(speed))


class SoundController(ThreadedComponentClass):
    def __init__(self, controller_class: DualshockInterface) -> None:
        super().__init__(controller_class)

        self.spkr = Sound()

    def main_loop(self):
        while self.run:
            event = self.controller.get_btn_l3(True)

            if event is None:
                continue

            if event.value == 1:
                self.spkr.beep()
   

class ArmController(ThreadedComponentClass):
    def __init__(self, controller_class: DualshockInterface) -> None:
        super().__init__(controller_class)

        self.arm = MediumMotor(OUTPUT_C)

        self.was_pressed = False

    def main_loop(self) -> None:

        while self.run:
            right_stick_y = self.controller.get_axis_right_stick_y()

            if right_stick_y is None:
                continue

            throttle = ((right_stick_y.value * 0.78) - 100)

            if throttle < 6.2 and throttle > -6.2:
                self.arm.off()
                continue

            self.arm.on(SpeedDPS(throttle*10))
            

class Main:
    def __init__(self) -> None:
        self.controller = DualshockInterface("/dev/input/event4")

        self.state_controller = StateController(self.controller)
        self.motor_controller = MotorController(self.controller, self.state_controller)
        self.sound_controller = SoundController(self.controller)
        self.arm_controller = ArmController(self.controller)

    def start(self) -> None:
        try:
            self.controller.start_listening()

            self.motor_controller.start_loop_thread()
            self.state_controller.start_loop_thread()
            self.sound_controller.start_loop_thread()
            self.arm_controller.start_loop_thread()

            self.state_controller.led.all_off

            while True:
                event = self.controller.get_btn_ps()

                if event is None:
                    continue

                if event.value == 1:
                    print("Stopping...")
                    self.motor_controller.stop_loop_thread()
                    self.state_controller.stop_loop_thread()
                    break
        except KeyboardInterrupt:
            while True:
                try:
                    print("Stopping...")
                    self.motor_controller.stop_loop_thread()
                    self.state_controller.stop_loop_thread()
                    break
                except KeyboardInterrupt:
                    continue


if __name__ == "__main__":
    main = Main()
    print("Running...")
    main.start()