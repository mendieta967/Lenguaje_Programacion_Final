# Análisis de paradigmas, calidad y pruebas

Este documento aporta evidencia técnica para el informe del desafío. Describe
el código actual; no implica que el sistema esté listo para utilizarse con
datos clínicos reales.

## Comparación de paradigmas

| Paradigma | Uso observable en el sistema | Ventajas para este caso | Desventajas o límites |
|---|---|---|---|
| Estructurado/procedimental | `main.py`, los menús por rol y las funciones de creación, consulta y cambio de estado en `modules/secretaria/`. | Representa directamente los pasos que sigue secretaría y facilita recorrer un flujo de consola sin dependencias externas. | Al crecer el sistema, los datos como diccionarios y las reglas repartidas entre funciones pueden dificultar mantener invariantes comunes. |
| Orientado a objetos | `AtencionClinica` en `modules/medico/consultas.py` encapsula los datos, expone propiedades de lectura y concentra la creación y las adendas. | Mantiene juntas las reglas asociadas a una atención, como permitir una adenda solo al médico autor, y separa el modelo de su serialización JSON. | Se aplica solo a la atención clínica; pacientes, turnos, agendas y usuarios continúan representados principalmente como diccionarios. |
| Funcional | `filter` selecciona las atenciones de una historia y `map` extrae sus IDs en `modules/medico/consultas.py`; también se usa `lambda` como clave de ordenamiento. | Expresa transformaciones de colecciones de forma concisa y permite probar las consultas con datos en memoria. | `map` y `filter` son iteradores perezosos; además, las lambdas complejas pueden restar claridad. El programa no es funcional en su totalidad porque otras operaciones modifican datos y archivos. |

El programa no implementa una interfaz gráfica basada en eventos: sus menús
son ciclos de consola que esperan una entrada con `input()`. Por eso no se
presenta la programación orientada a eventos como un paradigma aplicado.

## Selección y combinación

La selección se hizo por el tipo de problema, no para convertir todo el
proyecto a un único paradigma:

1. **Ajuste al flujo:** la atención de una secretaría se organiza en pasos
   secuenciales; los menús y funciones procedimentales reflejan ese flujo.
2. **Protección de reglas del dominio:** la atención clínica tiene datos y
   reglas propias; `AtencionClinica` encapsula la creación y las adendas.
3. **Trabajo con colecciones:** buscar atenciones de un paciente y calcular
   el próximo ID son transformaciones de listas; `filter` y `map` expresan
   esas operaciones sin cambiar el resultado esperado.
4. **Simplicidad de despliegue:** Python y JSON permiten ejecutar el proyecto
   académico sin un servidor ni paquetes externos.

La decisión trazable es conservar los procedimientos para coordinar los
flujos, usar el modelo orientado a objetos donde existe una regla propia de
la entidad y aplicar operaciones funcionales en consultas de colecciones.
Esto evita una reescritura amplia y mantiene los menús y la persistencia
actuales.

## Principios SOLID y buenas prácticas

### Principios SOLID observables

- **Responsabilidad Única (SRP):** las funciones de turnos se separan por
  responsabilidad: `creacion.py` registra, `consultas.py` busca y presenta,
  `estado.py` cancela o marca inasistencias, y `reprogramacion.py` valida y
  cambia horarios. La persistencia común se centraliza en
  `core/configuracion.py`.
- **Inversión de Dependencias (DIP), aplicada parcialmente:** las reglas
  `turno_puede_atenderse`, `turno_es_futuro` y `aplicar_estado_ausente`
  reciben el turno y, cuando se necesita, la hora actual como argumentos.
  Las pruebas pueden proporcionar una fecha fija sin depender del reloj real.
  También se usa `cargar_json`/`guardar_json` en lugar de abrir archivos desde
  cada operación. No hay, sin embargo, interfaces de repositorio ni inversión
  completa de las dependencias de persistencia en toda la aplicación.

### Buenas prácticas con ejemplos

1. **Modularidad por función del sistema:** pacientes, agenda y turnos tienen
   módulos separados; el cambio de un estado de turno no se mezcla con la
   captura de un paciente.
2. **Nombres del dominio:** funciones como `filtrar_horarios_paciente`,
   `aplicar_reprogramacion` y `obtener_historia_clinica` explican su propósito.
3. **Validación de entradas:** `utils/validaciones.py` reúne validaciones de
   DNI, teléfono, fecha, hora, rol y otros campos antes de persistirlos.
4. **Errores explícitos:** las reglas de dominio rechazan operaciones no
   permitidas con `ValueError`; el flujo de consola informa el error sin
   presentar la operación como exitosa.
5. **Pruebas deterministas:** los casos de turnos reciben fechas y horas fijas,
   lo que permite repetir pruebas sin depender de la fecha en que se ejecutan.

## Resultado de pruebas automatizadas

Ejecución realizada el **23/11/2026** en el entorno local del proyecto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

Resultado:

```text
Ran 14 tests
OK
```

Las 14 pruebas se distribuyen entre ausencias (`test_ausencia_turnos.py`),
reprogramación (`test_reprogramacion.py`) y consultas/atenciones médicas
(`test_medico.py`). Este resultado demuestra que esos casos automatizados
pasaron; no demuestra por sí solo que todas las funciones estén cubiertas ni
que el sistema sea seguro para producción.

## Impacto de la calidad en los usuarios

- Una regla incorrecta de disponibilidad o reprogramación puede generar turnos
  superpuestos, hacer que un paciente pierda una consulta o dejar tiempo médico
  sin aprovechar. En un establecimiento con recursos limitados, el error puede
  aumentar demoras y trabajo manual.
- Una atención incompleta, duplicada o atribuida al paciente equivocado puede
  confundir al profesional y afectar decisiones posteriores. Por eso se
  conserva la nota original al agregar una adenda y se verifica la relación
  entre turno, paciente y médico.
- Una validación deficiente puede crear registros duplicados o datos de
  contacto incorrectos, dificultando ubicar al paciente y mantener una
  historia consistente.
- La exposición de DNI, datos de contacto o notas clínicas puede dañar la
  privacidad y la confianza de los pacientes y afectar la responsabilidad
  profesional del personal de salud. La calidad del código no reemplaza las
  medidas de seguridad y las obligaciones legales correspondientes.

## Limitaciones pendientes

Los archivos de historias clínicas se guardan como JSON sin cifrado y las
contraseñas actuales usan SHA-256 sin salt. Este documento no presenta esas
medidas como conformes para datos reales; su tratamiento queda pendiente de la
consulta con el docente. Para demostraciones y repositorios compartidos deben
usarse únicamente datos ficticios.
