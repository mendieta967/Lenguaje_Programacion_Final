from core.configuracion import RUTA_TURNOS, cargar_json, guardar_json
from modules.secretaria.turnos.consultas import mostrar_turnos


def cancelar_turno():
    turnos = cargar_json(RUTA_TURNOS) or []
    turnos_reservados = [
        turno for turno in turnos if turno["estado"] == "RESERVADO"
    ]

    if not turnos_reservados:
        print("\nNo hay turnos reservados para cancelar.")
        return

    print("\nSeleccione el turno que desea cancelar.")
    mostrar_turnos(turnos_reservados)

    while True:
        opcion = input("\nIngrese el ID del turno (0 para volver): ").strip()

        if opcion == "0":
            return

        try:
            id_turno = int(opcion)
        except ValueError:
            print("\nEl ID debe ser un número.")
            continue

        turno_seleccionado = None
        for turno in turnos_reservados:
            if turno["id"] == id_turno:
                turno_seleccionado = turno
                break

        if turno_seleccionado is None:
            print("\nNo existe un turno reservado con ese ID.")
            continue

        confirmar = input("¿Confirma la cancelación? (S/N): ").strip().casefold()

        if confirmar == "s":
            turno_seleccionado["estado"] = "CANCELADO"
            guardar_json(RUTA_TURNOS, turnos)
            print("\nTurno cancelado correctamente.")
            return

        if confirmar == "n":
            print("\nCancelación anulada.")
            return

        print("\nIngrese S o N.")
