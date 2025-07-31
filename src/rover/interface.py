from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict

class IMotorControl(ABC):
    class Side(Enum):
        LEFT = auto()
        RIGHT = auto()
        BOTH = auto()

    class Motion(Enum):
        FORWARD = auto()
        STOP = auto()
        BACKWARD = auto()

    @abstractmethod
    def set_motion(self, side: 'IMotorControl.Side', motion: 'IMotorControl.Motion') -> Dict:
        pass

    @abstractmethod
    def get_motion(self, side: 'IMotorControl.Side') -> Dict:
        pass

    @abstractmethod
    def set_speed(self, side: 'IMotorControl.Side', speed: float) -> Dict:
        pass

    @abstractmethod
    def get_speed(self, side: 'IMotorControl.Side') -> Dict:
        pass

    @abstractmethod
    def set_frequency(self, side: 'IMotorControl.Side', frequency: int) -> Dict:
        pass

    @abstractmethod
    def get_frequency(self, side: 'IMotorControl.Side') -> Dict:
        pass

    @abstractmethod
    def shutdown(self, exit_program: bool):
        pass
