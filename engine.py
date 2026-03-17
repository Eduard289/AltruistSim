import random
import numpy as np

class Agent:
    def __init__(self, id, strategy, energy=15, parent_id=None):
        self.id = id
        self.strategy = strategy
        self.energy = energy
        self.history = []
        self.last_opponent_move = 'C'
        self.age = 0

    def decide(self):
        if self.strategy == 'Cooperator': return 'C'
        if self.strategy == 'Cheater': return 'D'
        if self.strategy == 'TitForTat': return self.last_opponent_move
        if self.strategy == 'Grudger':
            return 'D' if 'D' in self.history else 'C'
        
        # Estrategia Detective: Analiza al rival los primeros 4 turnos
        if self.strategy == 'Detective':
            if len(self.history) < 4:
                return ['C', 'D', 'C', 'C'][len(self.history)]
            return self.last_opponent_move if 'D' in self.history[:4] else 'D'
        return 'C'

def run_generation(agents, config):
    """
    config: diccionario con 'cost_of_living', 'repro_threshold', 'mutation_rate', 'max_age'
    """
    random.shuffle(agents)
    payoffs = {
        ('C', 'C'): (3, 3),
        ('C', 'D'): (0, 5),
        ('D', 'C'): (5, 0),
        ('D', 'D'): (1, 1)
    }

    # 1. Duelos (Interacción Social)
    for i in range(0, len(agents) - 1, 2):
        a1, a2 = agents[i], agents[i+1]
        m1, m2 = a1.decide(), a2.decide()
        
        r1, r2 = payoffs[(m1, m2)]
        a1.energy += r1
        a2.energy += r2
        
        # Actualizar memorias
        a1.history.append(m1)
        a2.history.append(m2)
        a1.last_opponent_move = m2
        a2.last_opponent_move = m1

    # 2. Metabolismo y Selección Natural
    survivors = []
    for a in agents:
        a.energy -= config['cost_of_living']
        a.age += 1
        # Sobrevive si tiene energía y no ha superado la edad máxima
        if a.energy > 0 and a.age < config['max_age']:
            survivors.append(a)

    # 3. Reproducción y Mutación
    new_generation = []
    for s in survivors:
        new_generation.append(s)
        if s.energy >= config['repro_threshold']:
            s.energy -= 10 # Costo energético de reproducirse
            
            # Lógica de Mutación
            child_strategy = s.strategy
            if random.random() < config['mutation_rate']:
                child_strategy = random.choice(['Cooperator', 'Cheater', 'TitForTat', 'Grudger', 'Detective'])
            
            # CAMBIO AQUÍ: Usamos 1000000 (int) en lugar de 1e6 (float)
            child = Agent(random.randint(0, 1000000), child_strategy, energy=10, parent_id=s.id)
            new_generation.append(child)
            
    return new_generation
