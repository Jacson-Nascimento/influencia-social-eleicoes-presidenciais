import importlib.util,unittest,numpy as np
from pathlib import Path
spec=importlib.util.spec_from_file_location("n",Path(__file__).resolve().parents[1]/"scripts/20_inferencia_espacial_validacao.py")
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
class TesteInferencia(unittest.TestCase):
    def test_bootstrap_reprodutivel(self):
        a=np.array([[1,4,2],[1,2,3],[1,3,1]],dtype=float)
        x=n.bootstrap_estados(a,999,33)
        self.assertEqual(x,n.bootstrap_estados(a,999,33))
        self.assertEqual(x["n_ufs"],3)
    def test_kernel_simetria(self):
        xyz=np.array([[1.,0,0],[0.99999,0.004472,0],[0.,1.,0.]])
        K,pares=n.kernel_conley(xyz,100)
        self.assertTrue(np.allclose(K.toarray(),K.toarray().T))
        self.assertTrue(np.allclose(K.diagonal(),1))
