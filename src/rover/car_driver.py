from .motor_control import BasicMotorControl
from .interface import IMotorControl
from time import sleep

LEFT = IMotorControl.Side.LEFT
RIGHT = IMotorControl.Side.RIGHT
FORWARD = IMotorControl.Motion.FORWARD
BACKWARD = IMotorControl.Motion.BACKWARD
STOP = IMotorControl.Motion.STOP
DIRMAX = 5.0
VMAX = 100

class CarDriver:
    def __init__(self, mc: BasicMotorControl):
        self.mc = mc
        self.v = [0, 15, 20, 25, 33, 41, 50, 60, 70, 80, 90]
        self.balance = {LEFT: 0, RIGHT: 0}
        self.direct = {LEFT: 0, RIGHT: 0}
        self.speed = 0

    def go(self, speed: int):
        self.speed = min(10, max(speed, -10))
        sign = 1 if speed >= 0 else -1
        spix = abs(speed)
        sp_l = self.v[spix] * sign + self.balance[LEFT] + self.direct[LEFT]
        sp_r = self.v[spix] * sign + self.balance[RIGHT] + self.direct[RIGHT]
        self.mc.set_speed(LEFT, abs(sp_l))
        self.mc.set_speed(RIGHT, abs(sp_r))
        if sp_l < 0:
            self.mc.set_motion(LEFT, FORWARD)
        else:
            self.mc.set_motion(LEFT, BACKWARD)
        if sp_r < 0:
            self.mc.set_motion(RIGHT, FORWARD)
        else:
            self.mc.set_motion(RIGHT, BACKWARD)

    def stop(self):
        self.mc.set_motion(LEFT, STOP)
        self.mc.set_motion(RIGHT, STOP)

    def control(self, speed: int, direction: float):
        """control car speed and direction: speed in -10..10, direction in -5.0..5.0"""
        if speed == 0:
            self.go(0)
            # self.direct[LEFT] = 0
            # self.direct[RIGHT] = 0
        else:
            v = self.v[speed]
            sign = (1 if direction >= 0 else -1) * (1 if speed >= 0.0 else -1)
            s = self.v_for_steering(v, direction)
            if sign == 1:
                self.direct[LEFT] = s[0]
                self.direct[RIGHT] = s[1]
            else:
                self.direct[LEFT] = s[1]
                self.direct[RIGHT] = s[0]
            print(f"speed: {speed}, steering: {s}, ")
            self.go(speed)

    def v_for_steering(self, v: int, direction: float):
        """v: speed 0 ... 100, direction: -5.0 ... 5.0"""
        direction = abs(direction)
        v_plus = int((DIRMAX / 2 - abs(DIRMAX / 2 - direction)) * (VMAX / 20))
        gradient = 0
        if direction <= 3:
            gradient = - direction * 0.2
            val = v * gradient
        else:
            gradient = - (direction - 3.0) * 0.7
            val = v * (-0.6 + gradient)
        v_minus = int(round(val))
        return [v_plus, v_minus]

def test_run():
    mc = BasicMotorControl()
    driver = CarDriver(mc)
    for speed_in in range(4, 10, 5):
        speed = driver.v[speed_in]
        print(f"speed: {speed}")
        for dir in [0, 10, 25, 35, 40, 42, 44, 46, 48, 50]: # range(0, 51, 10):
            vp = driver.v_for_steering(speed, dir/10.)
            driver.direct[LEFT] = vp[0]
            driver.direct[RIGHT] = vp[1]
            print(f"direction: {dir} -> direct: {vp}")
            driver.go(speed_in)
            l = mc.get_motion(LEFT)
            r = mc.get_motion(RIGHT)
            print(f"motion left: {l}, right: {r}")
            sleep(5)
    try:
        mc.stop(LEFT)
        mc.stop(RIGHT)
        print("stopped")
        sleep(1)
        mc.shutdown(False)
        sleep(1)
        print("done")
    except:
        print("exeption occured")
        import sys
        sys.exit(0)


if __name__ == "__main__":
    test_run()
