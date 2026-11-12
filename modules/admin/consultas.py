from core.configuracion import cargar_json


def listar_usuarios(ruta_usuarios):

    usuarios = cargar_json(ruta_usuarios) or []

    if not usuarios:
        print("\nNo hay usuarios registrados.")
        return

    print("\n" + "=" * 90)
    print("LISTA DE USUARIOS")
    print("=" * 90)
    print(
        f"{'ID':<4}"
        f"{'NOMBRE':<25}"
        f"{'DNI':<12}"
        f"{'USUARIO':<15}"
        f"{'ROL':<12}"
        f"{'ESTADO':<10}"
    )
    print("-" * 80)

    for usuario in usuarios:
        estado = "Activo" if usuario["activo"] else "Inactivo"
        nombre_completo = usuario["nombre"] + " " + usuario["apellido"]

        print(
            f"{usuario['id']:<4}"
            f"{nombre_completo:<25}"
            f"{usuario['dni']:<12}"
            f"{usuario['usuario']:<15}"
            f"{usuario['rol']:<12}"
            f"{estado:<10}"
        )


def buscar_usuario_por_id(usuarios, id_usuario):

    for usuario in usuarios:
        if usuario["id"] == id_usuario:
            return usuario

    return None


def buscar_usuario(ruta_usuarios):

    usuarios = cargar_json(ruta_usuarios) or []

    if not usuarios:
        print("\nNo hay usuarios registrados.")
        return

    print("\nBuscar usuario por:")
    print("1. ID")
    print("2. DNI")
    print("3. Nombre de usuario")

    opcion = input("Seleccione una opción: ").strip()
    usuario_encontrado = None

    if opcion == "1":
        try:
            id_usuario = int(input("Ingrese el ID: "))
        except ValueError:
            print("\nEl ID debe ser un número.")
            return

        usuario_encontrado = buscar_usuario_por_id(usuarios, id_usuario)

    elif opcion == "2":
        dni = input("Ingrese el DNI: ").strip()

        for usuario in usuarios:
            if usuario["dni"] == dni:
                usuario_encontrado = usuario
                break

    elif opcion == "3":
        nombre_usuario = input("Ingrese el nombre de usuario: ").strip().lower()

        for usuario in usuarios:
            if usuario["usuario"].lower() == nombre_usuario:
                usuario_encontrado = usuario
                break

    else:
        print("\nOpción inválida.")
        return

    if usuario_encontrado is None:
        print("\nNo se encontró el usuario.")
        return

    estado = "Activo" if usuario_encontrado["activo"] else "Inactivo"

    print("\nUsuario encontrado:")
    print(f"ID: {usuario_encontrado['id']}")
    print(
        f"Nombre: {usuario_encontrado['nombre']} "
        f"{usuario_encontrado['apellido']}"
    )
    print(f"DNI: {usuario_encontrado['dni']}")
    print(f"Usuario: {usuario_encontrado['usuario']}")
    print(f"Rol: {usuario_encontrado['rol']}")
    print(f"Estado: {estado}")