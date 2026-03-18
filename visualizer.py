import streamlit.components.v1 as components

def draw_petri_dish(counts):
    # Colores sólidos y vibrantes para máxima visibilidad
    colors = {
        'Cooperador': '#3498db', # Azul
        'Tramposo': '#e74c3c',   # Rojo
        'Recíproco': '#9b59b6',  # Púrpura
        'Rencoroso': '#f1c40f',  # Amarillo
        'Detective': '#2ecc71'   # Verde
    }
    
    # Preparamos los datos
    particles_data = []
    for estrategia, count in counts.items():
        if estrategia in colors:
            particles_data.append(f"{{ color: '{colors[estrategia]}', count: {count} }}")
    
    json_data = "[" + ", ".join(particles_data) + "]"

    # Código HTML/JS de alta visibilidad (como el de ayer)
    html_template = """
    <body style="margin: 0; padding: 0; background: #1a1a1a; overflow: hidden;">
        <canvas id="simCanvas" width="700" height="250" style="background:#1a1a1a; border-radius:8px;"></canvas>
        <script>
            const canvas = document.getElementById('simCanvas');
            const ctx = canvas.getContext('2d');
            const data = REPLACE_ME_DATA;
            let particles = [];

            class Particle {
                constructor(color) {
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.vx = (Math.random() - 0.5) * 4;
                    this.vy = (Math.random() - 0.5) * 4;
                    this.color = color;
                }
                update() {
                    this.x += this.vx; this.y += this.vy;
                    if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                    if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
                }
                draw() {
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, 4.5, 0, Math.PI * 2); // Puntos grandes y claros
                    ctx.fillStyle = this.color;
                    ctx.fill();
                    ctx.closePath();
                }
            }

            // Creamos las partículas inmediatamente
            data.forEach(group => {
                for(let i=0; i<group.count; i++) {
                    particles.push(new Particle(group.color));
                }
            });

            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                // Fondo sólido para evitar parpadeos blancos
                ctx.fillStyle = '#1a1a1a';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                particles.forEach(p => {
                    p.update();
                    p.draw();
                });
                requestAnimationFrame(animate);
            }
            animate();
        </script>
    </body>
    """
    
    final_html = html_template.replace("REPLACE_ME_DATA", json_data)
    return components.html(final_html, height=270)
