from datetime import timedelta, time
from typing import Any

class Player:
    """Representa un jugador mencionado en la lista de eventos.
    """    

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
    """Representa un equipo en la lista de eventos.
    """    

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
    """Se una para representar instantes de tiempo en los segmentos.
    Internamente utiliza el período del partido y el tiempo transcurrido dentro
    de ese período.
    """    

    def __init__(self, period:int, timestamp:str) -> None:
        self.period = period
        t_aux = time.fromisoformat(timestamp).replace(microsecond=0)
        self.timestamp = timedelta(minutes=t_aux.minute, seconds=t_aux.second)

    def __str__(self) -> str:
        return "{}T {}".format(self.period, self.timestamp)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, MatchTime):
            aaa1 = self.period == other.period 
            aaa2 = self.timestamp == other.timestamp
            return aaa1 and aaa2
        return False
      
    def absolute_time(self) -> timedelta:
        """Entrega el tiempo absoluto representado por este MatchTime. En otras palabras,
        "minuto 65" en lugar de "período 2, minuto 20".

        Returns:
            Un timedelta equivalente, pero contado desde el minuto 0, sin considerar períodos.
        """        
        if self.period == 1:
            return self.timestamp
        elif self.period == 2:
            return self.timestamp + timedelta(minutes=45)
        elif self.period == 3:
            return self.timestamp + timedelta(minutes=90)
        elif self.period == 4:
            return self.timestamp + timedelta(minutes=105)
        
    def minute(self):
        """Entrega el minuto de juego correspondiente al MatchTime.

        Returns:
            _description_
        """        
        return int(self.absolute_time().seconds/60)
    
class DefaultMatchTime(MatchTime):

    def __init__(self) -> None:
        super().__init__(1, '00:00:00')


class Substitution:
    """Representa una sustitución durante un partido.
    """    

    def __init__(self, team:Team, player_in:Player, player_out:Player) -> None:
        self.team = team
        self.player_in = player_in
        self.player_out = player_out

    def __str__(self) -> str:
        return "SUBSTITUTION: {} REPLACES {} ({})".format(self.player_in, self.player_out, self.team)
    
class SendOff:
    """Representa una expulsión durante un partido.
    """    

    def __init__(self, team:Team, player:Player) -> None:
        self.team = team
        self.player = player

    def __str__(self) -> str:
        return "SENDOFF: {} ({}) is sent off".format(self.player, self.team)
    
class Goal:
    """Representa un gol durante un partido.
    """    

    def __init__(self, team:Team, time:MatchTime) -> None:
        self.team = team
        self.time = time

    def __str__(self) -> str:
        return "GOAL: {} {}".format(self.time, self.team)
        
    

class Segment:
    """Representa un segmento de un partido según la definición de Kharrat, McHale y López Peña.
    """    

    def __init__(self, team1:Team, players1:list, team2:Team, players2:list, start:MatchTime, end:MatchTime) -> None:
        self.team1 = team1
        self.players1 = players1
        self.team2 = team2
        self.players2 = players2
        self.start = start
        self.end = end
        self.subs = []
        self.sendoffs = []
        self.home_goals = []
        self.away_goals = []

    def close(self, end:MatchTime):
        """Asigna un tiempo final al segmento.

        Arguments:
            end -- El tiempo final del segmento.
        """        
        self.end = end

    def add_sub(self, sub:Substitution):
        """Agrega una sustitución al segmento. Estas sustituciones se considera que
        finalizan el segmento, no lo inician.

        Arguments:
            sub -- la sustitución a agregar
        """        
        self.subs.append(sub)

    def add_sendoff(self, so:SendOff):
        self.sendoffs.append(so)

    def apply_subs(self, matchtime:MatchTime):
        """Hace efectivas las sustituciones del segmento. En otras palabras,
        genera un nuevo segmento tal que las sustituciones fueron aplicadas.

        Arguments:
            matchtime -- el momento en que ocurren las sustituciones

        Returns:
            Un nuevo segmento con los mismos equipos, los jugadores modificados,
            con tiempo de inicio igual al tiempo en que se realizan las sustituciones.
        """        
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

        for so in self.sendoffs:
            if so.team == self.team1:
                new_players1.remove(so.player)
            if so.team == self.team2:
                new_players2.remove(so.player)

        return Segment(self.team1, new_players1, self.team2, new_players2, matchtime, DefaultMatchTime())
    
    
    def print(self, f):
        """Imprime información del segmento a un archivo.

        Arguments:
            f -- el archivo en el que se guardará la información del segmento.
        """

        print("{}:".format(self.team1), file=f)
        for p in self.players1:
            print("\t{}".format(p), file=f)
        print(file=f)
        print("{}:".format(self.team2), file=f)
        for p in self.players2:
            print("\t{}".format(p), file=f)
        print("Start: {}".format(self.start), file=f)
        print("End: {}".format(self.end), file=f)
        
        print("HOME GOALS:", file=f)
        for hg in self.home_goals:
            print("\t{}".format(hg), file=f)
        print("AWAY GOALS:", file=f)
        for ag in self.away_goals:
            print("\t{}".format(ag), file=f)
        print("DIFF: {}".format(self.goal_difference()), file=f)

        for sub in self.subs:
            print(sub, file=f)
        for so in self.sendoffs:
            print(so, file=f)

    def contains_player_home(self, player:Player):
        """Determina si un jugador jugó por el equipo local durante este segmento.

        Arguments:
            player -- el jugador por el que se está consultando

        Returns:
            True si el jugador jugó por el equipo local durante el segmento, False si no
        """        
        return player in self.players1
    
    def contains_player_away(self, player:Player):
        """Determina si un jugador jugó por el equipo visitante durante este segmento.

        Arguments:
            player -- el jugador por el que se está consultando

        Returns:
            True si el jugador jugó por el equipo visitante durante el segmento, False si no
        """ 
        return player in self.players2
    
    def add_goal(self, goal:Goal):
        """Agrega un gol a la lista de goles que ocurrieron durante este segmento.

        Arguments:
            goal -- El gol que se desea agregar.
        """        
        if goal.team == self.team1:
            self.home_goals.append(goal)
        elif goal.team == self.team2:
            self.away_goals.append(goal)

    def goal_difference(self):
        """Calcula la diferencia enrte los goles anotados por el equipo local y
        los goles anotados por el equipo visitante durante este segmento.

        Returns:
            La diferencia de goles calculada.
        """        
        return len(self.home_goals) - len(self.away_goals)
    
    def contains(self, goal:Goal):
        """Determina si un gol ocurrió durante este segmento. Es decir, si el gol ocurrió
        entre los tiempos de inicio y fin de este segmento.

        Arguments:
            goal -- El gol a consultar

        Returns:
            True si el gol ocurrió durante este segmento, False si no
        """        
        return goal.time.absolute_time() >= self.start.absolute_time() and goal.time.absolute_time() < self.end.absolute_time()
    
    def start_minute(self):
        """Entrega el minuto en que se inició este segmento.
        """        
        return self.start.minute()
    
    def end_minute(self):
        """Entrega el minuto en que terminó este segmento.
        """        
        return self.end.minute()

            
