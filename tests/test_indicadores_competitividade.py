"""Testes de identidades aritméticas em cenários fictícios, sem imitar dados reais."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
import pandas as pd

P=Path(__file__).resolve().parents[1]/"scripts/15_indicadores_competitividade.py"
s=importlib.util.spec_from_file_location("compet",P)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class TestesCompetitividade(unittest.TestCase):
    def test_competitividade_e_direcao(self):
        a=np.array([50.,90.,100.]); b=np.array([50.,10.,0.])
        c=1-np.abs(a-b)/(a+b)
        self.assertTrue(np.allclose(c,[1.0,0.2,0.0]))
        margem=(a-b)/(a+b)
        self.assertTrue(np.allclose(c,1-np.abs(margem)))

    def test_cobertura_top2_com_multiplos_candidatos(self):
        votos=np.array([40.,30.,20.,10.])
        dois=np.sort(votos)[-2:].sum()
        self.assertAlmostEqual(dois/votos.sum(),.7)
        self.assertAlmostEqual(1-abs(40-30)/dois,6/7)

    def test_identificacoes_distintas(self):
        self.assertEqual(set(m.FINALISTAS[2018]),{13,17})
        self.assertEqual(set(m.FINALISTAS[2022]),{13,22})
        self.assertNotEqual(m.FINALISTAS[2018][13],m.FINALISTAS[2022][13])
