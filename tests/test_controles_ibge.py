import importlib.util
from pathlib import Path
import unittest
import pandas as pd
spec=importlib.util.spec_from_file_location("ibge",Path(__file__).resolve().parents[1]/"scripts/12_coletar_controles_ibge.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class TestControlesIbge(unittest.TestCase):
    def test_separar_categorias_censo(self):
        d=pd.DataFrame([
            {"CD_MUNICIPIO_IBGE":"5300108","ano":2010,"D2C":"93","D4C":"0","D5C":"0","valor":100},
            {"CD_MUNICIPIO_IBGE":"5300108","ano":2010,"D2C":"93","D4C":"1","D5C":"0","valor":70},
            {"CD_MUNICIPIO_IBGE":"5300108","ano":2010,"D2C":"93","D4C":"0","D5C":"5","valor":52},
            {"CD_MUNICIPIO_IBGE":"5300108","ano":2010,"D2C":"93","D4C":"5","D5C":"1","valor":40}
        ])
        a=m.series(d,2010,93,"total",lambda x:x.D4C.eq("0")&x.D5C.eq("0"))
        b=m.series(d,2010,93,"urbana",lambda x:x.D4C.eq("1")&x.D5C.eq("0"))
        c=m.series(d,2010,93,"mulheres",lambda x:x.D4C.eq("0")&x.D5C.eq("5"))
        self.assertEqual(int(a.total.iloc[0]),100)
        self.assertEqual(int(b.urbana.iloc[0]),70)
        self.assertEqual(int(c.mulheres.iloc[0]),52)
    def test_duplicacoes_reprovadas(self):
        d=pd.DataFrame({"CD_MUNICIPIO_IBGE":["1000000","1000000"],"ano":[2010,2010],"D2C":["93","93"],"valor":[2,4]})
        with self.assertRaises(ValueError):m.series(d,2010,93,"total")
