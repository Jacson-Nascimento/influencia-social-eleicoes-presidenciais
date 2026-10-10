"""Testes das capitais oficiais, amostras e pesos populacionais."""
import importlib.util, json, unittest
from pathlib import Path
import pandas as pd
spec=importlib.util.spec_from_file_location("rob",Path(__file__).resolve().parents[1]/"scripts/18_robustez_demografica_capitais.py")
rob=importlib.util.module_from_spec(spec);spec.loader.exec_module(rob)
class TestRobustez(unittest.TestCase):
    def test_capitais_tem_27(self):
        self.assertEqual(len(rob.CAPITAIS),27)
        self.assertEqual(len(set(rob.CAPITAIS)),27)
        self.assertEqual(rob.norm("São Luís"),"SAO LUIS")
        self.assertEqual(rob.norm("Goiânia"),"GOIANIA")
    def test_catalogo_incompleto_rejeitado(self):
        with self.assertRaises(ValueError):rob.capitais_do_ibge(json.dumps([]).encode())
    def test_capital_nao_pertence_duas_ufs(self):
        self.assertNotEqual(rob.CAPITAIS["RJ"],rob.CAPITAIS["SP"])
