from datetime import datetime

from core.configuracion import (
    RUTA_HISTORIAS_CLINICAS,
    RUTA_PACIENTES,
    RUTA_TURNOS,
    RUTA_USUARIOS,
    cargar_json,
    guardar_json,
)
from modules.secretaria.pacientes.consultas import buscar_paciente_por_dni
from modules.secretaria.turnos.consultas import mostrar_turnos
from utils.validaciones import validar_dni


def turno_puede_atenderse(turno, id_medico, ahora=None):
    if ahora is None:
        ahora = datetime.now()

    fecha_hora_turno = datetime.strptime(
        f"{turno['fecha']} {turno['hora']}",
        "%d/%m/%Y %H:%M",
    )
    return (
        turno["id_medico"] == id_medico
        and turno["estado"] == "RESERVADO"
        and fecha_hora_turno <= ahora
    )


def obtener_turnos_atendibles(turnos, id_medico, ahora=None):
    return [
        turno
        for turno in turnos
        if turno_puede_atenderse(turno, id_medico, ahora)
    ]


def obtener_turnos_medico(turnos, id_medico):
    turnos_medico = [
        turno
        for turno in turnos
        if turno["id_medico"] == id_medico
        and turno["estado"] != "CANCELADO"
    ]
    return sorted(
        turnos_medico,
        key=lambda turno: datetime.strptime(
            f"{turno['fecha']} {turno['hora']}",
            "%d/%m/%Y %H:%M",
        ),
    )


def _ordenar_atenciones(atenciones):
    return sorted(
        atenciones,
        key=lambda atencion: datetime.strptime(
            atencion["fecha_atencion"],
            "%d/%m/%Y %H:%M:%S",
        ),
    )


def obtener_atenciones_medico(atenciones, id_medico, id_paciente=None):
    atenciones = [
        atencion
        for atencion in atenciones
        if atencion["id_medico"] == id_medico
        and (
            id_paciente is None
            or atencion["id_paciente"] == id_paciente
        )
    ]
    return _ordenar_atenciones(atenciones)


def obtener_historia_clinica(atenciones, id_paciente):
    atenciones = [
        atencion
        for atencion in atenciones
        if atencion["id_paciente"] == id_paciente
    ]
    return _ordenar_atenciones(atenciones)


def obtener_siguiente_id_atencion(atenciones):
    return max(
        (atencion["id"] for atencion in atenciones),
        default=0,
    ) + 1


def crear_atencion(
    id_atencion,
    turno,
    id_medico,
    observaciones,
    diagnostico,
    indicaciones,
    momento_atencion,
):
    if not observaciones.strip():
        raise ValueError("Las observaciones no pueden estar vacías.")
    if not turno_puede_atenderse(turno, id_medico, momento_atencion):
        raise ValueError("El turno no está disponible para registrar la atención.")

    return {
        "id": id_atencion,
        "id_turno": turno["id"],
        "id_paciente": turno["id_paciente"],
        "id_medico": id_medico,
        "fecha_atencion": momento_atencion.strftime("%d/%m/%Y %H:%M:%S"),
        "motivo_consulta": turno.get("motivo_consulta", "No especificado"),
        "observaciones": observaciones.strip(),
        "diagnostico": diagnostico.strip() or None,
        "indicaciones": indicaciones.strip() or None,
        "adendas": [],
    }


def vincular_atencion_a_turno(turno, atencion, id_medico, ahora=None):
    if not turno_puede_atenderse(turno, id_medico, ahora):
        raise ValueError("El turno no está disponible para registrar la atención.")
    if (
        atencion["id_medico"] != id_medico
        or atencion["id_paciente"] != turno["id_paciente"]
        or atencion["id_turno"] != turno["id"]
    ):
        raise ValueError("La atención no corresponde a este turno.")

    turno["id_atencion"] = atencion["id"]
    turno["estado"] = "ATENDIDO"


def agregar_adenda_a_atencion(atencion, id_medico, texto, fecha_adenda):
    if atencion["id_medico"] != id_medico:
        raise ValueError("No se puede corregir esta atención.")
    if not texto.strip():
        raise ValueError("La corrección no puede estar vacía.")

    atencion.setdefault("adendas", []).append({
        "fecha": fecha_adenda.strftime("%d/%m/%Y %H:%M:%S"),
        "id_medico": id_medico,
        "texto": texto.strip(),
    })


