from core.configuracion import cargar_json, guardar_json
from modules.admin.consultas import buscar_usuario_por_id, listar_usuarios


def _confirmar_cambio_estado(accion, usuario):

    confirmacion = input(
        f"\n¿Confirma que desea {accion} la cuenta de "
        f"{usuario['usuario']}? (s/n): "
    ).strip().lower()

    if confirmacion not in ("s", "si"):
        print("\nOperación cancelada.")
        return False

    return True


def desactivar_usuario(ruta_usuarios):

    usuarios = cargar_json(ruta_usuarios) or []

    if not usuarios:
        print("\nNo hay usuarios registrados.")
        return

    listar_usuarios(ruta_usuarios)

    try:
        id_usuario = int(input("\nIngrese el ID del usuario a desactivar: "))
    except ValueError:
        print("\nEl ID debe ser un número.")
        return

    usuario = buscar_usuario_por_id(usuarios, id_usuario)

    if usuario is None:
        print("\nNo existe un usuario con ese ID.")
        return

    if usuario["rol"] == "ADMIN":
        print("\nNo es posible desactivar un administrador.")
        return

    if not usuario["activo"]:
        print("\nEse usuario ya está desactivado.")
        return

    if not _confirmar_cambio_estado("desactivar", usuario):
        return

    usuario["activo"] = False
    guardar_json(ruta_usuarios, usuarios)

    print("\nUsuario desactivado correctamente.")


def activar_usuario(ruta_usuarios):

    usuarios = cargar_json(ruta_usuarios) or []

    if not usuarios:
        print("\nNo hay usuarios registrados.")
        return

    listar_usuarios(ruta_usuarios)

    try:
        id_usuario = int(input("\nIngrese el ID del usuario a activar: "))
    except ValueError:
        print("\nEl ID debe ser un número.")
        return

    usuario = buscar_usuario_por_id(usuarios, id_usuario)

    if usuario is None:
        print("\nNo existe un usuario con ese ID.")
        return

    if usuario["activo"]:
        print("\nEse usuario ya está activo.")
        return

    if not _confirmar_cambio_estado("reactivar", usuario):
        return

    usuario["activo"] = True
    guardar_json(ruta_usuarios, usuarios)

    print("\nUsuario activado correctamente.")