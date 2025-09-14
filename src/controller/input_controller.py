from rover.definitions import *
from rover.car_driver import *
# from flask import Flask, request, render_template
from enum import Enum, auto

# class CMD(Enum):
#     # FORWARD = auto()
#     # BACKWARD = auto()
#     # STOP = auto()
#     PLUS = auto()
#     MINUS = auto()
#     UP = auto()
#     DOWN = auto()

driver = CarDriver()
mc = driver.mc

class InputController:
    def __init__(self):
        # mc = motor_controller
        self.STEPS_SPEED = 10
        self.STEPS_STEERING = 20
        self.RATIO_STEERING = int(self.STEPS_STEERING / DIRMAX)

    def handle_command(self, request):
        #print(f"form: {request.form}")
        side = Motion[request.form["side"].upper()]
        value = float(request.form["value"])
        command = CMD[request.form["command"].upper()]
        speed_left = mc[Motion.LEFT].get_motion()["speed"]
        speed_right = mc[Motion.RIGHT].get_motion()["speed"]
        f_left = max(mc[Motion.LEFT].get_frequency()["frequency"], 1)
        f_right = max(mc[Motion.RIGHT].get_frequency()["frequency"], 1)
        match command:
            case CMD.STOP:
                if side == Motion.BOTH:
                    mc[Motion.LEFT].set_motion(Motion.STOP)
                    mc[Motion.RIGHT].set_motion(Motion.STOP)
                else:
                    mc[side].set_motion(Motion.STOP)
            case CMD.FORWARD:
                if side == Motion.BOTH:
                    mc[Motion.LEFT].set_motion(Motion.FORWARD)
                    mc[Motion.RIGHT].set_motion(Motion.FORWARD)
                else:
                    mc[side].set_motion(Motion.FORWARD)
            case CMD.BACKWARD:
                if side == Motion.BOTH:
                    mc[Motion.LEFT].set_motion(Motion.BACKWARD)
                    mc[Motion.RIGHT].set_motion(Motion.BACKWARD)
                else:
                    mc[side].set_motion(Motion.BACKWARD)
            case CMD.PLUS:
                if side == Motion.BOTH:
                    mc[Motion.LEFT].set_speed(speed_left + value)
                    mc[Motion.RIGHT].set_speed(speed_right + value)
                if side == Motion.LEFT:
                    mc[Motion.LEFT].set_speed(speed_left + value)
                if side == Motion.RIGHT:
                    mc[Motion.RIGHT].set_speed(speed_right + value)
            case CMD.MINUS:
                if side == Motion.BOTH:
                    mc[Motion.LEFT].set_speed(speed_left - value)
                    mc[Motion.RIGHT].set_speed(speed_right - value)
                if side == Motion.LEFT:
                    mc[Motion.LEFT].set_speed(speed_left - value)
                if side == Motion.RIGHT:
                    mc[Motion.RIGHT].set_speed(speed_right - value)
            case CMD.UP:
                # mc.set_auto_frequency(False)
                if side == Motion.BOTH:
                    mc[Motion.LEFT].set_frequency(max(f_left + value, 1))
                    mc[Motion.RIGHT].set_frequency(max(f_right + value, 1))
                if side == Motion.LEFT:
                    mc[Motion.LEFT].set_frequency(max(f_left + value, 1))
                if side == Motion.RIGHT:
                    mc[Motion.RIGHT].set_frequency(max(f_right + value, 1))
            case CMD.DOWN:
                # mc.set_auto_frequency(False)
                if side == Motion.BOTH:
                    mc[Motion.LEFT].set_frequency(max(f_left - value, 1))
                    mc[Motion.RIGHT].set_frequency(max(f_right - value, 1))
                if side == Motion.LEFT:
                    mc[Motion.LEFT].set_frequency(max(f_left - value, 1))
                if side == Motion.RIGHT:
                    mc[Motion.RIGHT].set_frequency(max(f_right - value, 1))

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
            "left": mc[Motion.LEFT].get_motion(),
            "right": mc[Motion.RIGHT].get_motion(),
            "f_left": mc[Motion.LEFT].get_frequency(),
            "f_right": mc[Motion.RIGHT].get_frequency()
        }
        return status

