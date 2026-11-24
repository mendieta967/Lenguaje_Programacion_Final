from copy import deepcopy
class Usuario:
    def __init__(self, id, nombre, apellido, dni, usuario, password, rol, activo=True):
        self.__id = id
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni
        self.__usuario = usuario
        self.__password = password
        self.__rol = rol
        self.__activo = activo

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    @property
    def dni(self):
        return self.__dni

    @property
    def rol(self):
        return self.__rol

    @property
    def activo(self):
        return self.__activo

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "usuario": self.__usuario,
            "password": self.__password,
            "rol": self.rol,
            "activo": self.activo,
        }


class UsuarioMedico(Usuario):
    def __init__(self, id, nombre, apellido, dni, usuario, password, especialidad, activo=True):
        super().__init__(id, nombre, apellido, dni, usuario, password, "MEDICO", activo)
        self.__especialidad = especialidad

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["especialidad"] = self.__especialidad
        return datos


class UsuarioSecretaria(Usuario):
    pass


class Paciente:
    def __init__(self, id, nombre, apellido, dni, telefono, direccion, fecha_nacimiento, activo=True):
        self.__id = id
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni
        self.__telefono = telefono
        self.__direccion = direccion
        self.__fecha_nacimiento = fecha_nacimiento
        self.__activo = activo

    @property
    def id(self):
        return self.__id

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.__nombre,
            "apellido": self.__apellido,
            "dni": self.__dni,
            "telefono": self.__telefono,
            "direccion": self.__direccion,
            "fecha_nacimiento": self.__fecha_nacimiento,
            "activo": self.__activo,
        }


class Adenda:
    def __init__(self, texto, id_medico, fecha):
        self.__texto = texto
        self.__id_medico = id_medico
        self.__fecha = fecha

    def a_diccionario(self):
        return {
            "fecha": self.__fecha,
            "id_medico": self.__id_medico,
            "texto": self.__texto,
        }


class AtencionClinica:
    def __init__(self, datos):
        self.__datos = deepcopy(datos)

    @property
    def id(self):
        return self.__datos["id"]

    @property
    def id_paciente(self):
        return self.__datos["id_paciente"]

    @property
    def id_medico(self):
        return self.__datos["id_medico"]

    @property
    def observaciones(self):
        return self.__datos["observaciones"]

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(datos)

    def agregar_adenda(self, id_medico, texto, fecha_adenda):
        if self.id_medico != id_medico:
            raise ValueError("No se puede corregir esta atención.")
        if not texto.strip():
            raise ValueError("La corrección no puede estar vacía.")

        adenda = Adenda(
            texto.strip(),
            id_medico,
            fecha_adenda.strftime("%d/%m/%Y %H:%M:%S"),
        )
        self.__datos.setdefault("adendas", []).append(adenda.a_diccionario())

    def a_diccionario(self):
        return deepcopy(self.__datos)


class FabricaAtencion:
    @staticmethod
    def crear(id_atencion, turno, id_medico, observaciones, diagnostico, indicaciones, momento):
        if not observaciones.strip():
            raise ValueError("Las observaciones no pueden estar vacías.")

        datos = {
            "id": id_atencion,
            "id_turno": turno["id"],
            "id_paciente": turno["id_paciente"],
            "id_medico": id_medico,
            "fecha_atencion": momento.strftime("%d/%m/%Y %H:%M:%S"),
            "motivo_consulta": turno.get("motivo_consulta", "No especificado"),
            "observaciones": observaciones.strip(),
            "diagnostico": diagnostico.strip() or None,
            "indicaciones": indicaciones.strip() or None,
            "adendas": [],
        }
        return AtencionClinica(datos)
