import importlib.util
import unittest
from pathlib import Path
import numpy as np
sp=importlib.util.spec_from_file_location("w",Path(__file__).resolve().parents[1]/"scripts/17_sensibilidade_ponderacao_eleitoral.py")
w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
class TestePonderacao(unittest.TestCase):
    def test_wls_identifica_pesos(self):
        X=np.c_[np.ones(4),[0.,1.,2.,3.]]
        y=np.array([1.,3.,5.,10.])
        u=w.wls(X,y,np.ones(4))
        a=w.wls(X,y,np.array([1.,1.,1.,100.]))
        self.assertNotAlmostEqual(float(u["beta"][1]),float(a["beta"][1]),places=4)
        self.assertTrue(np.isfinite(a["r2_ponderado"]))
    def test_peso_zero_rejeitado(self):
        with self.assertRaises(ValueError):
            w.wls(np.c_[np.ones(2),[0.,1.]],[0.,1.],[0.,1.])
