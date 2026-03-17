import streamlit as st
import pandas as pd
import time
import random
from engine import Agent, run_generation
from visualizer import draw_petri_dish

# --- CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="AltruistSim - Jose Luis Asenjo", layout="centered")

# Inyección de CSS para tipografía Cardo y estética profesional
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cardo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cardo', serif;
        color: #2c3e50;
    }
    .stTitle {
        font-family: 'Cardo', serif;
        font-weight: 700;
        font-size: 3rem !important;
        border-bottom: 1px solid #dcdde1;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }
    .logic-box {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #2c3e50;
        margin: 10px 0 25px 0;
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

# --- TÍTULO Y EXPLICACIÓN DEL EXPERIMENTO ---
st.title("AltruistSim: Laboratorio de Conducta Social")

st.markdown("""
<div class="logic-box">
    <b>Propósito del Experimento:</b> Esta simulación analiza el Capital Social de una comunidad cerrada. 
    A través de la Teoría de Juegos, observamos cómo las premisas éticas individuales (cooperación vs. explotación) 
    determinan la prosperidad o el colapso de una civilización entera.
</div>
""", unsafe_allow_html=True)

with st.expander("📖 Conceptos de los Personajes", expanded=False):
    st.markdown("""
    * **Cooperadores:** Individuos que apuestan por el bien común de forma incondicional. Son el motor de la confianza pero vulnerables al parasitismo.
    * **Tramposos:** Actores que buscan maximizar su beneficio individual traicionando la confianza ajena.
    * **Recíprocos (Ojo por Ojo):** Representan la justicia distributiva; cooperan con quien coopera y sancionan a quien traiciona.
    * **Rencorosos:** Colaboradores iniciales que, ante una sola traición, pierden la confianza de forma permanente.
    * **Detectives:** Estrategas que analizan el entorno para decidir si es más rentable aliarse o explotar al prójimo.
    """)

with st.expander("📊 Glosario de Variables Sociales", expanded=False):
    st.markdown("""
    * **Población Inicial (Masa Crítica):** Define el tamaño del ecosistema. Determina si el anonimato favorece al tramposo o si la red social es estrecha.
    * **Tiempo Evolutivo (Legado):** Número de generaciones que se suceden. Mide la resiliencia y persistencia de las normas culturales.
    * **Tasa de Cambio (Fluidez Cultural):** Probabilidad de que surjan nuevas formas de pensar (mutaciones). Es el motor de la innovación y el riesgo social.
    * **Costo de Existencia (Escasez):** Energía necesaria para sobrevivir. En entornos de gran escasez, el altruismo se convierte en una estrategia de alto riesgo.
    """)

# --- CONFIGURACIÓN DE PARÁMETROS (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Variables de Control")
    pop_size = st.slider("Población Inicial", 50, 400, 150)
    generations_limit = st.slider("Tiempo Evolutivo", 10, 150, 50)
    mutation = st.slider("Tasa de Cambio", 0.0, 0.2, 0.02)
    cost = st.slider("Costo de Existencia", 1, 5, 2)
    
    config = {
        'cost_of_living': cost,
        'repro_threshold': 25,
        'mutation_rate': mutation,
        'max_age': 25
    }

# --- EJECUCIÓN DE LA SIMULACIÓN ---
if st.button("▶️ Iniciar Simulación Social"):
    # Inicialización de la población en español
    estrategias = ['Cooperador', 'Tramposo', 'Recíproco', 'Rencoroso', 'Detective']
    agents = [Agent(i, random.choice(estrategias)) for i in range(pop_size)]
    
    # Contenedores dinámicos
    viz_placeholder = st.empty()
    chart_placeholder = st.empty()
    
    history = []

    for g in range(generations_limit):
        # Ejecutar lógica del motor
        agents = run_generation(agents, config)
        
        # Calcular estadísticas actuales
        counts = {s: 0 for s in estrategias}
        for a in agents:
            counts[a.strategy] += 1
        history.append(counts)
        
        # Renderizado Visual del "Plato de Petri"
        with viz_placeholder.container():
            st.subheader(f"Estado de la Sociedad - Generación {g+1}")
            draw_petri_dish(counts)
        
        # Renderizado del Gráfico de Líneas
        with chart_placeholder.container():
            df = pd.DataFrame(history)
            st.line_chart(df)
            st.caption(f"Interpretación: El eje vertical (Y) indica el número de **Individuos** (Población). El eje horizontal (X) marca el **Tiempo** transcurrido en generaciones.")
        
        # Verificación de extinción
        if len(agents) == 0:
            st.error("📉 **Colapso Social:** La presión del entorno y la falta de cooperación han extinguido la población.")
            break
            
        time.sleep(0.05) # Control de velocidad de animación

    # Conclusión del Experimento
    st.success(f"""
    ### Simulación Finalizada
    Tras {len(history)} generaciones de interacción, el experimento social ha concluido. 
    Hemos observado cómo las estrategias de **Reciprocidad** suelen ser las únicas capaces de frenar el avance de los **Tramposos**, 
    creando sociedades estables. Sin una base de confianza mutua, el sistema colapsa bajo el peso del beneficio individual.
    """)

# --- PIE DE PÁGINA ---
st.markdown(f"""
    <div class="footer">
        Desarrollado por Jose Luis Asenjo<br>
        Experimento basado en Teoría de Juegos y Evolución de la Cooperación.
    </div>
""", unsafe_allow_html=True)
