from modules.secretaria.agenda.menu import menu_agenda_medica
from modules.secretaria.pacientes.menu import menu_gestion_pacientes
from modules.secretaria.turnos.menu import menu_turnos


def menu_secretaria():

    while True:

        print("\n=========== MENÚ SECRETARIA ===========")
        print("\n1. Gestión de pacientes")
        print("2. Gestión de agenda médica")
        print("3. Gestión de turnos")
        print("4. Cerrar sesión")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            menu_gestion_pacientes()

        elif opcion == "2":
            menu_agenda_medica()

        elif opcion == "3":
            menu_turnos()

        elif opcion == "4":
            print("\nCerrando sesión...")
            break

        else:
            print("\nOpción inválida.")
