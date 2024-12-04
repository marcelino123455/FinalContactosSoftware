from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

class Usuario:
    def __init__(self, alias, nombre, contactos=None):

        self.alias = alias
        self.nombre = nombre
        self.contactos = []
        self.mensajes_recibidos = []
        self.mensajes_enviados = []

        for contacto in contactos:
            self.add_contacto(contacto[0], contacto[1])


    def add_contacto(self, alias, nombre):
        if alias not in [contacto[0] for contacto in self.contactos]:
            fecha_registro = datetime.now()
            self.contactos.append((alias, nombre, fecha_registro))
        else:
            raise ValueError(f"El contacto con alias {alias} ya existe.")

    def recibir_mensaje(self, mensaje):
        self.mensajes_recibidos.append(mensaje)

    def enviar_mensaje(self, contacto, contenido):
        mensaje = {
            'de': self.alias,
            'para': contacto.alias,
            'contenido': contenido,
            'fecha': datetime.now()
        }
        contacto.recibir_mensaje(mensaje)
        self.mensajes_enviados.append(mensaje)


BD = [
    Usuario("cpaz", "Christian", [("lmunoz", "Luisa"), ("mgrau", "Miguel")]),
    Usuario("lmunoz", "Luisa", [("mgrau", "Miguel")]),
    Usuario("mgrau", "Miguel", [("cpaz", "Christian")])
]

def obtener_usuario_por_alias(alias):
    for usuario in BD:
        if usuario.alias == alias:
            return usuario
    return None


@app.route('/mensajeria/contactos/<alias>', methods=['GET'])
def obtener_contactos(alias):
    usuario = obtener_usuario_por_alias(alias)
    if usuario:
        contactos = {contacto[0]: contacto[1] for contacto in usuario.contactos}
        return jsonify(contactos)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404


@app.route('/mensajeria/contactos/<alias>', methods=['POST'])
def agregar_contacto(alias):
    data = request.get_json()
    contacto_alias = data.get("contacto")
    contacto_nombre = data.get("nombre")

    usuario = obtener_usuario_por_alias(alias)
    if usuario:
        try:
            usuario.add_contacto(contacto_alias, contacto_nombre)
            return jsonify({"message": f"Contacto {contacto_nombre} agregado a {alias}"}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400



@app.route('/mensajeria/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    usuario_alias = data.get("usuario")
    contacto_alias = data.get("contacto")
    mensaje = data.get("mensaje")

    usuario = obtener_usuario_por_alias(usuario_alias)
    contacto = obtener_usuario_por_alias(contacto_alias)

    if usuario and contacto:
        usuario.enviar_mensaje(contacto, mensaje)
        return jsonify({"message": f"Mensaje enviado de {usuario_alias} a {contacto_alias}"}), 200
    else:
        return jsonify({"error": "Usuario o contacto no encontrado"}), 404


@app.route('/mensajeria/recibidos', methods=['GET'])
def obtener_mensajes_recibidos():
    alias = request.args.get('mialias')
    usuario = obtener_usuario_por_alias(alias)

    if usuario:
        mensajes = [
            {
                "destinatario": mensaje['para'],
                "remitente": mensaje['de'],
                "contenido": mensaje['contenido'],
                "fecha": mensaje['fecha'].strftime("%Y-%m-%d %H:%M:%S")
            }
            for mensaje in usuario.mensajes_recibidos
        ]
        return jsonify(mensajes)
    else:
        return jsonify({"error": f"Usuario con alias {alias} no encontrado"}), 404

