from core.configuracion import cargar_json


def listar_pacientes(ruta_pacientes):

    pacientes = cargar_json(ruta_pacientes) or []

    if not pacientes:
        print("\nNo hay pacientes registrados.")
        return

    print("\n===== LISTA DE PACIENTES =====")

    for paciente in pacientes:
        mostrar_paciente(paciente)


def mostrar_paciente(paciente):

    estado = "Activo" if paciente["activo"] else "Inactivo"

    print("\n" + "-" * 35)
    print(f"ID: {paciente['id']}")
    print(f"Nombre: {paciente['nombre']} {paciente['apellido']}")
    print(f"DNI: {paciente['dni']}")
    print(f"Teléfono: {paciente['telefono']}")
    print(f"Dirección: {paciente['direccion']}")
    print(f"Fecha de nacimiento: {paciente['fecha_nacimiento']}")
    print(f"Estado: {estado}")
    print("-" * 35)


def buscar_paciente_por_id(pacientes, id_paciente):
    
    for paciente in pacientes:
        if paciente["id"] == id_paciente:
            return paciente

    return None


def buscar_paciente_por_dni(pacientes, dni):

    for paciente in pacientes:
        if paciente["dni"] == dni:
            return paciente

    return None


def buscar_paciente_por_nombre(pacientes, nombre_completo):

    nombre_buscado = " ".join(nombre_completo.strip().casefold().split())
    pacientes_encontrados = []

    for paciente in pacientes:
        nombre_paciente = (
            f"{paciente['nombre']} {paciente['apellido']}".casefold()
        )
        nombre_paciente = " ".join(nombre_paciente.split())

        if nombre_paciente == nombre_buscado:
            pacientes_encontrados.append(paciente)

    return pacientes_encontrados


def buscar_paciente(ruta_pacientes):

    pacientes = cargar_json(ruta_pacientes) or []

    if not pacientes:
        print("\nNo hay pacientes registrados.")
        return

    print("\nBuscar paciente por:")
    print("1. ID")
    print("2. DNI")
    print("3. Nombre y apellido")

    opcion = input("\nSeleccione una opción: ").strip()
    pacientes_encontrados = []

    if opcion == "1":
        try:
            id_paciente = int(input("Ingrese el ID del paciente: "))
        except ValueError:
            print("\nEl ID debe ser un número.")
            return

        paciente = buscar_paciente_por_id(pacientes, id_paciente)
        if paciente is not None:
            pacientes_encontrados.append(paciente)

    elif opcion == "2":
        dni = input("Ingrese el DNI del paciente: ").strip()
        paciente = buscar_paciente_por_dni(pacientes, dni)

        if paciente is not None:
            pacientes_encontrados.append(paciente)

    elif opcion == "3":
        nombre_completo = input(
            "Ingrese el nombre y apellido del paciente: "
        )
        pacientes_encontrados = buscar_paciente_por_nombre(
            pacientes,
            nombre_completo,
        )

    else:
        print("\nOpción inválida.")
        return

    if not pacientes_encontrados:
        print("\nNo se encontraron pacientes.")
        return

    if len(pacientes_encontrados) == 1:
        print("\nPaciente encontrado:")
    else:
        print("\nPacientes encontrados:")

    for paciente in pacientes_encontrados:
        mostrar_paciente(paciente)