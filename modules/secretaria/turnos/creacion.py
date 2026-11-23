from datetime import datetime, timedelta

from core.configuracion import (
    RUTA_AGENDA,
    RUTA_PACIENTES,
    RUTA_TURNOS,
    RUTA_USUARIOS,
    cargar_json,
    guardar_json,
)
from modules.secretaria.pacientes.consultas import buscar_paciente_por_dni
from modules.secretaria.pacientes.crear import registrar_paciente
from utils.validaciones import validar_dni


DIA_NOMBRE = {
    0: "LUNES",
    1: "MARTES",
    2: "MIERCOLES",
    3: "JUEVES",
    4: "VIERNES",
    5: "SABADO",
}
DIAS_TEXTO = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
}
DIAS_PARA_BUSCAR = 30


def hora_a_minutos(hora):
    horas, minutos = hora.split(":")
    return int(horas) * 60 + int(minutos)


def minutos_a_hora(minutos):
    horas = minutos // 60
    resto = minutos % 60
    return f"{horas:02d}:{resto:02d}"


def obtener_siguiente_id(turnos):
    if not turnos:
        return 1
    return max(turno["id"] for turno in turnos) + 1


def pedir_paciente():
    pacientes = cargar_json(RUTA_PACIENTES) or []

    while True:
        dni = input("\nIngrese el DNI del paciente (0 para cancelar): ").strip()

        if dni == "0":
            return None

        if not validar_dni(dni):
            print("\nDNI inválido. Debe tener exactamente 8 dígitos.")
            continue

        paciente = buscar_paciente_por_dni(pacientes, dni)

        if paciente is not None:
            if not paciente["activo"]:
                print("\nEl paciente existe, pero está inactivo.")
                return None

            print(
                f"\nPaciente encontrado: "
                f"{paciente['nombre']} {paciente['apellido']}"
            )
            return paciente

        print("\nEl paciente no está registrado.")
        confirmar = input("¿Desea registrarlo ahora? (S/N): ").strip().casefold()

        if confirmar == "s":
            nuevo_paciente = registrar_paciente(RUTA_PACIENTES, dni)
            return nuevo_paciente

        if confirmar == "n":
            return None

        print("\nIngrese S o N.")


def pedir_motivo_consulta():
    while True:
        motivo = input("\nIngrese el motivo de la consulta: ").strip()
        if motivo:
            return motivo
        print("\nEl motivo de la consulta no puede estar vacío.")


def pedir_medico():
    usuarios = cargar_json(RUTA_USUARIOS) or []
    medicos = [
        usuario
        for usuario in usuarios
        if usuario["rol"] == "MEDICO" and usuario["activo"]
    ]

    if not medicos:
        print("\nNo hay médicos activos registrados.")
        return None

    print("\n===== MÉDICOS DISPONIBLES =====")

    for medico in medicos:
        print(
            f"{medico['id']} - {medico['nombre']} {medico['apellido']} "
            f"({medico['especialidad']})"
        )

    while True:
        try:
            id_medico = int(input("\nIngrese el ID del médico (0 para cancelar): "))
        except ValueError:
            print("\nEl ID debe ser un número.")
            continue

        if id_medico == 0:
            return None

        for medico in medicos:
            if medico["id"] == id_medico:
                return medico

        print("\nNo existe un médico activo con ese ID.")


def buscar_agenda(id_medico):
    agendas = cargar_json(RUTA_AGENDA) or []

    for agenda in agendas:
        if agenda["id_medico"] == id_medico:
            return agenda

    return None


def generar_horarios(agenda, dia, fecha, id_medico):
    turnos = cargar_json(RUTA_TURNOS) or []
    horarios_ocupados = {
        turno["hora"]
        for turno in turnos
        if turno["id_medico"] == id_medico
        and turno["fecha"] == fecha
        and turno["estado"] != "CANCELADO"
    }

    disponibles = []
    ahora = datetime.now()

    for bloque in agenda["bloques"]:
        if bloque["dia"] != dia:
            continue

        inicio = hora_a_minutos(bloque["inicio"])
        fin = hora_a_minutos(bloque["fin"])

        while inicio + 30 <= fin:
            hora = minutos_a_hora(inicio)
            if (
                hora not in horarios_ocupados
                and not (
                    fecha == ahora.strftime("%d/%m/%Y")
                    and hora_a_minutos(hora) <= ahora.hour * 60 + ahora.minute
                )
            ):
                disponibles.append(hora)
            inicio += 30

    return disponibles


