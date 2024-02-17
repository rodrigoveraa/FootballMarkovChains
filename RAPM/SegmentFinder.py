import json
from datetime import time

from EventObjects import MatchTime, Team, Player, Segment, DefaultMatchTime, Substitution, SendOff

FILE_TO_READ = "./match_files/2275030.json"

with open(FILE_TO_READ, 'r', encoding='utf-8') as jsonfile:
    events = json.load(jsonfile)

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


segments = []

last_segment = Segment(team1, players1, team2, players2, DefaultMatchTime(), DefaultMatchTime())
last_segment_time = DefaultMatchTime()

segment_events = []

SENDOFF_CARDS = ["Second Yellow", "Red Card"]

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

end_time = MatchTime(events[-1].get('period'), events[-1].get('timestamp'))
final_segment = last_segment.apply_subs(last_segment.end)
final_segment.end = end_time
segments.append(final_segment)


for s in segments:
    s.print()
    print("------------------------------------------------------")

