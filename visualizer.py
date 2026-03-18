import streamlit.components.v1 as components

def draw_petri_dish(counts):
    # Definimos colores para cada estrategia
    # Nota: Esta versión usa los nombres originales en inglés
    colors = {
        'Cooperator': '#3498db', # Azul
        'Cheater': '#e74c3c',    # Rojo
        'TitForTat': '#9b59b6',  # Púrpura
        'Grudger': '#f1c40f',    # Amarillo
        'Detective': '#2ecc71'   # Verde
    }
    
    # Creamos la lista de partículas para el JavaScript
    particles_js = []
    for strategy, count in counts.items():
        if strategy != 'Total' and strategy in colors:
            particles_js.append(f"{{ color: '{colors[strategy]}', count: {count} }}")
    
    js_code = f"""
    <canvas id="simCanvas" width="700" height="300" style="background:#1e1e1e; border-radius:10px;"></canvas>
    <script>
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');
        const data = [{", ".join(particles_js)}];
        let particles = [];

        class Particle {{
            constructor(color) {{
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 4;
                this.vy = (Math.random() - 0.5) * 4;
                this.color = color;
            }}
            update() {{
                this.x += this.vx; this.y += this.vy;
                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
            }}
            draw() {{
                ctx.beginPath();
                ctx.arc(this.x, this.y, 4, 0, Math.PI * 2);
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
    return components.html(js_code, height=320)
