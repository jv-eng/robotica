#This script implements the fuzzy logic
#This script also controls the project

import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class FuzzyController:
    """
    Modelo de lógica borrosa
    Tenemos 5 etiquetas, lo que implica 8 valores
    """
 
    def __init__(self, fun):
        self.data = fun
        self.paso = 0.1
        
        #configurar modelo
        self.__crear_trapecios()
        self.__configure_model()

    #crear los rangos de los trapecios
    def __crear_trapecios(self):
        self.trapecios = [
            [0, 0, self.data[0], self.data[1]],
            [self.data[0], self.data[1], self.data[2], self.data[3]],
            [self.data[2], self.data[3], self.data[4], self.data[5]],
            [self.data[4], self.data[5], self.data[6], self.data[7]],
            [self.data[6], self.data[7], 256, 256],
        ]

    #configurar modelo y crear el sistema para simulación
    def __configure_model(self):
        #crear funciones
        self.err_actual = ctrl.Antecedent(np.arange(0, 256, self.paso), 'err_actual')
        self.err_pasado = ctrl.Antecedent(np.arange(0, 256, self.paso), 'err_pasado')
        self.res = ctrl.Consequent(np.arange(0, 256, self.paso), 'resultado')

        #crear universos
        self.err_actual['actual muy izq'] = fuzz.trapmf(self.err_actual.universe, self.trapecios[0])
        self.err_actual['actual izq'] = fuzz.trapmf(self.err_actual.universe, self.trapecios[1])
        self.err_actual['actual centrado'] = fuzz.trapmf(self.err_actual.universe, self.trapecios[2])
        self.err_actual['actual dcha'] = fuzz.trapmf(self.err_actual.universe, self.trapecios[3])
        self.err_actual['actual muy dcha'] = fuzz.trapmf(self.err_actual.universe, self.trapecios[4])

        self.err_pasado['pasado muy izq'] = fuzz.trapmf(self.err_pasado.universe, self.trapecios[0])
        self.err_pasado['pasado izq'] = fuzz.trapmf(self.err_pasado.universe, self.trapecios[1])
        self.err_pasado['pasado centrado'] = fuzz.trapmf(self.err_pasado.universe, self.trapecios[2])
        self.err_pasado['pasado dcha'] = fuzz.trapmf(self.err_pasado.universe, self.trapecios[3])
        self.err_pasado['pasado muy dcha'] = fuzz.trapmf(self.err_pasado.universe, self.trapecios[4])

        self.res['correccion muy izq'] = fuzz.trapmf(self.res.universe, self.trapecios[0])
        self.res['correccion izq'] = fuzz.trapmf(self.res.universe, self.trapecios[1])
        self.res['correccion centrado'] = fuzz.trapmf(self.res.universe, self.trapecios[2])
        self.res['correccion dcha'] = fuzz.trapmf(self.res.universe, self.trapecios[3])
        self.res['correccion muy dcha'] = fuzz.trapmf(self.res.universe, self.trapecios[4])

        #crear reglas
        regla1 = ctrl.Rule(self.err_actual['actual muy izq'] & self.err_pasado['pasado muy izq'], self.res['correccion muy dcha'])
        regla2 = ctrl.Rule(self.err_actual['actual muy izq'] & self.err_pasado['pasado izq'], self.res['correccion muy dcha'])
        regla3 = ctrl.Rule(self.err_actual['actual muy izq'] & self.err_pasado['pasado centrado'], self.res['correccion muy dcha'])
        regla4 = ctrl.Rule(self.err_actual['actual muy izq'] & self.err_pasado['pasado dcha'], self.res['correccion muy dcha'])
        regla5 = ctrl.Rule(self.err_actual['actual muy izq'] & self.err_pasado['pasado muy dcha'], self.res['correccion muy dcha'])
        regla6 = ctrl.Rule(self.err_actual['actual izq'] & self.err_pasado['pasado muy izq'], self.res['correccion muy dcha'])
        regla7 = ctrl.Rule(self.err_actual['actual izq'] & self.err_pasado['pasado izq'], self.res['correccion dcha'])
        regla8 = ctrl.Rule(self.err_actual['actual izq'] & self.err_pasado['pasado centrado'], self.res['correccion dcha'])
        regla9 = ctrl.Rule(self.err_actual['actual izq'] & self.err_pasado['pasado dcha'], self.res['correccion dcha'])
        regla10 = ctrl.Rule(self.err_actual['actual izq'] & self.err_pasado['pasado muy dcha'], self.res['correccion dcha'])
        regla11 = ctrl.Rule(self.err_actual['actual centrado'] & self.err_pasado['pasado muy izq'], self.res['correccion centrado'])
        regla12 = ctrl.Rule(self.err_actual['actual centrado'] & self.err_pasado['pasado izq'], self.res['correccion centrado'])
        regla13 = ctrl.Rule(self.err_actual['actual centrado'] & self.err_pasado['pasado centrado'], self.res['correccion centrado'])
        regla14 = ctrl.Rule(self.err_actual['actual centrado'] & self.err_pasado['pasado dcha'], self.res['correccion centrado'])
        regla15 = ctrl.Rule(self.err_actual['actual centrado'] & self.err_pasado['pasado muy dcha'], self.res['correccion centrado'])
        regla16 = ctrl.Rule(self.err_actual['actual dcha'] & self.err_pasado['pasado muy izq'], self.res['correccion izq'])
        regla17 = ctrl.Rule(self.err_actual['actual dcha'] & self.err_pasado['pasado izq'], self.res['correccion izq'])
        regla18 = ctrl.Rule(self.err_actual['actual dcha'] & self.err_pasado['pasado centrado'], self.res['correccion izq'])
        regla19 = ctrl.Rule(self.err_actual['actual dcha'] & self.err_pasado['pasado dcha'], self.res['correccion izq'])
        regla20 = ctrl.Rule(self.err_actual['actual dcha'] & self.err_pasado['pasado muy dcha'], self.res['correccion muy izq'])
        regla21 = ctrl.Rule(self.err_actual['actual muy dcha'] & self.err_pasado['pasado muy izq'], self.res['correccion muy izq'])
        regla22 = ctrl.Rule(self.err_actual['actual muy dcha'] & self.err_pasado['pasado izq'], self.res['correccion muy izq'])
        regla23 = ctrl.Rule(self.err_actual['actual muy dcha'] & self.err_pasado['pasado centrado'], self.res['correccion muy izq'])
        regla24 = ctrl.Rule(self.err_actual['actual muy dcha'] & self.err_pasado['pasado dcha'], self.res['correccion muy izq'])
        regla25 = ctrl.Rule(self.err_actual['actual muy dcha'] & self.err_pasado['pasado muy dcha'], self.res['correccion muy izq'])


        #crear sistema
        sistema = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, 
                                      regla7, regla8, regla9, regla10, regla11, regla12, regla13, 
                                      regla14, regla15, regla16, regla17, regla18, regla19, regla20, 
                                      regla21, regla22, regla23, regla24, regla25])
        self.simulation = ctrl.ControlSystemSimulation(sistema)


    """
    Realiza la simulación
    Devuelve la corrección de los motores (None si no hay corrección)
    """
    def sim(self, error_actual, error_pasado):
        #simulacion
        self.simulation.input['err_actual'] = error_actual
        self.simulation.input['err_pasado'] = error_pasado
        self.simulation.compute()
        res = self.simulation.output['resultado']
        #print("\nborroso\n" + "err_actual: " + str(error_actual) + "\nerr_pasado: " + str(error_pasado) + "\nres: " + str(res))

        #sacar etiqueta
        if res <= self.data[1]:
            self.etiqueta = 'correccion muy izq'
            return [+0.35, -0.2]
        elif res <= self.data[3]:
            self.etiqueta = 'correccion izq'
            return [+0.15, 0.0]
        elif res <= self.data[5]:
            self.etiqueta = 'correccion centrado'
            return None
        elif res <= self.data[7]:
            self.etiqueta = 'correccion dcha'
            return [0.0, +0.15]
        else:
            self.etiqueta = 'correccion muy dcha'
            return [-0.2, +0.35]

    #ver que etiqueta es
    def get_etiqueta(self):
        return self.etiqueta


    def plot(self):
        plt.figure(figsize=(8, 6))

        #error actual
        plt.subplot(3, 1, 1)
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.err_actual.universe, [0, 0, self.data[0], self.data[1]]), 'b', linewidth=1.5, label='muy izq')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.err_actual.universe, [self.data[0], self.data[1], self.data[2], self.data[3]]), 'g', linewidth=1.5, label='izq')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.err_actual.universe, [self.data[2], self.data[3], self.data[4], self.data[5]]), 'k', linewidth=1.5, label='centrado')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.err_actual.universe, [self.data[4], self.data[5], self.data[6], self.data[7]]), 'r', linewidth=1.5, label='dcha')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.err_actual.universe, [self.data[6], self.data[7], 256, 256]), 'm', linewidth=1.5, label='muy dcha')
        plt.title('Error actual')
        plt.xlabel('Valor')
        plt.ylabel('Membresía')
        plt.legend()

        #error pasado
        plt.subplot(3, 1, 2)
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.err_pasado.universe, [0, 0, self.data[0], self.data[1]]), 'b', linewidth=1.5, label='muy izq')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.err_pasado.universe, [self.data[0], self.data[1], self.data[2], self.data[3]]), 'g', linewidth=1.5, label='izq')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.err_pasado.universe, [self.data[2], self.data[3], self.data[4], self.data[5]]), 'k', linewidth=1.5, label='centrado')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.err_pasado.universe, [self.data[4], self.data[5], self.data[6], self.data[7]]), 'r', linewidth=1.5, label='dcha')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.err_pasado.universe, [self.data[6], self.data[7], 256, 256]), 'm', linewidth=1.5, label='muy dcha')
        plt.title('Error pasado')
        plt.xlabel('Valor')
        plt.ylabel('Membresía')
        plt.legend()

        #resultado
        plt.subplot(3, 1, 3)
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.res.universe, [0, 0, self.data[0], self.data[1]]), 'b', linewidth=1.5, label='muy izq')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.res.universe, [self.data[0], self.data[1], self.data[2], self.data[3]]), 'g', linewidth=1.5, label='izq')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.res.universe, [self.data[2], self.data[3], self.data[4], self.data[5]]), 'k', linewidth=1.5, label='centrado')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.res.universe, [self.data[4], self.data[5], self.data[6], self.data[7]]), 'r', linewidth=1.5, label='dcha')
        plt.plot(np.arange(0, 256, self.paso), fuzz.trapmf(self.res.universe, [self.data[6], self.data[7], 256, 256]), 'm', linewidth=1.5, label='muy dcha')
        plt.title('Corrección')
        plt.xlabel('Valor')
        plt.ylabel('Membresía')
        plt.legend()

        #mostrar gráfica
        plt.tight_layout()
        plt.show()