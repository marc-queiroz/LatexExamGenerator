__author__ = 'marc'


class Questao(object):
    def __init__(self):
        self._exercicios = []

    @property
    def exercicios(self):
        return self._exercicios

    @exercicios.setter
    def exercicios(self,exercicios):
        self._exercicios = exercicios

    def adicionarExercicio(self, exercicio):
        self._exercicios.append(exercicio)