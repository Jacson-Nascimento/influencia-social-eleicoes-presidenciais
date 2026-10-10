"""Testes mecânicos do novo desenho e das identidades de competitividade."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

P=Path(__file__).resolve().parents[1]/"scripts/16_modelos_competitividade.py"
spec=importlib.util.spec_from_file_location("modelos_comp",P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class TesteRegressaoCompetitividade(unittest.TestCase):
    def test_regressor_amostra_uf(self):
        import pandas as pd
        uf=pd.Series(["AC","AC","SP","SP","BA","BA","RJ","RJ","GO","GO"])
        x=np.c_[np.arange(10),np.arange(10)**2]
        y=np.linspace(.15,.85,10)
        reg=m.regress(x,y,uf)
        self.assertTrue(np.isfinite(reg["r2"]))
        self.assertLessEqual(reg["r2"],1+1e-10)
    def test_identidades(self):
        margem=np.array([-.8,-.25,0,.25,.8])
        c=1-np.abs(margem)
        self.assertTrue((c>=0).all())
        self.assertEqual(float(c[2]),1.)
        self.assertTrue(np.array_equal(c[0:2],c[4:2:-1]))
