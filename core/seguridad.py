import hashlib


def generar_hash(password):

    password_codificada = password.encode("utf-8")

    password_hash = hashlib.sha256(password_codificada).hexdigest()

    return password_hash


def verificar_password(password, password_hash):

    return generar_hash(password) == password_hash