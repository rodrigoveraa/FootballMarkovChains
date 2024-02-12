import argparse
import os
import json

from StateDetection import check_goal, check_eop, check_penalty, check_free_kick, check_corner, check_throw_in, check_zonal_state
from Event import Event
from Defs import NewStates


CHECKING_FUNCTIONS = [check_penalty, check_free_kick, check_corner, check_throw_in, check_goal, check_eop, check_zonal_state]

parser = argparse.ArgumentParser()

parser.add_argument('--input-file', type=str, help="Archivo de eventos")

parser.add_argument('--output-file', type=str, help="Archivo donde se guardarán los resultados. Si no está presente, se guardan en out.txt.")

parser.add_argument('--number-of-events', type=int, help="Número de eventos del partido a procesar (default: todos)")

args = parser.parse_args()

file_to_read = args.input_file

if file_to_read:
    with open(file_to_read, 'r', encoding='utf-8') as jsonfile:
        events = json.load(jsonfile)
else:
    raise Exception("Debe especificar un nombre de archivo.")

total_events = args.number_of_events if args.number_of_events else len(events)

events_list = events[0:total_events]

file_to_write = args.output_file if args.output_file else './out.txt'

# detectamos los equipos involucrados
teams = []

for e in events:
    if e['team']['name'] not in teams:
        teams.append(e['team']['name'])

# empezamos con un evento vacío
last_event = Event({'index': 0})

# preguntamos cuál equipo queremos ver
input_team = int(input("Equipo: {} (1) o {} (2)? ".format(teams[0], teams[1]))) - 1

# procesamos los eventos de a uno, dejando el último evento procesado como last_event
with open(file_to_write, 'w', encoding='utf-8') as outfile:
    for item in events_list:
        ev = Event(item)
        print("Procesando evento {}...".format(ev.index), file=outfile)
        # usamos cada una de las funciones de chequeo
        for cf in CHECKING_FUNCTIONS:
            state, state_team = cf(last_event, ev)
            if state and state_team == teams[input_team]:
                print("", file=outfile)
                print(last_event, file=outfile)
                print(ev, file=outfile)
                print((state, state_team), file=outfile)
                print("", file=outfile)
                print("------------------------------------------------", file=outfile)
                print("", file=outfile)

                if state == NewStates.END_OF_POSSESSION:
                    for i in range(4):
                        print("", file=outfile)

        last_event = ev




