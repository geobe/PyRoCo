from rover.motor_control import BasicMotorControl, IMotorControl as iMC
from rover.car_driver import CarDriver, DIRMAX
# from flask import Flask, request, render_template
from enum import Enum, auto

class CMD(Enum):
    FORWARD = auto()
    BACKWARD = auto()
    STOP = auto()
    PLUS = auto()
    MINUS = auto()
    UP = auto()
    DOWN = auto()

mc = BasicMotorControl()
driver = CarDriver(mc)

class InputController:
    def __init__(self):
        # mc = motor_controller
        self.STEPS_SPEED = 10
        self.STEPS_STEERING = 20
        self.RATIO_STEERING = int(self.STEPS_STEERING / DIRMAX)

    def handle_command(self, request):
        #print(f"form: {request.form}")
        side = iMC.Side[request.form["side"].upper()]
        value = float(request.form["value"])
        command = CMD[request.form["command"].upper()]
        speed_left = mc.get_motion(iMC.Side.LEFT)["speed"]
        speed_right = mc.get_motion(iMC.Side.RIGHT)["speed"]
        f_left = max(mc.get_frequency(iMC.Side.LEFT)["frequency"], 1)
        f_right = max(mc.get_frequency(iMC.Side.RIGHT)["frequency"], 1)
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
                    mc.set_speed(iMC.Side.LEFT, speed_left + value)
                    mc.set_speed(iMC.Side.RIGHT, speed_right + value)
                if side == iMC.Side.LEFT:
                    mc.set_speed(iMC.Side.LEFT, speed_left + value)
                if side == iMC.Side.RIGHT:
                    mc.set_speed(iMC.Side.RIGHT, speed_right + value)
            case CMD.MINUS:
                if side == iMC.Side.BOTH:
                    mc.set_speed(iMC.Side.LEFT, speed_left - value)
                    mc.set_speed(iMC.Side.RIGHT, speed_right - value)
                if side == iMC.Side.LEFT:
                    mc.set_speed(iMC.Side.LEFT, speed_left - value)
                if side == iMC.Side.RIGHT:
                    mc.set_speed(iMC.Side.RIGHT, speed_right - value)
            case CMD.UP:
                mc.set_auto_frequency(False)
                if side == iMC.Side.BOTH:
                    mc.set_frequency(iMC.Side.LEFT, max(f_left + value, 1))
                    mc.set_frequency(iMC.Side.RIGHT, max(f_right + value, 1))
                if side == iMC.Side.LEFT:
                    mc.set_frequency(iMC.Side.LEFT, max(f_left + value, 1))
                if side == iMC.Side.RIGHT:
                    mc.set_frequency(iMC.Side.RIGHT, max(f_right + value, 1))
            case CMD.DOWN:
                mc.set_auto_frequency(False)
                if side == iMC.Side.BOTH:
                    mc.set_frequency(iMC.Side.LEFT, max(f_left - value, 1))
                    mc.set_frequency(iMC.Side.RIGHT, max(f_right - value, 1))
                if side == iMC.Side.LEFT:
                    mc.set_frequency(iMC.Side.LEFT, max(f_left - value, 1))
                if side == iMC.Side.RIGHT:
                    mc.set_frequency(iMC.Side.RIGHT, max(f_right - value, 1))

        return {'file': "status.html", 'values': self.get_status()}

    def handle_drive(self, request):
        print(f"form: {request.form}")
        if 'command' in request.form:
           cmd = request.form['command']
        else:
            cmd = ''
        if 'value' in request.form:
            value = request.form['value']
        else:
            value = 0
        direction_input = int(request.form["direction"])
        speed = int(request.form["speed"])
        direction = direction_input / self.RATIO_STEERING
        if cmd:
            cmd = cmd.upper()
            print(f"cmd: {cmd}, value: {value}")
            if cmd == 'DIRECTION':
                direction_input += int(value)
                direction = direction_input / self.RATIO_STEERING
            elif cmd == 'SPEED':
                speed += int(value)
            elif cmd == 'STOP':
                speed = 0
        if speed == 0:
            driver.stop()
        else:
            driver.control(speed, direction)
        print(f"form direction: {int(request.form['direction'])}, direction_input: {direction_input} -> direction: {direction}, speed: {speed}")
        values = {"speed": speed, 'direction': direction_input,
                  'SPEED': self.STEPS_SPEED, 'STEER': self.STEPS_STEERING}
        return {'file': "steering.html", 'values': values}

    def get_status(self):
        status = {
            "left": mc.get_motion(iMC.Side.LEFT),
            "right": mc.get_motion(iMC.Side.RIGHT),
            "f_left": mc.get_frequency(iMC.Side.LEFT),
            "f_right": mc.get_frequency(iMC.Side.RIGHT)
        }
        return status

