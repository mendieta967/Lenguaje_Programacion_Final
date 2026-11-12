# Sistema de gestión hospitalaria

Proyecto académico de una aplicación de consola escrita en Python.

## Requisitos

- Python 3.13.
- No se necesitan paquetes externos.

## Ejecución

Abre una terminal en la carpeta raíz del proyecto (donde está `main.py`) y
ejecuta:

```bash
python main.py
```

En Windows también puedes usar:

```powershell
py main.py
```

En Git Bash, si Python está instalado en `C:\python313` y el comando `python`
no está en el `PATH`:

```bash
/c/python313/python.exe main.py
```

Las rutas de los datos se calculan desde la ubicación del proyecto, así que
también puedes indicar la ruta completa de `main.py`.

## Primer inicio y datos locales

Al iniciar, el programa crea la carpeta `data/` y el archivo
`data/usuarios.json` si no existen. Si el archivo no contiene usuarios, solicita
los datos para crear el primer administrador.

Los archivos `data/usuarios.json` y `data/pacientes.json` están excluidos de Git
mediante `.gitignore` porque pueden contener datos personales. No los publiques
ni compartas.

Cada usuario se guarda con estos campos: `id`, `nombre`, `apellido`, `dni`,
`usuario`, `password`, `rol` y `activo`. El archivo debe contener JSON válido
con una lista de usuarios. Si está mal formado, el programa no podrá iniciarse;
corrige o restaura el archivo local antes de volver a ejecutarlo.

Las contraseñas nuevas se guardan como hashes SHA-256, no como texto plano.
SHA-256 sin salt no es adecuado para proteger contraseñas en una aplicación
real; antes de usar datos reales, debe reemplazarse por una función diseñada
para contraseñas, como scrypt o PBKDF2. Los usuarios guardados con un formato
anterior de contraseña podrían necesitar un restablecimiento o una migración.

## Funcionalidades actuales

- **Menú principal:** permite iniciar sesión o salir.
- **Inicio de sesión:** busca el nombre de usuario sin distinguir mayúsculas de
  minúsculas, rechaza cuentas inactivas y verifica la contraseña.
- **Administrador inicial:** se registra durante el primer inicio cuando no
  hay usuarios.
- **Menú de administrador:**
  - Crear usuarios con rol de médico o secretaria.
  - Listar y buscar usuarios por ID, DNI o nombre de usuario.
  - Modificar nombre, apellido, DNI, nombre de usuario, contraseña y rol.
  - Desactivar y reactivar cuentas con confirmación.
- **Validaciones:** nombres y apellidos aceptan letras y espacios; el DNI debe
  tener ocho dígitos; el nombre de usuario debe tener al menos cuatro
  caracteres; y la contraseña, al menos seis.
- **Protección de cuentas:** no se permite desactivar administradores ni
  cambiar su rol desde la opción de modificación.
- **Menú de secretaria:** permite registrar, listar, buscar y modificar
  pacientes. La búsqueda funciona por ID, DNI o nombre y apellido. También
  permite desactivar y reactivar pacientes con confirmación. La gestión de
  turnos todavía está en desarrollo.
- **Menú de médico:** todavía está en desarrollo.

## Estructura del proyecto

```text
.
├── main.py
├── core/
│   ├── configuracion.py
│   ├── seguridad.py
│   └── sistema.py
├── modules/
│   ├── autenticacion.py
│   ├── admin/
│   │   ├── menu.py
│   │   ├── consultas.py
│   │   ├── creacion.py
│   │   ├── estado.py
│   │   └── modificacion.py
│   └── secretaria/
│       ├── menu.py
│       ├── crear_pacientes.py
│       └── consultas.py
├── utils/
│   └── validaciones.py
└── data/
    ├── usuarios.json
    └── pacientes.json
```

- `main.py` inicia el programa y dirige al usuario según su rol.
- `core/` contiene configuración, seguridad e inicialización.
- `modules/` contiene la autenticación y las funciones del administrador,
  separadas por responsabilidad, además del menú de secretaria y el registro
  y las consultas de pacientes.
- `utils/` contiene validaciones reutilizables.
- `data/` almacena los datos locales de usuarios y pacientes; no se versionan.

## Estado del proyecto

El sistema todavía está en desarrollo. El registro, las consultas, la
modificación y la gestión de estado de pacientes están implementados; la
gestión de turnos y el menú de médico siguen pendientes. Antes de usar el
sistema con datos reales, se debe mejorar el almacenamiento de contraseñas y
agregar pruebas automatizadas.
