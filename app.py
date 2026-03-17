import streamlit as st
import pandas as pd
import time
import random  # <--- ¡ESTA ES LA LÍNEA QUE FALTABA!
from engine import Agent, run_generation
from visualizer import draw_petri_dish

st.set_page_config(page_title="AltruistSim", layout="centered")

st.title("🧬 AltruistSim: Laboratorio Evolutivo")
st.markdown("Observa cómo las estrategias de cooperación y traición compiten por la supervivencia.")

# --- Configuración en Sidebar ---
with st.sidebar:
    st.header("⚙️ Parámetros")
    pop_size = st.slider("Población Inicial", 50, 300, 100)
    generations_limit = st.slider("Generaciones Máx.", 10, 100, 50)
    mutation = st.slider("Tasa Mutación", 0.0, 0.2, 0.05)
    cost = st.slider("Costo de vida", 1, 5, 2)
    
    config = {
        'cost_of_living': cost,
        'repro_threshold': 25,
        'mutation_rate': mutation,
        'max_age': 20
    }

# --- Ejecución de Simulación ---
if st.button("▶️ Iniciar Experimento"):
    strategies = ['Cooperator', 'Cheater', 'TitForTat', 'Grudger', 'Detective']
    # Aquí es donde usamos random:
    agents = [Agent(i, random.choice(strategies)) for i in range(pop_size)]
    
    # Espacios reservados para que la UI no salte
    viz_placeholder = st.empty()
    chart_placeholder = st.empty()
    
    history = []

    for g in range(generations_limit):
        agents = run_generation(agents, config)
        
        # Cómputo de estadísticas
        counts = {s: 0 for s in strategies}
        for a in agents:
            counts[a.strategy] += 1
        history.append(counts)
        
        # --- ACTUALIZACIÓN VISUAL ---
        with viz_placeholder.container():
            st.subheader(f"Generación {g+1}")
            draw_petri_dish(counts)
        
        with chart_placeholder.container():
            df = pd.DataFrame(history)
            st.line_chart(df)
        
        if len(agents) == 0:
            st.error("Extinción total.")
            break
            
        time.sleep(0.1) # Pausa para que el ojo humano lo siga

    st.success("Simulación finalizada.")
