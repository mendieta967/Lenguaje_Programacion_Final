from core.sistema import inicializar_sistema
def main():

    inicializar_sistema()

    while True:

        print("\n" + "=" * 45)
        print("       SISTEMA DE GESTIÓN HOSPITALARIA")
        print("=" * 45)

        print("\n1. Iniciar sesión")
        print("0. Salir")

        option = input("\nSeleccione una opción: ")

        if option == "1":
            print("\nIniciando sesión...")

        elif option == "0":
            print("\nGracias por utilizar el sistema.")
            break

        else:
            print("\nOpción inválida.")


if __name__ == "__main__":
    main()