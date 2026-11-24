import tempfile
import unittest
import os
from datetime import datetime

from core.repositorio_json import RepositorioJson
from modules.modelos import (
    AtencionClinica,
    FabricaAtencion,
    Paciente,
    UsuarioMedico,
    UsuarioSecretaria,
)


class ModelosTests(unittest.TestCase):
    def test_usuario_medico_y_secretaria_heredan_de_usuario(self):
        medico = UsuarioMedico(1, "Ana", "Rojas", "12345678", "ana", "hash", "Pediatría")
        secretaria = UsuarioSecretaria(2, "Luis", "Paz", "87654321", "luis", "hash", "SECRETARIA")

        self.assertEqual(medico.rol, "MEDICO")
        self.assertEqual(medico.a_diccionario()["especialidad"], "Pediatría")
        self.assertEqual(secretaria.rol, "SECRETARIA")

    def test_fabrica_crea_atencion_con_el_turno(self):
        turno = {
            "id": 4,
            "id_paciente": 8,
            "motivo_consulta": "Control",
        }
        atencion = FabricaAtencion.crear(
            2,
            turno,
            3,
            "Paciente estable.",
            "",
            "Hidratación.",
            datetime(2026, 11, 23, 10, 0),
        )

        datos = atencion.a_diccionario()
        self.assertIsInstance(atencion, AtencionClinica)
        self.assertEqual(datos["id_turno"], 4)
        self.assertEqual(datos["motivo_consulta"], "Control")
        self.assertEqual(datos["diagnostico"], None)

    def test_atencion_y_paciente_serializan_sin_cambiar_json(self):
        paciente = Paciente(8, "Eva", "Sol", "11111111", "999999999", "Calle 1", "01/01/2000")
        atencion = AtencionClinica.desde_diccionario({
            "id": 1,
            "id_paciente": 8,
            "id_medico": 3,
            "observaciones": "Nota.",
            "adendas": [],
        })

        self.assertEqual(paciente.a_diccionario()["dni"], "11111111")
        self.assertEqual(atencion.a_diccionario()["observaciones"], "Nota.")

    def test_repositorio_json_aplica_singleton(self):
        primer_repositorio = RepositorioJson()
        segundo_repositorio = RepositorioJson()
        self.assertIs(primer_repositorio, segundo_repositorio)

        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "datos.json")
            primer_repositorio.guardar(ruta, [{"id": 1}])
            self.assertEqual(segundo_repositorio.cargar(ruta), [{"id": 1}])


if __name__ == "__main__":
    unittest.main()
