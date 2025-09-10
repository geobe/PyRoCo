# gpio_config.py

from gpiozero import LED, PWMLED, Device
from .pin_factory_config import EnvironmentConfigurator

# class IoBase:
#     _initialized = False
#
#     @classmethod
#     def _init_class(cls):
#         print((f"init IoBase"))
#         if not cls._initialized:
#             configurator = PinFactoryConfigurator()
#             factory = configurator.get_pin_factory()
#             print((f"host: {factory.host} @ factory: {factory}"))
#             if factory != None:
#                 Device.pin_factory = factory
#             print("Device Factory initialized")
#             cls._initialized = True
#
#     def __init__(self):
#         IoBase._init_class()   # sorgt dafür, dass es beim ersten Objekt passiert
#

class DigitalOutput():
    '''
    DigitalOutput is LED in gpiozero speech, not only usable as led
    '''

    def __init__(self, pin: int, initial_value: bool = False):
        '''
        Constructor
        :param pin: pin number, BCM numbering
        :param initial_value: on or off
        '''
        configurator = EnvironmentConfigurator()
        factory = configurator.get_pin_factory()
        print((f"host: {factory.host} @ factory: {factory}"))
        self.led = LED(pin, initial_value=initial_value, pin_factory=factory)
    #    self.led(off)
    def high(self): self.led.on()
    def low(self): self.led.off()
    def shutdown(self): self.led.close()

class Pwm():
    '''
    Pwm (pulse width modulation) is PWMLED in gpiozero speech
    '''
    pass
    def __init__(self, pin: int, frequency: int = 0):
        '''
        Constructor
        :param pin: pin number, BCM numbering
        :param frequency: in Hz
        '''
        configurator = EnvironmentConfigurator()
        factory = configurator.get_pin_factory()
        print((f"host: {factory.host} @ factory: {factory}"))
        self.pwm = PWMLED(pin, frequency = frequency, pin_factory=factory)

    def on(self, duty_cycle: int, frequency: int):
        period = 1 / frequency
        duty_cycle = min(100, duty_cycle)
        onTime = duty_cycle * period / 100
        offTime = period - onTime
        # print(f"on: {onTime}, off: {offTime} aus freq: {frequency}, period: {period}, dutycycle: {duty_cycle}")
        self.pwm.blink(onTime, offTime)
    def off(self): self.pwm.off()
    def shutdown(self): self.pwm.close()
