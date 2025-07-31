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
    return render_template("control.html", status=status)

@app.route("/control", methods=["POST"])
def control():
    side = IMotorControl.Side[request.form["side"].upper()]
    motion = IMotorControl.Motion[request.form["motion"].upper()]
    speed = float(request.form["speed"])

    print(f"side: {side}, motion: {motion}, speed: {speed} ")

    mc.set_speed(side, speed)
    mc.set_motion(side, motion)
    status = {
        "left": mc.get_motion(IMotorControl.Side.LEFT),
        "right": mc.get_motion(IMotorControl.Side.RIGHT)
    }

    # Aktualisiertes Fragment senden
    fragment = render_template("status.html", status=status)
    for ws in list(clients):
        try:
            ws.send(fragment)
        except:
            clients.remove(ws)
    return ("", 204)  # kein direktes Update für den Sender

# WebSocket mit werkzeug.serving für Entwicklung (kein Produktionsbetrieb)
from flask_sock import Sock
sock = Sock(app)

@app.route("/command", methods=["POST"])
def command():
    to_render = ctrl.handleCommand(request)
    send_ws(to_render)
    return ("", 204)  # kein direktes Update für den Sender

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
