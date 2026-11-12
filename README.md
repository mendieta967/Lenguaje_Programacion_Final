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

El archivo de usuarios está excluido de Git mediante `.gitignore` porque puede
contener datos personales. No publiques ni compartas ese archivo.

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
- **Otros roles:** los menús de secretaria y médico todavía están en desarrollo.

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
│   └── admin/
│       ├── admin.py
│       ├── consultas.py
│       ├── creacion.py
│       ├── estado.py
│       └── modificacion.py
├── utils/
│   └── validaciones.py
└── data/
    └── usuarios.json
```

- `main.py` inicia el programa y dirige al usuario según su rol.
- `core/` contiene configuración, seguridad e inicialización.
- `modules/` contiene la autenticación y las funciones del administrador,
  separadas por responsabilidad.
- `utils/` contiene validaciones reutilizables.
- `data/usuarios.json` almacena los datos locales y no se versiona.

## Estado del proyecto

El sistema y las operaciones de administración están en desarrollo. Los
menús de médico y secretaria aún no están implementados. Antes de usar el
sistema con datos reales, se debe mejorar el almacenamiento de contraseñas y
agregar pruebas automatizadas.
