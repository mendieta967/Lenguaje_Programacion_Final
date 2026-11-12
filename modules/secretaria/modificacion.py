from core.configuracion import cargar_json, guardar_json
from modules.secretaria.consultas import (
    buscar_paciente_por_dni,
    buscar_paciente_por_id,
    listar_pacientes,
)
from utils.validaciones import (
    validar_nombre,
    validar_dni,
    validar_telefono,
    validar_direccion,
    validar_fecha,
)


def _pedir_nombre(campo):

    while True:
        nombre = input(f"Ingrese el nuevo {campo}: ").strip()

        if validar_nombre(nombre):
            return nombre

        print("\nIngrese solo letras y espacios.")


def _pedir_dni(pacientes, id_paciente):

    while True:
        dni = input("Ingrese el nuevo DNI: ").strip()

        if not validar_dni(dni):
            print("\nEl DNI debe tener exactamente 8 dígitos.")
            continue

        paciente_encontrado = buscar_paciente_por_dni(pacientes, dni)

        if (
            paciente_encontrado is not None
            and paciente_encontrado["id"] != id_paciente
        ):
            print("\nEse DNI ya está registrado.")
            continue

        return dni


def _pedir_telefono():

    while True:
        telefono = input("Ingrese el nuevo teléfono: ").strip()

        if validar_telefono(telefono):
            return telefono

        print("\nEl teléfono debe tener exactamente 9 dígitos.")


def _pedir_direccion():

    while True:
        direccion = input("Ingrese la nueva dirección: ").strip()

        if validar_direccion(direccion):
            return direccion

        print("\nLa dirección debe tener al menos 5 caracteres.")


def _pedir_fecha_nacimiento():

    while True:
        fecha = input(
            "Ingrese la nueva fecha de nacimiento (dd/mm/aaaa): "
        ).strip()

        if validar_fecha(fecha):
            return fecha

        print("\nIngrese una fecha válida que no sea futura.")


def modificar_paciente(ruta_pacientes):

    pacientes = cargar_json(ruta_pacientes) or []

    if not pacientes:
        print("\nNo hay pacientes registrados.")
        return

    listar_pacientes(ruta_pacientes)

    try:
        id_paciente = int(input("\nIngrese el ID del paciente a modificar: "))
    except ValueError:
        print("\nEl ID debe ser un número.")
        return

    paciente = buscar_paciente_por_id(pacientes, id_paciente)

    if paciente is None:
        print("\nNo existe un paciente con ese ID.")
        return

    while True:
        print("\n¿Qué dato desea modificar?")
        print("1. Nombre")
        print("2. Apellido")
        print("3. DNI")
        print("4. Teléfono")
        print("5. Dirección")
        print("6. Fecha de nacimiento")
        print("0. Volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            paciente["nombre"] = _pedir_nombre("nombre")

        elif opcion == "2":
            paciente["apellido"] = _pedir_nombre("apellido")

        elif opcion == "3":
            paciente["dni"] = _pedir_dni(pacientes, id_paciente)

        elif opcion == "4":
            paciente["telefono"] = _pedir_telefono()

        elif opcion == "5":
            paciente["direccion"] = _pedir_direccion()

        elif opcion == "6":
            paciente["fecha_nacimiento"] = _pedir_fecha_nacimiento()

        elif opcion == "0":
            print("\nVolviendo al menú de secretaria.")
            return

        else:
            print("\nOpción inválida.")
            continue

        guardar_json(ruta_pacientes, pacientes)
        print("\nDato actualizado correctamente.")