import json
from core.seguridad import verificar_password

def iniciar_sesion(ruta_usuarios):

    print("\n===== INICIO DE SESIÓN =====")

    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    with open(ruta_usuarios, "r", encoding="utf-8") as archivo:
        usuarios = json.load(archivo)

    usuario_encontrado = None

    for usuario_guardado in usuarios:

        if usuario_guardado["usuario"].lower() == usuario.lower():
            usuario_encontrado = usuario_guardado
            break

    if not usuario_encontrado:
        print("\nUsuario incorrecto.")
        return None

    if not usuario_encontrado.get("activo", False):
        print("\nLa cuenta está inactiva.")
        return None

    if not verificar_password(password, usuario_encontrado["password"]):
        print("\nContraseña incorrecta.")
        return None

    print(f"\nBienvenido {usuario_encontrado['nombre']} {usuario_encontrado['apellido']}")

    return usuario_encontrado