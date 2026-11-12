from core.configuracion import cargar_json, guardar_json
from modules.secretaria.consultas import (
    buscar_paciente_por_id,
    listar_pacientes,
    mostrar_paciente,
)


def _confirmar_cambio_estado(accion, paciente):

    confirmacion = input(
        f"\n¿Confirma que desea {accion} al paciente "
        f"{paciente['nombre']} {paciente['apellido']}? (s/n): "
    ).strip().lower()

    if confirmacion not in ("s", "si"):
        print("\nOperación cancelada.")
        return False

    return True


def _cambiar_estado_paciente(ruta_pacientes, estado_nuevo, accion_texto):

    pacientes = cargar_json(ruta_pacientes) or []

    if not pacientes:
        print("\nNo hay pacientes registrados.")
        return

    listar_pacientes(ruta_pacientes)

    try:
        id_paciente = int(input("\nIngrese el ID del paciente: "))
    except ValueError:
        print("\nEl ID debe ser un número.")
        return

    paciente = buscar_paciente_por_id(pacientes, id_paciente)

    if paciente is None:
        print("\nNo existe un paciente con ese ID.")
        return

    if paciente["activo"] == estado_nuevo:
        if estado_nuevo:
            print("\nEl paciente ya está activo.")
        else:
            print("\nEl paciente ya está inactivo.")
        return

    if not _confirmar_cambio_estado(accion_texto, paciente):
        return

    paciente["activo"] = estado_nuevo
    guardar_json(ruta_pacientes, pacientes)
    mostrar_paciente(paciente)

    if estado_nuevo:
        print("\nPaciente reactivado correctamente.")
    else:
        print("\nPaciente desactivado correctamente.")


def gestionar_estado_paciente(ruta_pacientes):

    print("\n===== GESTIÓN DE ESTADO =====")
    print("1. Desactivar paciente")
    print("2. Reactivar paciente")
    print("0. Volver")

    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        _cambiar_estado_paciente(ruta_pacientes, False, "desactivar")

    elif opcion == "2":
        _cambiar_estado_paciente(ruta_pacientes, True, "reactivar")

    elif opcion == "0":
        return

    else:
        print("\nOpción inválida.")