import streamlit as st
import pandas as pd
import time
import random
from engine import Agent, run_generation
from visualizer import draw_petri_dish

# --- CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="AltruistSim - Jose Luis Asenjo", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cardo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cardo', serif; color: #2c3e50; }
    .stTitle { font-weight: 700; border-bottom: 1px solid #dcdde1; padding-bottom: 15px; }
    .logic-box { background-color: #f9f9f9; padding: 20px; border-radius: 8px; border-left: 4px solid #2c3e50; margin-bottom: 25px; }
    .footer { text-align: center; margin-top: 50px; color: #7f8c8d; font-size: 0.9rem; border-top: 1px solid #eee; padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("AltruistSim: Laboratorio de Conducta Social")

st.markdown("""
<div class="logic-box">
    <b>Configuración de Partida:</b> Ahora puedes definir la composición ética inicial de tu sociedad. 
    Ajusta los porcentajes en la barra lateral para observar cómo influye la configuración inicial en la supervivencia colectiva.
</div>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN EN SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuración Global")
    pop_size = st.slider("Población Total", 50, 500, 200)
    generations_limit = st.slider("Tiempo Evolutivo (Generaciones)", 10, 150, 50)
    
    st.markdown("---")
    st.header("👥 Composición de la Sociedad (%)")
    p_coop = st.slider("Cooperadores", 0, 100, 20)
    p_tram = st.slider("Tramposos", 0, 100, 20)
    p_reci = st.slider("Recíprocos", 0, 100, 20)
    p_renc = st.slider("Rencorosos", 0, 100, 20)
    p_dete = st.slider("Detectives", 0, 100, 20)
    
    # Normalización automática de pesos
    total_weights = p_coop + p_tram + p_reci + p_renc + p_dete
    if total_weights == 0: total_weights = 1 # Evitar división por cero

    st.markdown("---")
    st.header("🌍 Reglas del Entorno")
    mutation = st.slider("Tasa de Cambio (Mutación)", 0.0, 0.2, 0.02)
    cost = st.slider("Costo de Existencia", 1, 5, 2)
    
    config = {
        'cost_of_living': cost,
        'repro_threshold': 25,
        'mutation_rate': mutation,
        'max_age': 25
    }

# --- LÓGICA DE INICIALIZACIÓN DE AGENTES ---
def crear_poblacion():
    poblacion = []
    # Calculamos cuántos agentes de cada tipo basándonos en los sliders
    counts = {
        'Cooperador': int((p_coop / total_weights) * pop_size),
        'Tramposo': int((p_tram / total_weights) * pop_size),
        'Recíproco': int((p_reci / total_weights) * pop_size),
        'Rencoroso': int((p_renc / total_weights) * pop_size),
        'Detective': int((p_dete / total_weights) * pop_size)
    }
    
    idx = 0
    for est, num in counts.items():
        for _ in range(num):
            poblacion.append(Agent(idx, est))
            idx += 1
            
    # Rellenar si por redondeo falta alguno para llegar a pop_size
    while len(poblacion) < pop_size:
        poblacion.append(Agent(idx, random.choice(list(counts.keys()))))
        idx += 1
    return poblacion

# --- EJECUCIÓN ---
if st.button("▶️ Lanzar Experimento Social"):
    agents = crear_poblacion()
    viz_placeholder = st.empty()
    chart_placeholder = st.empty()
    history = []
    estrategias = ['Cooperador', 'Tramposo', 'Recíproco', 'Rencoroso', 'Detective']

    for g in range(generations_limit):
        agents = run_generation(agents, config)
        
        # Estadísticas
        current_counts = {s: 0 for s in estrategias}
        for a in agents:
            current_counts[a.strategy] += 1
        history.append(current_counts)
        
        with viz_placeholder.container():
            st.subheader(f"Estado de la Sociedad - Generación {g+1}")
            draw_petri_dish(current_counts)
        
        with chart_placeholder.container():
            df = pd.DataFrame(history)
            st.line_chart(df)
            st.caption(f"Eje Y: Población | Eje X: Tiempo. Población actual: {len(agents)} agentes.")
        
        if len(agents) == 0:
            st.error("📉 **Colapso Social:** La falta de cohesión y el costo de vida han extinguido la sociedad.")
            break
        time.sleep(0.05)

    st.success("### Simulación Finalizada")

st.markdown(f"<div class='footer'>Desarrollado por Jose Luis Asenjo</div>", unsafe_allow_html=True)