def obtener_fechas_disponibles(agenda, id_medico):
    hoy = datetime.now().date()
    fechas_disponibles = []

    for dias_adelante in range(DIAS_PARA_BUSCAR):
        fecha = hoy + timedelta(days=dias_adelante)

        if fecha.weekday() not in DIA_NOMBRE:
            continue

        fecha_texto = fecha.strftime("%d/%m/%Y")
        dia = DIA_NOMBRE[fecha.weekday()]
        horarios = generar_horarios(agenda, dia, fecha_texto, id_medico)

        if horarios:
            fechas_disponibles.append((fecha_texto, fecha, horarios))

    return fechas_disponibles


def pedir_fecha(fechas_disponibles):
    if not fechas_disponibles:
        print("\nNo hay fechas disponibles en los próximos 30 días.")
        return None

    print("\n===== FECHAS DISPONIBLES =====")

    for numero, (fecha_texto, fecha, _) in enumerate(
        fechas_disponibles,
        start=1,
    ):
        print(f"{numero}. {DIAS_TEXTO[fecha.weekday()]} {fecha_texto}")

    while True:
        opcion = input("\nSeleccione una fecha (0 para cancelar): ").strip()

        try:
            numero = int(opcion)
        except ValueError:
            print("\nSeleccione una opción válida.")
            continue

        if numero == 0:
            return None

        if 1 <= numero <= len(fechas_disponibles):
            return fechas_disponibles[numero - 1]

        print("\nSeleccione una opción válida.")


def pedir_hora(horarios):
    if not horarios:
        print("\nNo hay horarios disponibles.")
        return None

    print("\n===== HORARIOS DISPONIBLES =====")

    for numero, hora in enumerate(horarios, start=1):
        print(f"{numero}. {hora}")

    while True:
        opcion = input("\nSeleccione una opción (0 para cancelar): ").strip()

        try:
            numero = int(opcion)
        except ValueError:
            print("\nSeleccione una opción válida.")
            continue

        if numero == 0:
            return None

        if 1 <= numero <= len(horarios):
            return horarios[numero - 1]

        print("\nSeleccione una opción válida.")


def registrar_turno():
    print("\n===== REGISTRAR TURNO =====")

    paciente = pedir_paciente()
    if paciente is None:
        return

    motivo_consulta = pedir_motivo_consulta()

    medico = pedir_medico()
    if medico is None:
        return

    agenda = buscar_agenda(medico["id"])
    if agenda is None:
        print("\nEl médico no tiene agenda registrada.")
        return

    fechas_disponibles = obtener_fechas_disponibles(agenda, medico["id"])
    fecha_seleccionada = pedir_fecha(fechas_disponibles)

    if fecha_seleccionada is None:
        return

    fecha, _, horarios = fecha_seleccionada
    hora = pedir_hora(horarios)

    if hora is None:
        return

    turnos = cargar_json(RUTA_TURNOS) or []

    for turno in turnos:
        if (
            turno["id_medico"] == medico["id"]
            and turno["fecha"] == fecha
            and turno["hora"] == hora
            and turno["estado"] != "CANCELADO"
        ):
            print("\nEse horario acaba de ser reservado.")
            return

    nuevo_turno = {
        "id": obtener_siguiente_id(turnos),
        "id_paciente": paciente["id"],
        "id_medico": medico["id"],
        "fecha": fecha,
        "hora": hora,
        "motivo_consulta": motivo_consulta,
        "estado": "RESERVADO",
    }

    turnos.append(nuevo_turno)
    guardar_json(RUTA_TURNOS, turnos)

    print("\nTurno registrado correctamente.")
