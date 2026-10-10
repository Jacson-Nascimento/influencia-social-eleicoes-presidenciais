import importlib.util,unittest
from pathlib import Path
import pandas as pd
spec=importlib.util.spec_from_file_location("aud",Path(__file__).resolve().parents[1]/"scripts/19_auditoria_presidencial_2018_2022.py")
aud=importlib.util.module_from_spec(spec);spec.loader.exec_module(aud)
class TesteAuditoriaEleitoral(unittest.TestCase):
    def test_residuo_candidaturas(self):
        self.assertEqual(20+46+10,76)
    def test_percentual_minimo(self):
        self.assertLess(76/107050673*100,0.001)
