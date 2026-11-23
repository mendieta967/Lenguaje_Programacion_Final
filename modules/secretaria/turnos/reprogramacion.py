from datetime import datetime

from core.configuracion import RUTA_TURNOS, cargar_json, guardar_json
from modules.secretaria.turnos.consultas import mostrar_turnos
from modules.secretaria.turnos.creacion import (
    DIA_NOMBRE,
    buscar_agenda,
    generar_horarios,
    hora_a_minutos,
    obtener_fechas_disponibles,
    pedir_fecha,
    pedir_hora,
    pedir_medico,
)


DURACION_TURNO_MINUTOS = 30


def turno_es_futuro(turno, ahora=None):
    if ahora is None:
        ahora = datetime.now()

    fecha_hora = datetime.strptime(
        f"{turno['fecha']} {turno['hora']}",
        "%d/%m/%Y %H:%M",
    )
    return fecha_hora > ahora


def obtener_turnos_reprogramables(turnos, ahora=None):
    return [
        turno
        for turno in turnos
        if turno["estado"] == "RESERVADO" and turno_es_futuro(turno, ahora)
    ]


def horario_se_solapa(hora, hora_existente):
    inicio = hora_a_minutos(hora)
    inicio_existente = hora_a_minutos(hora_existente)
    fin = inicio + DURACION_TURNO_MINUTOS
    fin_existente = inicio_existente + DURACION_TURNO_MINUTOS
    return inicio < fin_existente and inicio_existente < fin


def filtrar_horarios_paciente(
    turnos,
    id_paciente,
    id_turno_actual,
    fecha,
    horarios,
):
    horarios_ocupados = [
        turno["hora"]
        for turno in turnos
        if turno["id"] != id_turno_actual
        and turno["id_paciente"] == id_paciente
        and turno["fecha"] == fecha
        and turno["estado"] != "CANCELADO"
    ]

    return [
        hora
        for hora in horarios
        if not any(
            horario_se_solapa(hora, hora_ocupada)
            for hora_ocupada in horarios_ocupados
        )
    ]


def filtrar_fechas_paciente(fechas, turnos, turno):
    fechas_filtradas = []

    for fecha_texto, fecha, horarios in fechas:
        horarios_filtrados = filtrar_horarios_paciente(
            turnos,
            turno["id_paciente"],
            turno["id"],
            fecha_texto,
            horarios,
        )
        if horarios_filtrados:
            fechas_filtradas.append((fecha_texto, fecha, horarios_filtrados))

    return fechas_filtradas


def aplicar_reprogramacion(turno, id_medico, fecha, hora, fecha_cambio):
    historial = turno.get("historial_reprogramaciones", [])
    if not isinstance(historial, list):
        raise ValueError("El historial de reprogramaciones no es válido.")

    historial.append({
        "fecha_cambio": fecha_cambio,
        "id_medico_anterior": turno["id_medico"],
        "fecha_anterior": turno["fecha"],
        "hora_anterior": turno["hora"],
        "id_medico_nuevo": id_medico,
        "fecha_nueva": fecha,
        "hora_nueva": hora,
    })
    turno["historial_reprogramaciones"] = historial
    turno["id_medico"] = id_medico
    turno["fecha"] = fecha
    turno["hora"] = hora


def _pedir_turno(turnos_reprogramables):
    print("\nSeleccione el turno que desea reprogramar.")
    mostrar_turnos(turnos_reprogramables)

    while True:
        opcion = input("\nIngrese el ID del turno (0 para volver): ").strip()
        if opcion == "0":
            return None

        try:
            id_turno = int(opcion)
        except ValueError:
            print("\nEl ID debe ser un número.")
            continue

        for turno in turnos_reprogramables:
            if turno["id"] == id_turno:
                return turno

        print("\nNo existe un turno futuro reservado con ese ID.")


def _confirmar_reprogramacion(medico, fecha, hora):
    print("\n===== NUEVO TURNO =====")
    print(f"Médico: {medico['nombre']} {medico['apellido']}")
    print(f"Fecha: {fecha}")
    print(f"Hora: {hora}")

    while True:
        confirmar = input("\n¿Confirma la reprogramación? (S/N): ").strip().casefold()
        if confirmar == "s":
            return True
        if confirmar == "n":
            return False
        print("\nIngrese S o N.")


def _verificar_disponibilidad(turno, id_medico, fecha, fecha_obj, hora, turnos):
    agenda = buscar_agenda(id_medico)
    if agenda is None:
        return "El médico seleccionado ya no tiene agenda registrada."

    dia = DIA_NOMBRE.get(fecha_obj.weekday())
    if dia is None or hora not in generar_horarios(agenda, dia, fecha, id_medico):
        return "Ese horario ya no está disponible para el médico."

    horarios_paciente = filtrar_horarios_paciente(
        turnos,
        turno["id_paciente"],
        turno["id"],
        fecha,
        [hora],
    )
    if not horarios_paciente:
        return "El paciente ya tiene otro turno en un horario que se superpone."

    return None


def reprogramar_turno():
    turnos = cargar_json(RUTA_TURNOS) or []
    turnos_reprogramables = obtener_turnos_reprogramables(turnos)

    if not turnos_reprogramables:
        print("\nNo hay turnos futuros reservados para reprogramar.")
        return

    turno = _pedir_turno(turnos_reprogramables)
    if turno is None:
        return

    medico = pedir_medico()
    if medico is None:
        return

    agenda = buscar_agenda(medico["id"])
    if agenda is None:
        print("\nEl médico no tiene agenda registrada.")
        return

    fechas_disponibles = obtener_fechas_disponibles(agenda, medico["id"])
    fechas_disponibles = filtrar_fechas_paciente(
        fechas_disponibles,
        turnos,
        turno,
    )
    if not fechas_disponibles:
        print(
            "\nNo hay horarios disponibles que no se superpongan "
            "con otros turnos del paciente."
        )
        return

    fecha_seleccionada = pedir_fecha(fechas_disponibles)
    if fecha_seleccionada is None:
        return

    fecha, fecha_obj, horarios = fecha_seleccionada
    hora = pedir_hora(horarios)
    if hora is None:
        return

    if not _confirmar_reprogramacion(medico, fecha, hora):
        print("\nReprogramación cancelada; el turno original no cambió.")
        return

    turnos_actualizados = cargar_json(RUTA_TURNOS) or []
    turno_actualizado = next(
        (item for item in turnos_actualizados if item["id"] == turno["id"]),
        None,
    )
    if (
        turno_actualizado is None
        or turno_actualizado["estado"] != "RESERVADO"
        or not turno_es_futuro(turno_actualizado)
    ):
        print("\nEl turno ya no se puede reprogramar; no se realizaron cambios.")
        return

    disponibilidad_error = _verificar_disponibilidad(
        turno_actualizado,
        medico["id"],
        fecha,
        fecha_obj,
        hora,
        turnos_actualizados,
    )
    if disponibilidad_error is not None:
        print(f"\n{disponibilidad_error} No se realizaron cambios.")
        return

    aplicar_reprogramacion(
        turno_actualizado,
        medico["id"],
        fecha,
        hora,
        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    )
    guardar_json(RUTA_TURNOS, turnos_actualizados)
    print("\nTurno reprogramado correctamente.")
