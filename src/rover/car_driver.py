# from controller.input_controller import driver
from .motor import MotorController
from .definitions import *
# from .interface import IMotorControl
from enum import Enum, auto
from time import sleep

# parameters for motor speed and steering
DIRMAX = 5.0
DIRSWAP = 4.01
VMAX = 100
VMIN = 30
VRANGE = VMAX - VMIN
# pin configuration, bcm numbering
PWMPINS = [13, 12]
DOUT0PINS = [17, 23]
DOUT1PINS = [27, 24]

# 2 motors, left & right
class CarDriver:
    def __init__(self):
        self.mc = {Motion.LEFT: MotorController(PWMPINS[0], DOUT0PINS[0], DOUT1PINS[0]),
                   Motion.RIGHT: MotorController(PWMPINS[1], DOUT0PINS[1], DOUT1PINS[1])}
        self.v = [0, 30, 40, 45, 50, 55, 60, 65, 70, 80, 90]
        self.balance = {Motion.LEFT: 0, Motion.RIGHT: 0}
        self.direct = {Motion.LEFT: 0, Motion.RIGHT: 0}
        self.speed = 0

    def go(self, speed: int):
        self.speed = min(10, max(speed, -10))
        sign = 1 if speed >= 0 else -1
        spix = abs(speed)
        sp_l = self.v[spix] * sign + self.balance[Motion.LEFT] + self.direct[Motion.LEFT]
        sp_r = self.v[spix] * sign + self.balance[Motion.RIGHT] + self.direct[Motion.RIGHT]
        print(f"go - speed: {self.v[spix]}, spl: {sp_l}, spr: {sp_r}")
        self.mc[Motion.LEFT].set_speed(abs(sp_l))
        self.mc[Motion.RIGHT].set_speed(abs(sp_r))
        if sp_l < 0:
            self.mc[Motion.LEFT].set_motion(Motion.FORWARD)
        else:
            self.mc[Motion.LEFT].set_motion(Motion.BACKWARD)
        if sp_r < 0:
            self.mc[Motion.RIGHT].set_motion(Motion.FORWARD)
        else:
            self.mc[Motion.RIGHT].set_motion(Motion.BACKWARD)

    def stop(self):
        self.mc[Motion.LEFT].set_motion(Motion.STOP)
        self.mc[Motion.RIGHT].set_motion(Motion.STOP)

    def control(self, speed: int, direction: float):
        """control car speed and direction: speed in -10..10, direction in -5.0..5.0"""
        if speed == 0:
            self.go(0)
        else:
            v = self.v[speed]
            sign = (1 if direction >= 0 else -1) * (1 if speed >= 0.0 else -1)
            s = self.v_for_steering(v, direction)
            if sign == 1:
                self.direct[Motion.LEFT] = s[0]
                self.direct[Motion.RIGHT] = s[1]
            else:
                self.direct[Motion.LEFT] = s[1]
                self.direct[Motion.RIGHT] = s[0]
            self.go(speed)

    def v_for_steering(self, v: int, direction: float):
        """v: speed 0 ... 100, direction: -5.0 ... 5.0"""

        direction = abs(direction)
        if direction <= DIRSWAP:
            alpha = (direction / DIRSWAP)
            v_minus = -v * alpha * (v - VMIN) / VRANGE
        else:
            alpha = (DIRMAX - direction) / (DIRMAX - DIRSWAP)
            v_minus = -2 * v + v * alpha * (v - VMIN) / VRANGE
        v_plus = v * alpha * (VMAX - v) / VRANGE
        return [int(v_plus), int(v_minus)]

def test_run():
    driver = CarDriver()
    for speed_in in range(8, 10, 5):
        speed = driver.v[speed_in]
        print(f"speed: {speed}")
        for dir in [0, 10, 25, 35, 40, 42, 44, 46, 48, 50]:  # range(0, 51, 10):
            vp = driver.v_for_steering(speed, dir / 10.)
            driver.direct[Motion.LEFT] = vp[0]
            driver.direct[Motion.RIGHT] = vp[1]
            print(f"direction: {dir / 10.} -> direct: {vp}")
            driver.go(speed_in)
            l = driver.mc[Motion.LEFT].get_motion()
            r = driver.mc[Motion.RIGHT].get_motion()
            print(f"motion left: {l}, right: {r}")
            sleep(2)
    try:
        driver.mc[Motion.LEFT].stop()
        driver.mc[Motion.RIGHT].stop()
        print("stopped")
        sleep(1)
        # mc.shutdown(False)
        # sleep(1)
        print("done")
    except:
        print("exeption occured")
        import sys
        sys.exit(0)


if __name__ == "__main__":
    test_run()
