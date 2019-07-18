from DynaPy import *
from matplotlib import pyplot as plt
import numpy as np

# np.set_printoptions(linewidth=100, precision=2)

# dt = 0.5
# frequency = 20
# tt = 1

# diameter = 0.6
# width = 20
# waterHeight = 1
# amount = 1

# height = 10.

# config = Configurations(nonLinearAnalysis=True, timeStep=dt)

# stories = {1: Story(height=height), 2: Story(height=height), 3: Story(height=height)}
# tlcd_linear = TLCD(diameter=diameter, width=width, waterHeight=waterHeight,
#                     amount=amount, configurations=config)
# excitation_linear = Excitation(frequency=frequency, structure=stories, tlcd=tlcd_linear,
#                                 exctDuration=tt, anlyDuration=tt, amplitude=5)

# for i in stories.values():
#     i.calc_damping_coefficient(0.02)

# print(excitation_linear.amplitude)
# print(tlcd_linear.mass)
# print(tlcd_linear.width / tlcd_linear.length * tlcd_linear.mass * excitation_linear.amplitude * np.sin(excitation_linear.frequency * 0.5))
# print(tlcd_linear.width/tlcd_linear.length*tlcd_linear.mass*excitation_linear.amplitude*np.sin(excitation_linear.frequency*1))

# M_linear = assemble_mass_matrix(stories, tlcd_linear)
# F = assemble_force_matrix(excitation_linear, M_linear, config)

# print(F)

M = np.matrix([[1, 0, 0],
               [0, 1.5, 0],
               [0, 0, 2]])

K = 600*np.matrix([[1, -1, 0],
               [-1, 3, -2],
               [0, -2, 5]])

F = 500*np.matrix([[1, 2, 2]]).T

eigvals, eigvecs = get_eigenvec_eigenval(M, K)
for i in range(eigvecs.shape[0]):
    eigvecs[:, i] /= eigvecs[0, i]

Mi, Ki, Fi = assemble_modal_matrices(eigvecs, M, K, F)
# np.savetxt("./DynaPy/data_tests/modal_mass_matrix.csv", Mi, delimiter="\t")
# np.savetxt("./DynaPy/data_tests/modal_stiffness_matrix.csv", Ki, delimiter="\t")
# np.savetxt("./DynaPy/data_tests/modal_force_matrix.csv", Fi, delimiter="\t")
# np.savetxt("./DynaPy/data_tests/modes_matrix.csv", eigvecs, delimiter="\t")

# print(np.sqrt(eigvals))
# print(eigvecs)

# print(Mi, Ki, Fi, sep='\n\n')

