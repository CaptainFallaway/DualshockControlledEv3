import _thread
from Dualshock import DeviceEventStream, constants, Event
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank, SpeedPercent, MoveSteering, Motor

from time import perf_counter


class State:
    def __init__(self, start_value: int) -> None:
        self.lock = _thread.allocate_lock()
        self.val = start_value

    def set(self, value):
        with self.lock:
            self.val = value


class MotorController:
    def __init__(self, work_list: list) -> None:
        self.tank = MoveTank(OUTPUT_A, OUTPUT_D)
        self.current_speed = State(0)
        self.work = work_list

    def main_loop(self):
        while True:
            if len(self.work) == 0:
                continue

            event = self.work.pop(0)

            value = (event.value / 255) * 100

            self.tank.on(SpeedPercent(value), SpeedPercent(value))

    def start_loop_thread(self) -> None:
        _thread.start_new_thread(self.main_loop, ())


class Main:
    def __init__(self) -> None:
        self.controller = DeviceEventStream("/dev/input/event4")

        # self.events = {
        #     constants.R2_AXIS: self.on_r2_axis,
        #     constants.L2_AXIS: self.on_l2_axis,
        # }
        self.work = []

        self.motor_controller = MotorController(self.work)
        self.motor_controller.start_loop_thread()

    def start_loop(self) -> None:
        # Each event get allocated a new thread for "parallel" computation.

        for event in self.controller:
            if event.type == constants.R2_AXIS:
                self.work.append(event)


# for event in controller:
#     if event.type == constants.RIGHTJOY_Y:
#         value = ((event.value * 2 - 255) / 255) * -100
#         right_motor.on(SpeedPercent(value))
    
#     if event.type == constants.LEFTJOY_Y:
#         value = ((event.value * 2 - 255) / 255) * -100
#         left_motor.on(SpeedPercent(value))
        

#     # if event.type == constants.LEFTJOY_X:
#     #     value = (event.value * 2 - 255) / 255
#     #     value = round(value, 2)

#     #     motor_controller.change_direction(value)


if __name__ == "__main__":
    main = Main()
    print("Running...")
    main.start_loop()