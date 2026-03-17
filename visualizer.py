import streamlit.components.v1 as components

def draw_petri_dish(counts):
    # Colores asociados a la psicología del personaje
    colors = {
        'Cooperador': '#3498db', # Azul (Confianza)
        'Tramposo': '#e74c3c',   # Rojo (Peligro)
        'Recíproco': '#9b59b6',  # Púrpura (Justicia)
        'Rencoroso': '#f1c40f',  # Amarillo (Alerta)
        'Detective': '#2ecc71'   # Verde (Estrategia)
    }
    
    particles_js = []
    for estrategia, count in counts.items():
        if estrategia in colors:
            particles_js.append(f"{{ color: '{colors[estrategia]}', count: {count} }}")
    
    js_code = f"""
    <canvas id="simCanvas" width="700" height="250" style="background:#1a1a1a; border-radius:8px;"></canvas>
    <script>
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');
        const data = [{", ".join(particles_js)}];
        let particles = [];

        class Particle {{
            constructor(color) {{
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 3;
                this.vy = (Math.random() - 0.5) * 3;
                this.color = color;
            }}
            update() {{
                this.x += this.vx; this.y += this.vy;
                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
            }}
            draw() {{
                ctx.beginPath();
                ctx.arc(this.x, this.y, 3.5, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.fill();
                ctx.closePath();
            }}
        }}

        data.forEach(group => {{
            for(let i=0; i<group.count; i++) particles.push(new Particle(group.color));
        }});

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => {{ p.update(); p.draw(); }});
            requestAnimationFrame(animate);
        }}
        animate();
    </script>
    """
    return components.html(js_code, height=270)
