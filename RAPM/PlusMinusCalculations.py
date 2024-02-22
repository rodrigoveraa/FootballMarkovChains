import json
import numpy as np
from tqdm import tqdm
from EventObjects import Segment, Team, Player, DefaultMatchTime, MatchTime, Substitution, Goal
import ProbabilitiesGeneration as PGen


def find_segments(events_files):
    """Busca los distintos segmentos que ocurren en una lista de archivos de eventos.

    Arguments:
        events_files -- la lista de archivos de eventos

    Returns:
        Una lista con los segmentos encontrados.
    """    

    segments = []

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

        current_segments = []
        current_goals = []
        

        # para cada uno de los eventos, revisamos si corresponde crear un nuevo segmento
        # y los jugadores que entran y salen
        for e in events:
            event_type = e.get('type').get('name')
            event_time = MatchTime(e.get('period'), e.get('timestamp'))
            event_team = Team(e.get('team')['id'], e.get('team')['name'])
            if event_type == "Substitution":

                # event_time = MatchTime(e.get('period'), e.get('timestamp'))
                # event_team = Team(e.get('team')['id'], e.get('team')['name'])
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
                    current_segments.append(new_segment)
                    new_segment.add_sub(new_sub)
                    last_segment = new_segment
                    last_segment_time = event_time


                if last_segment.end == DefaultMatchTime():
                    last_segment.close(event_time)

            elif event_type == "Own Goal For":
                new_goal = Goal(event_team, event_time)
                current_goals.append(new_goal)

            elif event_type == "Shot":
                event_outcome = e.get('shot').get('outcome').get('name')
                if event_outcome == "Goal":
                    new_goal = Goal(event_team, event_time)
                    current_goals.append(new_goal)

        # agregamos el último segmento, aplicando los cambios pendientes
        end_time = MatchTime(events[-1].get('period'), events[-1].get('timestamp'))
        final_segment = last_segment.apply_subs(last_segment.end)
        final_segment.end = end_time
        segments.append(final_segment)
        current_segments.append(final_segment)

        for cs in current_segments:
            for cg in current_goals:
                if cs.contains(cg):
                    cs.add_goal(cg)

    return segments


def calculate_ridge_regression(X:np.ndarray, y, l):
    """Calcula la ridge regression como se explica en Kharrat, McHale y López Peña (página 5).

    Arguments:
        X -- la matriz de presencias
        y -- el vector target
        l -- el "penalty term" (lambda)

    Returns:
        Un vector correspondiente a la solución de la ridge regression (alpha)
    """    

    xtx = X.transpose() @ X
    l2i = (l*l)*np.identity(X.shape[1])

    inv_1 = np.linalg.inv(xtx + l2i)
    xty = X.transpose() @ y

    return inv_1 @ xty


def rapm_y(segments):
    """Calcula el valor del target para una lista de segmentos (RAPM)

    Arguments:
        segments -- la lista de segmentos

    Returns:
        Un vector con los valores del target
    """    
    return np.array([s.goal_difference() for s in segments])

def eppm_y(segments):
    """Calcula el valor del target para una lista de segmentos (EPPM)

    Arguments:
        segments -- la lista de segmentos

    Returns:
        Un vector con los valores del target
    """  
    probs = PGen.generate_all_probs(PGen.MATCH_LENGTH, PGen.DEFAULT_VARIATION)
    result = []
    for i, s in enumerate(segments):
        start = s.start_minute()
        end = s.end_minute()
        print(i)
        print(probs[start])
        print(probs[end])
        value = ((3*probs[end][PGen.PROBS['HW']] + probs[end][PGen.PROBS['D']] - 3*probs[start][PGen.PROBS['HW']] + probs[start][PGen.PROBS['D']]) -
                 (3*probs[end][PGen.PROBS['AW']] + probs[end][PGen.PROBS['D']] - 3*probs[start][PGen.PROBS['AW']] + probs[start][PGen.PROBS['D']]))
        result.append(value)

    return result