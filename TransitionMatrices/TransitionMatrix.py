import numpy as np
import random

from Defs import NewStates

class TransitionMatrix:
    """Representa y permite operar sobre una matriz de transiciones.
    """    

    def __init__(self, matrix: np.ndarray) -> None:
        self.matrix = matrix

    def take_actions(self, number_of_actions: int):
        """Calcula las probabilidades de la matriz de transiciones tras un número de acciones o pasos.

        Arguments:
            number_of_actions -- El número de acciones a tomar. Debe ser un entero mayor o igual a 1.

        Raises:
            ValueError: El número de acciones a tomar es menor a 1.

        Returns:
            Una nueva TransitionMatrix con las nuevas probabilidades.
        """               

        if number_of_actions <= 0:
            raise ValueError("No se puede tomar menos de 1 acción.")
        
        # la matriz de transiciones tras n acciones es la n-ésima potencia de la matriz original
        return TransitionMatrix(np.linalg.matrix_power(self.matrix, number_of_actions))
        
    def calculate_p_state(self, number_of_actions: int, state: NewStates) -> np.ndarray:
        """Calcula, para todos los estados, la probabilidad de terminar en un estado específico tras un número de acciones.

        Arguments:
            number_of_actions -- El número de acciones a tomar
            state -- El estado en el que se desea terminar. Debe ser uno de los estados definidos en States.STATES

        Raises:
            ValueError: El número de acciones a tomar es menor a 1
            ValueError: El estado final elegido no es un estado válido.

        Returns:
            Una lista (de tipo numpy.ndarray) que contiene las probabilidades finales de cada estado.
        """        
        
        if number_of_actions <= 0:
            raise ValueError("No se pueden calcular las probabilidades con menos de 1 acción.")
        
        if state not in list(NewStates):
            raise ValueError("Estado no válido.")
        
        matrix_after_n_actions = self.take_actions(number_of_actions)

        return matrix_after_n_actions.matrix[:, list(NewStates).index(state)]

    def __str__(self) -> str:
        np.set_printoptions(precision=4, suppress=True)
        return self.matrix.__str__()