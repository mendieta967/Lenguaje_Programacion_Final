# Sistema de gestión hospitalaria

Proyecto académico de una aplicación de consola escrita en Python. Actualmente
incluye el menú principal, la creación inicial de un administrador y un flujo
básico de inicio de sesión.

## Requisitos

- Python 3 (desarrollado y probado localmente con Python 3.13).
- No se necesitan paquetes externos.

## Ejecución

Abre una terminal en la carpeta raíz del proyecto (la que contiene `main.py`) y
ejecuta uno de estos comandos:

```bash
python main.py
```

En Windows también puedes usar el lanzador de Python:

```powershell
py main.py
```

En Git Bash, si Python está instalado en `C:\python313` y el comando `python` no
está en el `PATH`:

```bash
/c/python313/python.exe main.py
```

Las rutas de datos se resuelven desde la carpeta del proyecto. Para ejecutarlo
desde otra ubicación, indica la ruta completa de `main.py`. Si usas
`python main.py`, sitúate primero en la raíz del proyecto.

## Primer inicio y datos locales

Al iniciar, el programa crea `data/` si no existe. Si `data/usuarios.json` no
existe, crea el archivo; si está vacío o contiene una lista vacía, solicita los
datos para registrar el primer administrador. Si ya hay usuarios, muestra el
menú principal.

El archivo de usuarios es información local y está excluido de Git mediante
`.gitignore`. No publiques ni compartas ese archivo porque puede contener datos
personales. Las contraseñas nuevas se guardan como hashes SHA-256, no como texto
plano. Sin embargo, SHA-256 sin salt es demasiado rápido para proteger
contraseñas en una aplicación real; usa una función diseñada para contraseñas,
como scrypt o PBKDF2, antes de almacenar datos reales.

Si el archivo de usuarios se creó antes de incorporar el hash, sus contraseñas
están en el formato anterior y no coincidirán con el verificador actual. Restablece
esas contraseñas o migra los registros antes de iniciar sesión.

El archivo debe ser JSON válido con una lista de usuarios. Cada registro usa los
campos `id`, `nombre`, `apellido`, `dni`, `usuario`, `password`, `rol` y
`activo`. Si el JSON está mal formado, el programa no puede cargar los usuarios
y termina con un error; corrige o restaura el archivo local antes de volver a
ejecutarlo.

## Funcionalidades actuales

- **Menú principal:** permite iniciar sesión o salir.
- **Inicio de sesión:** busca el nombre de usuario sin distinguir mayúsculas de
  minúsculas, rechaza cuentas inactivas y verifica el hash de la contraseña.
- **Administrador inicial:** se registra cuando todavía no hay usuarios.
- **Menú de administrador:** muestra opciones para crear y listar usuarios, y
  permite cerrar sesión. La creación y el listado todavía están en desarrollo.
- **Otros roles:** secretaria y médico muestran un aviso de que sus menús están
  en desarrollo.

## Estructura del proyecto

```text
.
├── main.py                 # Menú principal y derivación según el rol
├── core/
│   ├── configuracion.py    # Rutas absolutas basadas en la ubicación del proyecto
│   ├── seguridad.py        # Generación y verificación de hashes
│   └── sistema.py          # Preparación y carga de usuarios
├── modules/
│   ├── admin.py            # Menú del administrador
│   ├── autenticacion.py    # Inicio de sesión
│   └── usuarios.py         # Creación del administrador inicial
└── data/
    └── usuarios.json       # Datos locales; no se versiona
```

## Estado y próximos pasos

El proyecto está en desarrollo. Las opciones de crear/listar usuarios y los
menús de secretaria y médico son marcadores, no funcionalidades terminadas.
También queda pendiente reemplazar SHA-256 sin salt por un algoritmo apropiado
para contraseñas antes de usar el sistema con datos reales.
