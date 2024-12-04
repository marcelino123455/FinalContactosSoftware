# FinalContactosSoftware

## Integrantes: Marcelino Maita, Luis Robledo

### Pregunta 3

Se debe modificar la clase Usuario para incluir validaciones de un máximo de contactos, y agregar métodos para eliminar tanto contactos como usuarios. La validación del máximo de contactos debe implementarse en add_contacto() y si se excede el límite, debe arrojar un error. Para la eliminación, se deben agregar métodos eliminar_contacto() y eliminar_usuario(). A su vez, la base de datos debe ser actualizada para reflejar la eliminación de usuarios, sin perder los mensajes previos. Loos nuevos casos de prueba deben verificar que no se pueda agregaar más contactos de lo permitido, que los contactos se eliminen correctamente sin perder los mensajes, y que la eliminación de usuarios no afecte la integridad de los mensajes. El riesgo de "romper" lo que ya funciona es moderado, especialmente por la complejidad de mantener la integridad de los mensajes al eliminar usuarios o contactos, lo que podría generar inconsistenciias si no se gestionan adecuadamente las referencias y la persistencia de los datos.
