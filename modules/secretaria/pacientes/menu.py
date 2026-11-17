from core.configuracion import RUTA_PACIENTES
from modules.secretaria.pacientes.crear import registrar_paciente
from modules.secretaria.pacientes.consultas import listar_pacientes, buscar_paciente
from modules.secretaria.pacientes.modificacion import modificar_paciente
from modules.secretaria.pacientes.estado import gestionar_estado_paciente


def menu_gestion_pacientes():

    while True:

        print("\n" + "=" * 45)
        print("       GESTIÓN DE PACIENTES")
        print("=" * 45)

        print("\n1. Registrar paciente")
        print("2. Listar pacientes")
        print("3. Buscar paciente")
        print("4. Modificar paciente")
        print("5. Gestionar estado")
        print("0. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

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

        elif opcion == "0":
            return

        else:
            print("\nOpción inválida.")
