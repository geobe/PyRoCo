from rover import BasicMotorControl, IMotorControl
from flask import Flask, request, render_template

class InputController:
    def __init__(self):
        pass
    def handleCommand(self, request):
        print(f"form: {request.form}")
        print(f"args: {request.args}")

