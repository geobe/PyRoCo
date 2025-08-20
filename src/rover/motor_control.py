from typing import Dict
from .interface import IMotorControl
from .gpio_config import DigitalOutput, Pwm

class BasicMotorControl(IMotorControl):
    def __init__(self):
        self.pwm = {
            self.Side.LEFT: Pwm(12),
            self.Side.RIGHT: Pwm(13),
        }
        self.dout = {
            self.Side.LEFT: [DigitalOutput(23),
                             DigitalOutput(24)],
            self.Side.RIGHT: [DigitalOutput(17),
                              DigitalOutput(27)],
        }
        self.motion = {
            self.Side.LEFT: self.Motion.STOP,
            self.Side.RIGHT: self.Motion.STOP
        }
        self.speed = {
            self.Side.LEFT: 0.0,
            self.Side.RIGHT: 0.0
        }
        self.freq = {
            self.Side.LEFT: 2,
            self.Side.RIGHT: 2
        }
        for pwm_pin in self.pwm.values():
            pwm_pin.off()

    def forward(self, side):
        pins = self.dout[side]
        pins[0].high()
        pins[1].low()
        if self.speed[side] > 0:
            self.pwm[side].on(self.speed[side], self.freq[side])
        return {"speed": self.speed[side], "motion": self.motion[side]}

    def reverse(self, side):
        pins = self.dout[side]
        pins[0].low()
        pins[1].high()
        if self.speed[side] > 0:
            self.pwm[side].on(self.speed[side], self.freq[side])
        return {"speed": self.speed[side], "motion": self.motion[side]}

    def stop(self, side):
        pins = self.dout[side]
        pins[0].low()
        pins[1].low()
        self.pwm[side].off()
        return {"speed": self.speed[side], "motion": self.motion[side]}

    def set_motion(self, side, motion):
        self.motion[side] = motion
        if motion == self.Motion.FORWARD:
            return self.forward(side)
        elif motion == self.Motion.BACKWARD:
            return self.reverse(side)
        else:
            return self.stop(side)

    def get_motion(self, side):
        motion = self.motion[side].name
        speed = self.speed[side]
        return {"speed": speed, "motion": motion}

    def set_speed(self, side, speed):
        self.speed[side] = max(0.0, min(100.0, speed))
        if self.speed[side] > 0:
            self.pwm[side].on(self.speed[side], self.freq4speed(self.speed[side], side))
        return self.get_motion(side)

    def get_speed(self, side):
        return self.get_motion(side)

    def set_frequency(self, side, frequency):
        self.freq[side] = frequency
        if self.speed[side] > 0:
            self.pwm[side].on(self.speed[side], self.freq[side])
        return {"frequency": self.freq[side]}

    def get_frequency(self, side):
        return {"frequency": self.freq[side]}

    def shutdown(self, exit_program=True):
        for side in [self.Side.LEFT, self.Side.RIGHT]:
            self.pwm[side].off()
            self.pwm[side].shutdown()
            for dout_pin in self.dout[side]:
                dout_pin.shutdown()
        if exit_program:
            import sys
            sys.exit(0)

    def freq4speed(self, speed, side):
        if speed < 7:
            result = 12
        # elif speed < 14:
        #     result = 8
        elif speed < 21:
            result = 12
        elif speed < 28:
            result = 16
        elif speed < 51:
            result = 32
        else:
            result = 32
        self.freq[side] = result
        return result
