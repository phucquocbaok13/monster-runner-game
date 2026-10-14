import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Chạy Trốn Quái Vật - Góc Nhìn Từ Sau Lưng",
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

st.markdown("<h1>🏃 CHẠY TRỐN QUÁI VẬT - GÓC NHÌN TỪ SAU LƯNG 🌳</h1>", unsafe_allow_html=True)

# Phần hướng dẫn điều khiển sáng rực Neon (Đã cập nhật phím W để nhảy)
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
            <li><b>Phím W:</b> Nhảy qua tảng đá / chướng ngại vật thấp.</li>
            <li><b>Phím A:</b> Né sang làn TRÁI.</li>
            <li><b>Phím D:</b> Né sang làn PHẢI.</li>
        </ul>
        <p style="margin-bottom: 0;"><i>🔥 Mẹo: Sử dụng phím W để nhảy và A/D để đổi làn thật mượt mà. Quái vật xanh đang rượt sát sau gáy bạn đấy!</i></p>
    </div>
    """, unsafe_allow_html=True)

# Mã nguồn HTML/JS trò chơi
game_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Monster Rear View Runner</title>
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
            background: #121c13;
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
            background: rgba(0, 0, 0, 0.88);
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
        <span id="danger-display" style="color: #ff4b4b;">⚠️ QUÁI VẬT: SÁT GÁY!</span>
    </div>

    <div id="start-screen">
        <h1 style="color: #4caf50; margin-bottom: 5px; text-shadow: 0 0 10px #2e7d32;">RỪNG SÂU TỬ THẦN - GÓC NHÌN TỪ SAU LƯNG</h1>
        <p style="max-width: 450px; color: #ccc; font-size: 14px; line-height: 1.4;">
            Sử dụng phím <b>W</b> để nhảy, <b>A</b> (Trái), <b>D</b> (Phải) để né làn!
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
let gameSpeed = 5;
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

const roadHorizonY = 180;
const roadBottomY = 500;

let playerLane = 1; // 0, 1, 2
let playerYOffset = 0;
let playerJumpVY = 0;
let isJumping = false;

let obstacles = [];
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
    gameSpeed = 5;
    obstacles = [];
    playerLane = 1;
    playerYOffset = 0;
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
        progress: 0.05,
        type: type
    });
}

setInterval(spawnObstacle, 1500);

function update() {
    if (!gameStarted || gameOver) return;

    score += 1;
    animTimer += 0.2;
    gameSpeed = 5 + Math.floor(score / 300) * 0.5;

    if (isJumping) {
        playerYOffset += playerJumpVY;
        playerJumpVY += 0.65;
        if (playerYOffset >= 0) {
            playerYOffset = 0;
            isJumping = false;
        }
    }

    roadScroll += gameSpeed * 3;

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
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#0a100c';
    ctx.fillRect(0, 0, canvas.width, roadHorizonY);

    ctx.beginPath();
    ctx.moveTo(400, roadHorizonY);
    ctx.lineTo(150, roadBottomY);
    ctx.lineTo(650, roadBottomY);
    ctx.closePath();
    ctx.fillStyle = '#1e2c20';
    ctx.fill();

    ctx.strokeStyle = '#38543b';
    ctx.lineWidth = 3;
    
    ctx.beginPath();
    ctx.moveTo(400, roadHorizonY);
    ctx.lineTo(316, roadBottomY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(400, roadHorizonY);
    ctx.lineTo(483, roadBottomY);
    ctx.stroke();

    ctx.fillStyle = '#141f15';
    for (let i = -2; i < 8; i++) {
        let treeProgress = (i * 0.2 + (roadScroll * 0.001)) % 1.0;
        let treeY = roadHorizonY + treeProgress * (roadBottomY - roadHorizonY);
        let leftTreeX = 400 - treeProgress * 300;
        let rightTreeX = 400 + treeProgress * 300;
        
        ctx.beginPath();
        ctx.arc(leftTreeX, treeY, 20 + treeProgress * 35, 0, Math.PI * 2);
        ctx.arc(rightTreeX, treeY, 20 + treeProgress * 35, 0, Math.PI * 2);
        ctx.fill();
    }

    obstacles.sort((a, b) => a.progress - b.progress);

    obstacles.forEach(obs => {
        let p = obs.progress;
        let screenY = roadHorizonY + p * (roadBottomY - roadHorizonY);
        
        let targetX = 400;
        if (obs.lane === 0) targetX = 400 - p * 250;
        else if (obs.lane === 1) targetX = 400;
        else if (obs.lane === 2) targetX = 400 + p * 250;

        let scale = 0.2 + p * 0.8;

        if (obs.type === 'rock') {
            ctx.fillStyle = '#4a5568';
            ctx.beginPath();
            ctx.arc(targetX, screenY, 30 * scale, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#718096';
            ctx.beginPath();
            ctx.arc(targetX - 5 * scale, screenY - 5 * scale, 12 * scale, 0, Math.PI * 2);
            ctx.fill();
        } else if (obs.type === 'fallen_tree') {
            ctx.fillStyle = '#5c4033';
            ctx.fillRect(targetX - 50 * scale, screenY - 15 * scale, 100 * scale, 22 * scale);
            ctx.fillStyle = '#2e7d32';
            ctx.beginPath();
            ctx.arc(targetX - 35 * scale, screenY - 10 * scale, 18 * scale, 0, Math.PI * 2);
            ctx.fill();
        } else if (obs.type === 'tree_stump') {
            ctx.fillStyle = '#6e4f3a';
            ctx.fillRect(targetX - 22 * scale, screenY - 25 * scale, 44 * scale, 30 * scale);
            ctx.fillStyle = '#3b2219';
            ctx.beginPath();
            ctx.ellipse(targetX, screenY - 25 * scale, 22 * scale, 9 * scale, 0, 0, Math.PI * 2);
            ctx.fill();
        }
    });

    let playerBaseX = 400;
    if (playerLane === 0) playerBaseX = 270;
    else if (playerLane === 1) playerBaseX = 400;
    else if (playerLane === 2) playerBaseX = 530;

    let playerDrawY = 430 + playerYOffset;
    let legAnim = isJumping ? 0 : Math.sin(animTimer * 6) * 8;

    ctx.fillStyle = '#ffcc00';
    ctx.fillRect(playerBaseX - 18, playerDrawY - 45, 36, 45);
    ctx.fillStyle = '#ffd1b3';
    ctx.beginPath();
    ctx.arc(playerBaseX, playerDrawY - 55, 14, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#1e88e5';
    ctx.beginPath();
    ctx.arc(playerBaseX, playerDrawY - 58, 14, Math.PI, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#1a237e';
    ctx.fillRect(playerBaseX - 12, playerDrawY, 9, 20 + legAnim);
    ctx.fillRect(playerBaseX + 3, playerDrawY, 9, 20 - legAnim);

    let monsterBreath = Math.sin(animTimer * 5) * 6;
    let monsterX = 400 + (playerLane - 1) * 60;
    let monsterY = 475 + monsterBreath;

    ctx.fillStyle = '#004d40';
    ctx.beginPath();
    ctx.arc(monsterX, monsterY, 55, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#00695c';
    ctx.beginPath();
    ctx.arc(monsterX, monsterY - 20, 35, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#ffea00';
    ctx.beginPath();
    ctx.arc(monsterX - 15, monsterY - 25, 7, 0, Math.PI * 2);
    ctx.arc(monsterX + 15, monsterY - 25, 7, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#ff3d00';
    ctx.beginPath();
    ctx.arc(monsterX - 15, monsterY - 25, 3, 0, Math.PI * 2);
    ctx.arc(monsterX + 15, monsterY - 25, 3, 0, Math.PI * 2);
    ctx.fill();

    if (gameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.88)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#ff3333';
        ctx.font = 'bold 38px "Courier New"';
        ctx.textAlign = 'center';
        ctx.fillText('BẠN ĐÃ BỊ QUÁI VẬT XANH TÚM TÓC!', canvas.width / 2, 190);
        
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
