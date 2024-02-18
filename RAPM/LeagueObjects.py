import json


class League:

    def __init__(self, league:dict) -> None:
        self.competition_id = league.get("competition_id")
        self.season_id = league.get("season_id")
        self.country = league.get("country_name")
        self.competition_name = league.get("competition_name")
        self.competition_gender = league.get("competition_gender")
        self.season_name = league.get("season_name")
