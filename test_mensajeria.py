import unittest
from main import app, BD, Usuario

class TestMensajeria(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.config['TESTING'] = True

        BD.clear()
        BD.extend([
            Usuario("cpaz", "Christian", [("lmunoz", "Luisa"), ("mgrau", "Miguel")]),
            Usuario("lmunoz", "Luisa", [("mgrau", "Miguel")]),
            Usuario("mgrau", "Miguel", [("cpaz", "Christian")])
        ])

    # Casos de éxito
    def test_obtener_contactos(self):
        response = self.client.get('/mensajeria/contactos/cpaz')
        self.assertEqual(response.status_code, 200)
        self.assertIn('lmunoz', response.json)  # Verifica que el contacto "lmunoz" esté en los contactos

    def test_agregar_contacto(self):
        data = {"contacto": "jdoe", "nombre": "John Doe"}
        response = self.client.post('/mensajeria/contactos/cpaz', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Contacto John Doe agregado a cpaz", response.json["message"])

    def test_enviar_mensaje(self):
        data = {"usuario": "cpaz", "contacto": "lmunoz", "mensaje": "Hola Luisa!"}
        response = self.client.post('/mensajeria/enviar', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mensaje enviado de cpaz a lmunoz", response.json["message"])

    def test_obtener_mensajes_recibidos(self):
        usuario_lmunoz = next((u for u in BD if u.alias == "lmunoz"), None)
        if usuario_lmunoz:
            usuario_lmunoz.mensajes_recibidos.clear()

        data = {"usuario": "cpaz", "contacto": "lmunoz", "mensaje": "Hola Luisa!"}
        self.client.post('/mensajeria/enviar', json=data)

        response = self.client.get('/mensajeria/recibidos?mialias=lmunoz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["contenido"], "Hola Luisa!")

    def test_obtener_contactos_usuario_no_encontrado(self):
        response = self.client.get('/mensajeria/contactos/nonexistentuser')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Usuario no encontrado", response.json["error"])

    def test_enviar_mensaje_usuario_no_encontrado(self):
        data = {"usuario": "cpaz", "contacto": "nonexistentuser", "mensaje": "Hola!"}
        response = self.client.post('/mensajeria/enviar', json=data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Usuario o contacto no encontrado", response.json["error"])

    def test_obtener_mensajes_recibidos_usuario_no_encontrado(self):
        response = self.client.get('/mensajeria/recibidos?mialias=nonexistentuser')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Usuario con alias nonexistentuser no encontrado", response.json["error"])

    def test_agregar_contacto_existente(self):
        data = {"contacto": "lmunoz", "nombre": "Luisa"}
        response = self.client.post('/mensajeria/contactos/cpaz', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("El contacto con alias lmunoz ya existe", response.json["error"])


