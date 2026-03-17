import streamlit as st
import pandas as pd
from engine import Agent, run_generation

st.title("🧬 AltruistSim V2")

# Sidebar con la nueva matemática
with st.sidebar:
    st.header("Configuración Evolutiva")
    pop_size = st.slider("Población Inicial", 20, 500, 100)
    mutation = st.slider("Tasa de Mutación", 0.0, 0.2, 0.05)
    repro = st.slider("Umbral Reprod. (Energía)", 15, 40, 25)
    cost = st.slider("Costo de vida", 1, 5, 2)
    max_age = st.slider("Longevidad máx.", 5, 50, 20)

config = {
    'cost_of_living': cost,
    'repro_threshold': repro,
    'mutation_rate': mutation,
    'max_age': max_age
}

if st.button("Simular"):
    strategies = ['Cooperator', 'Cheater', 'TitForTat', 'Grudger', 'Detective']
    agents = [Agent(i, random.choice(strategies)) for i in range(pop_size)]
    
    history = []
    
    # Barra de progreso
    bar = st.progress(0)
    for g in range(50): # 50 generaciones
        agents = run_generation(agents, config)
        counts = {s: 0 for s in strategies}
        for a in agents:
            counts[a.strategy] += 1
        history.append(counts)
        bar.progress((g + 1) / 50)

    df = pd.DataFrame(history)
    st.line_chart(df)
    st.write(f"Final de la simulación: {len(agents)} supervivientes.")
