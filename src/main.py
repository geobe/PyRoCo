from rover import BasicMotorControl, IMotorControl
from time import sleep

mc = BasicMotorControl()
for i in range(20, 101, 20):
    print(f"speed: {i}")
    mc.set_speed(IMotorControl.Side.LEFT, i)
    mc.set_motion(IMotorControl.Side.LEFT, IMotorControl.Motion.FORWARD)
    # print(mc.get_frequency(IMotorControl.Side.LEFT))
    mc.set_speed(IMotorControl.Side.RIGHT, i)
    mc.set_motion(IMotorControl.Side.RIGHT, IMotorControl.Motion.FORWARD)
    sleep(5)
mc.shutdown()
