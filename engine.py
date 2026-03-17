import random

# Definición de la matriz de pagos (Payoff Matrix)
# T: Tentación, R: Recompensa, P: Castigo, S: Sufrimiento
PAYOFFS = {
    ('C', 'C'): (3, 3),  # Ambos cooperan
    ('C', 'D'): (0, 5),  # Tú cooperas, el otro traiciona
    ('D', 'C'): (5, 0),  # Tú traicionas, el otro coopera
    ('D', 'D'): (1, 1)   # Ambos traicionan
}

class Agent:
    def __init__(self, id, strategy, energy=10):
        self.id = id
        self.strategy = strategy  # 'Cooperator', 'Cheater', 'TitForTat', 'Grudger'
        self.energy = energy
        self.history = []
        self.last_opponent_move = 'C'

    def decide(self):
        if self.strategy == 'Cooperator':
            return 'C'
        if self.strategy == 'Cheater':
            return 'D'
        if self.strategy == 'TitForTat':
            return self.last_opponent_move
        if self.strategy == 'Grudger':
            return 'D' if 'D' in self.history else 'C'
        return 'C'

def run_generation(agents, cost_of_living=1):
    random.shuffle(agents)
    # Emparejamiento y duelo
    for i in range(0, len(agents) - 1, 2):
        a1, a2 = agents[i], agents[i+1]
        move1, move2 = a1.decide(), a2.decide()
        
        p1, p2 = PAYOFFS[(move1, move2)]
        a1.energy += p1
        a2.energy += p2
        
        a1.history.append(move1)
        a2.history.append(move2)
        a1.last_opponent_move = move2
        a2.last_opponent_move = move1

    # Supervivencia y Reproducción
    new_population = []
    for a in agents:
        a.energy -= cost_of_living
        if a.energy > 0:
            new_population.append(a)
            # Reproducción si tiene mucha energía
            if a.energy > 20:
                a.energy -= 10
                new_population.append(Agent(random.randint(0,10000), a.strategy))
    
    return new_population
