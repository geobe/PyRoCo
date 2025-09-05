
from gpiozero.pins.pigpio import PiGPIOFactory
# from gpiozero.pins.lgpio import LGPIOFactory
# from gpiozero.pins.mock import MockFactory
from gpiozero.pins.pi import PiFactory

from enum import Enum, auto
from .utils import get_project_root
import platform
import subprocess


class SYS(Enum):
    '''
    Enum to tag own system
    '''
    RASPI = auto()  # Raspberry Pi
    LNX = auto()  # Linux
    WDW = auto()  # Windows
    # MAC: auto()"pigpio (>=1.78,<2.0.0)",

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Erzeuge Instanz")
            cls._instance = super().__new__(cls)
        return cls._instance


class PinFactoryConfigurator:
    '''
    Singleton class
    Configure pin factory for local (raspberry pi)
    or remote (linux, ???) system
    '''

    _instance = None
    '''
    the single instance is here
    '''

    def __new__(cls, *args, **kwargs):
        '''
        here we go whenever a constructor ios called
        :param args: constructor args
        :param kwargs: constructor kwargs
        '''
        if cls._instance is None:
            # print("create new instance")
            cls._instance = super().__new__(cls)
            cls._instance.init_once()
        # else:
        #     print("return existing")
        return cls._instance

    def __init__(self):
        pass

    def init_once(self):
        self.param = '-n' if platform.system().lower() == 'windows' else '-c'
        self._initialized = False
        self.factory = None


    def my_system(self) -> SYS:
        '''
        which  kind of system are we running on
        :return: SYS Enum value for our system
        '''
        pform = platform.platform()
        if 'rpi' in pform and 'aarch64' in pform:
            return SYS.RASPI
        elif 'Linux' in pform:
            return SYS.LNX
        else:
            return SYS.WDW

    def find_rover(self) -> str:
        rover_list = []
        project_root = get_project_root()
        file = project_root / 'data' / 'roverlist.txt'
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                rover_list.append(line)

        for rover_net_address in rover_list:
            if self.check_ping(rover_net_address):
                return rover_net_address
        return ''

    def check_ping(self, hostname: str) -> bool:
        cmd = ['ping', self.param, '1']
        cmd.append(hostname)
        print(f"hostname: {hostname}, cmd: {cmd}")
        response = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,  # unterdrückt normale Ausgabe
            stderr=subprocess.DEVNULL  # unterdrückt Fehlermeldungen (optional)
        )
        return  response.returncode == 0

    def get_pin_factory(self) -> PiFactory:
        if self._initialized:
            # print("factory exists")
            return self.factory
        else:
            # print("finding factory")
            self._initialized = True
            if self.my_system() == SYS.RASPI:
                return None #LGPIOFactory(chip=0)
            else:
                rover = self.find_rover()
                if len(rover) > 0:
                    # print(f"found {rover}")
                    self.factory = PiGPIOFactory(host=rover)
                    return self.factory
                else:
                    return None #MockFactory()

