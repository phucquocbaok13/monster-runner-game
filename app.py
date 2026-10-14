import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Rừng Xanh Nắng Vàng - Runner",
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
        color: #ffcc00;
        text-shadow: 0 0 10px rgba(255, 204, 0, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏃 CHẠY TRỐN QUÁI VẬT - RỪNG XANH NẮNG VÀNG 🌳</h1>", unsafe_allow_html=True)

# Phần hướng dẫn điều khiển với dòng Mẹo sáng rực Neon
with st.container():
    st.markdown("""
    <style>
    .neon-instructions {
        background: linear-gradient(135deg, #1e2530 0%, #152a1a 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 2px solid #4caf50;
        box-shadow: 0 0 15px rgba(76, 175, 80, 0.6);
    }
    .neon-instructions h3 {
        color: #66bb6a;
        text-shadow: 0 0 8px rgba(102, 187, 106, 0.8);
        margin-top: 0;
    }
    .neon-instructions li {
        color: #ffffff;
        font-size: 16px;
        margin-bottom: 8px;
    }
    .neon-instructions b {
        color: #ffcc00;
    }
    /* Hiệu ứng làm sáng rực cho dòng mẹo */
    .glow-tip {
        color: #ffeb3b !important;
        font-size: 16px;
        font-weight: bold;
        text-shadow: 0 0 10px #ffeb3b, 0 0 20px #ff9800;
        background: rgba(255, 235, 59, 0.1);
        padding: 8px 12px;
        border-radius: 6px;
        border-left: 4px solid #ffeb3b;
        margin-top: 10px;
    }
    </style>
    
    <div class="neon-instructions">
        <h3>🎮 HƯỚNG DẪN ĐIỀU KHIỂN:</h3>
        <ul>
            <li><b>Phím W:</b> Nhảy qua tảng đá / chướng ngại vật.</li>
            <li><b>Phím A:</b> Né sang làn TRÁI.</li>
            <li><b>Phím D:</b> Né sang làn PHẢI.</li>
        </ul>
        <div class="glow-tip">☀️ Mẹo: Thu thập tiền vàng, né tránh chướng ngại vật trong khung cảnh rừng xanh ngập tràn ánh nắng và âm thanh sống động!</div>
    </div>
    """, unsafe_allow_html=True)

# Mã nguồn trò chơi toàn diện (All-in-one)
game_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Subway Forest Runner</title>
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
            box-shadow: 0 0 25px rgba(255, 204, 0, 0.4);
            border-radius: 8px;
            overflow: hidden;
            background: #111;
        }
        canvas {
            display: block;
            background: linear-gradient(to bottom, #4fc3f7, #e1f5fe);
        }
        #ui {
            position: absolute;
            top: 10px;
            left: 15px;
            right: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 2px 2px #000;
            pointer-events: none;
            z-index: 5;
        }
        .score-badge {
            background: rgba(0, 0, 0, 0.4);
            padding: 5px 12px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        #start-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.82);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            z-index: 10;
        }
        .btn {
            background: #ff9800;
            color: white;
            border: none;
            padding: 12px 28px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
            box-shadow: 0 0 15px #ff9800;
            transition: 0.2s;
        }
        .btn:hover {
            background: #ffb74d;
            transform: scale(1.05);
        }
    </style>
</head>
<body>

<div id="game-container">
    <div id="ui">
        <div class="score-badge">⭐ ĐIỂM: <span id="score-display">0</span></div>
        <div class="score-badge" style="color: #ffeb3b;">🪙 VÀNG: <span id="coin-display">0</span></div>
        <div class="score-badge" style="color: #ff5252;">⚠️ QUÁI VẬT: SÁT GÁY!</div>
    </div>

    <div id="start-screen">
        <h1 style="color: #ffeb3b; margin-bottom: 5px; text-shadow: 0 0 15px #ff9800;">RỪNG XANH NẮNG VÀNG</h1>
        <p style="max-width: 450px; color: #eee; font-size: 14px; line-height: 1.4;">
            Trải nghiệm phong cách Subway Surfers rực rỡ dưới ánh mặt trời!<br>
            Dùng phím <b>W</b> để nhảy, <b>A</b> (Trái), <b>D</b> (Phải) để đổi làn và thu thập xu vàng!
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
let coins = 0;
let gameOver = false;
let gameSpeed = 5.5;
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
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(beat % 2 === 0 ? 220 : 330, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(110, audioCtx.currentTime + 0.12);
            
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.12);
            beat++;
        }, 200);
    }
}

