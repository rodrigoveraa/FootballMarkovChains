from enum import Enum, auto, unique

import itertools

# estados antiguos, no se usan actualmente
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


STATE_TUPLES = list(itertools.product(ZONES, UNDER_PRESSURE, PLAY_TYPE))

ZONAL_STATES = dict(zip(STATE_TUPLES, list(NewStates)[6:]))