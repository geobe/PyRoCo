from enum import Enum, auto
from .gpio_config import DigitalOutput, Pwm

class MotorController():
    class Motion(Enum):
        FORWARD = auto()
        STOP = auto()
        BACKWARD = auto()

    def __init__(self, pwm:int, dout0:int, dout1:int, inverse = False):
        self.pwm = Pwm(pwm)
        if inverse:
            self.dig_out = [DigitalOutput(dout1), DigitalOutput(dout0)]
        else:
            self.dig_out = [DigitalOutput(dout0), DigitalOutput(dout1)]
        self.motion = self.Motion.STOP
        self.speed = 0.0
        self.frequency = 2
        self.auto_frequency = True

    def set_auto_frequency(self, val: bool):
        self.auto_frequency = val
        return self

    def forward(self):
        self.dig_out[0].high()
        self.dig_out[1].low()
        if self.speed > 0:
            self.pwm.on(self.speed, self.frequency)
        return self #{"speed": self.speed, "motion": self.motion}

    def reverse(self):
        self.dig_out[0].low()
        self.dig_out[1].high()
        if self.speed > 0:
            self.pwm.on(self.speed, self.frequency)
        return self #{"speed": self.speed, "motion": self.motion}

    def stop(self):
        self.dig_out[0].low()
        self.dig_out[1].low()
        self.pwm.off()
        return self #{"speed": self.speed, "motion": self.motion}

    def set_motion(self, motion):
        self.motion = motion
        if motion == self.Motion.FORWARD:
            return self.forward()
        elif motion == self.Motion.BACKWARD:
            return self.reverse()
        else:
            return self.stop()

    def get_motion(self):
        motion = self.motion.name
        speed = self.speed
        return {"speed": speed, "motion": motion}

    def set_speed(self, speed):
        self.speed = max(0.0, min(100.0, speed))
        if self.speed > 0:
            self.pwm.on(self.speed, self.freq4speed(self.speed))
        return self.get_motion()

    def get_speed(self):
        return self.get_motion()

    def set_frequency(self, frequency):
        self.frequency = frequency
        if self.speed > 0:
            self.pwm.on(self.speed, self.frequency)
        return self # {"frequency": self.frequency}

    def get_frequency(self):
        return {"frequency": self.frequency}

    def shutdown(self, exit_program=True):
        self.pwm.off()
        self.pwm.shutdown()
        for dout_pin in self.dig_out:
            dout_pin.shutdown()
        if exit_program:
            import sys
            sys.exit(0)

    def freq4speed(self, speed):
        if not self.auto_frequency:
            result = self.frequency
        elif speed < 6:
            result = 1
        elif speed < 12:
            result = 4
        elif speed < 16:
            result = 7
        elif speed < 24:
            result = 15
        elif speed < 28:
            result = 20
        elif speed < 33:
            result = 25
        elif speed < 51:
            result = 32
        else:
            result = 64
        self.frequency = result
        return result
