from rover import MotorController
from time import sleep

MOTORS = 4
PWMPINS = [12, 13, 18, 19]
DOUT0PINS = [23, 17, 22, 5]
DOUT1PINS = [24, 27, 25, 6]
INVERSE = True

def xtest_motor():
    print(f"testing {MOTORS} motors")
    motor = []
    for i in range(MOTORS):
        motor.append(MotorController(PWMPINS[i], DOUT0PINS[i], DOUT1PINS[i], INVERSE))
    for speed in [100]:
        for i in range(MOTORS):
            motor[i].set_speed(speed)
            motor[i].forward()
        sleep(3)
        for i in range(MOTORS):
            motor[i].reverse()
        sleep(3)
            # motor[i].stop()
    for i in range(MOTORS):
        motor[i].stop()
        motor[i].shutdown(False)

def xtest_slide():
    if MOTORS != 4:
        print(f"test only for quads, not for {MOTORS} motors")
        return
    print(f"testing quad motions")
    motor = []
    for i in range(MOTORS):
        motor.append(MotorController(PWMPINS[i], DOUT0PINS[i], DOUT1PINS[i], INVERSE))
    front = [0, 1]
    back = [2, 3]
    diag1 = [0, 3]
    diag2 = [1, 2]
    left = [0, 2]
    right = [1, 3]
    for speed in [60, 100]:
        for i in left:
            motor[i].forward().set_speed(speed)
        for i in right:
            motor[i].reverse().set_speed(30)
        sleep(5)
        for i in right:
            motor[i].forward().set_speed(speed)
        for i in left:
            motor[i].reverse().set_speed(30)
        sleep(5)
    for i in range(MOTORS):
        motor[i].stop()
        motor[i].shutdown(False)
