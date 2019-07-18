from .DynaSolver import *
from .DpExcitation import *
import numpy as np


def test_assemble_force_matrix():
    M = np.matrix([[1, 0], [0, 1]])

    # Função para gerar a matriz... Usar auxiliar.py para salvar o csv
    # return assemble_force_matrix(Excitation(exctDuration=1, anlyDuration=1), M, Configurations(timeStep=0.5))

    # Teste
    answer = np.matrix(np.genfromtxt(r'./DynaPy/data_tests/force_matrix.csv', delimiter='\t'))
    foo = assemble_force_matrix(Excitation(exctDuration=1, anlyDuration=1), M, Configurations(timeStep=0.5))
    assert np.linalg.norm(foo - answer)/np.linalg.norm(answer) <= 1e-3
    # assert abs(np.max((foo-answer)/answer)) <= 1e-3

def test_modal_superposition():
    answer_M = np.matrix(np.genfromtxt(r'./DynaPy/data_tests/modal_mass_matrix.csv', delimiter = '\t'))
    answer_K = np.matrix(np.genfromtxt(r'./DynaPy/data_tests/modal_stiffness_matrix.csv', delimiter = '\t'))
    answer_F = np.matrix(np.genfromtxt(r'./DynaPy/data_tests/modal_force_matrix.csv', delimiter = '\n')).T
    modes = np.matrix(np.genfromtxt(r'./DynaPy/data_tests/modes_matrix.csv', delimiter = '\t'))
    M = np.matrix([[1, 0, 0],
               [0, 1.5, 0],
               [0, 0, 2]])

    K = 600*np.matrix([[1, -1, 0],
               [-1, 3, -2],
               [0, -2, 5]])

    F = 500*np.matrix([[1, 2, 2]]).T

    fooM, fooK, fooF = assemble_modal_matrices(modes, M, K, F)

    assert np.linalg.norm(fooM - answer_M)/np.linalg.norm(answer_M) <= 1e-3
    # assert answer_M == fooM
    # print('fooM = ', fooM, '\n')
    # print('M = ', answer_M)