import streamlit as st
import streamlit.components.v1 as components

# Configuración de página ancha
st.set_page_config(page_title="Sabores de Colombia", layout="wide")

# Eliminamos márgenes de Streamlit para que el juego ocupe bien el espacio
st.markdown("""
    <style>
    .block-container { padding: 0rem; }
    iframe { border: none; }
    </style>
    """, unsafe_allow_html=True)

html_comidas_corregido = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600&family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --col-yellow: #FFCD00;
            --col-blue: #003087;
            --col-red: #C8102E;
            --bg-light: #FFF9E6;
        }

        * { box-sizing: border-box; user-select: none; margin: 0; padding: 0; }
        
        body {
            font-family: 'Quicksand', sans-serif;
            background-color: var(--bg-light);
            display: flex; flex-direction: column; align-items: center;
            min-height: 100vh; overflow-x: hidden;
            padding-top: 80px; /* ESPACIO PARA QUE EL TITULO NO SE CORTE */
            padding-bottom: 50px;
        }

        header {
            background-color: var(--col-yellow);
            width: 100%; padding: 20px; text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-bottom: 10px solid var(--col-red);
            position: absolute; top: 0; left: 0; z-index: 10;
        }

        h1 { 
            margin: 0; color: var(--col-blue); font-family: 'Fredoka', sans-serif;
            font-size: 2.5rem; text-transform: uppercase; letter-spacing: 2px;
        }

        .game-container {
            display: grid; grid-template-columns: 1fr 1fr;
            gap: 30px; max-width: 900px; width: 95%;
            margin-top: 20px;
        }

        .column { display: flex; flex-direction: column; gap: 15px; }

        .word-card {
            background: white; border: 3px solid var(--col-blue);
            padding: 15px; border-radius: 15px; font-size: 1.2rem;
            font-weight: bold; text-align: center; cursor: grab;
            transition: 0.2s; box-shadow: 0 5px 0 var(--col-blue);
        }
        .word-card:hover { transform: translateY(-3px); background: #f0f4ff; }
        .word-card.dragging { opacity: 0.4; }
        .word-card.matched { display: none; } /* Desaparece al acertar */

        .image-card {
            background: white; border: 4px dashed #ccc;
            border-radius: 20px; height: 140px; position: relative;
            overflow: hidden; display: flex; align-items: center; justify-content: center;
            transition: 0.3s;
        }
        .image-card img { width: 100%; height: 100%; object-fit: cover; }
        .image-card.hover { border-color: var(--col-yellow); background: #fffde6; transform: scale(1.02); }
        .image-card.matched { border: 5px solid #4caf50; }
        .image-card.matched::after {
            content: "✅"; position: absolute; font-size: 3.5rem;
            background: rgba(255,255,255,0.7); width: 100%; height: 100%;
            display: flex; align-items: center; justify-content: center;
        }

        /* Feedback Popups */
        #feedback {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0);
            background: white; padding: 25px; border-radius: 25px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.3); z-index: 100;
            text-align: center; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            pointer-events: none;
        }
        #feedback.active { transform: translate(-50%, -50%) scale(1); }

        #final-screen {
            position: fixed; inset: 0; background: rgba(255,255,255,0.98);
            display: none; flex-direction: column; align-items: center; justify-content: center;
            z-index: 1000; text-align: center;
        }
        .dancer { font-size: 7rem; animation: jump 0.6s infinite alternate; }
        @keyframes jump { from { transform: translateY(0); } to { transform: translateY(-30px); } }

        .btn-restart {
            background: var(--col-blue); color: white; border: none;
            padding: 15px 40px; font-size: 1.6rem; border-radius: 50px;
            cursor: pointer; font-family: 'Fredoka'; margin-top: 20px;
            box-shadow: 0 6px 0 #001a4d;
        }
    </style>
