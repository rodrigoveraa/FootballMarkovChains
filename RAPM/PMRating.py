import json
import numpy as np
import argparse
from datetime import time
from tqdm import tqdm
from openpyxl import Workbook

import PlusMinusCalculations

# funciones para calcular los distintos ratings
RATING_CALC_TARGETS = {
    'RAPM': PlusMinusCalculations.rapm_y,
    'EPPM': PlusMinusCalculations.eppm_y
}

parser = argparse.ArgumentParser()

parser.add_argument('--input-file', type=str, help="Archivo con los paths de los archivos de eventos a utilizar.")

parser.add_argument('--output-file', type=str, default='./results.txt', help="Archivo donde se guardarán los resultados. Si no está presente, se guardan en results.txt.")

parser.add_argument('--penalty-term', type=float, default=1.0, help="Valor de lambda a utilizar para el cálculo de RAPM")

parser.add_argument('--matrix-file', type=str, help='Archivo donde se guardará la matriz de presencias de jugadores. Si no está presente, no se guarda.')

parser.add_argument('--segments-file', type=str, help='Archivo donde se guardará la secuencia de eventos detectados. Si no está presente, no se guarda.')

parser.add_argument('--rating', type=str, choices=RATING_CALC_TARGETS.keys(), default='RAPM', help="Tipo de rating a calcular")

parser.add_argument('--use-generated-probs', action="store_true", 
                    help="Sólo para EPPM. Incluir si se desea utilizar probabilidades generadas al momento de correr el script.")

parser.add_argument('--probs-file', type=str, default='./EPPM_probs.csv', 
                    help="Sólo para EPPM. El nombre del archivo que contiene las probabilidades necesarias para calcular el target de EPPM. Se ignorará si --use-generated-probs está presente.")

args = parser.parse_args()



if not args.input_file:
    raise Exception("Falta la lista de archivos de eventos.")
ids_file = args.input_file
segments_file = args.segments_file if args.segments_file else ""
matrix_file = args.matrix_file if args.matrix_file else ""

print("calculando {}...".format(args.rating))
if args.rating == 'EPPM':
    if args.use_generated_probs:
        print("Usando nuevas probabilidades generadas...")
    else:
        print("Usando probabilidades obtenidas de {}".format(args.probs_file))

# obtenemos la lista de archivos de eventos
with open(ids_file, 'r', encoding='utf-8') as f:
    events_files = f.readlines()

print("Leyendo partidos...")

# aquí vamos a guardar TODOS los segmentos de TODOS los archivos
segments = PlusMinusCalculations.find_segments(events_files)

# guardamos la lista de segmentos detectados si corresponde
if segments_file:
    with open(segments_file, 'w', encoding='utf-8') as sf:
        for s in segments:
            s.print(sf)
            print("------------------------------------------------------", file=sf)

matrix_players = []

# armamos una lista con todos los jugadores involucrados en algún segmento
print('Armando lista de jugadores...')
for s in tqdm(segments):
    for p in s.players1 + s.players2:
        if p not in matrix_players:
            matrix_players.append(p)

matrix = np.zeros((len(segments), len(matrix_players)))

# generamos la matriz de presencias
print("Generando matriz...")
for i in tqdm(range(len(segments))):
    for j in range(len(matrix_players)):

        if segments[i].contains_player_home(matrix_players[j]):
            matrix[i,j] = 1
        elif segments[i].contains_player_away(matrix_players[j]):
            matrix[i,j] = -1

# guardamos la matriz de presencias si corresponde
print("Guardando matriz...")
if matrix_file:
    np.savetxt(matrix_file, matrix)



# A partir de acá calculamos la solución de la regresión

print("Calculando ratings...")
# obtenemos la función apropiada para calcular el target
rating_function = RATING_CALC_TARGETS[args.rating]
X = matrix
# calculamos el target a partir de la lista de segmentos
y = rating_function(segments, use_generated_probs=args.use_generated_probs, probs_file=args.probs_file)
l = args.penalty_term

result = PlusMinusCalculations.calculate_ridge_regression(X, y, l)

# guardamos los ratings obtenidos en una lista y la ordenamos de mayor a menor
ratings = []
for i in range(len(result)):
    ratings.append((matrix_players[i], result[i]))

ratings.sort(key=lambda x: x[1], reverse=True)

# guardamos la lista de ratings obtenidos
with open(args.output_file, 'w', encoding='utf-8') as rfile:
    for i in range(len(result)):
        print("{}: {}".format(ratings[i][0], ratings[i][1]), file=rfile)

print("Listo! Resultados están en {}".format(args.output_file))


