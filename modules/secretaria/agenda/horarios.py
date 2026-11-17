from utils.validaciones import validar_hora


DIAS = {
    "1": "LUNES",
    "2": "MARTES",
    "3": "MIERCOLES",
    "4": "JUEVES",
    "5": "VIERNES",
    "6": "SABADO",
}

DIA_NOMBRE = {
    "LUNES": "Lunes",
    "MARTES": "Martes",
    "MIERCOLES": "Miércoles",
    "JUEVES": "Jueves",
    "VIERNES": "Viernes",
    "SABADO": "Sábado",
}


def hora_a_minutos(hora):

    horas, minutos = hora.split(":")

    return int(horas) * 60 + int(minutos)


def validar_bloque_horario(dia, inicio, fin, bloques):

    if dia not in DIA_NOMBRE:
        print("\nSeleccione un día válido de lunes a sábado.")
        return False

    if not validar_hora(inicio) or not validar_hora(fin):
        print("\nLa hora debe tener formato HH:MM y ser válida.")
        return False

    inicio_min = hora_a_minutos(inicio)
    fin_min = hora_a_minutos(fin)

    if inicio_min >= fin_min:
        print("\nLa hora de inicio debe ser menor que la hora de fin.")
        return False

    if fin_min - inicio_min < 30:
        print("\nEl bloque debe tener una duración mínima de 30 minutos.")
        return False

    apertura = 8 * 60
    cierre = 13 * 60 if dia == "SABADO" else 18 * 60

    if inicio_min < apertura or fin_min > cierre:
        print("\nEl horario está fuera del horario de atención.")
        return False

    for bloque in bloques:
        if bloque["dia"] != dia:
            continue

        bloque_inicio = hora_a_minutos(bloque["inicio"])
        bloque_fin = hora_a_minutos(bloque["fin"])

        if inicio_min < bloque_fin and fin_min > bloque_inicio:
            print("\nEl bloque horario se superpone con otro ya registrado.")
            return False

    return True


def pedir_tipo_horario():

    print("\nSeleccione el tipo de horario:")
    print("1. Jornada corrida (un bloque)")
    print("2. Jornada partida (dos bloques)")
    print("0. Volver")

    while True:
        opcion = input("Opción: ").strip()

        if opcion == "0":
            return None

        if opcion == "1":
            return 1

        if opcion == "2":
            return 2

        print("\nSeleccione 1 o 2.")


def _pedir_hora(etiqueta):

    while True:
        hora = input(f"{etiqueta} (HH:MM): ").strip()

        if validar_hora(hora):
            return hora

        print("\nLa hora debe tener formato HH:MM y ser válida.")


def _pedir_bloque_horario(dia, bloques):

    while True:
        inicio = _pedir_hora("Hora de inicio")
        fin = _pedir_hora("Hora de fin")

        if validar_bloque_horario(dia, inicio, fin, bloques):
            return {
                "dia": dia,
                "inicio": inicio,
                "fin": fin,
            }


def pedir_bloques_horarios(dia, cantidad, bloques_existentes):

    bloques_nuevos = []

    for numero_bloque in range(1, cantidad + 1):
        print(f"\nIngrese el bloque {numero_bloque} de {cantidad}.")

        while True:
            bloques = bloques_existentes + bloques_nuevos
            bloque = _pedir_bloque_horario(dia, bloques)

            if (
                numero_bloque == 2
                and hora_a_minutos(bloque["inicio"])
                <= hora_a_minutos(bloques_nuevos[0]["fin"])
            ):
                print(
                    "\nEn la jornada partida, el segundo bloque debe "
                    "comenzar después del primero."
                )
                continue

            bloques_nuevos.append(bloque)
            break

    return bloques_nuevos
