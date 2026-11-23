from datetime import datetime

from core.configuracion import RUTA_PACIENTES, RUTA_TURNOS, RUTA_USUARIOS, cargar_json
from utils.validaciones import validar_dni


def filtrar_turnos(turnos, fecha=None, id_medico=None, id_paciente=None):
    turnos_encontrados = []

    for turno in turnos:
        if fecha is not None and turno["fecha"] != fecha:
            continue

        if id_medico is not None and turno["id_medico"] != id_medico:
            continue

        if id_paciente is not None and turno["id_paciente"] != id_paciente:
            continue

        turnos_encontrados.append(turno)

    return turnos_encontrados


def mostrar_turnos(turnos):
    if not turnos:
        print("\nNo se encontraron turnos.")
        return

    pacientes = cargar_json(RUTA_PACIENTES) or []
    usuarios = cargar_json(RUTA_USUARIOS) or []
    pacientes_por_id = {paciente["id"]: paciente for paciente in pacientes}
    medicos_por_id = {
        usuario["id"]: usuario
        for usuario in usuarios
        if usuario["rol"] == "MEDICO"
    }

    print("\n===== TURNOS =====")

    for turno in turnos:
        paciente = pacientes_por_id.get(turno["id_paciente"])
        medico = medicos_por_id.get(turno["id_medico"])

        nombre_paciente = "No encontrado"
        if paciente is not None:
            nombre_paciente = f"{paciente['nombre']} {paciente['apellido']}"

        nombre_medico = "No encontrado"
        if medico is not None:
            nombre_medico = f"{medico['nombre']} {medico['apellido']}"

        print("\n" + "-" * 40)
        print(f"Turno: {turno['id']}")
        print(f"Fecha: {turno['fecha']}")
        print(f"Hora: {turno['hora']}")
        print(f"Paciente: {nombre_paciente}")
        print(f"DNI: {paciente['dni'] if paciente is not None else 'No encontrado'}")
        print(f"Médico: {nombre_medico}")
        print(f"Motivo: {turno.get('motivo_consulta', 'No especificado')}")
        print(f"Estado: {turno['estado']}")


def pedir_fecha():
    while True:
        texto = input("\nIngrese la fecha (dd/mm/aaaa, 0 para volver): ").strip()

        if texto == "0":
            return None

        try:
            fecha = datetime.strptime(texto, "%d/%m/%Y")
        except ValueError:
            print("\nFecha inválida.")
            continue

        if fecha.strftime("%d/%m/%Y") == texto:
            return texto

        print("\nFecha inválida.")


def pedir_medico():
    usuarios = cargar_json(RUTA_USUARIOS) or []
    medicos = [
        usuario
        for usuario in usuarios
        if usuario["rol"] == "MEDICO"
    ]

    if not medicos:
        print("\nNo hay médicos registrados.")
        return None

    print("\n===== MÉDICOS =====")
    for medico in medicos:
        print(f"{medico['id']} - {medico['nombre']} {medico['apellido']}")

    while True:
        opcion = input("\nIngrese el ID del médico (0 para volver): ").strip()

        if opcion == "0":
            return None

        try:
            id_medico = int(opcion)
        except ValueError:
            print("\nEl ID debe ser un número.")
            continue

        for medico in medicos:
            if medico["id"] == id_medico:
                return id_medico

        print("\nNo existe un médico con ese ID.")


def pedir_dni_paciente():
    while True:
        dni = input("\nIngrese el DNI del paciente (0 para volver): ").strip()

        if dni == "0":
            return None

        if validar_dni(dni):
            return dni

        print("\nDNI inválido. Debe tener exactamente 8 dígitos.")


def consultar_turnos():
    turnos = cargar_json(RUTA_TURNOS) or []

    if not turnos:
        print("\nNo hay turnos registrados.")
        return

    print("\nConsultar turnos por:")
    print("1. Fecha")
    print("2. Médico")
    print("3. DNI del paciente")
    print("4. Todos")
    print("0. Volver")

    opcion = input("\nSeleccione una opción: ").strip()

    if opcion == "1":
        fecha = pedir_fecha()
        if fecha is None:
            return
        turnos = filtrar_turnos(turnos, fecha=fecha)

    elif opcion == "2":
        id_medico = pedir_medico()
        if id_medico is None:
            return
        turnos = filtrar_turnos(turnos, id_medico=id_medico)

    elif opcion == "3":
        dni = pedir_dni_paciente()
        if dni is None:
            return

        pacientes = cargar_json(RUTA_PACIENTES) or []
        paciente = next(
            (paciente for paciente in pacientes if paciente.get("dni") == dni),
            None,
        )
        if paciente is None:
            print("\nNo se encontró un paciente con ese DNI.")
            return

        turnos = filtrar_turnos(turnos, id_paciente=paciente["id"])

    elif opcion != "4":
        if opcion != "0":
            print("\nOpción inválida.")
        return

    mostrar_turnos(turnos)
