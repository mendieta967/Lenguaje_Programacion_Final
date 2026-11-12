from core.configuracion import RUTA_USUARIOS
from modules.admin.creacion import crear_usuario
from modules.admin.consultas import listar_usuarios, buscar_usuario
from modules.admin.estado import desactivar_usuario, activar_usuario
from modules.admin.modificacion import modificar_usuario


def menu_admin():

    while True:

        print("\n" + "=" * 45)
        print("          MENÚ ADMINISTRADOR")
        print("=" * 45)

        print("\n1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Buscar usuario")
        print("4. Modificar usuarios")
        print("5. Desactivar usuarios")
        print("6. Reactivar usuarios")
        print("7. Cerrar sesión")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            crear_usuario(RUTA_USUARIOS)

        elif opcion == "2":
            listar_usuarios(RUTA_USUARIOS)

        elif opcion == "3":
            buscar_usuario(RUTA_USUARIOS)

        elif opcion == "4":
            modificar_usuario(RUTA_USUARIOS)

        elif opcion == "5":
            desactivar_usuario(RUTA_USUARIOS)

        elif opcion == "6":
            activar_usuario(RUTA_USUARIOS)

        elif opcion == "7":
            print("\nCerrando sesión...")
            break

        else:
            print("\nOpción inválida.")