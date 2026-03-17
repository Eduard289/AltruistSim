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
    
    html, body, [class*="css"] {
        font-family: 'Cardo', serif;
        color: #2c3e50;
    }
    .stTitle {
        font-weight: 700;
        font-size: 2.8rem !important;
        border-bottom: 1px solid #dcdde1;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }
    .logic-box {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #2c3e50;
        margin-bottom: 25px;
        line-height: 1.6;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #7f8c8d;
        font-size: 0.9rem;
        border-top: 1px solid #eee;
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("AltruistSim: Laboratorio de Conducta Social")

# --- BLOQUE INFORMATIVO INICIAL ---
st.markdown("""
<div class="logic-box">
    <b>Propósito del Experimento:</b> Esta simulación analiza el Capital Social de una comunidad. 
    A través de la Teoría de Juegos, observamos cómo las premisas éticas individuales determinan 
    la prosperidad o el colapso de una civilización. Configure la composición inicial de su sociedad 
    en la barra lateral.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    with st.expander("📖 Definición de Roles Sociales", expanded=False):
        st.markdown("""
        * **Cooperadores:** Individuos que apuestan por el bien común de forma incondicional. Motor de la confianza pero vulnerables al parasitismo.
        * **Tramposos:** Actores que buscan maximizar su beneficio individual traicionando la confianza ajena.
        * **Recíprocos (Ojo por Ojo):** Representan la justicia distributiva; cooperan con quien coopera y sancionan la traición.
        * **Rencorosos:** Colaboradores iniciales que, ante una sola traición, pierden la confianza permanentemente.
        * **Detectives:** Estrategas que analizan el entorno para decidir si es más rentable aliarse o explotar al prójimo.
        """)

with col2:
    with st.expander("📊 Glosario de Variables", expanded=False):
        st.markdown("""
        * **Población Inicial:** Tamaño del ecosistema. Determina la masa crítica para la propagación de conductas.
        * **Tiempo Evolutivo:** Duración de la simulación. Mide la resiliencia de las normas culturales.
        * **Tasa de Cambio:** Probabilidad de nuevas ideas o mutaciones éticas en las nuevas generaciones.
        * **Costo de Existencia:** Presión del entorno. Si es alto, el altruismo se vuelve una estrategia de riesgo.
        """)

# --- CONFIGURACIÓN EN SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuración Global")
    pop_size = st.slider("Población Total", 50, 500, 200)
    generations_limit = st.slider("Tiempo Evolutivo (Generaciones)", 10, 150, 50)
    
    st.markdown("---")
    st.header("👥 Perfiles de Personalidad (%)")
    p_coop = st.slider("Cooperadores", 0, 100, 20)
    p_tram = st.slider("Tramposos", 0, 100, 20)
    p_reci = st.slider("Recíprocos", 0, 100, 20)
    p_renc = st.slider("Rencorosos", 0, 100, 20)
    p_dete = st.slider("Detectives", 0, 100, 20)
    
    total_w = p_coop + p_tram + p_reci + p_renc + p_dete
    if total_w == 0: total_w = 1

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

# --- MOTOR DE INICIALIZACIÓN ---
def inicializar_sociedad():
    poblacion = []
    counts = {
        'Cooperador': int((p_coop / total_w) * pop_size),
        'Tramposo': int((p_tram / total_w) * pop_size),
        'Recíproco': int((p_reci / total_w) * pop_size),
        'Rencoroso': int((p_renc / total_w) * pop_size),
        'Detective': int((p_dete / total_w) * pop_size)
    }
    
    idx = 0
    for est, num in counts.items():
        for _ in range(num):
            poblacion.append(Agent(idx, est))
            idx += 1
    
    while len(poblacion) < pop_size:
        poblacion.append(Agent(idx, random.choice(list(counts.keys()))))
        idx += 1
    return poblacion

# --- EJECUCIÓN DEL EXPERIMENTO ---
if st.button("▶️ Lanzar Experimento Social"):
    agents = inicializar_sociedad()
    viz_placeholder = st.empty()
    chart_placeholder = st.empty()
    history = []
    estrategias = ['Cooperador', 'Tramposo', 'Recíproco', 'Rencoroso', 'Detective']

    for g in range(generations_limit):
        agents = run_generation(agents, config)
        
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
            st.caption(f"Análisis de Datos: El eje vertical representa el Número de Individuos. El eje horizontal representa el Tiempo.")
        
        if len(agents) == 0:
            st.error("📉 **Colapso Social:** La presión del entorno ha extinguido la población.")
            break
        time.sleep(0.05)

    # --- CONCLUSIÓN DINÁMICA ---
    if len(agents) > 0:
        st.success(f"""
        ### Simulación Finalizada
        Tras {len(history)} generaciones, la sociedad ha logrado sobrevivir. La reciprocidad ha protegido la confianza mutua.
        """)
    else:
        st.warning(f"""
        ### Conclusión del Experimento
        La sociedad ha colapsado. El beneficio individual ha agotado los recursos colectivos.
        """)

# --- PIE DE PÁGINA ---
st.markdown(f"<div class='footer'>Desarrollado por Jose Luis Asenjo</div>", unsafe_allow_html=True)
