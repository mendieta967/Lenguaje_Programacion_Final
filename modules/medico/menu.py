from modules.medico.consultas import (
    agregar_correccion,
    consultar_historia_por_dni,
    listar_mis_turnos,
    registrar_atencion,
)


def menu_medico(usuario):
    while True:
        print("\n=========== MENÚ MÉDICO ===========")
        print("1. Ver mis turnos")
        print("2. Registrar atención")
        print("3. Consultar historia clínica por DNI")
        print("4. Agregar corrección a una atención")
        print("5. Cerrar sesión")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            listar_mis_turnos(usuario["id"])

        elif opcion == "2":
            registrar_atencion(usuario["id"])

        elif opcion == "3":
            consultar_historia_por_dni()

        elif opcion == "4":
            agregar_correccion(usuario["id"])

        elif opcion == "5":
            print("\nCerrando sesión...")
            return

        else:
            print("\nOpción inválida.")
