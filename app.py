import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Chạy Trốn Quái Vật - Side Runner",
    page_icon="🏃",
    layout="centered"
)

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stApp {
        max-width: 900px;
        margin: 0 auto;
    }
    h1 {
        text-align: center;
        color: #ff4b4b;
        text-shadow: 0 0 10px rgba(255, 75, 75, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏃 CHẠY TRỐN QUÁI VẬT - GÓC NHÌN NGANG 🌳</h1>", unsafe_allow_html=True)

# Phần hướng dẫn điều khiển sáng rực Neon
with st.container():
    st.markdown("""
    <style>
    .neon-instructions {
        background: linear-gradient(135deg, #1e2530 0%, #2a1515 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 2px solid #ff4b4b;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.6);
    }
    .neon-instructions h3 {
        color: #ff6b6b;
        text-shadow: 0 0 8px rgba(255, 107, 107, 0.8);
        margin-top: 0;
    }
    .neon-instructions li {
        color: #ffffff;
        font-size: 16px;
        margin-bottom: 8px;
    }
    .neon-instructions b {
        color: #ffcc00;
        text-shadow: 0 0 5px rgba(255, 204, 0, 0.6);
    }
    .neon-instructions i {
        color: #00ffcc;
    }
    </style>
    
    <div class="neon-instructions">
        <h3>🎮 HƯỚNG DẪN ĐIỀU KHIỂN:</h3>
        <ul>
            <li><b>Phím SPACE (Dấu cách):</b> Nhảy qua chướng ngại vật (Cây đổ, đá).</li>
            <li><b>Phím A:</b> Né lùi lại (xuống làn sau).</li>
            <li><b>Phím D:</b> Tiến lên (lên làn trước).</li>
        </ul>
        <p style="margin-bottom: 0;"><i>🔥 Mẹo: Quái vật xanh đang rượt sát phía sau! Hãy tập trung góc nhìn ngang để né tránh chướng ngại vật kịp thời và bật âm thanh để nghe nhạc nền căng thẳng nhé!</i></p>
    </div>
    """, unsafe_allow_html=True)

# Mã nguồn HTML/JS của trò chơi góc nhìn ngang
game_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Monster Side Runner</title>
    <style>
        body {
            margin: 0;
            background: #050505;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: 'Courier New', Courier, monospace;
            color: white;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            box-shadow: 0 0 25px rgba(0, 255, 128, 0.3);
            border-radius: 8px;
            overflow: hidden;
            background: #111;
        }
        canvas {
            display: block;
            background: #151f16;
        }
        #ui {
            position: absolute;
            top: 10px;
            left: 15px;
            right: 15px;
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 2px 2px #000;
            pointer-events: none;
            z-index: 5;
        }
        #start-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            z-index: 10;
        }
        .btn {
            background: #2e7d32;
            color: white;
            border: none;
            padding: 12px 25px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 15px;
            box-shadow: 0 0 10px #4caf50;
            transition: 0.2s;
        }
        .btn:hover {
            background: #388e3c;
            transform: scale(1.05);
        }
    </style>
</head>
<body>

<div id="game-container">
    <div id="ui">
        <span id="score-display">ĐIỂM: 0</span>
        <span id="danger-display" style="color: #4caf50;">⚠️ QUÁI VẬT XANH: BÁM SÁT</span>
    </div>

    <div id="start-screen">
        <h1 style="color: #4caf50; margin-bottom: 5px; text-shadow: 0 0 10px #2e7d32;">RỪNG SÂU TỬ THẦN - GÓC NHÌN NGANG</h1>
        <p style="max-width: 450px; color: #ccc; font-size: 14px; line-height: 1.4;">
            Quái vật xanh khát máu đang đuổi sát phía sau bạn!<br>
            Sử dụng <b>SPACE</b> để nhảy, <b>A</b> và <b>D</b> để chuyển làn trước/sau.
        </p>
        <button class="btn" onclick="startGame()">BẮT ĐẦU CHẠY</button>
    </div>

    <canvas id="gameCanvas" width="800" height="500"></canvas>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let gameStarted = false;
let score = 0;
let gameOver = false;
let gameSpeed = 7;
let animTimer = 0;

