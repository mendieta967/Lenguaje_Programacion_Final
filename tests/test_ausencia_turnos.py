import unittest
from datetime import datetime

from modules.secretaria.turnos.estado import (
    aplicar_estado_ausente,
    obtener_turnos_para_marcar_ausente,
)


class AusenciaTurnosTests(unittest.TestCase):
    def test_solo_incluye_reservas_cuyo_bloque_ya_termino(self):
        ahora = datetime(2026, 11, 23, 10, 0)
        turnos = [
            {
                "id": 1,
                "fecha": "23/11/2026",
                "hora": "09:30",
                "estado": "RESERVADO",
            },
            {
                "id": 2,
                "fecha": "23/11/2026",
                "hora": "09:31",
                "estado": "RESERVADO",
            },
            {
                "id": 3,
                "fecha": "23/11/2026",
                "hora": "09:00",
                "estado": "CANCELADO",
            },
            {
                "id": 4,
                "fecha": "23/11/2026",
                "hora": "09:00",
                "estado": "ATENDIDO",
            },
            {
                "id": 5,
                "fecha": "23/11/2026",
                "hora": "09:00",
                "estado": "RESERVADO",
                "atencion": {"observaciones": "Atención registrada"},
            },
            {
                "id": 6,
                "fecha": "23/11/2026",
                "hora": "09:00",
                "estado": "RESERVADO",
                "id_atencion": 2,
            },
        ]

        self.assertEqual(
            [
                turno["id"]
                for turno in obtener_turnos_para_marcar_ausente(turnos, ahora)
            ],
            [1],
        )

    def test_marcar_ausente_no_crea_atencion(self):
        turno = {
            "id": 7,
            "fecha": "23/11/2026",
            "hora": "09:00",
            "estado": "RESERVADO",
        }

        aplicar_estado_ausente(turno, datetime(2026, 11, 23, 10, 0))

        self.assertEqual(turno["estado"], "AUSENTE")
        self.assertNotIn("atencion", turno)

    def test_no_permite_marcar_antes_de_terminar_el_bloque(self):
        turno = {
            "id": 7,
            "fecha": "23/11/2026",
            "hora": "09:30",
            "estado": "RESERVADO",
        }

        with self.assertRaises(ValueError):
            aplicar_estado_ausente(turno, datetime(2026, 11, 23, 9, 59))


if __name__ == "__main__":
    unittest.main()
