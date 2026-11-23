from modules.secretaria.turnos.creacion import registrar_turno
from modules.secretaria.turnos.consultas import consultar_turnos
from modules.secretaria.turnos.reprogramacion import reprogramar_turno
from modules.secretaria.turnos.estado import cancelar_turno, marcar_ausente


def menu_turnos():

    while True:
        print("\n===== GESTIÓN DE TURNOS =====")
        print("1. Registrar turno")
        print("2. Consultar turnos")
        print("3. Cancelar turno")
        print("4. Reprogramar turno")
        print("5. Marcar no asistió")
        print("0. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            registrar_turno()

        elif opcion == "2":
            consultar_turnos()

        elif opcion == "3":
            cancelar_turno()

        elif opcion == "4":
            reprogramar_turno()

        elif opcion == "5":
            marcar_ausente()

        elif opcion == "0":
            return

        else:
            print("\nOpción inválida.")