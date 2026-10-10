"""Testes de controle com registros inteiramente fictícios."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def carregar(script, nome):
    spec = importlib.util.spec_from_file_location(nome, ROOT / "scripts" / script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

coleta = carregar("01_coletar_tse.py", "coleta_tse")
tratamento = carregar("02_tratar_votacao.py", "tratamento")
indicadores = carregar("03_indicadores.py", "indicadores")

class TesteFluxo(unittest.TestCase):
    def setUp(self):
        self.rows = pd.DataFrame([
            {"ANO_ELEICAO": "2022", "NR_TURNO": "1", "SG_UF": "DF", "CD_MUNICIPIO": "97012", "DS_CARGO": "PRESIDENTE", "NR_CANDIDATO": "11", "QT_VOTOS_NOMINAIS": "6"},
            {"ANO_ELEICAO": "2022", "NR_TURNO": "1", "SG_UF": "DF", "CD_MUNICIPIO": "97012", "DS_CARGO": "PRESIDENTE", "NR_CANDIDATO": "22", "QT_VOTOS_NOMINAIS": "4"},
            {"ANO_ELEICAO": "2022", "NR_TURNO": "1", "SG_UF": "DF", "CD_MUNICIPIO": "97012", "DS_CARGO": "PRESIDENTE", "NR_CANDIDATO": "11", "QT_VOTOS_NOMINAIS": "3"},
            {"ANO_ELEICAO": "2022", "NR_TURNO": "1", "SG_UF": "DF", "CD_MUNICIPIO": "97012", "DS_CARGO": "SENADOR", "NR_CANDIDATO": "11", "QT_VOTOS_NOMINAIS": "99"},
        ])

    def test_filtra_presidente_agrega_zonas(self):
        t = tratamento.consolidar([self.rows.iloc[:2], self.rows.iloc[2:]], 2022)
        self.assertEqual(len(t), 2)
        self.assertEqual(int(t.QT_VOTOS_NOMINAIS.sum()), 13)
        h = indicadores.calcular(t)
        self.assertEqual(len(h), 1)
        self.assertEqual(int(h.total_votos_nominais.iloc[0]), 13)
        self.assertAlmostEqual(h.hhi.iloc[0], (9 / 13)**2 + (4 / 13)**2)

    def test_ano_divergente_bloqueado(self):
        with self.assertRaises(ValueError):
            tratamento.consolidar([self.rows], 2018)

    def test_negativo_bloqueado(self):
        df = self.rows.copy()
        df.loc[0, "QT_VOTOS_NOMINAIS"] = "-1"
        with self.assertRaises(ValueError):
            tratamento.consolidar([df], 2022)

    def test_zip_csv_latin1(self):
        with tempfile.TemporaryDirectory() as d:
            z = Path(d) / "oficial_teste.zip"
            with zipfile.ZipFile(z, "w") as archive:
                archive.writestr("votacao_candidato_munzona_2022.csv", self.rows.to_csv(index=False, sep=";").encode("latin1"))
            t = tratamento.consolidar(tratamento.ler_chunks(z, chunksize=2), 2022)
            self.assertEqual(int(t.QT_VOTOS_NOMINAIS.sum()), 13)

    def test_dominios_oficiais(self):
        self.assertTrue(coleta.validar_url_tse("https://cdn.tse.jus.br/a.zip"))
        self.assertFalse(coleta.validar_url_tse("https://tse.jus.br.exemplo.com/a.zip"))
        self.assertFalse(coleta.validar_url_tse("http://cdn.tse.jus.br/a.zip"))

    def test_id_repetido_bloqueado(self):
        t = tratamento.consolidar([self.rows], 2022)
        with self.assertRaises(ValueError):
            indicadores.calcular(pd.concat([t, t], ignore_index=True))

if __name__ == "__main__":
    unittest.main()
