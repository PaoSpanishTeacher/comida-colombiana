import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Sabores de Colombia", layout="wide")

# Eliminamos márgenes de Streamlit
st.markdown("""
    <style>
    .block-container { padding: 0rem; }
    iframe { border: none; }
    </style>
    """, unsafe_allow_html=True)

html_comidas = r"""
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

        * { box-sizing: border-box; user-select: none; }
        body {
            margin: 0; font-family: 'Quicksand', sans-serif;
            background-color: var(--bg-light);
            display: flex; flex-direction: column; align-items: center;
            min-height: 100vh; overflow-x: hidden;
            padding-bottom: 50px;
        }

        header {
            background-color: var(--col-yellow);
            width: 100%; padding: 25px; text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-bottom: 10px solid var(--col-red);
            margin-bottom: 30px;
        }

        h1 { 
            margin: 0; color: var(--col-blue); font-family: 'Fredoka', sans-serif;
            font-size: 2.8rem; text-transform: uppercase; letter-spacing: 2px;
        }

        .game-container {
            display: grid; grid-template-columns: 1fr 1fr;
            gap: 40px; max-width: 1000px; width: 95%;
        }

        .column { display: flex; flex-direction: column; gap: 15px; }

        .word-card {
            background: white; border: 3px solid var(--col-blue);
            padding: 18px; border-radius: 15px; font-size: 1.3rem;
            font-weight: bold; text-align: center; cursor: grab;
            transition: 0.2s; box-shadow: 0 5px 0 var(--col-blue);
        }
        .word-card:hover { transform: translateY(-3px); background: #f0f4ff; }
        .word-card.dragging { opacity: 0.4; }
        .word-card.matched { display: none; } /* Desaparece al acertar */

        .image-card {
            background: white; border: 4px dashed #ccc;
            border-radius: 20px; height: 160px; position: relative;
            overflow: hidden; display: flex; align-items: center; justify-content: center;
            transition: 0.3s;
        }
        .image-card img { width: 100%; height: 100%; object-fit: cover; }
        .image-card.hover { border-color: var(--col-yellow); background: #fffde6; transform: scale(1.02); }
        .image-card.matched { border: 5px solid #4caf50; }
        .image-card.matched::after {
            content: "✅"; position: absolute; font-size: 4rem;
            background: rgba(255,255,255,0.6); width: 100%; height: 100%;
            display: flex; align-items: center; justify-content: center;
        }

        /* Popups */
        #feedback {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0);
            background: white; padding: 30px; border-radius: 30px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.3); z-index: 100;
            text-align: center; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #feedback.active { transform: translate(-50%, -50%) scale(1); }

        #final-screen {
            position: fixed; inset: 0; background: rgba(255,255,255,0.98);
            display: none; flex-direction: column; align-items: center; justify-content: center;
            z-index: 1000; text-align: center;
        }
        .dancer { font-size: 8rem; animation: jump 0.6s infinite alternate; }
        @keyframes jump { from { transform: translateY(0); } to { transform: translateY(-30px); } }

        .btn-restart {
            background: var(--col-blue); color: white; border: none;
            padding: 20px 50px; font-size: 1.8rem; border-radius: 50px;
            cursor: pointer; font-family: 'Fredoka'; margin-top: 20px;
            box-shadow: 0 6px 0 #001a4d;
        }
    </style>
</head>
<body onclick="unmuteAudio()">

    <header>
        <h1>SABORES DE COLOMBIA</h1>
        <p style="font-weight: bold; color: var(--col-blue);">¡Arrastra la palabra hacia su imagen!</p>
    </header>

    <div class="game-container">
        <div class="column" id="words-col"></div>
        <div class="column" id="images-col"></div>
    </div>

    <div id="feedback">
        <span style="font-size: 5rem;">👨‍🏫</span><br>
        <span style="font-size: 2.5rem; font-weight: 900; color: var(--col-blue);" id="fb-text">¡Mmm, qué rico!</span>
    </div>

    <div id="final-screen">
        <div style="display: flex; gap: 30px;">
            <div class="dancer">💃</div>
            <div class="dancer">🕺</div>
        </div>
        <h2 style="font-size: 3rem; color: var(--col-red); font-family: 'Fredoka';">¡Felicidades, Chef!</h2>
        <p style="font-size: 1.5rem;">Has dominado la gastronomía colombiana.</p>
        <button class="btn-restart" onclick="location.reload()">Jugar otra vez</button>
    </div>

    <audio id="s-ok" src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>
    <audio id="s-no" src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>
    <audio id="s-cumbia" loop src="https://www.chosic.com/wp-content/uploads/2021/07/The-Joy-of-Success-Cumbia.mp3"></audio>

    <script>
        const BANCO_COMIDAS = [
            { name: 'Arepa de Huevo', img: 'https://images.unsplash.com/photo-1598215437220-822822a7f920?w=400' },
            { name: 'Bandeja Paisa', img: 'https://images.unsplash.com/photo-1512058560564-9a037666497d?w=400' },
            { name: 'Ajiaco', img: 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400' },
            { name: 'Empanadas', img: 'https://images.unsplash.com/photo-1628102476629-f8c32189679c?w=400' },
            { name: 'Lechona', img: 'https://images.unsplash.com/photo-1544025162-d76694265947?w=400' },
            { name: 'Tamal Tolimense', img: 'https://images.unsplash.com/photo-1601303516514-46328905335e?w=400' },
            { name: 'Patacones', img: 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=400' },
            { name: 'Buñuelos', img: 'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=400' },
            { name: 'Deditos de Queso', img: 'https://images.unsplash.com/photo-1623653387945-2fd25214f8fc?w=400' },
            { name: 'Chigüiro', img: 'https://images.unsplash.com/photo-1532636875304-4c89119d9b4d?w=400' },
            { name: 'Pescado Frito', img: 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400' },
            { name: 'Café de Colombia', img: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400' },
            { name: 'Pandebono', img: 'https://images.unsplash.com/photo-1608039755401-742074f0548d?w=400' },
            { name: 'Lulada', img: 'https://images.unsplash.com/photo-1540308304961-3a0553754e3f?w=400' },
            { name: 'Mazamorra', img: 'https://images.unsplash.com/photo-1593560737063-8f010e2867c4?w=400' },
            { name: 'Mote de Queso', img: 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400' },
            { name: 'Cholado', img: 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400' },
            { name: 'Sancocho', img: 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400' },
            { name: 'Changua', img: 'https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=400' },
            { name: 'Arroz con Coco', img: 'https://images.unsplash.com/photo-1512058560564-9a037666497d?w=400' }
        ];

        let correctos = 0;
        let draggedName = "";
        let audioIniciado = false;

        function unmuteAudio() {
            if(!audioIniciado) {
                const cumbia = document.getElementById('s-cumbia');
                cumbia.play().then(() => { cumbia.pause(); audioIniciado = true; });
            }
        }

        function init() {
            // Seleccionar 6 al azar
            const randomList = BANCO_COMIDAS.sort(() => Math.random() - 0.5).slice(0, 6);
            
            const wordsCol = document.getElementById('words-col');
            const imagesCol = document.getElementById('images-col');

            // Barajar palabras e imágenes por separado
            const wordsShuffle = [...randomList].sort(() => Math.random() - 0.5);
            const imagesShuffle = [...randomList].sort(() => Math.random() - 0.5);

            wordsShuffle.forEach(item => {
                const div = document.createElement('div');
                div.className = 'word-card';
                div.textContent = item.name;
                div.draggable = true;
                div.id = "w-" + item.name;
                div.ondragstart = (e) => { draggedName = item.name; div.classList.add('dragging'); };
                div.ondragend = () => div.classList.remove('dragging');
                wordsCol.appendChild(div);
            });

            imagesShuffle.forEach(item => {
                const div = document.createElement('div');
                div.className = 'image-card';
                div.dataset.name = item.name;
                div.innerHTML = `<img src="${item.img}">`;
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

components.html(html_comidas, height=900, scrolling=False)
