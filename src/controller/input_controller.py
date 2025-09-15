from rover.definitions import Motion
from rover.car_driver import *
# from flask import Flask, request, render_template
from enum import Enum, auto

driver = CarDriver()
mc = driver.mc

class InputController:
    def __init__(self):
        # mc = motor_controller
        self.STEPS_SPEED = 10
        self.STEPS_STEERING = 20
        self.RATIO_STEERING = int(self.STEPS_STEERING / DIRMAX)

    def decode_request(self, request) -> dict:
        print(f"form: {request.form}")
        values = {}
        if 'side' in request.form:
            values['side'] = Motion[request.form["side"].upper()]
        else:
            values['side'] = Motion.NONE
        if 'command' in request.form:
            values["command"] = Motion[request.form['command'].upper()]
        else:
            values["command"] = Motion.NONE
        if 'value' in request.form:
            values["value"] = request.form['value']
        else:
            values["value"] = '0'
        if 'speed' in request.form:
            values['speed'] = int(request.form["speed"])
        else:
            values['speed'] = 0
        if 'direction' in request.form:
            values["direction"] = int(request.form["direction"])
        else:
            values["direction"] = 0
        return values

    def handle_command(self, values):
        print(f"side: {values['side']}")
        side = values['side'] if 'side' in values else Motion.BOTH
        value = float(values['value']) if 'value' in values else 0.0
        command = values['command'] if 'command' in values else ''
        speed = {}
        speed[Motion.LEFT] = mc[Motion.LEFT].get_motion()["speed"]
        speed[Motion.RIGHT] = mc[Motion.RIGHT].get_motion()["speed"]
        f = {}
        f[Motion.LEFT] = max(mc[Motion.LEFT].get_frequency()["frequency"], 1)
        f[Motion.RIGHT] = max(mc[Motion.RIGHT].get_frequency()["frequency"], 1)
        if side == Motion.BOTH:
            directions = [Motion.LEFT, Motion.RIGHT]
        else:
            directions = [side]
        for dir in directions:
            match command:
                case Motion.STOP:
                    # mc.set_auto_frequency(True)
                    mc[dir].set_motion(Motion.STOP)
                case Motion.FORWARD:
                    mc[dir].set_motion(Motion.FORWARD)
                case Motion.BACKWARD:
                    mc[dir].set_motion(Motion.BACKWARD)
                case Motion.PLUS:
                    mc[dir].set_speed(speed[dir] + value)
                case Motion.MINUS:
                    mc[dir].set_speed(speed[dir] - value)
                case Motion.UP:
                    # mc.set_auto_frequency(False)
                    mc[dir].set_frequency(f[dir] + value)
                case Motion.DOWN:
                    # mc.set_auto_frequency(False)
                    mc[dir].set_frequency(f[dir] - value)

        return {'file': "status.html", 'values': self.get_status()}

    def handle_drive(self, values):
        cmd = values['command']
        value = values['value']
        direction_input = values["direction"]
        speed = values["speed"]
        direction = direction_input / self.RATIO_STEERING
        match cmd:
            case Motion.DIRECTION:
                direction_input += int(value)
                direction = direction_input / self.RATIO_STEERING
            case Motion.SPEED:
                speed += int(value)
            case Motion.STOP:
                speed = 0
        if speed == 0:
            driver.stop()
        else:
            driver.control(speed, direction)
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