def _pedir_turno(turnos, accion):
    print(f"\nSeleccione el turno para {accion}.")
    mostrar_turnos(turnos)

    while True:
        opcion = input("\nIngrese el ID del turno (0 para volver): ").strip()
        if opcion == "0":
            return None

        try:
            id_turno = int(opcion)
        except ValueError:
            print("\nEl ID debe ser un número.")
            continue

        for turno in turnos:
            if turno["id"] == id_turno:
                return turno

        print("\nNo existe un turno disponible con ese ID.")


def _pedir_atencion(atenciones, accion):
    print(f"\nSeleccione la atención para {accion}.")
    for atencion in atenciones:
        print(
            f"Atención {atencion['id']} - "
            f"{atencion['fecha_atencion']} - "
            f"{atencion['observaciones']}"
        )

    while True:
        opcion = input("\nIngrese el ID de la atención (0 para volver): ").strip()
        if opcion == "0":
            return None

        try:
            id_atencion = int(opcion)
        except ValueError:
            print("\nEl ID debe ser un número.")
            continue

        for atencion in atenciones:
            if atencion["id"] == id_atencion:
                return atencion

        print("\nNo existe una atención disponible con ese ID.")


def _pedir_observaciones():
    while True:
        observaciones = input("\nObservaciones de la atención: ").strip()
        if observaciones:
            return observaciones
        print("\nLas observaciones no pueden estar vacías.")


def _pedir_dato_opcional(etiqueta):
    return input(f"{etiqueta} (opcional, Enter para omitir): ").strip()


def _confirmar(mensaje):
    while True:
        respuesta = input(f"\n{mensaje} (S/N): ").strip().casefold()
        if respuesta == "s":
            return True
        if respuesta == "n":
            return False
        print("\nIngrese S o N.")


def listar_mis_turnos(id_medico):
    turnos = cargar_json(RUTA_TURNOS) or []
    turnos_medico = obtener_turnos_medico(turnos, id_medico)

    if not turnos_medico:
        print("\nNo tiene turnos registrados.")
        return

    mostrar_turnos(turnos_medico)


def registrar_atencion(id_medico):
    turnos = cargar_json(RUTA_TURNOS) or []
    atenciones = cargar_json(RUTA_HISTORIAS_CLINICAS) or []
    turnos_atendibles = obtener_turnos_atendibles(turnos, id_medico)
    if not turnos_atendibles:
        print("\nNo tiene turnos reservados que ya puedan ser atendidos.")
        return

    turno = _pedir_turno(turnos_atendibles, "registrar la atención")
    if turno is None:
        return

    atencion_existente = next(
        (
            atencion
            for atencion in atenciones
            if atencion.get("id_turno") == turno["id"]
        ),
        None,
    )
    if atencion_existente is not None:
        try:
            vincular_atencion_a_turno(
                turno,
                atencion_existente,
                id_medico,
            )
        except ValueError as error:
            print(f"\n{error}")
            return
        guardar_json(RUTA_TURNOS, turnos)
        print("\nLa atención ya existía; el turno quedó marcado como ATENDIDO.")
        return

    observaciones = _pedir_observaciones()
    diagnostico = _pedir_dato_opcional("Diagnóstico")
    indicaciones = _pedir_dato_opcional("Indicaciones")

    print("\n===== RESUMEN DE LA ATENCIÓN =====")
    print(f"Observaciones: {observaciones}")
    print(f"Diagnóstico: {diagnostico or 'No registrado'}")
    print(f"Indicaciones: {indicaciones or 'No registradas'}")
    if not _confirmar("¿Confirma guardar la atención?"):
        print("\nAtención cancelada; el turno sigue reservado.")
        return

    turnos_actualizados = cargar_json(RUTA_TURNOS) or []
    atenciones_actualizadas = cargar_json(RUTA_HISTORIAS_CLINICAS) or []
    turno_actualizado = next(
        (item for item in turnos_actualizados if item["id"] == turno["id"]),
        None,
    )
    momento_atencion = datetime.now()
    if turno_actualizado is None:
        print("\nEl turno ya no está disponible.")
        return

    atencion_existente = next(
        (
            atencion
            for atencion in atenciones_actualizadas
            if atencion.get("id_turno") == turno["id"]
        ),
        None,
    )
    if atencion_existente is not None:
        try:
            vincular_atencion_a_turno(
                turno_actualizado,
                atencion_existente,
                id_medico,
                momento_atencion,
            )
        except ValueError as error:
            print(f"\n{error}")
            return
        guardar_json(RUTA_TURNOS, turnos_actualizados)
        print("\nLa atención ya existía; el turno quedó marcado como ATENDIDO.")
        return

    try:
        atencion = crear_atencion(
            obtener_siguiente_id_atencion(atenciones_actualizadas),
            turno_actualizado,
            id_medico,
            observaciones,
            diagnostico,
            indicaciones,
            momento_atencion,
        )
    except ValueError as error:
        print(f"\n{error}")
        return

    atenciones_actualizadas.append(atencion)
    guardar_json(RUTA_HISTORIAS_CLINICAS, atenciones_actualizadas)
    turno_actualizado["id_atencion"] = atencion["id"]
    turno_actualizado["estado"] = "ATENDIDO"
    guardar_json(RUTA_TURNOS, turnos_actualizados)
    print("\nAtención registrada y turno marcado como ATENDIDO.")


