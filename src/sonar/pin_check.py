from gpiozero import LED
from signal import pause

# check if bcm pins with special roles can be used as simple led pins
class pin_check():
    def __init__(self):
        bcm_pins=[14, 15, 16, 20, 21, 22, 25, 26]
        self.leds = [LED(i) for i in bcm_pins]
    def run(self):
        for led in self.leds:
            led.blink()
        pause()

if __name__ == "__main__":
    pick = pin_check()
    pick.run()

