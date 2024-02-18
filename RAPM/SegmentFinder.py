import json
import numpy as np
from datetime import time
from tqdm import tqdm
from openpyxl import Workbook

from EventObjects import MatchTime, Team, Player, Segment, DefaultMatchTime, Substitution, SendOff

def save_matrix_to_xlsx(tm: np.ndarray, file):

    workbook = Workbook()
    sheet = workbook.active

    for i in range(tm.shape[0]):
        row = tm[i,:].tolist()
        sheet.append(row)

    workbook.save(file)

# FILE_TO_READ = "./match_files/2275030.json"

# archivo obtenido usando MatchFinder.py
ids_file = "./2-27.txt"
segments_file = './segments.txt'

with open(ids_file, 'r', encoding='utf-8') as f:
    events_files = f.readlines()

# aquí vamos a guardar TODOS los segmentos de TODOS los archivos
segments = []

print("Leyendo partidos...")
for FILE_TO_READ in tqdm(events_files):

    # leemos los eventos del archivo
    with open(FILE_TO_READ.strip(), 'r', encoding='utf-8') as jsonfile:
        events = json.load(jsonfile)

    # obtenemos los equipos y los jugadores iniciales
    ev_team1 = events[0].get('team')
    team1 = Team(ev_team1['id'], ev_team1['name'])

    ev_team2 = events[1].get('team')
    team2 = Team(ev_team2['id'], ev_team2['name'])

    ev_players1 = events[0].get('tactics').get('lineup')
    players1 = []
    for ep in ev_players1:
        p = Player(ep['player']['id'], ep['player']['name'])
        players1.append(p)

    ev_players2 = events[1].get('tactics').get('lineup')
    players2 = []
    for ep in ev_players2:
        p = Player(ep['player']['id'], ep['player']['name'])
        players2.append(p)

    # segmento inicial
    last_segment = Segment(team1, players1, team2, players2, DefaultMatchTime(), DefaultMatchTime())
    last_segment_time = DefaultMatchTime()

    segment_events = []

    # para cada uno de los eventos, revisamos si corresponde crear un nuevo segmento
    # y los jugadores que entran y salen
    for e in events:
        event_type = e.get('type').get('name')
        if event_type == "Substitution":

            event_time = MatchTime(e.get('period'), e.get('timestamp'))
            event_team = Team(e.get('team')['id'], e.get('team')['name'])
            event_player_out = Player(e.get('player')['id'], e.get('player')['name'])
            p_in = e.get('substitution').get('replacement')
            event_player_in = Player(p_in['id'], p_in['name'])

            if event_time == last_segment_time:
                new_sub = Substitution(event_team, event_player_in, event_player_out)
                last_segment.add_sub(new_sub)

            else:
                new_sub = Substitution(event_team, event_player_in, event_player_out)
                new_segment = last_segment.apply_subs(last_segment.end)
                segments.append(new_segment)
                new_segment.add_sub(new_sub)
                last_segment = new_segment
                last_segment_time = event_time


            if last_segment.end == DefaultMatchTime():
                last_segment.close(event_time)

    # agregamos el último segmento, aplicando los cambios pendientes
    end_time = MatchTime(events[-1].get('period'), events[-1].get('timestamp'))
    final_segment = last_segment.apply_subs(last_segment.end)
    final_segment.end = end_time
    segments.append(final_segment)

with open(segments_file, 'w', encoding='utf-8') as sf:
    for s in segments:
        s.print(sf)
        print("------------------------------------------------------", file=sf)

matrix_players = []

print('Armando lista de jugadores...')
for s in tqdm(segments):
    for p in s.players1 + s.players2:
        if p not in matrix_players:
            matrix_players.append(p)

matrix = np.zeros((len(segments), len(matrix_players)))
print("Generando matriz...")
for i in tqdm(range(len(segments))):
    for j in range(len(matrix_players)):

        if segments[i].contains_player_home(matrix_players[j]):
            matrix[i,j] = 1
        elif segments[i].contains_player_away(matrix_players[j]):
            matrix[i,j] = -1

save_matrix_to_xlsx(matrix, './matrix.xlsx')


