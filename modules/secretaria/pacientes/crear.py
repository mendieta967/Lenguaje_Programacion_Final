from core.configuracion import cargar_json, guardar_json
from utils.validaciones import (
    validar_dni,
    validar_nombre,
    validar_direccion,
    validar_telefono,
    validar_fecha,
)


def _paciente_existe(pacientes, dni=None):

    for paciente in pacientes:
        if dni is not None and paciente.get("dni") == dni:
            return True

    return False


def _pedir_nombre(etiqueta):

    while True:
        nombre = input(f"{etiqueta}: ").strip()

        if validar_nombre(nombre):
            return nombre

        print("\nIngrese solo letras y espacios.")


def _pedir_dni(pacientes):

    while True:
        dni = input("DNI: ").strip()

        if not validar_dni(dni):
            print("\nDNI inválido. Debe tener exactamente 8 dígitos.")
            continue

        if _paciente_existe(pacientes, dni=dni):
            print("\nYa existe un paciente registrado con ese DNI.")
            continue

        return dni


def _pedir_telefono():

    while True:
        telefono = input("Teléfono: ").strip()

        if validar_telefono(telefono):
            return telefono

        print("\nEl teléfono debe tener exactamente 9 dígitos.")


def _pedir_direccion():

    while True:
        direccion = input("Dirección: ").strip()

        if validar_direccion(direccion):
            return direccion

        print("\nIngrese una dirección válida.")


def _pedir_fecha_nacimiento():

    while True:
        fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ").strip()

        if not validar_fecha(fecha_nacimiento):
            print("\nFecha inválida.")
            continue

        return fecha_nacimiento


def _pedir_datos_paciente(pacientes):

    nombre = _pedir_nombre("Nombre")
    apellido = _pedir_nombre("Apellido")
    dni = _pedir_dni(pacientes)
    telefono = _pedir_telefono()
    direccion = _pedir_direccion()
    fecha_nacimiento = _pedir_fecha_nacimiento()

    return {
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "telefono": telefono,
        "direccion": direccion,
        "fecha_nacimiento": fecha_nacimiento,
    }


def obtener_siguiente_id(pacientes):

    if not pacientes:
        return 1

    return max(paciente["id"] for paciente in pacientes) + 1


def registrar_paciente(ruta_pacientes):

    pacientes = cargar_json(ruta_pacientes) or []

    print("\n===== REGISTRAR PACIENTE =====")

    datos = _pedir_datos_paciente(pacientes)

    nuevo_paciente = {
        "id": obtener_siguiente_id(pacientes),
        "nombre": datos["nombre"],
        "apellido": datos["apellido"],
        "dni": datos["dni"],
        "telefono": datos["telefono"],
        "direccion": datos["direccion"],
        "fecha_nacimiento": datos["fecha_nacimiento"],
        "activo": True
    }

    pacientes.append(nuevo_paciente)

    guardar_json(ruta_pacientes, pacientes)

    print("\nPaciente registrado correctamente.")