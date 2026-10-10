"""Testes para reconciliação contábil dos totais históricos do TSE."""
import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('agregados', ROOT / 'scripts' / '04_conferir_agregados_historicos.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
CSV = ROOT / 'data' / 'controles' / 'totalizacao_presidencial_2022_tse.csv'

class TestAgregadosHistoricos(unittest.TestCase):
    def test_controles_oficiais_conciliam(self):
        resultado = mod.avaliar(mod.carregar_controles(CSV))
        self.assertTrue(resultado['identidade_aritmetica_verificada'])
        self.assertEqual(resultado['diferenca_votos_validos'], 322634)
        self.assertEqual(resultado['diferencas_por_candidatura']['13'], 3086495)
        self.assertEqual(resultado['diferencas_por_candidatura']['22'], 7134009)

    def test_inconsistencia_bloqueada(self):
        with CSV.open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream))
        rows[0]['QT_VOTOS_NOMINAIS'] = '57259505'
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'alterado.csv'
            with p.open('w', encoding='utf-8', newline='') as stream:
                out = csv.DictWriter(stream, fieldnames=rows[0].keys())
                out.writeheader()
                out.writerows(rows)
            with self.assertRaises(ValueError):
                mod.carregar_controles(p)

    def test_duplicidade_bloqueada(self):
        with CSV.open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream))
        rows.append(rows[0].copy())
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'duplicado.csv'
            with p.open('w', encoding='utf-8', newline='') as stream:
                out = csv.DictWriter(stream, fieldnames=rows[0].keys())
                out.writeheader()
                out.writerows(rows)
            with self.assertRaises(ValueError):
                mod.carregar_controles(p)

if __name__ == '__main__':
    unittest.main()
