from core.configuracion import cargar_json, guardar_json
from core.seguridad import generar_hash
from modules.admin.consultas import buscar_usuario_por_id, listar_usuarios
from utils.validaciones import (
    validar_nombre,
    validar_dni,
    validar_usuario,
    validar_password,
)


def _pedir_nombre(campo):

    while True:
        nombre = input(f"Ingrese el nuevo {campo}: ").strip()

        if validar_nombre(nombre):
            return nombre

        print("\nIngrese solo letras y espacios.")


def _pedir_dni(usuarios, id_usuario):

    while True:
        dni = input("Ingrese el nuevo DNI: ").strip()

        if not validar_dni(dni):
            print("\nEl DNI debe tener exactamente 8 dígitos.")
            continue

        dni_en_uso = False

        for usuario in usuarios:
            if usuario["id"] != id_usuario and usuario["dni"] == dni:
                dni_en_uso = True
                break

        if dni_en_uso:
            print("\nEse DNI ya está registrado.")
            continue

        return dni


def _pedir_nombre_usuario(usuarios, id_usuario):

    while True:
        nombre_usuario = input("Ingrese el nuevo nombre de usuario: ").strip()

        if not validar_usuario(nombre_usuario):
            print("\nEl usuario debe tener al menos 4 caracteres.")
            continue

        usuario_en_uso = False

        for usuario in usuarios:
            if (
                usuario["id"] != id_usuario
                and usuario["usuario"].lower() == nombre_usuario.lower()
            ):
                usuario_en_uso = True
                break

        if usuario_en_uso:
            print("\nEse nombre de usuario ya está en uso.")
            continue

        return nombre_usuario


def _pedir_password():

    while True:
        password = input("Ingrese la nueva contraseña: ")

        if validar_password(password):
            return generar_hash(password)

        print("\nLa contraseña debe tener al menos 6 caracteres.")


def _pedir_rol():

    print("\nSeleccione el nuevo rol:")
    print("1. Médico")
    print("2. Secretaria")

    while True:
        opcion = input("Opción: ").strip()

        if opcion == "1":
            return "MEDICO"

        if opcion == "2":
            return "SECRETARIA"

        print("\nOpción inválida. Seleccione 1 o 2.")


def modificar_usuario(ruta_usuarios):

    usuarios = cargar_json(ruta_usuarios) or []

    if not usuarios:
        print("\nNo hay usuarios registrados.")
        return

    listar_usuarios(ruta_usuarios)

    try:
        id_usuario = int(input("\nIngrese el ID del usuario a modificar: "))
    except ValueError:
        print("\nEl ID debe ser un número.")
        return

    usuario = buscar_usuario_por_id(usuarios, id_usuario)

    if usuario is None:
        print("\nNo existe un usuario con ese ID.")
        return

    while True:
        print("\n¿Qué dato desea modificar?")
        print("1. Nombre")
        print("2. Apellido")
        print("3. DNI")
        print("4. Nombre de usuario")
        print("5. Contraseña")
        print("6. Rol")
        print("0. Volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            usuario["nombre"] = _pedir_nombre("nombre")

        elif opcion == "2":
            usuario["apellido"] = _pedir_nombre("apellido")

        elif opcion == "3":
            usuario["dni"] = _pedir_dni(usuarios, id_usuario)

        elif opcion == "4":
            usuario["usuario"] = _pedir_nombre_usuario(usuarios, id_usuario)

        elif opcion == "5":
            usuario["password"] = _pedir_password()

        elif opcion == "6":
            if usuario["rol"] == "ADMIN":
                print("\nNo se puede cambiar el rol de un administrador.")
                continue

            usuario["rol"] = _pedir_rol()

        elif opcion == "0":
            print("\nVolviendo al menú administrador.")
            return

        else:
            print("\nOpción inválida.")
            continue

        guardar_json(ruta_usuarios, usuarios)
        print("\nDato actualizado correctamente.")