def _pedir_paciente_por_dni():
    while True:
        dni = input("\nIngrese el DNI del paciente (0 para volver): ").strip()
        if dni == "0":
            return None
        if validar_dni(dni):
            pacientes = cargar_json(RUTA_PACIENTES) or []
            paciente = buscar_paciente_por_dni(pacientes, dni)
            if paciente is not None:
                return paciente
            print("\nNo se encontró un paciente con ese DNI.")
            return None
        print("\nDNI inválido. Debe tener exactamente 8 dígitos.")


def _mostrar_atencion(atencion, medicos_por_id):
    id_medico = atencion["id_medico"]
    medico = medicos_por_id.get(id_medico)
    nombre_medico = "No encontrado"
    if medico is not None:
        nombre_medico = f"{medico['nombre']} {medico['apellido']}"

    print("\n" + "-" * 45)
    if atencion.get("id_turno") is not None:
        print(f"Turno: {atencion['id_turno']}")
    else:
        print("Atención sin turno asociado")
    print(f"ID de atención: {atencion['id']}")
    print(f"Fecha de atención: {atencion['fecha_atencion']}")
    print(f"Médico: {nombre_medico}")
    print(f"Motivo de consulta: {atencion['motivo_consulta']}")
    print(f"Observaciones: {atencion['observaciones']}")
    print(f"Diagnóstico: {atencion['diagnostico'] or 'No registrado'}")
    print(f"Indicaciones: {atencion['indicaciones'] or 'No registradas'}")
    for adenda in atencion.get("adendas", []):
        print(f"Corrección ({adenda['fecha']}): {adenda['texto']}")


def consultar_historia_por_dni():
    paciente = _pedir_paciente_por_dni()
    if paciente is None:
        return

    atenciones_guardadas = cargar_json(RUTA_HISTORIAS_CLINICAS) or []
    atenciones = obtener_historia_clinica(
        atenciones_guardadas,
        paciente["id"],
    )
    if not atenciones:
        print("\nNo hay atenciones registradas para ese paciente.")
        return

    usuarios = cargar_json(RUTA_USUARIOS) or []
    medicos_por_id = {
        usuario["id"]: usuario
        for usuario in usuarios
        if usuario["rol"] == "MEDICO"
    }

    print(
        f"\nHistoria clínica de {paciente['nombre']} {paciente['apellido']} "
        f"(DNI: {paciente['dni']})"
    )
    for turno in atenciones:
        _mostrar_atencion(turno, medicos_por_id)


def agregar_correccion(id_medico):
    paciente = _pedir_paciente_por_dni()
    if paciente is None:
        return

    atenciones_guardadas = cargar_json(RUTA_HISTORIAS_CLINICAS) or []
    atenciones = obtener_atenciones_medico(
        atenciones_guardadas,
        id_medico,
        paciente["id"],
    )
    if not atenciones:
        print("\nNo tiene atenciones propias para corregir.")
        return

    atencion = _pedir_atencion(atenciones, "agregar una corrección")
    if atencion is None:
        return

    texto = _pedir_observaciones()
    if not _confirmar("¿Confirma agregar la corrección como adenda?"):
        print("\nCorrección cancelada; la atención original no cambió.")
        return

    atenciones_actualizadas = cargar_json(RUTA_HISTORIAS_CLINICAS) or []
    atencion_actualizada = next(
        (item for item in atenciones_actualizadas if item["id"] == atencion["id"]),
        None,
    )
    if atencion_actualizada is None:
        print("\nLa atención ya no está disponible.")
        return

    try:
        agregar_adenda_a_atencion(
            atencion_actualizada,
            id_medico,
            texto,
            datetime.now(),
        )
    except ValueError as error:
        print(f"\n{error}")
        return

    guardar_json(RUTA_HISTORIAS_CLINICAS, atenciones_actualizadas)
    print("\nCorrección agregada sin modificar la atención original.")
