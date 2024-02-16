from enum import Enum, auto

from Defs import ZONES, UNDER_PRESSURE, PLAY_TYPE

class Event:

    def __init__(self, event:dict) -> None:
        self.type = event.get('type', {}).get('name')
        self.possession_team = event.get('possession_team', {}).get('name')
        # self.foul_advantage = event.get('foul_won', {}).get('advantage')
        # self.foul_penalty = event.get('foul_won', {}).get('penalty')
        self.location = event.get('location')
        self.under_pressure = event.get('under_pressure', False)
        self.index = event.get('index')
        self.timestamp = event.get('timestamp')
        self.outcome = event.get('shot', {}).get('outcome', {}).get('name')
        self.period = event.get('period')
        self.team = event.get('team', {}).get('name')
        self.shot_type = event.get('shot', {}).get('type', {}).get('name')
        self.pass_type = event.get('pass', {}).get('type', {}).get('name')
        self.play_type = event.get('play_pattern', {}).get('name')

    def get_zone(self) -> ZONES:
        """
        Entrega la zona en la cancha en la cual se produce el evento.
        """

        if not self.location:
            return ZONES.NONE

        # las coordenadas son siempre de (0, 0) a (120, 80) con respecto al equipo que actúa
        # por ejemplo, los corner son siempre alrededor de (120, 0) o (120, 80)
        if self.location[0] > 102:
            if self.location[1] < 18:
                return ZONES.Z4
            elif self.location[1] < 62:
                return ZONES.Z5
            else:
                return ZONES.Z6
        elif self.location[0] > 80:
            if self.location[1] < 18:
                return ZONES.Z1
            elif self.location[1] < 62:
                return ZONES.Z2
            else:
                return ZONES.Z3
        else:
            return ZONES.Z0
        
    def get_pressure(self) -> UNDER_PRESSURE:
        if self.under_pressure:
            return UNDER_PRESSURE.YES
        return UNDER_PRESSURE.NO
    
    def get_play_type(self) -> PLAY_TYPE:
        if self.play_type == 'From Counter':
            return PLAY_TYPE.COUNTER
        if self.play_type in ['From Corner', 'From Free Kick', 'From Throw In']:
            return PLAY_TYPE.SET_PIECE
        return PLAY_TYPE.OPEN_PLAY
            
    def __str__(self) -> str:
        
        event_str = "({}) {}T {} {}{}\n{} {}\n{}{}{}{}{}".format(
            self.index,
            self.period,
            self.timestamp,
            self.type,
            "-" if self.team != self.possession_team else "",

            self.location,
            self.get_zone(),

            "UNDER PRESSURE\n" if self.under_pressure else "",
            self.play_type + '\n' if self.play_type else "",
            self.shot_type + '\n' if self.shot_type else "",
            self.outcome + '\n' if self.outcome else "",
            self.pass_type + '\n' if self.pass_type else ""

        )

        return event_str
