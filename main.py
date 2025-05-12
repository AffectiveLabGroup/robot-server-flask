from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Almacén de mensajes
messages = {
    "robot_a": "",
    "robot_b": ""
}

# Mapa de SID (cliente) a rol ("a" o "b")
client_roles = {}

@app.route('/')
def home():
    return "Servidor de comunicación entre robots activo 🚀"

@socketio.on('connect')
def handle_connect():
    print(f"Cliente conectado: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Cliente desconectado: {request.sid}")
    client_roles.pop(request.sid, None)

@socketio.on('register')
def handle_register(data):
    robot = data.get('robot')
    if robot in ['a', 'b']:
        client_roles[request.sid] = robot
        print(f"Cliente {request.sid} registrado como robot {robot}")
        emit("registered", {"status": "ok", "robot": robot})
    else:
        emit("registered", {"status": "error", "message": "Rol inválido"})

@socketio.on('send_message')
def handle_send(data):
    sender_role = client_roles.get(request.sid)
    if not sender_role:
        emit("error", {"message": "Cliente no registrado"})
        return

    message = data.get('message')
    if not message:
        emit("error", {"message": "Mensaje vacío"})
        return

    # Enviar mensaje al otro robot
    if sender_role == "a":
        messages["robot_b"] = message
        emit("receive_message", {"robot": "b", "message": message}, broadcast=True)
    elif sender_role == "b":
        messages["robot_a"] = message
        emit("receive_message", {"robot": "a", "message": message}, broadcast=True)

@socketio.on('request_message')
def handle_request():
    requester = client_roles.get(request.sid)
    if not requester:
        emit("error", {"message": "Cliente no registrado"})
        return

    if requester == "a":
        msg = messages["robot_a"]
        messages["robot_a"] = ""
        emit("receive_message", {"robot": "a", "message": msg})
    elif requester == "b":
        msg = messages["robot_b"]
        messages["robot_b"] = ""
        emit("receive_message", {"robot": "b", "message": msg})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
