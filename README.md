# AltruistSim: A Generative Laboratory for Social Evolution & Game Theory

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://altruistsim.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Desarrollado por Jose Luis Asenjo**

---

##  La Arquitectura de la Confianza: Fundamento Sociológico

¿Es el ser humano egoísta por naturaleza o es la cooperación nuestra ventaja evolutiva definitiva? **AltruistSim** nace como una respuesta algorítmica a esta pregunta fundamental de la sociología, la filosofía política y la economía conductual.

En sociología, el **Capital Social** es el entramado invisible de confianza y reciprocidad que permite a una comunidad prosperar sin necesidad de vigilancia constante. Sin embargo, este capital es extremadamente frágil. Cuando los incentivos para el engaño (el beneficio individual a corto plazo) superan las recompensas de la colaboración, las sociedades caen en lo que se conoce como la **Tragedia de los Comunes**. 

En este estado, el individuo racional decide agotar los recursos colectivos para su propio beneficio, llevando al colapso sistémico. AltruistSim no es solo un script; es un espejo digital de este fenómeno. Transforma debates sociológicos abstractos en un **Sistema Complejo Computable** mediante la simulación basada en agentes (Agent-Based Modeling).

### Traducción de la Sociología al Código
Nuestra herramienta implementa estos conceptos mediante variables matemáticas exactas:
* **La Confianza** se traduce en **Transferencia de Energía** (Matriz de Pagos).
* **La Escasez** se modela mediante el **Costo de Existencia** (Deducción metabólica por turno).
* **El Cambio Cultural** se simula a través de la **Tasa de Mutación** intergeneracional.

---

## El Ecosistema Ético: Perfiles y Heurística

La simulación somete a la población al **Dilema del Prisionero Iterado**. Cada individuo en el sistema opera bajo una heurística moral inmutable durante su vida, determinando cómo interactúa con sus pares. 

### 1. Cooperador (Altruismo Incondicional)
* **Perfil Social:** El motor de la riqueza comunitaria. Aporta valor al grupo de forma sistemática asumiendo que los demás harán lo mismo.
* **Vulnerabilidad:** Es la presa natural del parásito social. En sistemas sin mecanismos de justicia, el cooperador agota su energía y se extingue, llevándose consigo el capital social.

### 2. Tramposo (Egoísmo Racional)
* **Perfil Social:** Maximizador de utilidad a corto plazo. Extrae valor del sistema sin aportar nada a cambio.
* **Impacto Sistémico:** Funciona como un depredador. Su éxito inicial es explosivo, pero lleva la semilla de su propia destrucción: si elimina a todos los cooperadores, se queda sin "huéspedes" a los que explotar, provocando el colapso demográfico.

### 3. Recíproco (Justicia Distributiva / Ojo por Ojo)
* **Perfil Social:** El sistema inmunológico de la sociedad. Inicia cooperando, pero tiene memoria y replica el último movimiento de su adversario.
* **Estabilidad:** Es la estrategia evolutiva más robusta. Permite la formación de clústeres de confianza al tiempo que aísla y penaliza a los tramposos, haciendo que el egoísmo deje de ser rentable.

### 4. Rencoroso (Tolerancia Cero)
* **Perfil Social:** Representa la confianza frágil. Coopera incondicionalmente hasta que sufre una sola traición. A partir de ese momento, retira su colaboración para siempre.
* **Efecto:** En entornos con alta mutación (ruido social), el rencoroso termina paralizando el ecosistema al negarse a reanudar la cooperación.

### 5. Detective (Oportunismo Calculado)
* **Perfil Social:** El estratega analítico. Evalúa a su contraparte con una secuencia de prueba. Si detecta pasividad, se convierte en un explotador; si detecta resistencia, se pliega a las normas de reciprocidad.

---

## Arquitectura Técnica

El software está diseñado bajo una arquitectura de tres capas para garantizar rendimiento y fluidez visual, incluso con cientos de agentes en pantalla.

* **Capa Lógica (Python / engine.py):** Motor algorítmico puro. Procesa los emparejamientos estocásticos, resuelve las matrices de pago, aplica el decaimiento metabólico (costo de vida) y ejecuta el algoritmo genético de reproducción y mutación.
* **Capa Visual (JavaScript Canvas / visualizer.py):** Para sortear el cuello de botella de renderizado del servidor de Streamlit, la visualización del "plato de Petri" se delega al cliente mediante HTML5 Canvas. Esto permite interpolación fluida a 60 FPS sin parpadeos ni carga asíncrona pesada.
* **Interfaz de Control (Streamlit / app.py):** Dashboard reactivo que permite inyectar perturbaciones en el ecosistema en tiempo real, modificando parámetros macroeconómicos (presión del entorno) y demográficos.

---

## Instalación y Despliegue Local

Para ejecutar este laboratorio social en tu propia máquina y testear diferentes hipótesis de comportamiento:

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/altruistsim.git](https://github.com/tu-usuario/altruistsim.git)
   cd altruistsim

   Instala las dependencias requeridas (asegúrate de usar un entorno virtual)           pip install -r requirements.txt

   Inicia el servidor local de Streamlit:    streamlit run app.py


A través de AltruistSim, demostramos de forma matemática que el egoísmo puro es una estrategia autodestructiva a nivel macroscópico. La supervivencia a largo plazo de una sociedad sometida a la escasez de recursos no depende de la bondad ingenua, sino de la reciprocidad estructurada: la capacidad de una comunidad para castigar la traición y crear círculos virtuosos de cooperación.

Proyecto de código abierto bajo licencia MIT. Las contribuciones, bifurcaciones y debates sociológicos son bienvenidos.