</head>
<body>

    <header>
        <h1>SABORES DE COLOMBIA</h1>
        <p style="font-weight: bold; color: var(--col-blue);">Une la palabra con la imagen correcta</p>
    </header>

    <div class="game-container">
        <div class="column" id="words-col"></div>
        <div class="column" id="images-col"></div>
    </div>

    <div id="feedback">
        <span style="font-size: 4rem;">👨‍🏫</span><br>
        <span style="font-size: 2rem; font-weight: 900; color: var(--col-blue);" id="fb-text">¡Muy bien!</span>
    </div>

    <div id="final-screen">
        <div style="display: flex; gap: 30px; margin-bottom: 20px;">
            <div class="dancer">💃</div>
            <div class="dancer">🕺</div>
        </div>
        <h2 style="font-size: 2.8rem; color: var(--col-red); font-family: 'Fredoka';">¡Felicidades, Chef!</h2>
        <p style="font-size: 1.4rem;">Has dominado la gastronomía colombiana.</p>
        <button class="btn-restart" onclick="location.reload()">Jugar de nuevo</button>
    </div>

    <audio id="s-ok" src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>
    <audio id="s-no" src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>
    <audio id="s-cumbia" loop src="https://www.chosic.com/wp-content/uploads/2021/07/The-Joy-of-Success-Cumbia.mp3"></audio>

    <script>
        // BANCO ACTUALIZADO CON IMÁGENES PRECISAS
        const BANCO_COMIDAS = [
            { name: 'Bandeja Paisa', img: 'https://img.freepik.com/foto-gratis/bandeja-paisa-tipica-comida-colombiana_181624-43391.jpg' },
            { name: 'Ajiaco', img: 'https://img.freepik.com/foto-gratis/sopa-pollo-cremosa-estilo-colombiano-mazorca-maiz-papas-alcaparras_2829-18182.jpg' },
            { name: 'Empanadas', img: 'https://img.freepik.com/foto-gratis/apetitosas-empanadas-fritas-hojas-verdes-sobre-tabla-madera_181624-41916.jpg' },
            { name: 'Arepa de Huevo', img: 'https://img.freepik.com/foto-gratis/arepas-huevo-tipicas-comida-caribe-colombiano_181624-43405.jpg' },
            { name: 'Patacones con Todo', img: 'https://img.freepik.com/foto-gratis/patacones-deliciosos-carne-desmechada-guacamole_181624-43395.jpg' },
            { name: 'Sancocho de Gallina', img: 'https://img.freepik.com/foto-gratis/sopa-colombiana-caliente-con-carne-gallina_181624-43409.jpg' },
            { name: 'Tamal Tolimense', img: 'https://img.freepik.com/foto-gratis/tamales-mexicanos-plato-madera-hojas_181624-34304.jpg' }, // Imagen representativa de tamal en hoja
            { name: 'Buñuelos', img: 'https://img.freepik.com/foto-gratis/deliciosos-bunuelos-colombianos-plato_181624-43393.jpg' },
            { name: 'Lulada Caleña', img: 'https://i.ytimg.com/vi/bX7jofkR-Ww/maxresdefault.jpg' }, // Imagen de Lulada
            { name: 'Obleas con Arequipe', img: 'https://cdn.colombia.com/images/gastronomia/recetas/obleas.jpg' }, // Imagen de oblea
            { name: 'Lechona Tolimense', img: 'https://i.ytimg.com/vi/uY2QunW9I2g/maxresdefault.jpg' }, // Imagen de Lechona
            { name: 'Café de Colombia', img: 'https://img.freepik.com/foto-gratis/primer-plano-mano-sosteniendo-taza-cafe-fresco_181624-43389.jpg' }
        ];

        let correctos = 0;
        let draggedName = "";
        let audioHabilitado = false;

        // Desbloqueo de audio para navegadores
        function unmuteAudio() {
            if(!audioHabilitado) {
                const sfx = document.getElementById('s-ok');
                sfx.play().then(() => { sfx.pause(); sfx.currentTime = 0; audioHabilitado = true; }).catch(()=>{});
            }
        }

        function init() {
            unmuteAudio();
            completedCount = 0;
            correctos = 0;
            // Seleccionar 6 al azar
            const selection = [...BANCO_COMIDAS].sort(() => Math.random() - 0.5).slice(0, 6);
            
            const wordsCol = document.getElementById('words-col');
            const imagesCol = document.getElementById('images-col');
            wordsCol.innerHTML = '';
            imagesCol.innerHTML = '';

            // Barajar palabras e imágenes por separado
            const wordsShuffle = [...selection].sort(() => Math.random() - 0.5);
            const imagesShuffle = [...selection].sort(() => Math.random() - 0.5);

            wordsShuffle.forEach(item => {
                const div = document.createElement('div');
                div.className = 'word-card';
                div.textContent = item.name;
                div.draggable = true;
                div.id = "w-" + item.name;
                div.ondragstart = (e) => { e.dataTransfer.setData('text', div.id); draggedName = item.name; div.classList.add('dragging'); };
                div.ondragend = () => div.classList.remove('dragging');
                wordsCol.appendChild(div);
            });

            imagesShuffle.forEach(item => {
                const div = document.createElement('div');
                div.className = 'image-card';
                div.dataset.name = item.name;
                div.innerHTML = `<img src="${item.img}" alt="${item.name}">`;
                div.ondragover = (e) => e.preventDefault();
                div.ondragenter = () => div.classList.add('hover');
                div.ondragleave = () => div.classList.remove('hover');
                div.ondrop = (e) => {
                    div.classList.remove('hover');
                    if(draggedName === item.name) {
                        div.classList.add('matched');
                        document.getElementById("w-"+draggedName).classList.add('matched');
                        document.getElementById('s-ok').play();
                        showFeedback();
                        correctos++;
                        if(correctos === 6) celebrar();
                    } else {
                        document.getElementById('s-no').play();
                    }
                };
                imagesCol.appendChild(div);
            });
        }

        function showFeedback() {
            const fb = document.getElementById('feedback');
            fb.classList.add('active');
            setTimeout(() => fb.classList.remove('active'), 1000);
            confetti({ particleCount: 50, spread: 60, origin: { y: 0.7 } });
        }

        function celebrar() {
            document.getElementById('s-cumbia').play();
            document.getElementById('final-screen').style.display = 'flex';
            var end = Date.now() + (5 * 1000);
            (function frame() {
                confetti({ particleCount: 3, angle: 60, spread: 55, origin: { x: 0 } });
                confetti({ particleCount: 3, angle: 120, spread: 55, origin: { x: 1 } });
                if (Date.now() < end) requestAnimationFrame(frame);
            }());
        }

        init();
    </script>
</body>
</html>
"""

# Renderizamos el componente con la altura ajustada (height=920)
components.html(html_comidas_corregido, height=920, scrolling=False)
