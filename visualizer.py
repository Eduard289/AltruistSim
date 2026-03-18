import streamlit.components.v1 as components

def draw_petri_dish(counts):
    # Mantenemos los colores psicológicos de tus personajes
    colors = {
        'Cooperador': '#3498db', # Azul (Confianza)
        'Tramposo': '#e74c3c',   # Rojo (Peligro)
        'Recíproco': '#9b59b6',  # Púrpura (Justicia)
        'Rencoroso': '#f1c40f',  # Amarillo (Alerta)
        'Detective': '#2ecc71'   # Verde (Estrategia)
    }
    
    # Preparamos los datos de las partículas de forma segura
    particles_data = []
    for estrategia, count in counts.items():
        if estrategia in colors:
            color = colors[estrategia]
            particles_data.append(f"{{ color: '{color}', count: {count} }}")
    
    json_data = "[" + ", ".join(particles_data) + "]"

    # El código HTML/JS optimizado para máxima visibilidad
    html_template = """
    <style>
        /* Mantenemos la tipografía Cardo para coherencia visual */
        @import url('https://fonts.googleapis.com/css2?family=Cardo:wght@400;700&display=swap');
        
        body { margin: 0; padding: 0; background: #1a1a1a; overflow: hidden; font-family: 'Cardo', serif; }
        
        #simCanvas {
            display: block;
            background: #1a1a1a;
            border-radius: 8px;
            box-shadow: inset 0 0 20px #000;
            /* Suavizamos la aparición del canvas entero, no de los puntos */
            animation: fadeInCanvas 0.3s ease-in-out;
        }
        @keyframes fadeInCanvas {
            from { opacity: 0.5; }
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
                // Velocidad equilibrada: ni muy estática ni muy frenética
                this.vx = (Math.random() - 0.5) * 2.2;
                this.vy = (Math.random() - 0.5) * 2.2;
                this.color = color;
                // CORRECCIÓN 1: Empiezan con opacidad total (1) para asegurar visibilidad inmediata
                this.alpha = 1; 
            }
            update() {
                this.x += this.vx; this.y += this.vy;
                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
            }
            draw() {
                ctx.beginPath();
                // CORRECCIÓN 2: Puntos ligeramente más grandes (3.5 -> 3.9) para el vídeo
                ctx.arc(this.x, this.y, 3.9, 0, Math.PI * 2);
                
                const r = parseInt(this.color.slice(1,3), 16);
                const g = parseInt(this.color.slice(3,5), 16);
                const b = parseInt(this.color.slice(5,7), 16);
                ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${this.alpha})`;
                ctx.fill();
                ctx.closePath();
            }
        }

        rawData.forEach(group => {
            for(let i=0; i<group.count; i++) {
                particles.push(new Particle(group.color));
            }
        });

        function animate() {
            // CORRECCIÓN 3: Rastro de movimiento reducido drásticamente (0.9 de opacidad de limpieza)
            // Esto mantiene la fluidez pero asegura que los puntos viejos desaparezcan rápido
            // y los nuevos sean perfectamente visibles sobre el fondo oscuro.
            ctx.fillStyle = 'rgba(26, 26, 26, 0.9)'; 
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
    
    # Insertamos los datos en el template de forma segura (sin f-strings propensos a errores)
    final_html = html_template.replace("REPLACE_ME_DATA", json_data)
    
    return components.html(final_html, height=270)
