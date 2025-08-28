# gpio_config.py

from gpiozero import LED, PWMLED

# DigitalOutput is LED in gpiozero speech, not only usable as led
class DigitalOutput:
    def __init__(self, pin: int, initial_value: bool = False):
        self.led = LED(pin, initial_value=initial_value)
    #    self.led(off)
    def high(self): self.led.on()
    def low(self): self.led.off()
    def shutdown(self): self.led.close()

# Pwm (pulse width modulation) is PWMLED in gpiozero speech
class Pwm:
    def __init__(self, pin: int, dutyCycle: int = 0, frequency: int = 0):
        self.pwm = PWMLED(pin, frequency = frequency)
        # self.dutyCycle = dutyCycle

    def on(self, duty_cycle: int, frequency: int):
        period = 1 / frequency
        duty_cycle = min(100, duty_cycle)
        onTime = duty_cycle * period / 100
        offTime = period - onTime
        # print(f"on: {onTime}, off: {offTime} aus freq: {frequency}, period: {period}, dutycycle: {duty_cycle}")
        self.pwm.blink(onTime, offTime)
    def off(self): self.pwm.off()
    def shutdown(self): self.pwm.close()
#
# class GpioConfigService:
#     @staticmethod
#     def create_pwm(pin: int) -> Pwm:
#         return Pwm(pin)
#
#     @staticmethod
#     def create_digital_output(pin: int) -> DigitalOutput:
#         return DigitalOutput(pin)
