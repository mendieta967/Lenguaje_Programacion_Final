import unittest
from datetime import datetime

from modules.medico.consultas import (
    agregar_adenda_a_atencion,
    obtener_atenciones_medico,
    obtener_historia_clinica,
    obtener_siguiente_id_atencion,
    obtener_turnos_atendibles,
    crear_atencion,
    vincular_atencion_a_turno,
)


class ConsultasMedicasTests(unittest.TestCase):
    def test_solo_muestra_turnos_propios_reservados_cuyo_horario_llego(self):
        ahora = datetime(2026, 11, 23, 10, 0)
        turnos = [
            {
                "id": 1,
                "id_medico": 3,
                "fecha": "23/11/2026",
                "hora": "09:30",
                "estado": "RESERVADO",
            },
            {
                "id": 2,
                "id_medico": 3,
                "fecha": "23/11/2026",
                "hora": "10:30",
                "estado": "RESERVADO",
            },
            {
                "id": 3,
                "id_medico": 5,
                "fecha": "23/11/2026",
                "hora": "09:30",
                "estado": "RESERVADO",
            },
            {
                "id": 4,
                "id_medico": 3,
                "fecha": "23/11/2026",
                "hora": "09:30",
                "estado": "ATENDIDO",
            },
        ]

        self.assertEqual(
            [
                turno["id"]
                for turno in obtener_turnos_atendibles(turnos, 3, ahora)
            ],
            [1],
        )

    def test_registra_atencion_y_preserva_datos_del_turno(self):
        turno = {
            "id": 12,
            "id_paciente": 7,
            "id_medico": 3,
            "fecha": "23/11/2026",
            "hora": "09:30",
            "motivo_consulta": "Control",
            "estado": "RESERVADO",
        }

        atencion = crear_atencion(
            1,
            turno,
            id_medico=3,
            observaciones="Paciente estable.",
            diagnostico="",
            indicaciones="Hidratación.",
            momento_atencion=datetime(2026, 11, 23, 10, 0),
        )
        vincular_atencion_a_turno(
            turno,
            atencion,
            id_medico=3,
            ahora=datetime(2026, 11, 23, 10, 0),
        )

        self.assertEqual(turno["estado"], "ATENDIDO")
        self.assertEqual(turno["id_paciente"], 7)
        self.assertEqual(turno["motivo_consulta"], "Control")
        self.assertEqual(turno["id_atencion"], 1)
        self.assertNotIn("atencion", turno)
        self.assertIsNone(atencion["diagnostico"])
        self.assertEqual(atencion["observaciones"], "Paciente estable.")

    def test_atencion_no_puede_registrarse_para_otro_medico(self):
        turno = {
            "id_medico": 5,
            "fecha": "23/11/2026",
            "hora": "09:30",
            "estado": "RESERVADO",
        }

        with self.assertRaises(ValueError):
            crear_atencion(
                1,
                turno,
                id_medico=3,
                observaciones="Observación.",
                diagnostico="",
                indicaciones="",
                momento_atencion=datetime(2026, 11, 23, 10, 0),
            )

    def test_historia_incluye_atenciones_de_todos_los_medicos(self):
        atenciones = [
            {
                "id": 1,
                "id_medico": 3,
                "id_paciente": 7,
                "fecha_atencion": "23/11/2026 10:00:00",
                "observaciones": "Primera atención.",
            },
            {
                "id": 2,
                "id_medico": 5,
                "id_paciente": 7,
                "fecha_atencion": "24/11/2026 10:00:00",
                "observaciones": "Segunda atención.",
            },
            {
                "id": 3,
                "id_medico": 3,
                "id_paciente": 8,
                "fecha_atencion": "23/11/2026 10:00:00",
                "observaciones": "Otro paciente.",
            },
        ]

        self.assertEqual(
            obtener_historia_clinica(atenciones, 7),
            atenciones[:2],
        )

    def test_siguiente_id_se_calcula_con_ids_existentes_o_lista_vacia(self):
        self.assertEqual(
            obtener_siguiente_id_atencion([{"id": 2}, {"id": 6}]),
            7,
        )
        self.assertEqual(obtener_siguiente_id_atencion([]), 1)

    def test_edicion_sigue_limitada_al_medico_autor(self):
        atenciones = [
            {
                "id": 1,
                "id_medico": 3,
                "id_paciente": 7,
                "fecha_atencion": "23/11/2026 10:00:00",
                "observaciones": "Nota.",
            },
            {
                "id": 2,
                "id_medico": 5,
                "id_paciente": 7,
                "fecha_atencion": "24/11/2026 10:00:00",
                "observaciones": "Otra nota.",
            },
        ]

        self.assertEqual(
            obtener_atenciones_medico(atenciones, 3, 7),
            [atenciones[0]],
        )

    def test_adenda_no_sobrescribe_observaciones_originales(self):
        atencion = {
            "id": 1,
            "id_medico": 3,
            "observaciones": "Nota original.",
            "adendas": [],
        }

        agregar_adenda_a_atencion(
            atencion,
            3,
            "Aclaración.",
            datetime(2026, 11, 23, 11, 0),
        )

        self.assertEqual(atencion["observaciones"], "Nota original.")
        self.assertEqual(atencion["adendas"][0]["texto"], "Aclaración.")


if __name__ == "__main__":
    unittest.main()
