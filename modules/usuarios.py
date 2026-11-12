import json


def crear_primer_admin(ruta_usuarios):

    print("\n===== CREAR ADMINISTRADOR =====")

    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    dni = input("DNI: ")
    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    administrador = {
        "id": 1,
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "usuario": usuario,
        "password": password,
        "rol": "ADMIN",
        "activo": True
    }

    with open(ruta_usuarios, "w", encoding="utf-8") as archivo:
        json.dump([administrador], archivo, indent=4, ensure_ascii=False)

    print("\nAdministrador creado correctamente.")