function playSound(type) {
    if (!audioCtx) return;
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    
    if (type === 'jump') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(180, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(400, audioCtx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
    } else if (type === 'coin') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(600, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.15);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
    } else if (type === 'hit') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(120, audioCtx.currentTime);
        osc.frequency.linearRampToValueAtTime(40, audioCtx.currentTime + 0.3);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
    }
    
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.3);
}

const roadHorizonY = 160;
const roadBottomY = 500;

let playerLane = 1; 
let playerYOffset = 0;
let playerJumpVY = 0;
let isJumping = false;

let obstacles = [];
let coinItems = [];
let roadScroll = 0;

window.addEventListener('keydown', (e) => {
    if (!gameStarted || gameOver) return;
    
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') {
        if (playerLane > 0) playerLane--;
    } else if (e.code === 'KeyD' || e.code === 'ArrowRight') {
        if (playerLane < 2) playerLane++;
    } else if ((e.code === 'KeyW' || e.code === 'ArrowUp') && !isJumping) {
        isJumping = true;
        playerJumpVY = -12;
        playSound('jump');
        e.preventDefault();
    }
});

function startGame() {
    gameStarted = true;
    gameOver = false;
    score = 0;
    coins = 0;
    gameSpeed = 5.5;
    obstacles = [];
    coinItems = [];
    playerLane = 1;
    playerYOffset = 0;
    document.getElementById('start-screen').style.display = 'none';
    initAudio();
}

function spawnEntity() {
    if (!gameStarted || gameOver) return;
    let lane = Math.floor(Math.random() * 3);
    
    if (Math.random() < 0.6) {
        let types = ['rock', 'fallen_tree', 'tree_stump'];
        let type = types[Math.floor(Math.random() * types.length)];
        obstacles.push({ lane: lane, progress: 0.05, type: type });
    } else {
        coinItems.push({ lane: lane, progress: 0.05 });
    }
}

setInterval(spawnEntity, 1300);

