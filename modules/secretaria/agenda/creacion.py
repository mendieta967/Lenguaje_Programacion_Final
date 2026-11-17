from core.configuracion import (
    RUTA_AGENDA,
    RUTA_USUARIOS,
    cargar_json,
    guardar_json,
)
from modules.secretaria.agenda.horarios import (
    DIAS,
    pedir_bloques_horarios,
    pedir_tipo_horario,
)


def _obtener_medicos(ruta_usuarios):

    usuarios = cargar_json(ruta_usuarios) or []

    medicos = []

    for usuario in usuarios:
        if usuario["rol"] == "MEDICO" and usuario["activo"]:
            medicos.append(usuario)

    return medicos


def _pedir_medico(medicos):

    if not medicos:
        print("\nNo hay médicos activos registrados.")
        return None

    print("\n===== MÉDICOS DISPONIBLES =====")

    print(
        f"\n{'ID':<5}"
        f"{'NOMBRE':<30}"
        f"{'ESPECIALIDAD':<25}"
    )

    print("-" * 60)

    for medico in medicos:
        nombre_completo = f"{medico['nombre']} {medico['apellido']}"

        print(
            f"{medico['id']:<5}"
            f"{nombre_completo:<30}"
            f"{medico['especialidad']:<25}"
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

        print("\nNo existe un médico con ese ID.")


def _buscar_agenda_medico(agendas, id_medico):

    for agenda in agendas:
        if agenda["id_medico"] == id_medico:
            return agenda

    return None


def _pedir_dia(dias_registrados):

    print("\nSeleccione el día del bloque:")
    print("1. Lunes")
    print("2. Martes")
    print("3. Miércoles")
    print("4. Jueves")
    print("5. Viernes")
    print("6. Sábado")
    print("0. Finalizar agenda")

    while True:
        opcion = input("Opción: ").strip()

        if opcion == "0":
            return None

        if opcion in DIAS:
            dia = DIAS[opcion]
            if dia not in dias_registrados:
                return dia
            print("\nEse día ya tiene un horario registrado.")
            continue

        print("\nSeleccione una opción válida.")


def crear_agenda():

    agendas = cargar_json(RUTA_AGENDA) or []
    medicos = _obtener_medicos(RUTA_USUARIOS)
    medico = _pedir_medico(medicos)

    if medico is None:
        return

    agenda_medico = _buscar_agenda_medico(agendas, medico["id"])
    bloques = list(agenda_medico["bloques"]) if agenda_medico else []
    bloques_iniciales = len(bloques)
    dias_registrados = {bloque["dia"] for bloque in bloques}

    if agenda_medico:
        print(
            f"\n===== COMPLETAR AGENDA DE "
            f"{medico['nombre']} {medico['apellido']} ====="
        )
        print("Puede agregar horarios para días todavía no configurados.")
    else:
        print(
            f"\n===== REGISTRAR AGENDA DE "
            f"{medico['nombre']} {medico['apellido']} ====="
        )
        print("Para cada día puede elegir jornada corrida o jornada partida.")

    if agenda_medico:
        print("Los horarios existentes se conservarán sin cambios.")

    while True:
        dia = _pedir_dia(dias_registrados)

        if dia is None:
            if len(bloques) == bloques_iniciales:
                if agenda_medico:
                    print("\nNo se agregaron horarios. La agenda quedó sin cambios.")
                else:
                    print("\nNo se registraron bloques. Operación cancelada.")
                return
            break

        cantidad_bloques = pedir_tipo_horario()
        if cantidad_bloques is None:
            continue

        bloques.extend(
            pedir_bloques_horarios(dia, cantidad_bloques, bloques)
        )

        dias_registrados.add(dia)
        print("\nHorario del día agregado.")

    if agenda_medico:
        agenda_medico["bloques"] = bloques
    else:
        agendas.append({
            "id_medico": medico["id"],
            "bloques": bloques,
        })

    guardar_json(RUTA_AGENDA, agendas)

    if agenda_medico:
        print("\nAgenda completada correctamente.")
    else:
        print("\nAgenda registrada correctamente.")