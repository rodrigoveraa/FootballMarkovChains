import argparse

from States import STATES
import TransitionMatrixLoader

DEFAULT_MATRIX_SIZE = len(STATES)

parser = argparse.ArgumentParser()

parser.add_argument('--penalty-goal-chance', default=0.7, type=float, 
                    help="Probabilidad de pasar de PENALTY a GOAL (default: %(default)s)")
parser.add_argument('--state-stay-chance', default=0.5, type=float, 
                    help='Probabilidad media de quedarse en un estado Sn (default: %(default)s)')
parser.add_argument('--number-of-actions', default=20, type=int, 
                    help='Número de acciones a tomar (default: %(default)s)')
parser.add_argument('--final-state', default='GOAL', choices=STATES.keys(), type=str,
                    help='Estado del que se quieren obtener las probabilidades')
parser.add_argument('--output-style', choices={'list', 'dict'}, default='list', type=str,
                    help='Formato en que se muestran los resultados.')

args = parser.parse_args()

print('Generando matriz de transiciones...')
print()
newTM = TransitionMatrixLoader.realistic_random_transition_matrix(
    DEFAULT_MATRIX_SIZE,
    args.penalty_goal_chance,
    args.state_stay_chance
)

print('Calculando probabilidades después de {} acciones...'.format(args.number_of_actions))
print()
final_probs = newTM.calculate_p_state(args.number_of_actions, STATES[args.final_state])

print("Listo!")

print('Probabilidades calculadas:')
if args.output_style == 'list':
    print(final_probs)
elif args.output_style == 'dict':
    probs_dict = dict(zip(STATES.keys(), final_probs))
    for item in probs_dict.items():
        print(item)