function update() {
    if (!gameStarted || gameOver) return;

    score += 1;
    animTimer += 0.2;
    gameSpeed = 5.5 + Math.floor(score / 300) * 0.4;

    if (isJumping) {
        playerYOffset += playerJumpVY;
        playerJumpVY += 0.65;
        if (playerYOffset >= 0) {
            playerYOffset = 0;
            isJumping = false;
        }
    }

    roadScroll += gameSpeed * 3.5;

    for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.progress += gameSpeed * 0.0022;

        if (obs.progress >= 0.82 && obs.progress <= 0.92) {
            if (obs.lane === playerLane) {
                if (obs.type === 'rock' && isJumping && playerYOffset < -35) {
                    // Nhảy qua an toàn
                } else {
                    gameOver = true;
                    playSound('hit');
                }
            }
        }

        if (obs.progress > 1.05) {
            obstacles.splice(i, 1);
        }
    }

    for (let i = coinItems.length - 1; i >= 0; i--) {
        let c = coinItems[i];
        c.progress += gameSpeed * 0.0022;

        if (c.progress >= 0.82 && c.progress <= 0.92) {
            if (c.lane === playerLane && playerYOffset > -40) {
                coins += 1;
                playSound('coin');
                coinItems.splice(i, 1);
                continue;
            }
        }

        if (c.progress > 1.05) {
            coinItems.splice(i, 1);
        }
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    let skyGrad = ctx.createLinearGradient(0, 0, 0, roadHorizonY);
    skyGrad.addColorStop(0, '#4fc3f7');
    skyGrad.addColorStop(1, '#e1f5fe');
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, canvas.width, roadHorizonY);

    ctx.fillStyle = 'rgba(255, 235, 59, 0.85)';
    ctx.beginPath();
    ctx.arc(650, 60, 35, 0, Math.PI * 2);
    ctx.fill();

    let groundGrad = ctx.createLinearGradient(0, roadHorizonY, 0, roadBottomY);
    groundGrad.addColorStop(0, '#2e7d32');
    groundGrad.addColorStop(1, '#1b5e20');
    ctx.fillStyle = groundGrad;
    ctx.fillRect(0, roadHorizonY, canvas.width, roadBottomY - roadHorizonY);

    ctx.beginPath();
    ctx.moveTo(400, roadHorizonY);
    ctx.lineTo(180, roadBottomY);
    ctx.lineTo(620, roadBottomY);
    ctx.closePath();
    ctx.fillStyle = '#8d6e63';
    ctx.fill();

    ctx.strokeStyle = '#4e342e';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(400, roadHorizonY); ctx.lineTo(290, roadBottomY);
    ctx.moveTo(400, roadHorizonY); ctx.lineTo(510, roadBottomY);
    ctx.stroke();

    for (let i = -2; i < 8; i++) {
        let treeProgress = (i * 0.2 + (roadScroll * 0.0012)) % 1.0;
        let treeY = roadHorizonY + treeProgress * (roadBottomY - roadHorizonY);
        let leftX = 400 - treeProgress * 340;
        let rightX = 400 + treeProgress * 340;
        let radius = 15 + treeProgress * 50;

        ctx.fillStyle = '#5d4037';
        ctx.fillRect(leftX - 4, treeY, 8, 30);
        ctx.fillRect(rightX - 4, treeY, 8, 30);

        ctx.fillStyle = '#4caf50';
        ctx.beginPath();
        ctx.arc(leftX, treeY - 10, radius, 0, Math.PI * 2);
        ctx.arc(rightX, treeY - 10, radius, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = '#81c784';
        ctx.beginPath();
        ctx.arc(leftX - 5, treeY - 15, radius * 0.4, 0, Math.PI * 2);
        ctx.arc(rightX - 5, treeY - 15, radius * 0.4, 0, Math.PI * 2);
        ctx.fill();
    }

    let allEntities = [];
    obstacles.forEach(obs => allEntities.push({type: 'obs', data: obs, p: obs.progress}));
    coinItems.forEach(coin => allEntities.push({type: 'coin', data: coin, p: coin.progress}));
    
    allEntities.sort((a, b) => a.p - b.p);

    allEntities.forEach(item => {
        let p = item.p;
        let screenY = roadHorizonY + p * (roadBottomY - roadHorizonY);
        let lane = item.data.lane;
        
        let targetX = 400;
        if (lane === 0) targetX = 400 - p * 220;
        else if (lane === 1) targetX = 400;
        else if (lane === 2) targetX = 400 + p * 220;

        let scale = 0.2 + p * 0.8;

        if (item.type === 'coin') {
            let coinBounce = Math.sin(animTimer * 5) * 5;
            ctx.fillStyle = '#ffeb3b';
            ctx.beginPath();
            ctx.arc(targetX, screenY - 20 * scale + coinBounce, 12 * scale, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#fbc02d';
            ctx.lineWidth = 2;
            ctx.stroke();
        } else {
            let obs = item.data;
            if (obs.type === 'rock') {
                ctx.fillStyle = '#78909c';
                ctx.beginPath();
                ctx.arc(targetX, screenY, 28 * scale, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#b0bec5';
                ctx.beginPath();
                ctx.arc(targetX - 4 * scale, screenY - 4 * scale, 10 * scale, 0, Math.PI * 2);
                ctx.fill();
            } else if (obs.type === 'fallen_tree') {
                ctx.fillStyle = '#6d4c41';
                ctx.fillRect(targetX - 45 * scale, screenY - 15 * scale, 90 * scale, 20 * scale);
                ctx.fillStyle = '#66bb6a';
                ctx.beginPath();
                ctx.arc(targetX - 30 * scale, screenY - 10 * scale, 15 * scale, 0, Math.PI * 2);
                ctx.fill();
            } else if (obs.type === 'tree_stump') {
                ctx.fillStyle = '#795548';
                ctx.fillRect(targetX - 20 * scale, screenY - 22 * scale, 40 * scale, 26 * scale);
                ctx.fillStyle = '#4e342e';
                ctx.beginPath();
                ctx.ellipse(targetX, screenY - 22 * scale, 20 * scale, 8 * scale, 0, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    });

    // --- VỊ TRÍ NHÂN CHÍNH (Đã được chỉnh lên rõ ràng ở trung tâm phía trước) ---
    let playerBaseX = 400;
    if (playerLane === 0) playerBaseX = 290;
    else if (playerLane === 1) playerBaseX = 400;
    else if (playerLane === 2) playerBaseX = 510;

    let playerDrawY = 320 + playerYOffset;
    let legAnim = isJumping ? 0 : Math.sin(animTimer * 6) * 10;

    // Vòng hào quang sáng dưới chân nhân vật giúp dễ nhận diện
    ctx.fillStyle = 'rgba(255, 235, 59, 0.4)';
    ctx.beginPath();
    ctx.ellipse(playerBaseX, playerDrawY + 15, 25, 10, 0, 0, Math.PI * 2);
    ctx.fill();

    // Thân nhân vật
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(playerBaseX - 18, playerDrawY - 50, 36, 50);
    // Ba lô
    ctx.fillStyle = '#e91e63';
    ctx.fillRect(playerBaseX - 12, playerDrawY - 42, 24, 28);
    // Đầu
    ctx.fillStyle = '#ffd1b3';
    ctx.beginPath();
    ctx.arc(playerBaseX, playerDrawY - 62, 15, 0, Math.PI * 2);
    ctx.fill();
    // Mũ đỏ
    ctx.fillStyle = '#e53935';
    ctx.beginPath();
    ctx.arc(playerBaseX, playerDrawY - 66, 15, Math.PI, Math.PI * 2);
    ctx.fill();
    // Chân chạy
    ctx.fillStyle = '#1565c0';
    ctx.fillRect(playerBaseX - 11, playerDrawY, 9, 22 + legAnim);
    ctx.fillRect(playerBaseX + 2, playerDrawY, 9, 22 - legAnim);

    // --- QUÁI VẬT XANH BÁM ĐUỔI NGAY PHÍA SAU ---
    let monsterBreath = Math.sin(animTimer * 5) * 6;
    let monsterX = 400 + (playerLane - 1) * 35;
    let monsterY = 390 + monsterBreath;

    ctx.fillStyle = '#00796b';
    ctx.beginPath();
    ctx.arc(monsterX, monsterY, 55, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#00897b';
    ctx.beginPath();
    ctx.arc(monsterX, monsterY - 20, 35, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#ffeb3b';
    ctx.beginPath();
    ctx.arc(monsterX - 12, monsterY - 25, 7, 0, Math.PI * 2);
    ctx.arc(monsterX + 12, monsterY - 25, 7, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#d32f2f';
    ctx.beginPath();
    ctx.arc(monsterX - 12, monsterY - 25, 3, 0, Math.PI * 2);
    ctx.arc(monsterX + 12, monsterY - 25, 3, 0, Math.PI * 2);
    ctx.fill();

    if (gameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.85)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#ff5252';
        ctx.font = 'bold 38px "Courier New"';
        ctx.textAlign = 'center';
        ctx.fillText('BẠN ĐÃ BỊ QUÁI VẬT TÚM TÓC!', canvas.width / 2, 180);
        
        ctx.fillStyle = '#ffeb3b';
        ctx.font = '22px "Courier New"';
        ctx.fillText('⭐ Điểm số: ' + score + '   |   🪙 Tiền vàng: ' + coins, canvas.width / 2, 240);
        
        ctx.fillStyle = '#ffffff';
        ctx.font = '16px "Courier New"';
        ctx.fillText('Nhấn nút bên dưới để thử lại', canvas.width / 2, 300);
        
        document.getElementById('start-screen').style.display = 'flex';
        document.getElementById('start-screen').querySelector('h1').innerText = 'THUA MẤT RỒI!';
        document.getElementById('start-screen').querySelector('button').innerText = 'CHƠI LẠI NGAY';
    }

    document.getElementById('score-display').innerText = score;
    document.getElementById('coin-display').innerText = coins;
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

components.html(game_html, height=580, scrolling=False)
