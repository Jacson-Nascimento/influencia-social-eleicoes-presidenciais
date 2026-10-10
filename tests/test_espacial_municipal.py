import importlib.util, unittest
from pathlib import Path
import numpy as np
spec=importlib.util.spec_from_file_location("mod",Path(__file__).resolve().parents[1]/"scripts/10_espacial_municipal.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestesMoranMunicipal(unittest.TestCase):
    def test_holm(self):
        self.assertTrue(np.allclose(m.holm([.03,.01,.20,.5]),[.09,.04,.40,.5]))
    def test_sinal_moran(self):
        n=np.array([[1],[0],[3],[2]],dtype=int)
        self.assertAlmostEqual(m.moran([1,1,-1,-1],n),1)
        self.assertAlmostEqual(m.moran([1,-1,1,-1],n),-1)
    def test_permutacao_estavel(self):
        n=np.array([[1,2],[0,2],[0,1],[4,5],[3,5],[3,4]])
        x=np.array([1.,2.,3.,4.,5.,6.]);uf=np.array(["AC"]*3+["SP"]*3)
        self.assertEqual(m.permutar(x,n,uf,99,17,True),m.permutar(x,n,uf,99,17,True))
