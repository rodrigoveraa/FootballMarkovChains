import random

# Este script genera un set de probabilidades para cada minuto del partido,'
# de la forma [P_HW, P_D, P_AW], donde
# P_HW es la probabilidad de que el equipo local gane,
# P_D es la probabilidad de que el partido termine empatado, 
# P_AW es la probabilidad de que el equipo visitante gane,
# todo en el minuto t.


PROBS = {
    'HW': 0,
    'D': 1,
    'AW': 2
}

MATCH_LENGTH = 90
DEFAULT_VARIATION = 0.05

# Genera una lista de probabilidades de un cierto largo
# La suma de la lista es 1
def generate_probs(amount):
    probs = [random.random() for x in range(amount)]
    
    return [probs[i]/sum(probs) for i in range(len(probs))]

# Toma una lista de valores y le suma un valor aleatorio a cada elemento
# El valor sumado es distinto para cada elemento y está enre -var y var
# El valor resultante no puede ser menor a 0
def vary_probs(probs, var):
    vars = []
    for p in probs:
        new_var = p + random.uniform(-var, var)
        new_p = new_var if new_var > 0 else 0
        vars.append(new_p)

    return [x/sum(vars) for x in vars]



# Generamos probabilidades hasta que P_HW > P_AW > P_D
def generate_all_probs(length, variation):
    while True:
        # Tripleta de probabilidades mencionada en el paper
        a = [0.46, 0.26, 0.28]
        all_probs = []
        all_probs.append(a)

        for i in range(1, length):
            a = vary_probs(a, variation)
            all_probs.append(a)

        if all_probs[-1][PROBS['HW']] > all_probs[-1][PROBS['AW']] and all_probs[-1][PROBS['AW']] > all_probs[-1][PROBS['D']]:
            return all_probs




