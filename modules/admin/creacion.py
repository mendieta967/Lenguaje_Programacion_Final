from core.seguridad import generar_hash
from core.configuracion import cargar_json, guardar_json
from utils.validaciones import (
    validar_nombre,
    validar_dni,
    validar_usuario,
    validar_password,
)


def _usuario_existe(usuarios, dni=None, nombre_usuario=None):

    for usuario in usuarios:
        if dni is not None and usuario.get("dni") == dni:
            return True

        if (
            nombre_usuario is not None
            and usuario.get("usuario", "").lower() == nombre_usuario.lower()
        ):
            return True

    return False


def _pedir_nombre(etiqueta):

    while True:
        nombre = input(f"{etiqueta}: ").strip()

        if validar_nombre(nombre):
            return nombre

        print("\nIngrese solo letras y espacios.")


def _pedir_dni(usuarios):

    while True:
        dni = input("DNI: ").strip()

        if not validar_dni(dni):
            print("\nDNI inválido. Debe tener exactamente 8 dígitos.")
            continue

        if _usuario_existe(usuarios, dni=dni):
            print("\nYa existe un usuario registrado con ese DNI.")
            continue

        return dni


def _pedir_nombre_usuario(usuarios):

    while True:
        nombre_usuario = input("Usuario: ").strip()

        if not validar_usuario(nombre_usuario):
            print("\nUsuario inválido. Debe tener al menos 4 caracteres.")
            continue

        if _usuario_existe(usuarios, nombre_usuario=nombre_usuario):
            print("\nEse nombre de usuario ya está en uso.")
            continue

        return nombre_usuario


def _pedir_password():

    while True:
        password = input("Contraseña: ")

        if validar_password(password):
            return generar_hash(password)

        print("\nContraseña inválida. Debe tener al menos 6 caracteres.")


def _pedir_datos_usuario(usuarios):

    nombre = _pedir_nombre("Nombre")
    apellido = _pedir_nombre("Apellido")
    dni = _pedir_dni(usuarios)
    nombre_usuario = _pedir_nombre_usuario(usuarios)
    password = _pedir_password()

    return {
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "usuario": nombre_usuario,
        "password": password,
    }


def obtener_siguiente_id(usuarios):

    if not usuarios:
        return 1

    return max(usuario["id"] for usuario in usuarios) + 1


def crear_primer_admin(ruta_usuarios):

    usuarios = cargar_json(ruta_usuarios) or []

    print("\n===== CREAR ADMINISTRADOR =====")

    datos = _pedir_datos_usuario(usuarios)

    administrador = {
        "id": 1,
        "nombre": datos["nombre"],
        "apellido": datos["apellido"],
        "dni": datos["dni"],
        "usuario": datos["usuario"],
        "password": datos["password"],
        "rol": "ADMIN",
        "activo": True,
    }

    guardar_json(ruta_usuarios, [administrador])

    print("\nAdministrador creado correctamente.")


def crear_usuario(ruta_usuarios):

    usuarios = cargar_json(ruta_usuarios) or []

    print("\n===== CREAR USUARIO =====")

    datos = _pedir_datos_usuario(usuarios)

    print("\nSeleccione un rol")
    print("1. Médico")
    print("2. Secretaria")

    while True:
        opcion = input("Opción: ").strip()

        if opcion == "1":
            rol = "MEDICO"
            break

        if opcion == "2":
            rol = "SECRETARIA"
            break

        print("\nRol inválido. Seleccione 1 para Médico o 2 para Secretaria.")

    nuevo_usuario = {
        "id": obtener_siguiente_id(usuarios),
        "nombre": datos["nombre"],
        "apellido": datos["apellido"],
        "dni": datos["dni"],
        "usuario": datos["usuario"],
        "password": datos["password"],
        "rol": rol,
        "activo": True,
    }

    usuarios.append(nuevo_usuario)
    guardar_json(ruta_usuarios, usuarios)

    print("\nUsuario creado correctamente.")