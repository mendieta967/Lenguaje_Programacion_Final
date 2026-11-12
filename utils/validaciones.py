from datetime import date, datetime


# ==========================================
# CONSTANTES
# ==========================================

ROLES = ("ADMIN", "SECRETARIA", "MEDICO")

# ==========================================
# VALIDACIONES
# ==========================================

# Validamos que el nombre solo contenga letras y espacios
def validar_nombre(nombre):

    nombre = nombre.strip()

    return nombre.replace(" ", "").isalpha()


# Validamos que el DNI tenga exactamente 8 dígitos
def validar_dni(dni):

    return dni.isdigit() and len(dni) == 8


# Validamos el nombre de usuario
def validar_usuario(nombre_usuario):

    nombre_usuario = nombre_usuario.strip()

    return len(nombre_usuario) >= 4


# Validamos que la contraseña tenga al menos 6 caracteres
def validar_password(password):

    return len(password) >= 6


# Validamos que el rol sea uno de los permitidos
def validar_rol(rol):

    return rol in ROLES

def validar_telefono(telefono):

    return telefono.isdigit() and len(telefono) == 9


def validar_direccion(direccion):

    return len(direccion.strip()) >= 5


def validar_fecha(fecha):

    try:
        fecha_convertida = datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        return False

    return (
        fecha_convertida.strftime("%d/%m/%Y") == fecha
        and fecha_convertida.date() <= date.today()
    )