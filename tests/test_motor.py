from rover import MotorController
from time import sleep

MOTORS = 2
PWMPINS = [12, 13, 18, 19]
DOUT0PINS = [23, 17, 22, 5]
DOUT1PINS = [24, 27, 25, 6]

def test_motor():
    motor = []
    for i in range(MOTORS):
        motor.append(MotorController(PWMPINS[i], DOUT0PINS[i], DOUT1PINS[i]))
    for speed in [40, 75, 100]:
        for i in range(MOTORS):
            motor[i].set_speed(speed)
            motor[i].forward()
            sleep(3)
        # for i in range(MOTORS):
            motor[i].reverse()
            sleep(3)
            motor[i].stop()
    for i in range(MOTORS):
        motor[i].stop()
        motor[i].shutdown(False)
