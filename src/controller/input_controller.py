from rover import BasicMotorControl, IMotorControl as iMC
from flask import Flask, request, render_template
from enum import Enum, auto

class CMD(Enum):
    FORWARD = auto()
    BACKWARD = auto()
    STOP = auto()
    PLUS = auto()
    MINUS = auto()

mc = BasicMotorControl()

class InputController:
    def __init__(self):
        # mc = motor_controller
        pass
    def handleCommand(self, request):
        print(f"form: {request.form}")
        side = iMC.Side[request.form["side"].upper()]
        speed = float(request.form["value"])
        command = CMD[request.form["command"].upper()]
        speed_left = mc.get_motion(iMC.Side.LEFT)["speed"]
        speed_right = mc.get_motion(iMC.Side.RIGHT)["speed"]
        match command:
            case CMD.STOP:
                if side == iMC.Side.BOTH:
                    mc.set_motion(iMC.Side.LEFT, iMC.Motion.STOP)
                    mc.set_motion(iMC.Side.RIGHT, iMC.Motion.STOP)
                else:
                    mc.set_motion(side, iMC.Motion.STOP)
            case CMD.FORWARD:
                if side == iMC.Side.BOTH:
                    mc.set_motion(iMC.Side.LEFT, iMC.Motion.FORWARD)
                    mc.set_motion(iMC.Side.RIGHT, iMC.Motion.FORWARD)
                else:
                    mc.set_motion(side, iMC.Motion.FORWARD)
            case CMD.BACKWARD:
                if side == iMC.Side.BOTH:
                    mc.set_motion(iMC.Side.LEFT, iMC.Motion.BACKWARD)
                    mc.set_motion(iMC.Side.RIGHT, iMC.Motion.BACKWARD)
                else:
                    mc.set_motion(side, iMC.Motion.BACKWARD)
            case CMD.PLUS:
                if side == iMC.Side.BOTH:
                    mc.set_speed(iMC.Side.LEFT, speed_left + speed)
                    mc.set_speed(iMC.Side.RIGHT, speed_right + speed)
                if side == iMC.Side.LEFT:
                    mc.set_speed(iMC.Side.LEFT, speed_left + speed)
                if side == iMC.Side.RIGHT:
                    mc.set_speed(iMC.Side.RIGHT, speed_right + speed)
            case CMD.MINUS:
                if side == iMC.Side.BOTH:
                    mc.set_speed(iMC.Side.LEFT, speed_left - speed)
                    mc.set_speed(iMC.Side.RIGHT, speed_right - speed)
                if side == iMC.Side.LEFT:
                    mc.set_speed(iMC.Side.LEFT, speed_left - speed)
                if side == iMC.Side.RIGHT:
                    mc.set_speed(iMC.Side.RIGHT, speed_right - speed)

        return {'file': "status.html", 'values': self.get_status()}

    def get_status(self):
        status = {
            "left": mc.get_motion(iMC.Side.LEFT),
            "right": mc.get_motion(iMC.Side.RIGHT)
        }
        return status

