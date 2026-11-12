import os

from core.sistema import inicializar_sistema
from core.configuracion import RUTA_USUARIOS
from modules.autenticacion import iniciar_sesion
from modules.admin.menu import menu_admin
from modules.secretaria.menu import menu_secretaria


def main():

    inicializar_sistema()

    while True:

        print("\n" + "=" * 45)
        print("       SISTEMA DE GESTIÓN HOSPITALARIA")
        print("=" * 45)

        print("\n1. Iniciar sesión")
        print("0. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":

            usuario = iniciar_sesion(RUTA_USUARIOS)

            if usuario:

                if usuario["rol"] == "ADMIN":
                    menu_admin()

                elif usuario["rol"] == "SECRETARIA":
                    menu_secretaria()

                elif usuario["rol"] == "MEDICO":
                    print("\nMenú médico en desarrollo...")

        elif opcion == "0":
            print("\nGracias por utilizar el sistema.")
            break

        else:
            print("\nOpción inválida.")


if __name__ == "__main__":
    main()