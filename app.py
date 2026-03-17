import streamlit as st
import pandas as pd
from engine import Agent, run_generation

st.set_page_config(page_title="AltruistSim", layout="wide")

st.title("🧬 AltruistSim: Evolución Social")
st.sidebar.header("Parámetros de la Simulación")

# Inputs del usuario
pop_size = st.sidebar.slider("Población Inicial", 10, 200, 50)
generations = st.sidebar.slider("Generaciones", 5, 100, 20)
cost = st.sidebar.slider("Costo de Vida (Energía)", 1, 5, 2)

if st.button("Lanzar Simulación"):
    # Inicializar población mixta
    strategies = ['Cooperator', 'Cheater', 'TitForTat', 'Grudger']
    agents = [Agent(i, random.choice(strategies)) for i in range(pop_size)]
    
    stats = []

    for g in range(generations):
        agents = run_generation(agents, cost_of_living=cost)
        # Contar tipos
        counts = {s: 0 for s in strategies}
        for a in agents:
            counts[a.strategy] += 1
        counts['Total'] = len(agents)
        stats.append(counts)

    # Mostrar resultados
    df = pd.DataFrame(stats)
    st.line_chart(df[strategies])
    st.write(f"Población final: {len(agents)} agentes.")
