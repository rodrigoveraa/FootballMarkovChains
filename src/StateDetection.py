from Event import Event
from Defs import NewStates, ZONAL_STATES


"""
Definiciones de funciones para detectar distintos estados.

Todas las funciones entregan un estado y el nombre del equipo que se encuentra en ese estado.

"""

def check_goal(e1: Event, e2: Event) -> (NewStates, str):
    """
    Revisa si un evento conduce al estado GOAL.
    Puede ocurrir de dos formas:
    - Si hubo un remate que terminó en gol
    - Si se produjo un autogol a favor del equipo
    """
    if e2.type == 'Shot' and e2.outcome == 'Goal':
        return (NewStates.GOAL, e2.team)
    if e2.type == 'Own Goal For':
        return (NewStates.GOAL, e2.team)
    return (None, None)

def check_eop(e1: Event, e2: Event) -> (NewStates, str):
    """
    Revisa si se llegó al estado END_OF_POSSESSION.

    Ocurre cuando el equipo con la posesión cambia.
    Entrega el equipo que perdió la posesión.
    """
    if e1.possession_team != e2.possession_team:
        return (NewStates.END_OF_POSSESSION, e1.possession_team) 
    return (None, None)

def check_penalty(e1: Event, e2: Event) -> (NewStates, str):
    """
    Revisa si se llegó al estado PENALTY.

    Ocurre cuando se produce un remate de tipo Penalty.
    """
    if e2.type == 'Shot' and e2.shot_type == 'Penalty':
        return (NewStates.PENALTY, e2.team)
    return (None, None)

def check_free_kick(e1: Event, e2: Event) -> (NewStates, str):
    """
    Revisa si se llegó al estado FREE_KICK.

    Ocurre cuando se produce un pase o un remate de tipo Free Kick.
    """
    if e2.type == 'Shot' and e2.shot_type == 'Free Kick':
        return (NewStates.FREE_KICK, e2.team)
    if e2.type == 'Pass' and e2.shot_type == 'Free Kick':
        return (NewStates.FREE_KICK, e2.team)
    return (None, None)

def check_corner(e1: Event, e2: Event) -> (NewStates, str):
    """
    Revisa si se llegó al estado CORNER.

    Ocurre cuando se produce un pase o un remate de tipo Corner.
    """
    if e2.type == 'Pass' and e2.pass_type == 'Corner':
        return (NewStates.CORNER, e2.team)
    if e2.type == 'Shot' and e2.shot_type == 'Corner':
        return (NewStates.CORNER, e2.team)
    return (None, None)

def check_throw_in(e1: Event, e2: Event) -> (NewStates, str):
    """
    Revisa si se llegó al estado THROW_IN.

    Ocurre cuando se produce un pase de tipo Throw-in.
    """
    if e2.type == 'Pass' and e2.pass_type == 'Throw-in':
        return (NewStates.THROW_IN, e2.team)
    return (None, None)

def check_zonal_state(e1: Event, e2: Event) -> (NewStates, str):
    """
    Revisa si se está en uno de los estados zonales. Los estados zonales son estados que dependen
    de la ubicación zonal en la cancha (en cuál zona se tiene la pelota) y de la presencia o
    ausencia de presión por parte del equipo contrario.

    Sólo se revisa cuando el equipo que actúa es el mismo equipo que tiene la posesión.
    """

    if e2.team == e2.possession_team:
        zone = e2.get_zone()
        state = ZONAL_STATES.get((zone, e2.under_pressure))
        return(state, e2.team)
    
    return (None, None)