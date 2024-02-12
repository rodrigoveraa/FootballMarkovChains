from enum import Enum, auto

from Defs import ZONES

class Event:

    def __init__(self, event:dict) -> None:
        self.type = event.get('type', {}).get('name')
        self.possession_team = event.get('possession_team', {}).get('name')
        self.foul_advantage = event.get('foul_won', {}).get('advantage')
        self.foul_penalty = event.get('foul_won', {}).get('penalty')
        self.location = event.get('location')
        self.under_pressure = event.get('under_pressure', False)
        self.index = event.get('index')
        self.timestamp = event.get('timestamp')
        self.outcome = event.get('shot', {}).get('outcome', {}).get('name')
        self.period = event.get('period')
        self.team = event.get('team', {}).get('name')
        self.shot_type = event.get('shot', {}).get('type', {}).get('name')
        self.pass_type = event.get('pass', {}).get('type', {}).get('name')

    def get_zone(self) -> ZONES:
        """
        Entrega la zona en la cancha en la cual se produce el evento.
        """

        if not self.location:
            return ZONES.NONE

        # las coordenadas son siempre de (0, 0) a (120, 80) con respecto al equipo que actúa
        # por ejemplo, los corner son siempre alrededor de (120, 0) o (120, 80)
        if self.location[1] < 18:
            if self.location[0] < 40:
                return ZONES.DEF_LW
            elif self.location[0] < 80:
                return ZONES.M_LW
            else:
                return ZONES.OFF_LW
        elif self.location[1] < 62:
            if self.location[0] < 40:
                return ZONES.DEF_C
            elif self.location[0] < 80:
                return ZONES.M_C
            elif self.location[0] < 102:
                return ZONES.OFF_C
            else:
                return ZONES.PENALTY_BOX
        else:
            if self.location[0] < 40:
                return ZONES.DEF_RW
            elif self.location[0] < 80:
                return ZONES.M_RW
            else:
                return ZONES.OFF_RW
            
    def __str__(self) -> str:
        
        event_str = "({}) {}T {} {}{}\n{} {}\n{}{}{}{}{}{}".format(
            self.index,
            self.period,
            self.timestamp,
            self.type,
            "-" if self.team != self.possession_team else "",
            self.location,
            self.get_zone(),
            "ADVANTAGE\n" if self.foul_advantage else "",
            "PENALTY\n" if self.foul_penalty else "",
            "UNDER PRESSURE\n" if self.under_pressure else "",
            self.shot_type + '\n' if self.shot_type else "",
            self.outcome + '\n' if self.outcome else "",
            self.pass_type + '\n' if self.pass_type else ""

        )

        return event_str
