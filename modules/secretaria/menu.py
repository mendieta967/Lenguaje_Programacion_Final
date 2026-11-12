from core.configuracion import RUTA_PACIENTES
from modules.secretaria.crear_pacientes import registrar_paciente
from modules.secretaria.consultas import listar_pacientes, buscar_paciente
from modules.secretaria.modificacion import modificar_paciente
from modules.secretaria.estado import gestionar_estado_paciente


def menu_secretaria():

    while True:

        print("\n" + "=" * 45)
        print("           MENÚ SECRETARIA")
        print("=" * 45)

        print("\n1. Registrar paciente")
        print("2. Listar pacientes")
        print("3. Buscar paciente")
        print("4. Modificar paciente")
        print("5. Gestionar estado")
        print("6. Gestionar turnos")
        print("7. Cerrar sesión")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            registrar_paciente(RUTA_PACIENTES)

        elif opcion == "2":
            listar_pacientes(RUTA_PACIENTES)

        elif opcion == "3":
            buscar_paciente(RUTA_PACIENTES)

        elif opcion == "4":
            modificar_paciente(RUTA_PACIENTES)

        elif opcion == "5":
            gestionar_estado_paciente(RUTA_PACIENTES)

        elif opcion == "6":
            print("\nDesarrollando la opción de gestionar turnos...")

        elif opcion == "7":
            print("\nCerrando sesión...")
            break

        else:
            print("\nOpción inválida.")