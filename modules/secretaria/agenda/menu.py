from modules.secretaria.agenda.creacion import crear_agenda
from modules.secretaria.agenda.consultas import consultar_agenda
from modules.secretaria.agenda.modificacion import modificar_agenda


def menu_agenda_medica():

    while True:

        print("\n" + "=" * 45)
        print("      GESTIÓN DE AGENDA MÉDICA")
        print("=" * 45)

        print("\n1. Registrar o completar agenda")
        print("2. Consultar agenda")
        print("3. Modificar agenda")
        print("4. Eliminar agenda")
        print("0. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            crear_agenda()

        elif opcion == "2":
            consultar_agenda()

        elif opcion == "3":
            modificar_agenda()

        elif opcion == "4":
            print("\nDesarrollando eliminación de agenda...")

        elif opcion == "0":
            break

        else:
            print("\nOpción inválida.")
