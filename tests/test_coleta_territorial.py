"""Testes estruturais para o ZIP nacional do TSE, sem dados eleitorais inventados como observações."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

tratamento = load("05_consolidar_presidente_tse.py", "consolidar_zip")
auditoria = load("06_auditar_totalizacao_municipal.py", "auditoria_munzona")


class TestarColetaTerritorial(unittest.TestCase):
    def test_escolha_brasil_sem_duplicar_uf(self):
        nomes = ["votacao_candidato_munzona_2022_AC.csv",
                 "votacao_candidato_munzona_2022_BRASIL.csv",
                 "votacao_candidato_munzona_2022_SP.csv"]
        self.assertEqual(tratamento.escolher_csv(nomes, 2022), nomes[1])

    def test_brasil_2018(self):
        nomes = ["votacao_candidato_munzona_2018_BR.csv",
                 "votacao_candidato_munzona_2018_MG.csv"]
        self.assertEqual(tratamento.escolher_csv(nomes, 2018), nomes[0])

    def test_sem_arquivo_nacional_e_ambiguo(self):
        with self.assertRaises(ValueError):
            tratamento.escolher_csv(["votacao_candidato_munzona_2018_AC.csv",
                                    "votacao_candidato_munzona_2018_SP.csv"], 2018)

    def test_nacional_ficticio_agrupado(self):
        with tempfile.TemporaryDirectory() as tmp:
            zpath = Path(tmp) / "ficticio.zip"
            header = ["ANO_ELEICAO", "NR_TURNO", "SG_UF", "CD_MUNICIPIO",
                      "DS_CARGO", "NR_CANDIDATO", "QT_VOTOS_NOMINAIS"]
            fake = pd.DataFrame([
                [2022, 1, "DF", 97012, "PRESIDENTE", 13, 5],
                [2022, 1, "DF", 97012, "PRESIDENTE", 13, 8],
                [2022, 1, "DF", 97012, "PRESIDENTE", 22, 7],
                [2022, 1, "DF", 97012, "GOVERNADOR", 5, 999],
                [2022, 2, "ZZ", 99999, "PRESIDENTE", 13, 3],
            ], columns=header)
            with zipfile.ZipFile(zpath, "w") as z:
                z.writestr("votacao_candidato_munzona_2022_BRASIL.csv",
                           fake.to_csv(sep=";", index=False).encode("latin1"))
                z.writestr("votacao_candidato_munzona_2022_DF.csv",
                           fake.to_csv(sep=";", index=False).encode("latin1"))
            df, rel = tratamento.consolidar_zip(zpath, 2022, chunksize=2)
            self.assertEqual(int(df["QT_VOTOS_NOMINAIS"].sum()), 23)
            self.assertEqual(rel["linhas_presidenciais_lidas"], 4)
            self.assertEqual(len(df), 3)

    def test_conciliacao_erro_impede_aprovacao(self):
        dados = pd.DataFrame([
            [2022, 1, "DF", 97012, 13, 10],
            [2022, 1, "DF", 97012, 22, 20],
            [2022, 2, "DF", 97012, 13, 11],
            [2022, 2, "DF", 97012, 22, 19],
        ], columns=["ANO_ELEICAO","NR_TURNO","SG_UF","CD_MUNICIPIO",
                    "NR_CANDIDATO","QT_VOTOS_NOMINAIS"])
        controle = pd.read_csv(ROOT / "data/controles/totalizacao_2018_2022_fontes_tse.csv")
        resultado = auditoria.auditar(dados, controle, 2022)
        self.assertFalse(resultado["aprovado"])
        self.assertNotEqual(resultado["turnos"][0]["residuo_total"], 0)


if __name__ == "__main__":
    unittest.main()
