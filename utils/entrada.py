import sys


def pedir_password(mensaje="Contraseña: "):
    print(mensaje, end="", flush=True)

    if sys.platform == "win32":
        import msvcrt

        password = ""

        while True:
            tecla = msvcrt.getwch()

            if tecla in ("\r", "\n"):
                print()
                return password

            if tecla == "\b":
                if password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
                continue

            if tecla in ("\x03", "\x04"):
                raise KeyboardInterrupt

            if tecla.isprintable():
                password += tecla
                print("*", end="", flush=True)

    password = ""
    print()
    print("Modo sin soporte de contraseña oculta; usando entrada normal:")
    return input()
