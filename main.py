from flask import Flask, request, jsonify

app = Flask(__name__)

# Mensajes en memoria (simple para la demo)
messages = {
    "robot_a": "",
    "robot_b": ""
}

@app.route("/send/<robot>", methods=["POST"])
def send_message(robot):
    data = request.get_json()
    message = data.get("message")

    if robot == "a":
        messages["robot_b"] = message
    elif robot == "b":
        messages["robot_a"] = message
    else:
        return jsonify({"error": "robot inválido"}), 400

    return jsonify({"status": "mensaje enviado"}), 200

@app.route("/receive/<robot>", methods=["GET"])
def receive_message(robot):
    if robot == "a":
        msg = messages["robot_a"]
        messages["robot_a"] = ""
    elif robot == "b":
        msg = messages["robot_b"]
        messages["robot_b"] = ""
    else:
        return jsonify({"error": "robot inválido"}), 400

    return jsonify({"message": msg}), 200

@app.route("/", methods=["GET"])
def home():
    return "Servidor de comunicación entre robots activo 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
