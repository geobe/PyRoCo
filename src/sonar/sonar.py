from distance_sensor import SonarSensor
from stepper_motor import StepperMotor, STEPDEFAULT
from time import sleep

class Sonar:
    def __init__(self):
        self.sensor = SonarSensor()
        self.motor = StepperMotor()

    # find the zero position by identifying an object straight ahead
    def center_calibrate(self, far_limit=0.5):
        scout = Scout(sensor=self.sensor, limit=far_limit)
        print('Distance: ', self.sensor.gpio_sensor.distance * 100)
        sleep(1)
        # look at minus side for marker echo
        self.motor.run_steps(step_count=STEPDEFAULT)
        sleep(1)
        self.motor.run_steps(step_count=-2*STEPDEFAULT, delay=0.01, eval=scout.find_in_range, truncate=False)
        center = (scout.limitPlus + scout.limitMinus) // 2
        print(f"limits: {scout.limitPlus}, {scout.limitMinus} -> center {center}")
        sleep(1)
        self.motor.run_zero()
        sleep(1)
        self.motor.run_steps(center)
        self.motor.set_zero()
        resolution = abs(scout.limitPlus - scout.limitMinus) / 4096
        resolution_degrees = resolution * 360
        print(f"resolution: {resolution_degrees}°, {resolution}%")


class Scout:
    def __init__(self, sensor: SonarSensor,  limit = 0.3):
        self.found = False
        self.sensor = sensor
        self.limit = limit
        self.limitPlus = 0
        self.limitMinus = 0

    def find_in_range(self, position):
        distance = self.sensor.distance
        if position % 32 == 0:
            print(f"{'found' if self.found else 'not found'} - {position}: {distance}")
        if distance < self.limit and not self.found:
            # first hit of target
            self.found = True
            self.limitPlus = position
            return True
        elif distance < self.limit and self.found:
            # proceed on target
            return True
        elif not self.found:
            # target not yet found
            return True
        else:
            # after last hit of target
            self.limitMinus = position + 1
            return False

    def reset(self):
        self.found = False
        self.count = 0

if __name__ == "__main__":
    sonar = Sonar()
    sonar.center_calibrate()