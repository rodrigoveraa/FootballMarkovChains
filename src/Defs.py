from enum import Enum, auto, unique

import itertools


STATES = {
                'GOAL': 0,
                'END_OF_POSSESSION': 1,
                'PENALTY': 2,
                'SHORT_CORNER': 3,
                'LONG_CORNER': 4,
                'SHORT_FREE_KICK': 5,
                'LONG_FREE_KICK': 6,
                'SHALLOW_THROW_IN': 7,
                'DEEP_THROW_IN': 8,
                'S01': 9,
                'S02': 10,
                'S03': 11,
                'S04': 12,
                'S05': 13,
                'S06': 14,
                'S07': 15,
                'S08': 16,
                'S09': 17,
                'S10': 18,
                'S11': 19,
                'S12': 20,
                'S13': 21,
                'S14': 22,
                'S15': 23,
                'S16': 24,
                'S17': 25,
                'S18': 26,
                'S19': 27,
                'S20': 28,
                'S21': 29,
                'S22': 30,
                'S23': 31,
                'S24': 32,
                'S25': 33,
                'S26': 34,
                'S27': 35,
                'S28': 36,
                'S29': 37,
                'S30': 38
            }
# @unique
# class NewStates(Enum):
#     GOAL = 1
#     END_OF_POSSESSION = 2
#     PENALTY = 3
#     FREE_KICK = 4
#     CORNER = 5
#     THROW_IN = 6
#     DEF_LW = 7
#     DEF_LW_P = 8
#     DEF_C = 9
#     DEF_C_P = 10
#     DEF_RW = 11
#     DEF_RW_P = 12
#     M_LW = 13
#     M_LW_P = 14
#     M_C = 15
#     M_C_P = 16
#     M_RW = 17
#     M_RW_P = 18
#     OFF_LW = 19
#     OFF_LW_P = 20
#     OFF_C = 21
#     OFF_C_P = 22
#     OFF_RW = 23
#     OFF_RW_P = 24
#     P_BOX = 25
#     P_BOX_P = 26

STATE_NAME_LIST = [
    'GOAL',
    'END_OF_POSSESSION',
    'PENALTY',
    'FREE_KICK',
    'CORNER',
    'THROW_IN',
    'Z0_P_OP',
    'Z0_P_SP',
    'Z0_P_C',
    'Z0_NP_OP',
    'Z0_NP_SP',
    'Z0_NP_C',
    'Z1_P_OP',
    'Z1_P_SP',
    'Z1_P_C',
    'Z1_NP_OP',
    'Z1_NP_SP',
    'Z1_NP_C',
    'Z2_P_OP',
    'Z2_P_SP',
    'Z2_P_C',
    'Z2_NP_OP',
    'Z2_NP_SP',
    'Z2_NP_C',
    'Z3_P_OP',
    'Z3_P_SP',
    'Z3_P_C',
    'Z3_NP_OP',
    'Z3_NP_SP',
    'Z3_NP_C',
    'Z4_P_OP',
    'Z4_P_SP',
    'Z4_P_C',
    'Z4_NP_OP',
    'Z4_NP_SP',
    'Z4_NP_C',
    'Z5_P_OP',
    'Z5_P_SP',
    'Z5_P_C',
    'Z5_NP_OP',
    'Z5_NP_SP',
    'Z5_NP_C',
    'Z6_P_OP',
    'Z6_P_SP',
    'Z6_P_C',
    'Z6_NP_OP',
    'Z6_NP_SP',
    'Z6_NP_C'
]


    
# @unique    
# class ZONES(Enum):
#     PENALTY_BOX = auto()
#     OFF_LW = auto()
#     OFF_C = auto()
#     OFF_RW = auto()
#     M_LW = auto()
#     M_C = auto()
#     M_RW = auto()
#     DEF_LW = auto()
#     DEF_C = auto()
#     DEF_RW = auto()
#     NONE = auto()

@unique
class ZONES(Enum):
    Z0 = auto()
    Z1 = auto()
    Z2 = auto()
    Z3 = auto()
    Z4 = auto()
    Z5 = auto()
    Z6 = auto()
    NONE = auto()

class UNDER_PRESSURE(Enum):
    YES = auto()
    NO = auto()

class PLAY_TYPE(Enum):
    OPEN_PLAY = auto()
    SET_PIECE = auto()
    COUNTER = auto()

NewStates = Enum('NewStates', STATE_NAME_LIST)


# ZONAL_STATES = {
#     (ZONES.PENALTY_BOX, True): NewStates.P_BOX_P,
#     (ZONES.PENALTY_BOX, False): NewStates.P_BOX,
#     (ZONES.OFF_LW, True): NewStates.OFF_LW_P,
#     (ZONES.OFF_LW, False): NewStates.OFF_LW,
#     (ZONES.OFF_C, True): NewStates.OFF_C_P,
#     (ZONES.OFF_C, False): NewStates.OFF_C,
#     (ZONES.OFF_RW, True): NewStates.OFF_RW_P,
#     (ZONES.OFF_RW, False): NewStates.OFF_RW,
#     (ZONES.M_LW, True): NewStates.M_LW_P,
#     (ZONES.M_LW, False): NewStates.M_LW,
#     (ZONES.M_C, True): NewStates.M_C_P,
#     (ZONES.M_C, False): NewStates.M_C,
#     (ZONES.M_RW, True): NewStates.M_RW_P,
#     (ZONES.M_RW, False): NewStates.M_RW,
#     (ZONES.DEF_LW, True): NewStates.DEF_LW_P,
#     (ZONES.DEF_LW, False): NewStates.DEF_LW,
#     (ZONES.DEF_C, True): NewStates.DEF_C_P,
#     (ZONES.DEF_C, False): NewStates.DEF_C,
#     (ZONES.DEF_RW, True): NewStates.DEF_RW_P,
#     (ZONES.DEF_RW, False): NewStates.DEF_RW,
# }

STATE_TUPLES = list(itertools.product(ZONES, UNDER_PRESSURE, PLAY_TYPE))

ZONAL_STATES = dict(zip(STATE_TUPLES, list(NewStates)[6:]))