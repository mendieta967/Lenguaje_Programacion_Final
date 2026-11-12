import json
from core.seguridad import generar_hash

def crear_primer_admin(ruta_usuarios):

    print("\n===== CREAR ADMINISTRADOR =====")

    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    dni = input("DNI: ")
    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    password = generar_hash(password)

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

def obtener_siguiente_id(usuarios):
    if not usuarios:
        return 1

    return max(usuario["id"] for usuario in usuarios) + 1