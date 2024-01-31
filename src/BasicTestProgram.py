import argparse
import os

import numpy as np

from States import STATES
import TransitionMatrixLoader
import TransitionMatrixFileHandler as tmfh

DEFAULT_MATRIX_SIZE = len(STATES)

parser = argparse.ArgumentParser()

parser.add_argument('--penalty-goal-chance', default=0.7, type=float, 
                    help="Probabilidad de pasar de PENALTY a GOAL (default: %(default)s)")
parser.add_argument('--state-stay-chance', default=0.5, type=float, 
                    help='Probabilidad media de quedarse en un estado Sn (default: %(default)s)')
parser.add_argument('--number-of-actions', default=20, type=int, 
                    help='Número de acciones a tomar (default: %(default)s)')
parser.add_argument('--final-state', default='GOAL', choices=STATES.keys(), type=str,
                    help='Nombre del estado del que se quieren obtener las probabilidades')
parser.add_argument('--output-style', choices={'list', 'dict'}, default='list', type=str,
                    help='Formato en que se muestran los resultados.')
parser.add_argument('--input-file', type=str, help="Archivo que contiene una matriz de transiciones")

parser.add_argument('--output-file', type=str, help="Archivo en el que se guardarán los resultados")

args = parser.parse_args()

print(args)

print('Obteniendo matriz de transiciones...')
print()

if args.input_file:
    filename, fileext = os.path.splitext(args.input_file)
    if fileext == '.xlsx':
        newTM = tmfh.load_matrix_from_xlsx(args.input_file)
    else:    
        newTM = tmfh.load_matrix_from_txt(args.input_file)

else:
    newTM = TransitionMatrixLoader.realistic_random_transition_matrix(
        DEFAULT_MATRIX_SIZE,
        args.penalty_goal_chance,
        args.state_stay_chance
    )

print('Calculando probabilidades de terminar en {} después de {} acciones...'.format(args.final_state, args.number_of_actions))
print()
final_probs = newTM.calculate_p_state(args.number_of_actions, STATES[args.final_state])

print("Listo!")

if args.output_file:
    print("Guardando resultados en {}".format(args.output_file))
    tmfh.save_results_to_file(final_probs, args.output_file, args.output_style)

print('Probabilidades calculadas:')
if args.output_style == 'list':
    print(final_probs)
elif args.output_style == 'dict':
    probs_dict = dict(zip(STATES.keys(), final_probs))
    for item in probs_dict.items():
        print(item)
