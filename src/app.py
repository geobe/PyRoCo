from flask import Flask, request, render_template
# from flask_socketio import SocketIO, emit
from rover import BasicMotorControl, IMotorControl
from controller import InputController

app = Flask(__name__)
# mc = BasicMotorControl()
ctrl = InputController()
# socketio = SocketIO(app)

clients = set()

@app.route("/")
def index():
    status = ctrl.get_status()
    #     {
    #     "left": mc.get_motion(IMotorControl.Side.LEFT),
    #     "right": mc.get_motion(IMotorControl.Side.RIGHT)
    # }
    values = {'SPEED': ctrl.STEPS_SPEED, 'STEER': ctrl.STEPS_STEERING }
    merged = status | values
    return render_template("control.html", status=merged)

# WebSocket mit werkzeug.serving für Entwicklung (kein Produktionsbetrieb)
from flask_sock import Sock
sock = Sock(app)

@app.route("/command", methods=["POST"])
def command():
    to_render = ctrl.handle_command(request)
    send_ws(to_render)
    return ("", 204)  # kein direktes Update für den Sender

@app.route("/drive", methods=["POST"])
def drive():
    to_render = ctrl.handle_drive(request)
    file = to_render['file']
    values = to_render['values']
    fragment = render_template(file, status=values)
    send_fragment_ws(fragment)
    send_ws({'file': 'status.html', 'values': ctrl.get_status()})
    return ("", 204)  # kein direktes Update für den Sender

def send_fragment_ws(fragment):
    for ws in list(clients):
        try:
            ws.send(fragment)
        except:
            clients.remove(ws)

def send_ws(to_render):
    fragment = render_template(to_render["file"], status=to_render["values"])
    for ws in list(clients):
        try:
            ws.send(fragment)
        except:
            clients.remove(ws)


@sock.route("/ws")
def websocket(ws):
    clients.add(ws)
    try:
        while True:
            msg = ws.receive()  # blockiert
            if msg is None:
                break
    finally:
        clients.discard(ws)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
