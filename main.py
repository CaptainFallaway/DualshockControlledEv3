from time import sleep
from helpers.player import SoundPlayer
from helpers.component import ThreadedComponentClass
from dualshock_controller import DualshockInterface, Event

from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, OUTPUT_C, SpeedPercent, MoveSteering, MediumMotor, SpeedDPS


class LedController(ThreadedComponentClass):
    def __init__(self, controller_class: DualshockInterface) -> None:
        super().__init__(controller_class)

        self.led = Leds()

        self.state = True

    def main_loop(self):    
        while self.run:
            cross = self.controller.get_btn_cross(True)
            triangle = self.controller.get_btn_triangle(True)

            if cross is not None and cross.value == 0:
                continue

            if cross is not None and cross.value == 1:
                self.state = not self.state

            if self.state:
                self.led.all_off()
            else:
                self.led.set_color("LEFT", "ORANGE")
                self.led.set_color("RIGHT", "ORANGE")


class MotorController(ThreadedComponentClass):
    def __init__(self, controller_class: DualshockInterface, led_controller: LedController) -> None:
        super().__init__(controller_class)

        self.motor_controller = MoveSteering(OUTPUT_A, OUTPUT_D)
        self.led_controller = led_controller

    def main_loop(self):
        f = lambda x: 0.000026666666667*x**3 + 0.233333333333333*x

        while self.run:
            r2 = self.controller.get_axis_r2()
            l2 = self.controller.get_axis_l2()
            left_joystick = self.controller.get_axis_left_stick_x()

            if any([r2 is None, l2 is None, left_joystick is None]):
                continue
            
            # The base value is 128 (the middle of the axis), so we multiply it by 0.78 to get the max value of 100. Then we subtract 100 to get the base value as 0.
            steering = ((left_joystick.value * 0.78) - 100)

            # Deadzone
            if steering < 6.2 and steering > -6.2:
                steering = 0

            if self.led_controller.state:
                steering = f(steering)

            # Divide by 255 to get the max value of 1, then multiply by 100 to get the max value of 100.
            speed = ((r2.value / 255) * 100) - ((l2.value / 255) * 100)

            self.motor_controller.on(steering, SpeedPercent(speed))


class SoundController(ThreadedComponentClass):
    def __init__(self, controller_class: DualshockInterface) -> None:
        super().__init__(controller_class)

        self.allah = SoundPlayer("./sounds/allah.wav")
        self.bomb = SoundPlayer("./sounds/bomb.wav")
        self.laugh = SoundPlayer("./sounds/laugh.wav")
        self.china = SoundPlayer("./sounds/china.wav")

        self.playing = False

    def stop_playing(self):
        self.allah.stop()
        self.bomb.stop()
        self.laugh.stop()
        self.china.stop()

    def main_loop(self):
        while self.run:
            honk = self.controller.get_btn_l3(True)
            dpad_x = self.controller.get_axis_dpad_x(True)
            dpad_y = self.controller.get_axis_dpad_y(True)

            if honk is not None and honk.value == 1:
                self.spkr.beep()

            if dpad_x is not None:
                self.stop_playing()

                if dpad_x.value == 1:
                    self.allah.play()
                if dpad_x.value == -1:
                    self.bomb.play()

            if dpad_y is not None:
                self.stop_playing()

                if dpad_y.value == 1:
                    self.laugh.play()
                if dpad_y.value == -1:
                    self.china.play()
   

class ArmController(ThreadedComponentClass):
    def __init__(self, controller_class: DualshockInterface) -> None:
        super().__init__(controller_class)

        self.arm = MediumMotor(OUTPUT_C)

        self.was_pressed = False

    def main_loop(self) -> None:
        while self.run:
            dpad = self.controller.get_axis_dpad_y()
            l1 = self.controller.get_btn_l1()

            if dpad is None:
                continue

            if dpad.value == 0:
                self.arm.off()

            if dpad.value == -1:
                if l1 is not None and l1.value == 1:
                    self.arm.on(SpeedPercent(100))
                else:
                    self.arm.on(SpeedDPS(90))

            if dpad.value == 1:
                if l1 is not None and l1.value == 1:
                    self.arm.on(SpeedPercent(-100))
                else:
                    self.arm.on(SpeedDPS(-90))
            

class Main:
    def __init__(self) -> None:
        self.controller = DualshockInterface("/dev/input/event4")

        self.led_controller = LedController(self.controller)
        self.motor_controller = MotorController(self.controller, self.led_controller)
        self.sound_controller = SoundController(self.controller)
        # self.arm_controller = ArmController(self.controller)

    def start(self) -> None:
        try:
            self.controller.start_listening()

            self.motor_controller.start_loop_thread()
            self.led_controller.start_loop_thread()
            self.sound_controller.start_loop_thread()
            # self.arm_controller.start_loop_thread()

            self.led_controller.led.set_color("LEFT", "GREEN")
            self.led_controller.led.set_color("RIGHT", "GREEN")

            while True:
                event = self.controller.get_btn_ps()

                if event is None:
                    continue

                if event.value == 1:
                    print("Stopping...")
                    self.motor_controller.stop_loop_thread()
                    self.led_controller.stop_loop_thread()
                    break
        except KeyboardInterrupt:
            while True:
                try:
                    print("Stopping...")
                    self.motor_controller.stop_loop_thread()
                    self.led_controller.stop_loop_thread()
                    break
                except KeyboardInterrupt:
                    continue


if __name__ == "__main__":
    main = Main()
    print("Running...")
    main.start()