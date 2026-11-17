from core.configuracion import RUTA_AGENDA, RUTA_USUARIOS, cargar_json
from modules.secretaria.agenda.horarios import DIA_NOMBRE


def buscar_agenda_por_medico(agendas, id_medico):

    for agenda in agendas:
        if agenda["id_medico"] == id_medico:
            return agenda

    return None


def consultar_agenda():

    agendas = cargar_json(RUTA_AGENDA) or []

    if not agendas:
        print("\nNo hay agendas registradas.")
        return

    usuarios = cargar_json(RUTA_USUARIOS) or []
    medicos = {
        usuario["id"]: usuario
        for usuario in usuarios
        if usuario["rol"] == "MEDICO"
    }

    print("\n===== AGENDAS MÉDICAS =====")

    for agenda in agendas:
        medico = medicos.get(agenda["id_medico"])
        print(f"\nID del médico: {agenda['id_medico']}")

        if medico is None:
            print("Médico: no encontrado")
        else:
            nombre_completo = f"{medico['nombre']} {medico['apellido']}"
            print(f"Médico: {nombre_completo}")
            print(f"Especialidad: {medico['especialidad']}")

        bloques = sorted(
            agenda["bloques"],
            key=lambda bloque: (
                list(DIA_NOMBRE).index(bloque["dia"]),
                bloque["inicio"],
            ),
        )

        if not bloques:
            print("No hay horarios configurados.")
            continue

        for bloque in bloques:
            dia = DIA_NOMBRE.get(bloque["dia"], bloque["dia"])
            print(
                f"  {dia}: {bloque['inicio']} - {bloque['fin']}"
            )