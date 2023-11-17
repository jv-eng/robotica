import unittest
from proy.fuzzy_controller import FuzzyController 

class TestFuzzyMethods(unittest.TestCase):
    var = [38,64,102,115,141,154,192,218]

    def test_1(self):
        f = FuzzyController(self.var)
        f.sim(210, 200)
        self.assertEqual(f.get_etiqueta(), 'muy izq')

    def test_2(self):
        f = FuzzyController(self.var)
        f.sim(150, 100)
        self.assertEqual(f.get_etiqueta(), 'izq')

    def test_3(self):
        f = FuzzyController(self.var)
        f.sim(125,120)
        self.assertEqual(f.get_etiqueta(), 'centrado')
    
    def test_4(self):
        f = FuzzyController(self.varo)
        f.sim(65, 50)
        self.assertEqual(f.get_etiqueta(), 'dcha')

    def test_5(self):
        f = FuzzyController(self.var)
        f.sim(20, 10)
        self.assertEqual(f.get_etiqueta(), 'muy dcha')

if __name__ == '__main__':
    unittest.main()
