import numpy as np
import random

from TransitionMatrix import TransitionMatrix
from Defs import STATES

def generate_random_row(size: int) -> list:
    """Genera una lista de probabilidades random que suman 1.

    Arguments:
        size -- la cantidad de probabilidades a generar

    Returns:
        Una lista, de largo n, de probabilidades aleatorias que suman 1.
    """        
    initial_row = []
    for i in range(size):
        initial_row.append(random.random())
    initial_total = sum(initial_row)
    return [x/initial_total for x in initial_row]


def generate_random_row_with_fixed_values(size: int, fixed_values: dict) -> list: 
    """Genera una lista de valores aleatorios, con algunos valores fijos, tal que la suma es 1.

    Los valores fijos vienen en un dict y se fijan según su posición en la lista. Por ejemplo,
    fixed_values={2:0.5, 7:0.1} significa que lista[2] será 0.5, lista[7] será 0.1, y los demás 
    valores serán aleatorios.


    Arguments:
        size -- El largo de la lista a generar.
        fixed_values -- Un dict que asigna valores a posiciones específicas de la lista.

    Returns:
        Una lista con los valores fijos y generados.
    """    

    initial_row = []

    max_sum = 1 - sum(fixed_values.values())

    for i in range(size - len(fixed_values)):
        initial_row.append(random.random())
    initial_total = sum(initial_row)
    other_values = [x*max_sum/initial_total for x in initial_row]

    final_row = []

    for i in range(size):
        if i in fixed_values:
            final_row.append(fixed_values[i])
        else:
            final_row.append(other_values.pop())

    return final_row

def random_transition_matrix(size: int) -> TransitionMatrix:
    """Genera una matriz de transiciones con valores aleatorios.

    La única restricción de la matriz es que los valores de cada fila deben sumar 1.

    Arguments:
        size -- El tamaño de la matriz.

    Returns:
        Una TransitionMatrix de tamaño (size, size) con valores aleatorios.
    """    

    matrix = np.eye(size)

    for i in range(size):
        matrix[i,:] = generate_random_row(size)

    return TransitionMatrix(matrix)

def realistic_random_transition_matrix(size: int, penalty_chance=0.7, stay_chance=0.5) -> TransitionMatrix:
    """Genera una matriz de transiciones con valores aleatorios, cumpliendo ciertas restricciones adicionales.

    Las restricciones son:
    - La suma de los valores de cada fila debe ser 1
    - Transiciones GOAL -> GOAL y END_OF_POSSESSION -> END_OF_POSSESSION son 1
    - Transición PENALTY -> GOAL es alta, default es 0.7
    - En los estados Sn, mantenerse en el mismo estado es un valor aleatorio relativamente alto, default es alrededor de 0.5

    Arguments:
        size -- El tamaño de la matriz.
        penalty_chance -- La probabilidad de la transición PENALTY -> GOAL
        stay_chance -- La probabilidad media de que un estado Sn se mantenga en el mismo estado.

    Returns:
        Una TransitionMatrix con la estructura descrita.
    """    

    matrix = np.zeros((size, size))

    matrix[STATES['GOAL'],:] = generate_random_row_with_fixed_values(size, {STATES['GOAL']:1})
    matrix[STATES['END_OF_POSSESSION'],:] = generate_random_row_with_fixed_values(size, {STATES['END_OF_POSSESSION']:1})

    matrix[STATES['PENALTY'],:] = generate_random_row_with_fixed_values(size, {STATES['GOAL']:penalty_chance})

    for i in range(STATES['SHORT_CORNER'], STATES['SHORT_CORNER']+6):
        matrix[i,:] = generate_random_row(size)

    for i in range(STATES['S01'], len(STATES)):
        matrix[i,:] = generate_random_row_with_fixed_values(size, {i:random.uniform(stay_chance-0.05, stay_chance+0.05)})

    return TransitionMatrix(matrix)
