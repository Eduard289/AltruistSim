import random

class Agent:
    """
    Representa a un individuo en la simulación social con una 
    estrategia de comportamiento específica.
    """
    def __init__(self, id, strategy, energy=15, parent_id=None):
        self.id = id
        self.strategy = strategy
        self.energy = energy
        self.history = []
        self.last_opponent_move = 'C'  # Por defecto empieza cooperando
        self.age = 0

    def decide(self):
        """
        Determina la acción del agente ('C' para Cooperar, 'D' para Defraudar/Traicionar)
        basándose en su personalidad (estrategia).
        """
        # 1. Cooperador: Siempre ayuda, pase lo que pase.
        if self.strategy == 'Cooperador': 
            return 'C'
        
        # 2. Tramposo: Siempre busca el beneficio propio traicionando.
        if self.strategy == 'Tramposo': 
            return 'D'
        
        # 3. Recíproco (Ojo por Ojo): Hace lo que le hicieron en el turno anterior.
        if self.strategy == 'Recíproco': 
            return self.last_opponent_move
        
        # 4. Rencoroso: Coopera hasta que le traicionan una sola vez. Luego nunca olvida.
        if self.strategy == 'Rencoroso':
            return 'D' if 'D' in self.history else 'C'
        
        # 5. Detective: Analiza al rival. Si detecta debilidad, explota. Si no, coopera.
        if self.strategy == 'Detective':
            if len(self.history) < 4:
                # Secuencia de prueba: Cooperar, Traicionar, Cooperar, Cooperar
                return ['C', 'D', 'C', 'C'][len(self.history)]
            # Si el oponente le traicionó en la prueba, juega como Recíproco
            if 'D' in self.history[:4]:
                return self.last_opponent_move
            # Si el oponente fue siempre bueno, el Detective se vuelve Tramposo para explotarlo
            return 'D'
            
        return 'C'

def run_generation(agents, config):
    """
    Ejecuta una iteración completa del experimento social:
    Interacción, Metabolismo, Selección Natural y Reproducción.
    """
    # Mezclamos la población para encuentros aleatorios
    random.shuffle(agents)
    
    # Matriz de pagos (Dilema del Prisionero)
    # (Acción A, Acción B) : (Puntos A, Puntos B)
    payoffs = {
        ('C', 'C'): (3, 3), # Cooperación mutua
        ('C', 'D'): (0, 5), # Explotación del cooperador
        ('D', 'C'): (5, 0), # Beneficio del tramposo
        ('D', 'D'): (1, 1)  # Conflicto mutuo
    }

    # --- 1. Fase de Interacción Social ---
    for i in range(0, len(agents) - 1, 2):
        a1, a2 = agents[i], agents[i+1]
        m1, m2 = a1.decide(), a2.decide()
        
        r1, r2 = payoffs[(m1, m2)]
        a1.energy += r1
        a2.energy += r2
        
        # Registro de memoria para estrategias con historial
        a1.history.append(m1)
        a2.history.append(m2)
        a1.last_opponent_move = m2
        a2.last_opponent_move = m1

    # --- 2. Fase de Metabolismo y Supervivencia ---
    # Aplicamos el costo de vida y filtramos a los que mueren por falta de energía o vejez
    survivors = []
    for a in agents:
        a.energy -= config['cost_of_living']
        a.age += 1
        if a.energy > 0 and a.age < config['max_age']:
            survivors.append(a)

    # --- 3. Fase de Reproducción y Mutación ---
    new_generation = []
    for s in survivors:
        new_generation.append(s) # El progenitor sobrevive
        
        # Si tiene suficiente energía, genera un descendiente
        if s.energy >= config['repro_threshold']:
            s.energy -= 10 # Costo biológico de la reproducción
            
            # Lógica de Mutación (Cambio de valores sociales en el hijo)
            child_strategy = s.strategy
            if random.random() < config['mutation_rate']:
                child_strategy = random.choice(['Cooperador', 'Tramposo', 'Recíproco', 'Rencoroso', 'Detective'])
            
            # Crear el nuevo individuo con ID único entero
            child = Agent(
                id=random.randint(0, 1000000), 
                strategy=child_strategy, 
                energy=10, 
                parent_id=s.id
            )
            new_generation.append(child)
            
    return new_generation
