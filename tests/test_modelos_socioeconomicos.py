import importlib.util
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

spec=importlib.util.spec_from_file_location("controls",Path(__file__).resolve().parents[1]/"scripts/13_modelos_controles_socioeconomicos.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TestModelosSocioeconomicos(unittest.TestCase):
    def test_ols_exato(self):
        X=np.c_[np.ones(50),np.arange(50,dtype=float)]
        y=2+0.3*np.arange(50)
        out=mod.fit(X,y)
        self.assertAlmostEqual(out["r2"],1,places=10)
        self.assertAlmostEqual(out["rmse_treino"],0,places=10)
    def test_matriz_uf_com_dummies(self):
        d=pd.DataFrame({
            "SG_UF":["AC","AC","SP","SP","BA","BA"],
            "log_pop":[10,11,12,13,14,15],
            "log_pibpc_proxy":[8,8.3,9,9.6,10,10.5],
            "urbanizacao_2010":[.1,.2,.3,.4,.5,.6],
            "fracao_feminina_2010":[.40,.41,.42,.43,.44,.45]})
        x0,x1,mu,sd=mod.matrizes(d)
        self.assertEqual(x0.shape,(6,3))
        self.assertEqual(x1.shape,(6,7))
        self.assertTrue(np.isfinite(x1).all())
    def test_particao_exclui_uf(self):
        x=[]
        for idx,uf in enumerate(["AC","AL","AP","BA","CE","SP"]):
            for j in range(2):
                x.append({"SG_UF":uf,"hhi":.3+.01*idx+.002*j,
                   "log_pop":8+.1*idx+.03*j,
                   "log_pibpc_proxy":9+.12*idx+.01*j,
                   "urbanizacao_2010":.1+.1*idx+.01*j,
                   "fracao_feminina_2010":.44+.005*idx+.004*j})
        out=mod.validacao_externa_uf(pd.DataFrame(x))
        self.assertEqual(out["n_folds"],5)
        self.assertEqual(sum(i["n_teste"] for i in out["folds"]),12)
        self.assertTrue(np.isfinite(out["rmse_controles"]))
