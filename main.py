from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Mensajes en memoria para la demo
messages = {
    "robot_a": "",
    "robot_b": ""
}

@app.route('/')
def home():
    return "Servidor de comunicación entre robots activo 🚀"

# Evento de conexión de WebSocket
@socketio.on('connect')
def handle_connect():
    print("Cliente conectado")

# Evento para enviar mensaje de Robot A o B
@socketio.on('send_message')
def handle_message(data):
    robot = data['robot']
    message = data['message']
    
    if robot == "a":
        messages["robot_b"] = message
        emit("receive_message", {"robot": "b", "message": message}, broadcast=True)
    elif robot == "b":
        messages["robot_a"] = message
        emit("receive_message", {"robot": "a", "message": message}, broadcast=True)

# Evento para recibir mensaje
@socketio.on('request_message')
def handle_request(data):
    robot = data['robot']
    if robot == "a":
        emit("receive_message", {"robot": "a", "message": messages["robot_a"]})
        messages["robot_a"] = ""  # Borra el mensaje después de enviarlo
    elif robot == "b":
        emit("receive_message", {"robot": "b", "message": messages["robot_b"]})
        messages["robot_b"] = ""  # Borra el mensaje después de enviarlo

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
