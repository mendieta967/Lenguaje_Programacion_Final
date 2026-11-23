import unittest
from datetime import datetime

from modules.secretaria.turnos.reprogramacion import (
    aplicar_reprogramacion,
    filtrar_horarios_paciente,
    horario_se_solapa,
    obtener_turnos_reprogramables,
)


class ReprogramacionTests(unittest.TestCase):
    def test_solo_incluye_turnos_reservados_futuros(self):
        ahora = datetime(2026, 11, 23, 10, 0)
        turnos = [
            {
                "id": 1,
                "fecha": "24/11/2026",
                "hora": "09:00",
                "estado": "RESERVADO",
            },
            {
                "id": 2,
                "fecha": "23/11/2026",
                "hora": "09:00",
                "estado": "RESERVADO",
            },
            {
                "id": 3,
                "fecha": "24/11/2026",
                "hora": "09:00",
                "estado": "CANCELADO",
            },
        ]

        self.assertEqual(
            [turno["id"] for turno in obtener_turnos_reprogramables(turnos, ahora)],
            [1],
        )

    def test_detecta_solapamiento_entre_turnos_de_30_minutos(self):
        self.assertTrue(horario_se_solapa("09:00", "09:15"))
        self.assertFalse(horario_se_solapa("09:00", "09:30"))

    def test_filtra_horarios_que_se_solapan_con_turnos_del_paciente(self):
        turnos = [
            {
                "id": 1,
                "id_paciente": 10,
                "fecha": "24/11/2026",
                "hora": "09:00",
                "estado": "RESERVADO",
            },
            {
                "id": 2,
                "id_paciente": 10,
                "fecha": "24/11/2026",
                "hora": "09:30",
                "estado": "CANCELADO",
            },
            {
                "id": 3,
                "id_paciente": 20,
                "fecha": "24/11/2026",
                "hora": "10:00",
                "estado": "RESERVADO",
            },
            {
                "id": 4,
                "id_paciente": 10,
                "fecha": "24/11/2026",
                "hora": "10:00",
                "estado": "RESERVADO",
            },
        ]

        disponibles = filtrar_horarios_paciente(
            turnos,
            id_paciente=10,
            id_turno_actual=4,
            fecha="24/11/2026",
            horarios=["08:30", "09:00", "09:30", "10:00"],
        )

        self.assertEqual(disponibles, ["08:30", "09:30", "10:00"])

    def test_reprogramacion_preserva_datos_y_agrega_historial(self):
        turno = {
            "id": 7,
            "id_paciente": 10,
            "id_medico": 3,
            "fecha": "24/11/2026",
            "hora": "09:00",
            "motivo_consulta": "Control",
            "estado": "RESERVADO",
        }

        aplicar_reprogramacion(
            turno,
            id_medico=5,
            fecha="25/11/2026",
            hora="10:30",
            fecha_cambio="23/11/2026 10:00:00",
        )

        self.assertEqual(turno["id"], 7)
        self.assertEqual(turno["id_paciente"], 10)
        self.assertEqual(turno["motivo_consulta"], "Control")
        self.assertEqual(turno["estado"], "RESERVADO")
        self.assertEqual(turno["id_medico"], 5)
        self.assertEqual(turno["fecha"], "25/11/2026")
        self.assertEqual(turno["hora"], "10:30")
        self.assertEqual(
            turno["historial_reprogramaciones"][0],
            {
                "fecha_cambio": "23/11/2026 10:00:00",
                "id_medico_anterior": 3,
                "fecha_anterior": "24/11/2026",
                "hora_anterior": "09:00",
                "id_medico_nuevo": 5,
                "fecha_nueva": "25/11/2026",
                "hora_nueva": "10:30",
            },
        )


if __name__ == "__main__":
    unittest.main()
