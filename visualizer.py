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
    
    particles_js = []
    for estrategia, count in counts.items():
        if estrategia in colors:
            particles_js.append(f"{{ color: '{colors[estrategia]}', count: {count} }}")
    
    js_code = f"""
    <style>
        /* Animación para suavizar la carga del componente y evitar el parpadeo */
        #simCanvas {{
            animation: fadeIn 0.4s ease-in-out;
            background: #1a1a1a;
            border-radius: 8px;
            box-shadow: inset 0 0 20px #000;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0.3; }}
            to {{ opacity: 1; }}
        }}
    </style>
    
    <canvas id="simCanvas" width="700" height="250"></canvas>
    
    <script>
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');
        const data = [{", ".join(particles_js)}];
        let particles = [];

        class Particle {{
            constructor(color) {{
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 2.5;
                this.vy = (Math.random() - 0.5) * 2.5;
                this.color = color;
                this.alpha = 0; // Empiezan invisibles para un fade-in suave
            }}
            update() {{
                this.x += this.vx; this.y += this.vy;
                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
                
                // Aparecen gradualmente
                if (this.alpha < 1) this.alpha += 0.05;
            }}
            draw() {{
                ctx.beginPath();
                ctx.arc(this.x, this.y, 3.5, 0, Math.PI * 2);
                // Aplicamos la opacidad para suavizar la transición entre generaciones
                ctx.fillStyle = this.color.replace('#', 'rgba(' + 
                    parseInt(this.color.slice(1,3), 16) + ',' + 
                    parseInt(this.color.slice(3,5), 16) + ',' + 
                    parseInt(this.color.slice(5,7), 16) + ',' + 
                    this.alpha + ')');
                ctx.fill();
                ctx.closePath();
            }}
        }}

        // Poblamos el mundo
        data.forEach(group => {{
            for(let i=0; i<group.count; i++) particles.push(new Particle(group.color));
        }});

        function animate() {{
            // Usamos un ligero "rastro" en lugar de limpiar el canvas totalmente
            ctx.fillStyle = 'rgba(26, 26, 26, 0.3)'; 
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            particles.forEach(p => {{ 
                p.update(); 
                p.draw(); 
            }});
            requestAnimationFrame(animate);
        }}
        animate();
    </script>
    """
    # Reducimos ligeramente el tiempo de respuesta del componente
    return components.html(js_code, height=270)270)
