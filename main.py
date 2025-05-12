from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Almacén de mensajes
messages = {
    "robot_a": "",
    "robot_b": ""
}

@app.route('/')
def home():
    return "Servidor de comunicación entre robots activo 🚀"

@socketio.on('connect')
def handle_connect():
    print("Cliente conectado")

@socketio.on('disconnect')
def handle_disconnect():
    print("Cliente desconectado")

@socketio.on('send_message')
def handle_send(data):
    robot = data.get('robot')
    message = data.get('message')
    if not robot or not message:
        emit("error", {"message": "Datos incompletos"})
        return

    if robot == "a":
        messages["robot_b"] = message
        emit("receive_message", {"robot": "b", "message": message}, broadcast=True)
    elif robot == "b":
        messages["robot_a"] = message
        emit("receive_message", {"robot": "a", "message": message}, broadcast=True)
    else:
        emit("error", {"message": "Robot desconocido"})

@socketio.on('request_message')
def handle_request(data):
    robot = data.get('robot')
    if robot == "a":
        msg = messages["robot_a"]
        messages["robot_a"] = ""
        emit("receive_message", {"robot": "a", "message": msg})
    elif robot == "b":
        msg = messages["robot_b"]
        messages["robot_b"] = ""
        emit("receive_message", {"robot": "b", "message": msg})
    else:
        emit("error", {"message": "Robot desconocido"})

if __name__ == "__main__":
    import eventlet
    eventlet.monkey_patch()
    socketio.run(app, host="0.0.0.0", port=10000)
