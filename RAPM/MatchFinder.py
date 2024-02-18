import os
import json

from LeagueObjects import League

def find_selected_league(leagues:League, country:str, name:str, season:str):
    for l in leagues:
        if l.country == country and l.competition_name == name and l.season_name == season:
            return l
    raise Exception("Liga no encontrada")


COMPETITIONS_FILE = '../data/competitions.json'
MATCHES_FOLDER = '../data/matches'
EVENTS_FOLDER = '../data/events'

with open(COMPETITIONS_FILE, 'r', encoding='utf-8') as jsonfile:
    leagues = json.load(jsonfile)

competitions = []
countries = []
for c in leagues:
    league = League(c)
    competitions.append(league)
    if league.country not in countries:
        countries.append(league.country)

for i in range(len(countries)):
    print("{}: {}".format(i, countries[i]))

country_index = int(input("Seleccione el país: "))
print()

selected_country = countries[country_index]

comps_by_country = []
comp_names = []
for c in competitions:
    if c.country == selected_country:
        comps_by_country.append(c)
        if c.competition_name not in comp_names:
            comp_names.append(c.competition_name)

for i in range(len(comp_names)):
    print("{}: {}".format(i, comp_names[i]))

comp_name_index = int(input("Seleccione la competencia: "))
print()

selected_comp_name = comp_names[comp_name_index]

comps_by_country_and_name = []
seasons = []
for c in comps_by_country:
    if c.competition_name == selected_comp_name:
        comps_by_country_and_name.append(c)
        if c.season_name not in seasons:
            seasons.append(c.season_name)

for i in range(len(seasons)):
    print("{}: {}".format(i, seasons[i]))

season_index = int(input("Seleccione la temporada: "))
print()

selected_season = seasons[season_index]

print("Eligió la siguiente competencia:")
print(selected_country)
print(selected_comp_name)
print(selected_season)

selected_league = find_selected_league(competitions, selected_country, selected_comp_name, selected_season)
print(selected_league.competition_id)
print(selected_league.season_id)

matches_file = "{}/{}/{}.json".format(MATCHES_FOLDER, selected_league.competition_id, selected_league.season_id)

with open(matches_file, 'r', encoding='utf-8') as jsonfile:
    matches = json.load(jsonfile)

match_ids = []
for m in matches:
    match_ids.append(m.get("match_id"))

match_ids_file = "{}-{}.txt".format(selected_league.competition_id, selected_league.season_id)
with open(match_ids_file, 'w', encoding='utf-8') as outfile:
    for m in match_ids:
        id_file = "{}/{}.json".format(EVENTS_FOLDER, m)
        print(id_file, file=outfile)

