from datetime import time
from typing import Any

class Player:

    def __init__(self, id:int, name:str) -> None:
        self.id = id
        self.name = name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Player):
            return self.id == other.id
        return False
    
    def __str__(self) -> str:
        return self.name

    
class Team:

    def __init__(self, id:int, name:str) -> None:
        self.id = id
        self.name = name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Team):
            return self.id == other.id
        return False
    
    def __str__(self) -> str:
        return self.name
    

class MatchTime:

    def __init__(self, period:int, timestamp:str) -> None:
        self.period = period
        self.timestamp = time.fromisoformat(timestamp).replace(microsecond=0)

    def __str__(self) -> str:
        return "{}T {}".format(self.period, self.timestamp)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, MatchTime):
            aaa1 = self.period == other.period 
            aaa2 = self.timestamp == other.timestamp
            return aaa1 and aaa2
        return False
    
class DefaultMatchTime(MatchTime):

    def __init__(self) -> None:
        super().__init__(1, '00:00:00')


class Substitution:

    def __init__(self, team:Team, player_in:Player, player_out:Player) -> None:
        self.team = team
        self.player_in = player_in
        self.player_out = player_out

    def __str__(self) -> str:
        return "SUBSTITUTION: {} REPLACES {} ({})".format(self.player_in, self.player_out, self.team)
    
class SendOff:

    def __init__(self, team:Team, player:Player) -> None:
        self.team = team
        self.player = player

    def __str__(self) -> str:
        return "SENDOFF: {} ({}) is sent off".format(self.player, self.team)
        
    

class Segment:

    def __init__(self, team1:Team, players1:list, team2:Team, players2:list, start:MatchTime, end:MatchTime) -> None:
        self.team1 = team1
        self.players1 = players1
        self.team2 = team2
        self.players2 = players2
        self.start = start
        self.end = end
        self.subs = []
        self.sendoffs = []

    def close(self, end:MatchTime):
        self.end = end

    def add_sub(self, sub:Substitution):
        self.subs.append(sub)

    def add_sendoff(self, so:SendOff):
        self.sendoffs.append(so)

    def apply_subs(self, matchtime:MatchTime):
        new_players1 = self.players1.copy()
        new_players2 = self.players2.copy()

        for sub in self.subs:
            if sub.team == self.team1:
                for i in range(len(new_players1)):
                    if new_players1[i] == sub.player_out:
                        new_players1[i] = sub.player_in

            if sub.team == self.team2:
                for i in range(len(new_players2)):
                    if new_players2[i] == sub.player_out:
                        new_players2[i] = sub.player_in

        return Segment(self.team1, new_players1, self.team2, new_players2, matchtime, DefaultMatchTime())
    
    def apply_sendoffs(self, matchtime:MatchTime):
        new_players1 = self.players1.copy()
        new_players2 = self.players2.copy()

        print(len(self.sendoffs))
        print("AAAAAAAAAAA")

        for so in self.sendoffs:
            if so.team == self.team1:
                if so.player in new_players1:
                    print("{} in {}".format(so.player, self.team1))
                new_players1.remove(so.player)
            if so.team == self.team2:
                if so.player in new_players2:
                    print("{} in {}".format(so.player, self.team2))
                new_players2.remove(so.player)

        print(len(new_players1))
        print(len(new_players2))

        return Segment(self.team1, new_players1, self.team2, new_players2, matchtime, DefaultMatchTime())
    
    
    def print(self):
        print("{}:".format(self.team1))
        for p in self.players1:
            print("\t{}".format(p))
        print()
        print("{}:".format(self.team2))
        for p in self.players2:
            print("\t{}".format(p))
        print("Start: {}".format(self.start))
        print("End: {}".format(self.end))
        for sub in self.subs:
            print(sub)
        for so in self.sendoffs:
            print(so)

            
