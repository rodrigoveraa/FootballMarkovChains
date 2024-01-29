import numpy as np
import os
import math

from openpyxl import Workbook

from TransitionMatrix import TransitionMatrix
from States import STATES

def save_matrix_to_txt(tm: TransitionMatrix, file):
    """Guarda una TransitionMatrix a un archivo de texto.

    Arguments:
        tm -- La TransitionMatrix a guardar
        file -- El path del archivo en el que se guarda la TransitionMatrix.
    """    
    np.savetxt(file, tm.matrix)

def save_matrix_to_xlsx(tm: TransitionMatrix, file):
    workbook = Workbook()
    sheet = workbook.active

    for i in range(tm.matrix.shape[0]):
        row = tm.matrix[i,:].tolist()
        sheet.append(row)

    workbook.save(file)


def load_matrix_from_txt(file) -> TransitionMatrix:
    """Carga una TransitionMatrix desde un archivo de texto y la valida.

    Arguments:
        file -- El path del archivo de texto que contiene la TransitionMatrix

    Returns:
        La TransitionMatrix leída del archivo de texto, validada.
    """
    matrix = np.loadtxt(file)

    check_if_matrix_is_valid(matrix)

    return TransitionMatrix(matrix)

def check_if_matrix_is_valid(matrix: np.ndarray):
    """Revisa si una matriz cumple con las condiciones para ser una TransitionMatrix válida.

    Las condiciones son dos:
    - Los valores de cada fila deben sumar 1.
    - La matriz debe tener una número apropiado de filas y columnas, correspondientes al número de estados con los que se está trabajando.

    Arguments:
        matrix -- La matriz a validar.

    Raises:
        Exception: La forma de la matriz no es consistente con el número de estados
        Exception: Al menos una fila de la matriz tiene una suma distinta de 1.
    """    
    if matrix.shape != (len(STATES), len(STATES)):
        raise Exception("La matriz tiene una forma no válida ({})".format(matrix.shape))
    
    for i in range(len(STATES)):
        row = matrix[i, :]
        row_total = sum(row)
        if not math.isclose(row_total, 1):
            raise Exception("La fila {} suma {} en lugar de 1.".format(i, row_total))
    
def save_results_to_txt(col: np.ndarray, file, format):
    """Guarda un np.ndrray, que contiene resultados de procesar una TransitionMatrix, en un archivo de texto.

    Arguments:
        col -- Los resultados que se quieren guardar
        file -- El archivo en el que se guardarán los reusltados
        format -- El formato que tendrá la información dentro del archivo

    Raises:
        Exception: El formato especificado debe ser uno de los formatos válidos.
    """    

    if format not in ('list, dict'):
        raise Exception("'{}' no es un formato válido.")
    
    if format == 'list':
        np.savetxt(file, col)

    elif format == 'dict':
        probs_dict = dict(zip(STATES.keys(), col))
        with open(file, 'w') as f:
            print('{', file=f)
            for item in probs_dict.items():
                print(item, file=f)
            print('}', file=f)