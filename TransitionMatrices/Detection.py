import argparse
import json
import os
import numpy as np
import math

from StateDetection import DETECTION_FUNCTIONS
from Event import Event
from TransitionCount import TransitionCount
from Defs import NewStates
from TransitionMatrix import TransitionMatrix
import TransitionMatrixFileHandler as tmfh
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument('--input-folder', type=str, help="Directorio con archivos de eventos")

parser.add_argument('--output-file', type=str, default='./out.txt', 
                    help="Archivo donde se guardarán los resultados. Si no está presente, se guardan en out.txt.")
parser.add_argument('--states-file', type=str, default='./states.txt',
                     help="Archivo donde se guardarán los estados encontrados. Si no está presente, se guardan en states.txt.")

parser.add_argument('--number-of-iterations', type=int, help="Número de iteraciones para la matriz de transiciones.")

args = parser.parse_args()

folder = args.input_folder

# lista que contiene todos los estados definidos
state_def_list = list(NewStates)

# lista de estados encontrados
states = []

# lista de equipos encontrados en el directorio
teams = []

print("Detectando equipos...")

# leemos todos los archivos del directorio para ver cuáles equipos están en el directorio
for file_to_read in tqdm(os.listdir(folder)):
    with open(os.path.join(folder, file_to_read), 'r', encoding='utf-8') as jsonfile:
        events = json.load(jsonfile)

    # los 2 primeros eventos de cada archivo son las alineaciones de cada equipo
    # no es necesario ver más eventos por ahora
    for e in events[0:2]:
        if e['team']['name'] not in teams:
            teams.append(e['team']['name'])

print("Archivos detectados: {}".format(len(os.listdir(folder))))

print("Equipos detectados:")
for i in range(len(teams)):   
    print("{}: {}".format(i, teams[i]))

# pedimos al usuario que elija el equipo que quiere analizar
team_index = int(input("Ingrese código del equipo a analizar: "))

# el nombre del equipo elegido
team = teams[team_index]

file_to_write = args.output_file
states_file = args.states_file

print("Buscando eventos de {}...".format(team))
# nuevamente leemos todos los eventos
# esta vez para detectar todos los estados correspondientes al equipo elegido
for file_to_read in tqdm(os.listdir(folder)):
    with open(os.path.join(folder, file_to_read), 'r', encoding='utf-8') as jsonfile:
        events = json.load(jsonfile)

    # comenzamos con un evento vacío
    last_event = Event({'index': 0})

    for item in events:
        ev = Event(item)
        # llamamos a cada una de las funciones de detección con el evento que estamos analizando
        for cf in DETECTION_FUNCTIONS:
            state, state_team = cf(last_event, ev)
            # si detectamos un estado y corresponde al equipo elegido,
            # agregamos el evento a la lista
            if state and state_team == team:
                states.append(state)

        last_event = ev

# lista de los estados presentes en nuestra lista de estados
# siempre incluye GOAL y END_OF_POSSESSION como estados absorbentes
states_used = [NewStates.GOAL, NewStates.END_OF_POSSESSION]

# recorremos la lista de estados encontrados para ver cuáles están presentes
for s in states:
    if s not in states_used:
        states_used.append(s)

# ordenamos los estados presentes según el orden original definido en Defs
states_used.sort(key=lambda x: state_def_list.index(x))

tc = TransitionCount(states_used)

# agregamos todas las transiciones al TransitionCount
for i in range(len(states)-1):
    tc.add(states[i], states[i+1])

print("Contando estados...")

# vamos a construir la matriz for filas
rows = []

# i,j son ESTADOS, no ÍNDICES
for i in states_used:
    print("Construyendo fila para {}...".format(i))
    # obtenemos los totales de las transiciones desde este estado
    row_counts = tc.get_counts_from_state(i)
    # y la suma total de las transiciones
    row_total = sum(row_counts.values())

    # aquí guardamos los elementos de la fila
    row = []
    
    for j in states_used:
        # caso especial: fila GOAL
        if i == NewStates.GOAL:
            value = 1 if j == NewStates.GOAL else 0
            
        # caso especial: fila END_OF_POSSESSION
        elif i == NewStates.END_OF_POSSESSION:
            value = 1 if j == NewStates.END_OF_POSSESSION else 0
        
        # en el resto de la matriz, el valor en (i,j) es el total de transiciones i -> j
        # dividido por el total de transiciones desde i
        else:
            value = row_counts[(i,j)]/row_total

        # agregamos el valor a la fila
        row.append(value)

    # si la suma de la fila no es 1, algo salió mal
    i_total = sum(row)
    if not math.isclose(i_total, 1):
        raise Exception("Row {} does not equal 1 but {}".format(i, i_total))
    
    # agregamos la fila a la lista
    rows.append(row)
    
# creamos la matriz a partir de la lista de filas
matrix = np.array(rows)
print(matrix.shape)
tm = TransitionMatrix(matrix)

# procesamos la matriz
new_tm = tm.take_actions(args.number_of_iterations)

# si el archivo de salida es .xlsx, guardamos la matriz a xlsx
name, ext = os.path.splitext(file_to_write)
if ext == '.xlsx':
    tmfh.save_matrix_to_xlsx(new_tm, file_to_write)
else:
    tmfh.save_matrix_to_txt(new_tm, file_to_write)

# también guardamos la lista de estados presentes
with open(states_file, 'w', encoding='utf-8') as sf:
    for i in range(len(states_used)):
        print("{}: {}".format(i+1, states_used[i]), file=sf)

print()

print("Análisis de {} listo".format(team))

print()


print("Matriz guardada en {}".format(file_to_write))
print("Lista de estados guardada en {}".format(states_file))


