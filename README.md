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

Los archivos `data/usuarios.json`, `data/pacientes.json`, `data/agendas.json`,
`data/turnos.json` y `data/historiasClinicas.json` están excluidos de Git
mediante `.gitignore` porque contienen datos locales. No los publiques ni
compartas.
Las atenciones médicas y sus adendas se almacenan en
`data/historiasClinicas.json`, separadas de las reservas. El archivo no cifra
esos datos ni ofrece controles de acceso fuera de la aplicación. No uses
información clínica real en este proyecto académico.

Cada usuario se guarda con estos campos: `id`, `nombre`, `apellido`, `dni`,
`usuario`, `password`, `rol` y `activo`. Los usuarios con rol `MEDICO` también
guardan el campo `especialidad`; es obligatorio al crear usuarios médicos.
El archivo debe contener JSON válido con una lista de usuarios. Si está mal
formado, el programa no podrá iniciarse; corrige o restaura el archivo local
antes de volver a ejecutarlo.

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
  - Crear usuarios con rol de médico o secretaria; al médico se le solicita
    una especialidad.
  - Listar y buscar usuarios por ID, DNI o nombre de usuario.
  - Modificar nombre, apellido, DNI, nombre de usuario, contraseña y
    especialidad médica.
  - Desactivar y reactivar cuentas con confirmación.
- **Validaciones:** nombres y apellidos aceptan letras y espacios; el DNI debe
  tener ocho dígitos; el nombre de usuario debe tener al menos cuatro
  caracteres; y la contraseña, al menos seis.
- **Protección de cuentas:** no se permite desactivar administradores ni
  cambiar el rol de ningún usuario después de su creación.
- **Menú de secretaria:** agrupa las operaciones de pacientes (registrar,
  listar, buscar, modificar y gestionar su estado) y ofrece opciones
  principales para agenda médica y turnos. El registro de agendas médicas
  permite registrar, completar, consultar, modificar y eliminar horarios
  semanales corridos o partidos por médico. La eliminación puede hacerse por
  día o para toda la agenda. No se elimina un día ni una agenda que tenga
  turnos asociados. La búsqueda de pacientes funciona por ID, DNI o nombre y
  apellido.
- **Gestión de turnos:** permite buscar un paciente por DNI y registrar el
  turno si existe; si no existe, solicita sus datos y lo registra antes de
  continuar. Al reservar, solicita y guarda el motivo de consulta. Consulta la
  agenda del médico seleccionado y muestra los horarios y fechas disponibles
  durante los próximos 30 días, en intervalos de 30 minutos. Permite consultar
  turnos por fecha, médico, DNI del paciente o todos; cada turno muestra el DNI
  y el motivo registrado. Permite cancelar reservas sin borrar el registro y
  reprogramar turnos futuros, incluso con otro médico, si el horario está
  disponible para el médico y no se superpone con otro turno del paciente. Los
  cambios conservan el turno y su motivo, y guardan un historial de
  reprogramaciones. Secretaría también puede marcar como `AUSENTE` un turno
  reservado después de que termine el bloque de 30 minutos, con confirmación y
  sin crear una atención médica. El motivo de consulta sirve como antecedente
  de la solicitud, pero no reemplaza una historia clínica documentada por el
  profesional.
- **Menú de médico:** permite consultar sus turnos y registrar atenciones cuando
  llegó el horario reservado. Las observaciones son obligatorias; diagnóstico
  e indicaciones son opcionales. Al guardar la atención, el turno pasa a
  `ATENDIDO`. Las atenciones se guardan en `historiasClinicas.json`, separadas
  de los turnos, y quedan vinculadas al paciente y a la reserva. Cualquier
  médico activo puede consultar por DNI la historia clínica completa y ver qué
  profesional registró cada atención. Solo el médico autor puede agregar
  correcciones como adendas, sin sobrescribir la nota original; secretaría no
  tiene acceso a las notas clínicas.

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
│   ├── secretaria/
│   │   ├── menu.py
│   │   ├── pacientes/
│   │   │   ├── menu.py
│   │   │   ├── crear.py
│   │   │   ├── consultas.py
│   │   │   ├── modificacion.py
│   │   │   └── estado.py
│   │   ├── agenda/
│   │   │   ├── menu.py
│   │   │   ├── creacion.py
│   │   │   ├── consultas.py
│   │   │   ├── modificacion.py
│   │   │   ├── horarios.py
│   │   │   └── estado.py
│   │   └── turnos/
│   │       ├── menu.py
│   │       ├── creacion.py
│   │       ├── consultas.py
│   │       ├── estado.py
│   │       └── reprogramacion.py
│   ├── medico/
│   │   ├── menu.py
│   │   └── consultas.py
├── utils/
│   └── validaciones.py
└── data/
    ├── usuarios.json
    ├── pacientes.json
    ├── agendas.json
    ├── turnos.json
    └── historiasClinicas.json
```

- `main.py` inicia el programa y dirige al usuario según su rol.
- `core/` contiene configuración, seguridad e inicialización.
- `modules/` contiene autenticación y administración. `secretaria/` agrupa
  las gestiones de pacientes, agenda y turnos; `medico/` contiene la atención
  de turnos y la consulta de historias clínicas.
- `utils/` contiene validaciones reutilizables.
- `data/` almacena los datos locales de usuarios, pacientes, agendas, turnos y
  historias clínicas; no se versionan.

## Estado del proyecto

El sistema todavía está en desarrollo. El registro, las consultas, la
modificación y la gestión de estado de pacientes están implementados. La
agenda permite registrar, consultar, modificar y eliminar horarios. El alta de
turnos permite reutilizar pacientes existentes o registrar uno nuevo durante
la operación, y guardar el motivo de consulta. Los turnos se pueden consultar
por fecha, médico o DNI del paciente, cancelar, reprogramar con historial de
cambios y marcar como AUSENTE. El menú de médico permite registrar atenciones,
consultar por DNI historias clínicas compartidas entre médicos y agregar
adendas a las atenciones propias. Antes de usar el sistema con datos reales, se
debe mejorar el almacenamiento de contraseñas y ampliar la cobertura de
pruebas automatizadas.