let audioCtx = null;
let musicInterval = null;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
    if (!musicInterval) {
        let beat = 0;
        musicInterval = setInterval(() => {
            if (!gameStarted || gameOver) return;
            let osc = audioCtx.createOscillator();
            let gain = audioCtx.createGain();
            osc.type = beat % 2 === 0 ? 'sawtooth' : 'square';
            osc.frequency.setValueAtTime(beat % 4 === 0 ? 80 : 120, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.15);
            
            gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.15);
            beat++;
        }, 180);
    }
}

function playSound(type) {
    if (!audioCtx) return;
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    
    if (type === 'jump') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(150, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(350, audioCtx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
    } else if (type === 'hit') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(100, audioCtx.currentTime);
        osc.frequency.linearRampToValueAtTime(30, audioCtx.currentTime + 0.3);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
    }
    
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.3);
}

const laneYs = [340, 390, 440];
let playerLane = 1; 
let playerBaseY = laneYs[playerLane];
let playerX = 220;
let playerY = playerBaseY;
let playerJumpVY = 0;
let isJumping = false;

const player = {
    width: 45,
    height: 75
};

let obstacles = [];
let bgScrollX = 0;

window.addEventListener('keydown', (e) => {
    if (!gameStarted || gameOver) return;
    
    if (e.code === 'KeyA' || e.code === 'ArrowUp') {
        if (playerLane > 0) {
            playerLane--;
            playerBaseY = laneYs[playerLane];
        }
    } else if (e.code === 'KeyD' || e.code === 'ArrowDown') {
        if (playerLane < 2) {
            playerLane++;
            playerBaseY = laneYs[playerLane];
        }
    } else if (e.code === 'Space' && !isJumping) {
        isJumping = true;
        playerJumpVY = -13;
        playSound('jump');
        e.preventDefault();
    }
});

function startGame() {
    gameStarted = true;
    gameOver = false;
    score = 0;
    gameSpeed = 7;
    obstacles = [];
    playerLane = 1;
    playerBaseY = laneYs[playerLane];
    playerY = playerBaseY;
    document.getElementById('start-screen').style.display = 'none';
    initAudio();
}

function spawnObstacle() {
    if (!gameStarted || gameOver) return;
    let lane = Math.floor(Math.random() * 3);
    let types = ['rock', 'fallen_tree', 'tree_stump'];
    let type = types[Math.floor(Math.random() * types.length)];
    
    obstacles.push({
        lane: lane,
        x: 850,
        y: laneYs[lane],
        type: type,
        width: 60,
        height: 45
    });
}

setInterval(spawnObstacle, 1600);

