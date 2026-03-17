import streamlit.components.v1 as components

def draw_petri_dish(counts):
    # Colores asociados a la psicología del personaje
    colors = {
        'Cooperador': '#3498db', # Azul
        'Tramposo': '#e74c3c',   # Rojo
        'Recíproco': '#9b59b6',  # Púrpura
        'Rencoroso': '#f1c40f',  # Amarillo
        'Detective': '#2ecc71'   # Verde
    }
    
    # Preparamos los datos de las partículas
    particles_data = []
    for estrategia, count in counts.items():
        if estrategia in colors:
            color = colors[estrategia]
            particles_data.append(f"{{ color: '{color}', count: {count} }}")
    
    # Unimos los datos en una cadena para JS
    json_data = "[" + ", ".join(particles_data) + "]"

    # El código HTML/JS puro (Sin f-string para evitar errores de llaves {})
    html_template = """
    <style>
        #simCanvas {
            animation: fadeIn 0.6s ease-in-out;
            background: #1a1a1a;
            border-radius: 8px;
            box-shadow: inset 0 0 20px #000;
        }
        @keyframes fadeIn {
            from { opacity: 0.2; }
            to { opacity: 1; }
        }
    </style>
    
    <canvas id="simCanvas" width="700" height="250"></canvas>
    
    <script>
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');
        const rawData = REPLACE_ME_DATA;
        let particles = [];

        class Particle {
            constructor(color) {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 2;
                this.vy = (Math.random() - 0.5) * 2;
                this.color = color;
                this.alpha = 0;
            }
            update() {
                this.x += this.vx; this.y += this.vy;
                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
                if (this.alpha < 1) this.alpha += 0.05;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, 3.5, 0, Math.PI * 2);
                // Convertir HEX a RGBA de forma manual para el efecto suavizado
                const r = parseInt(this.color.slice(1,3), 16);
                const g = parseInt(this.color.slice(3,5), 16);
                const b = parseInt(this.color.slice(5,7), 16);
                ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${this.alpha})`;
                ctx.fill();
                ctx.closePath();
            }
        }

        // Crear partículas
        rawData.forEach(group => {
            for(let i=0; i<group.count; i++) {
                particles.push(new Particle(group.color));
            }
        });

        function animate() {
            // Fondo con estela suave
            ctx.fillStyle = 'rgba(26, 26, 26, 0.4)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            particles.forEach(p => {
                p.update();
                p.draw();
            });
            requestAnimationFrame(animate);
        }
        animate();
    </script>
    """
    
    # Insertamos los datos en el template de forma segura
    final_html = html_template.replace("REPLACE_ME_DATA", json_data)
    
    return components.html(final_html, height=270)
