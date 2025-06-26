from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)


# Almacén de mensajes
messages = {
    "robot_lola": "",
    "robot_lolo": "",
    "humano": ""
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

    if robot == "lola":
        messages["robot_lolo"] = message
        emit("receive_message", {"robot": "lolo", "message": message}, broadcast=True)
    elif robot == "lolo":
        messages["robot_lola"] = message
        emit("receive_message", {"robot": "lola", "message": message}, broadcast=True)
    elif robot == "humano":
        messages["humano"] = message
        emit("receive_message", {"robot": "humano", "message": message}, broadcast=True)
    else:
        emit("error", {"message": "Robot desconocido"})

@socketio.on('request_message')
def handle_request(data):
    robot = data.get('robot')
    if robot == "lola":
        msg = messages["robot_lola"]
        messages["robot_lola"] = ""
        emit("receive_message", {"robot": "lola", "message": msg})
    elif robot == "lolo":
        msg = messages["robot_lolo"]
        messages["robot_lolo"] = ""
        emit("receive_message", {"robot": "lolo", "message": msg})
    elif robot == "humano":
        msg = messages["humano"]
        messages["humano"] = ""
        emit("receive_message", {"robot": "humano", "message": msg})
    else:
        emit("error", {"message": "Robot desconocido"})

if __name__ == "__main__":
    import eventlet
    eventlet.monkey_patch()
    socketio.run(app, host="0.0.0.0", port=10000)