function update() {
    if (!gameStarted || gameOver) return;

    score += 1;
    animTimer += 0.2;
    gameSpeed = 7 + Math.floor(score / 350);

    playerY += (playerBaseY - playerY) * 0.3;

    if (isJumping) {
        playerY += playerJumpVY;
        playerJumpVY += 0.65;
        if (playerY >= playerBaseY) {
            playerY = playerBaseY;
            isJumping = false;
        }
    }

    bgScrollX += gameSpeed;

    for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.x -= gameSpeed;

        let inSameLane = playerLane === obs.lane;
        let isHitX = (playerX + player.width - 10 > obs.x && playerX < obs.x + obs.width - 10);
        let isHitY = (playerY >= obs.y - 30);

        if (inSameLane && isHitX && isHitY) {
            if (obs.type === 'rock' && isJumping && playerY < obs.y - 15) {
                // Nhảy qua an toàn
            } else {
                gameOver = true;
                playSound('hit');
            }
        }

        if (obs.x < -100) {
            obstacles.splice(i, 1);
        }
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#111912';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#1a261c';
    for (let i = -1; i < 5; i++) {
        let treeX = (i * 250 - (bgScrollX * 0.3) % 250);
        ctx.beginPath();
        ctx.arc(treeX, 180, 70, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillRect(treeX - 12, 180, 24, 150);
    }

    ctx.fillStyle = '#223324';
    ctx.fillRect(0, 310, canvas.width, 170);

    ctx.strokeStyle = '#3d5c40';
    ctx.lineWidth = 3;
    ctx.setLineDash([20, 20]);
    ctx.lineDashOffset = -bgScrollX;

    ctx.beginPath();
    ctx.moveTo(0, 365); ctx.lineTo(canvas.width, 365);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, 420); ctx.lineTo(canvas.width, 420);
    ctx.stroke();
    ctx.setLineDash([]);

    let renderObjects = [];
    obstacles.forEach(obs => renderObjects.push({type: 'obs', obj: obs, y: obs.y}));
    renderObjects.push({type: 'player', y: playerBaseY});
    renderObjects.push({type: 'monster', y: laneYs[1] + 20});

    renderObjects.sort((a, b) => a.y - b.y);

    renderObjects.forEach(item => {
        if (item.type === 'obs') {
            let obs = item.obj;
            let renderX = obs.x;
            let renderY = obs.y;

            if (obs.type === 'rock') {
                ctx.fillStyle = '#4a5568';
                ctx.beginPath();
                ctx.arc(renderX + 30, renderY, 25, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#718096';
                ctx.beginPath();
                ctx.arc(renderX + 25, renderY - 5, 10, 0, Math.PI * 2);
                ctx.fill();
            } else if (obs.type === 'fallen_tree') {
                ctx.fillStyle = '#5c4033';
                ctx.fillRect(renderX, renderY - 15, 75, 22);
                ctx.fillStyle = '#2e7d32';
                ctx.beginPath();
                ctx.arc(renderX + 20, renderY - 10, 15, 0, Math.PI * 2);
                ctx.fill();
            } else if (obs.type === 'tree_stump') {
                ctx.fillStyle = '#6e4f3a';
                ctx.fillRect(renderX + 10, renderY - 20, 35, 30);
                ctx.fillStyle = '#3b2219';
                ctx.beginPath();
                ctx.ellipse(renderX + 27, renderY - 20, 18, 8, 0, 0, Math.PI * 2);
                ctx.fill();
            }
        } 
        else if (item.type === 'monster') {
            let monsterBreath = Math.sin(animTimer * 4) * 4;
            let mX = 90;
            let mY = laneYs[1] + 10 + monsterBreath;

            ctx.fillStyle = '#004d40';
            ctx.beginPath();
            ctx.arc(mX, mY - 25, 30, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#ffea00';
            ctx.beginPath();
            ctx.arc(mX + 10, mY - 32, 6, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#ff3d00';
            ctx.beginPath();
            ctx.arc(mX + 12, mY - 32, 2.5, 0, Math.PI * 2);
            ctx.fill();
        }
        else if (item.type === 'player') {
            let legOffset = isJumping ? 0 : Math.sin(animTimer * 6) * 12;
            
            ctx.fillStyle = '#ffcc00';
            ctx.fillRect(playerX + 5, playerY - 45, 26, 32);
            ctx.fillStyle = '#ffd1b3';
            ctx.beginPath();
            ctx.arc(playerX + 18, playerY - 55, 12, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#1e88e5';
            ctx.beginPath();
            ctx.arc(playerX + 18, playerY - 58, 12, Math.PI, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#1a237e';
            ctx.fillRect(playerX + 8, playerY - 15, 8, 18 + legOffset);
            ctx.fillRect(playerX + 20, playerY - 15, 8, 18 - legOffset);
        }
    });

    if (gameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.85)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#ff3333';
        ctx.font = 'bold 38px "Courier New"';
        ctx.textAlign = 'center';
        ctx.fillText('BẠN ĐÃ BỊ QUÁI VẬT XANH BẮT!', canvas.width / 2, 190);
        
        ctx.fillStyle = '#ffffff';
        ctx.font = '24px "Courier New"';
        ctx.fillText('Điểm đạt được: ' + score, canvas.width / 2, 250);
        
        ctx.fillStyle = '#aaaaaa';
        ctx.font = '16px "Courier New"';
        ctx.fillText('Nhấn nút bên dưới để thử lại', canvas.width / 2, 300);
        
        document.getElementById('start-screen').style.display = 'flex';
        document.getElementById('start-screen').querySelector('h1').innerText = 'THUA MẤT RỒI!';
        document.getElementById('start-screen').querySelector('button').innerText = 'CHƠI LẠI NGAY';
    }

    document.getElementById('score-display').innerText = 'ĐIỂM: ' + score;
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

gameLoop();
</script>

</body>
</html>
"""

# Hiển thị game trực tiếp
components.html(game_html, height=580, scrolling=False)
