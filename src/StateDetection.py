from Event import Event
from Defs import NewStates


def check_goal(e1: Event, e2: Event) -> (NewStates, str):
    if e2.type == 'Shot' and e2.outcome == 'Goal':
        return (NewStates.GOAL, e2.team)
    if e2.type == 'Own Goal For':
        return (NewStates.GOAL, e2.team)
    return (None, None)

def check_eop(e1: Event, e2: Event) -> (NewStates, str):
    if e1.possession_team != e2.possession_team:
        return (NewStates.END_OF_POSSESSION, e1.possession_team) 
    return (None, None)

def check_penalty(e1: Event, e2: Event) -> (NewStates, str):
    if e2.type == 'Shot' and e2.shot_type == 'Penalty':
        return (NewStates.PENALTY, e2.team)
    return (None, None)

def check_free_kick(e1: Event, e2: Event) -> (NewStates, str):
    if e2.type == 'Shot' and e2.shot_type == 'Free Kick':
        return (NewStates.FREE_KICK, e2.team)
    if e2.type == 'Pass' and e2.shot_type == 'Free Kick':
        return (NewStates.FREE_KICK, e2.team)
    return (None, None)

def check_corner(e1: Event, e2: Event) -> (NewStates, str):
    if e2.type == 'Pass' and e2.pass_type == 'Corner':
        return (NewStates.CORNER, e2.team)
    if e2.type == 'Shot' and e2.shot_type == 'Corner':
        return (NewStates.CORNER, e2.team)
    return (None, None)

def check_throw_in(e1: Event, e2: Event) -> (NewStates, str):
    if e2.type == 'Pass' and e2.pass_type == 'Throw-in':
        return (NewStates.THROW_IN, e2.team)
    return (None, None)