from gpiozero import DistanceSensor
from time import sleep

class SonarSensor:
    def __init__(self, max_distance=3.0, threshold_distance=0.3, queue_len=4):
        self.gpio_sensor = DistanceSensor(trigger=14, echo=15,
                                          max_distance=max_distance,
                                          threshold_distance=threshold_distance,
                                          queue_len=queue_len)

    distance = property(fget=lambda self: self.gpio_sensor.distance)

    def _set_md(self, val):
        if self.gpio_sensor.threshold_distance > val:
            self.gpio_sensor.threshold_distance = max(val - 0.01, 0)
        self.gpio_sensor.max_distance = val

    max_distance = property(fget=lambda self: self.gpio_sensor.max_distance,
        fset=_set_md)

    def check(self):
        md = 1.0
        while True:
            print(f"Distance: {self.distance * 100}, max: {self.max_distance * 100}")
            self.max_distance = md
            md -= 0.05
            if md <= 0.05:
                break
            sleep(1)

if __name__ == "__main__":
    dist = SonarSensor()
    dist.check()
