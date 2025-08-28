from gpiozero import LED
from time import sleep
from random import randrange

STEPLIMIT = 1024
STEPDEFAULT = 768

step_sequence = [[1, 0, 0, 1],
                  [1, 0, 0, 0],
                  [1, 1, 0, 0],
                  [0, 1, 0, 0],
                  [0, 1, 1, 0],
                  [0, 0, 1, 0],
                  [0, 0, 1, 1],
                  [0, 0, 0, 1]]

class StepperMotor:
    def __init__(self):
        # BCM pins used
        motor_pins = [26, 16, 20, 21]
        # the hardware output pins
        self.motor_pins = [LED(i) for i in motor_pins]
        # the actual step
        self.motor_step = 0
        # the actual sequence position
        self.motor_sequence_index = 0
        # sleep time between steps
        # careful lowering this, at some point you run into
        # the mechanical limitation of how quick your motor can move
        self.step_sleep = 0.005
        self.step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°

        # defining stepper motor sequence (
        # found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
    def run_steps(self, step_count = STEPDEFAULT, delay = 0.005, delay2=0.005, truncate = True, eval=lambda a: True):
            if truncate and step_count > STEPLIMIT:
                step_count = STEPDEFAULT
            elif truncate and step_count < -STEPLIMIT:
                step_count = -STEPDEFAULT
            forward =  step_count >= 0
            step_count = abs(step_count)

            # sequence_count = len(step_sequence) * step_count
            for i in range(step_count):
                if forward:
                    self.motor_sequence_index = i % 8
                    self.motor_step += 1
                else:
                    self.motor_sequence_index = 7 - i % 8
                    self.motor_step -= 1
                sequence = step_sequence[self.motor_sequence_index]
                for pin in range(len(sequence)):
                    if(sequence[pin]):
                        self.motor_pins[pin].on()
                    else:
                        self.motor_pins[pin].off()
                if not i % 4:
                    sleep(delay2)
                    if not eval(self.motor_step):
                        break
                else:
                    sleep(delay)

    def run_zero(self):
        # print(f"stepcount: {self.motor_step}")
        self.run_steps(-self.motor_step, truncate=False)
        # print(f"end stepcount: {self.motor_step}")

    def set_zero(self):
        self.motor_step = self.motor_sequence_index
        self.run_zero()


