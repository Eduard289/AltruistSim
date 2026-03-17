import streamlit as st
import pandas as pd
import time
import random
from engine import Agent, run_generation
from visualizer import draw_petri_dish

# Inyección de estilo Cardo y personalización estética
st.set_page_config(page_title="AltruistSim", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cardo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cardo', serif;
    }
    .stTitle {
        font-weight: 700;
        color: #2c3e50;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 10px;
    }
    .social-logic {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #34495e;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("AltruistSim: Laboratorio de Conducta Social")

# Explicación de la Lógica del Experimento
with st.expander("📖 Ver Lógica del Experimento Social", expanded=True):
    st.markdown("""
    <div class="social-logic">
    Este experimento simula el <b>Capital Social</b> de una comunidad. 
    Cada individuo interactúa bajo una premisa ética diferente:
    <ul>
        <li><b>Cooperadores:</b> La base de la confianza. Siempre ayudan, pero son vulnerables.</li>
        <li><b>Tramposos:</b> Buscan el beneficio individual a corto plazo, erosionando el tejido social.</li>
        <li><b>Recíprocos (Ojo por Ojo):</b> Representan la justicia distributiva. Cooperan, pero castigan la traición.</li>
        <li><b>Rencorosos:</b> Cooperan hasta que se les defrauda una sola vez; simbolizan la pérdida total de confianza.</li>
        <li><b>Detectives:</b> Analistas que evalúan si el entorno es propenso a la explotación o a la alianza.</li>
    </ul>
    La supervivencia depende de si la estructura social premia la colaboración o permite que el parasitismo colapse el sistema.
    </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Variables de Entorno")
    pop_size = st.slider("Población Inicial", 50, 400, 150)
    generations_limit = st.slider("Tiempo Evolutivo (Generaciones)", 10, 150, 50)
    mutation = st.slider("Tasa de Cambio (Mutación)", 0.0, 0.2, 0.02)
    cost = st.slider("Costo de Existencia", 1, 5, 2)
    
    config = {
        'cost_of_living': cost,
        'repro_threshold': 25,
        'mutation_rate': mutation,
        'max_age': 25
    }

if st.button("▶️ Iniciar Simulación Social"):
    estrategias = ['Cooperador', 'Tramposo', 'Recíproco', 'Rencoroso', 'Detective']
    agents = [Agent(i, random.choice(estrategias)) for i in range(pop_size)]
    
    viz_placeholder = st.empty()
    chart_placeholder = st.empty()
    history = []

    for g in range(generations_limit):
        agents = run_generation(agents, config)
        
        counts = {s: 0 for s in estrategias}
        for a in agents:
            counts[a.strategy] += 1
        history.append(counts)
        
        with viz_placeholder.container():
            st.subheader(f"Estado de la Sociedad - Generación {g+1}")
            draw_petri_dish(counts)
        
        with chart_placeholder.container():
            df = pd.DataFrame(history)
            st.line_chart(df)
            st.info(f"📊 **Interpretación del gráfico:** El eje vertical representa el **Número de Individuos** (máx. observado: {df.max().max()}). El eje horizontal representa el transcurso del **Tiempo (Generaciones)**.")
        
        if len(agents) == 0:
            st.error("📉 **Colapso Social:** La comunidad no ha podido sostenerse y se ha extinguido.")
            break
        time.sleep(0.05)

    # Conclusión final detallada
    st.success(f"""
    ### 🏁 Simulación Finalizada
    El experimento ha concluido tras {len(history)} generaciones. 
    A través de este proceso, hemos observado cómo los patrones de conducta individuales dictan el destino colectivo. 
    Una sociedad que sobrevive es aquella donde la **Reciprocidad** actúa como escudo contra el parasitismo de los **Tramposos**.
    """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #95a5a6;'>Desarrollado por Jose Luis Asenjo</div>", unsafe_allow_html=True)
