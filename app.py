import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Chạy Trốn Quái Vật - Rừng Đêm 3D",
    page_icon="🌲",
    layout="centered"
)

st.markdown("""
    <style>
    .main {
        background-color: #050811;
        color: #ffffff;
    }
    .stApp {
        max-width: 900px;
        margin: 0 auto;
    }
    h1 {
        text-align: center;
        color: #00ffff;
        text-shadow: 0 0 15px rgba(0, 255, 255, 0.7);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌲 CHẠY TRỐN QUÁI VẬT - RỪNG ĐÊM 3D 🌙</h1>", unsafe_allow_html=True)

# Hướng dẫn điều khiển
with st.container():
    st.markdown("""
    <style>
    .box-hd {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        padding: 18px;
        border-radius: 10px;
        border: 2px solid #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
        margin-bottom: 20px;
    }
    .box-hd h3 { color: #38bdf8; margin-top: 0; }
    .box-hd li { color: #f8fafc; font-size: 16px; margin-bottom: 6px; }
    .box-hd b { color: #fde047; }
    .tip { color: #34d399; font-weight: bold; margin-top: 8px; }
    </style>
    <div class="box-hd">
        <h3>🎮 ĐIỀU KHIỂN TRÒ CHƠI:</h3>
        <ul>
            <li><b>Phím W:</b> Nhảy lên tránh chướng ngại vật (Cây đổ ngang).</li>
            <li><b>Phím A:</b> Chuyển sang làn TRÁI.</li>
            <li><b>Phím D:</b> Chuyển sang làn PHẢI.</li>
        </ul>
        <div class="tip">💡 Mẹo: Nhân vật mặc áo hoodie xám sáng rõ và quái vật xanh neon cực kỳ nổi bật ở ngay phía trước màn hình!</div>
    </div>
    """, unsafe_allow_html=True)

# Mã nguồn HTML/JS hoàn toàn mới, tối ưu hóa chống lỗi và hiển thị chắc chắn nhân vật
game_code = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Night Forest 3D Runner</title>
    <style>
        body {
            margin: 0;
            background: #000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: monospace;
            color: white;
            overflow: hidden;
        }
        #game-wrap {
            position: relative;
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.4);
            border-radius: 8px;
            overflow: hidden;
        }
        canvas {
            display: block;
            background: #030712;
        }
        #hud {
            position: absolute;
            top: 12px;
            left: 15px;
            right: 15px;
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 2px 2px #000;
            pointer-events: none;
        }
        .badge {
            background: rgba(15, 23, 42, 0.85);
            padding: 6px 14px;
            border-radius: 6px;
            border: 1px solid #38bdf8;
        }
        #menu {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(3, 7, 18, 0.94);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            z-index: 10;
        }
        .play-btn {
            background: #0284c7;
            color: white;
            border: none;
            padding: 14px 32px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 20px;
            box-shadow: 0 0 15px #38bdf8;
            transition: 0.2s;
        }
        .play-btn:hover {
            background: #38bdf8;
            color: #0f172a;
            transform: scale(1.05);
        }
    </style>
</head>
<body>

<div id="game-wrap">
    <div id="hud">
        <div class="badge">⭐ ĐIỂM: <span id="score">0</span></div>
        <div class="badge" style="color: #fde047;">🪙 VÀNG: <span id="coins">0</span></div>
        <div class="badge" style="color: #f43f5e;">⚠️ QUÁI VẬT: SÁT GÁY</div>
    </div>

    <div id="menu">
        <h1 style="color: #38bdf8; margin-bottom: 10px; text-shadow: 0 0 15px #0284c7;">RỪNG ĐÊM 3D: CHẠY TRỐN</h1>
        <p style="max-width: 450px; color: #94a3b8; font-size: 15px; line-height: 1.5;">
            Nhân vật áo hoodie xám và quái vật xanh neon xuất hiện trực diện!<br>
            Dùng phím <b>W</b> để nhảy, <b>A</b> và <b>D</b> để né tránh chướng ngại vật!
        </p>
        <button class="play-btn" onclick="startTheGame()">BẮT ĐẦU CHƠI</button>
    </div>

    <canvas id="cvs" width="800" height="500"></canvas>
</div>

<script>
const cvs = document.getElementById('cvs');
const ctx = cvs.getContext('2d');

let playing = false;
let score = 0;
let coins = 0;
let speed = 5;
let timer = 0;

const lanes = [260, 400, 540];
let currentLane = 1;

let jumpY = 0;
let jumpVY = 0;
let isJumping = false;

let obstacles = [];
let coinList = [];
let roadOffset = 0;

window.addEventListener('keydown', (e) => {
    if (!playing) return;
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') {
        if (currentLane > 0) currentLane--;
    } else if (e.code === 'KeyD' || e.code === 'ArrowRight') {
        if (currentLane < 2) currentLane++;
    } else if ((e.code === 'KeyW' || e.code === 'ArrowUp') && !isJumping) {
        isJumping = true;
        jumpVY = -12;
        e.preventDefault();
    }
});

function startTheGame() {
    playing = true;
    score = 0;
    coins = 0;
    speed = 5.5;
    currentLane = 1;
    jumpY = 0;
    isJumping = false;
    obstacles = [];
    coinList = [];
    document.getElementById('menu').style.display = 'none';
}

function spawnObjects() {
    if (!playing) return;
    let lane = Math.floor(Math.random() * 3);
    if (Math.random() < 0.6) {
        let types = ['rock', 'log', 'tree'];
        let type = types[Math.floor(Math.random() * types.length)];
        obstacles.push({ lane: lane, z: 0.05, type: type });
    } else {
        coinList.push({ lane: lane, z: 0.05 });
    }
}
setInterval(spawnObjects, 1300);

function updateGame() {
    if (!playing) return;

    score++;
    timer += 0.2;
    speed = 5.5 + Math.floor(score / 350) * 0.4;
    roadOffset += speed * 4;

    if (isJumping) {
        jumpY += jumpVY;
        jumpVY += 0.65;
        if (jumpY >= 0) {
            jumpY = 0;
            isJumping = false;
        }
    }

    for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.z += speed * 0.0025;

        if (obs.z >= 0.84 && obs.z <= 0.95 && obs.lane === currentLane) {
            if (obs.type === 'log' && isJumping && jumpY < -35) {
                // Nhảy qua an toàn
            } else {
                playing = false;
            }
        }

        if (obs.z > 1.05) obstacles.splice(i, 1);
    }

    for (let i = coinList.length - 1; i >= 0; i--) {
        let c = coinList[i];
        c.z += speed * 0.0025;

        if (c.z >= 0.84 && c.z <= 0.95 && c.lane === currentLane && jumpY > -45) {
            coins++;
            coinList.splice(i, 1);
            continue;
        }

        if (c.z > 1.05) coinList.splice(i, 1);
    }
}

function renderGame() {
    ctx.clearRect(0, 0, cvs.width, cvs.height);

    // 1. Bầu trời & Trăng
    let skyGrad = ctx.createLinearGradient(0, 0, 0, 160);
    skyGrad.addColorStop(0, '#0f172a');
    skyGrad.addColorStop(1, '#1e293b');
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, cvs.width, 160);

    ctx.fillStyle = '#f1f5f9';
    ctx.beginPath(); ctx.arc(680, 50, 28, 0, Math.PI * 2); ctx.fill();

    // 2. Con đường 3D
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 160, cvs.width, 340);

    ctx.beginPath();
    ctx.moveTo(400, 160);
    ctx.lineTo(100, 500);
    ctx.lineTo(700, 500);
    ctx.closePath();
    ctx.fillStyle = '#1e293b';
    ctx.fill();

    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(400, 160); ctx.lineTo(260, 500);
    ctx.moveTo(400, 160); ctx.lineTo(540, 500);
    ctx.stroke();

    // 3. Hai hàng cây hai bên
    for (let i = -2; i < 8; i++) {
        let tProg = (i * 0.2 + (roadOffset * 0.001)) % 1.0;
        let tY = 160 + tProg * 340;
        let lX = 400 - tProg * 380;
        let rX = 400 + tProg * 380;
        let s = 0.2 + tProg * 0.8;

        ctx.fillStyle = '#334155';
        ctx.fillRect(lX - 6*s, tY, 12*s, 40*s);
        ctx.fillRect(rX - 6*s, tY, 12*s, 40*s);

        ctx.fillStyle = '#10b981';
        ctx.beginPath(); ctx.arc(lX, tY - 10*s, 22*s, 0, Math.PI*2); ctx.fill();
        ctx.beginPath(); ctx.arc(rX, tY - 10*s, 22*s, 0, Math.PI*2); ctx.fill();
    }

    // 4. Vật thể & Tiền vàng
    obstacles.forEach(o => {
        let z = o.z;
        let screenY = 160 + z * 340;
        let sc = 0.2 + z * 0.8;
        let targetX = (o.lane === 0) ? 400 - z * 300 : (o.lane === 2) ? 400 + z * 300 : 400;

        if (o.type === 'rock') {
            ctx.fillStyle = '#94a3b8';
            ctx.beginPath(); ctx.arc(targetX, screenY, 30*sc, 0, Math.PI*2); ctx.fill();
        } else if (o.type === 'log') {
            ctx.fillStyle = '#a16207';
            ctx.fillRect(targetX - 45*sc, screenY - 15*sc, 90*sc, 22*sc);
        } else if (o.type === 'tree') {
            ctx.fillStyle = '#78350f';
            ctx.fillRect(targetX - 12*sc, screenY - 45*sc, 24*sc, 50*sc);
        }
    });

    coinList.forEach(c => {
        let z = c.z;
        let screenY = 160 + z * 340;
        let sc = 0.2 + z * 0.8;
        let targetX = (c.lane === 0) ? 400 - z * 300 : (c.lane === 2) ? 400 + z * 300 : 400;

        ctx.fillStyle = '#fde047';
        ctx.beginPath(); ctx.arc(targetX, screenY - 20*sc, 14*sc, 0, Math.PI*2); ctx.fill();
    });

    // ==========================================
    // 5. NHÂN VẬT CHÍNH (HOODIE XÁM SÁNG) - LUÔN HIỂN THỊ Ở TIỀN CẢNH
    // ==========================================
    let pX = lanes[currentLane];
    let pY = 410 + jumpY;
    let legMove = isJumping ? 0 : Math.sin(timer * 0.8) * 12;

    // Bóng nhân vật
    ctx.fillStyle = 'rgba(0,0,0,0.6)';
    ctx.beginPath(); ctx.ellipse(pX, pY + 30, 26, 10, 0, 0, Math.PI*2); ctx.fill();

    // Thân áo hoodie xám sáng
    ctx.fillStyle = '#cbd5e1';
    ctx.fillRect(pX - 22, pY - 60, 44, 60);
    // Mũ hoodie trùm phía sau
    ctx.fillStyle = '#94a3b8';
    ctx.beginPath(); ctx.arc(pX, pY - 52, 20, Math.PI, Math.PI*2); ctx.fill();
    // Đầu và tóc
    ctx.fillStyle = '#fef08a';
    ctx.beginPath(); ctx.arc(pX, pY - 74, 16, 0, Math.PI*2); ctx.fill();
    // Chân chạy
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(pX - 13, pY, 11, 28 + legMove);
    ctx.fillRect(pX + 2, pY, 11, 28 - legMove);

    // ==========================================
    // 6. QUÁI VẬT XANH LÁ NEON - SÁT GÁY NGAY SAU LƯNG
    // ==========================================
    let mBreath = Math.sin(timer * 0.5) * 6;
    let mX = pX;
    let mY = 465 + mBreath;

    ctx.fillStyle = '#16a34a';
    ctx.beginPath(); ctx.arc(mX, mY, 75, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = '#22c55e';
    ctx.beginPath(); ctx.arc(mX, mY - 25, 52, 0, Math.PI*2); ctx.fill();

    // Mắt phát sáng dữ dội
    ctx.fillStyle = '#fde047';
    ctx.beginPath(); ctx.arc(mX - 16, mY - 32, 10, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(mX + 16, mY - 32, 10, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = '#ef4444';
    ctx.beginPath(); ctx.arc(mX - 16, mY - 32, 4.5, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(mX + 16, mY - 32, 4.5, 0, Math.PI*2); ctx.fill();

    // 7. MÀN HÌNH GAME OVER
    if (!playing && score > 0) {
        ctx.fillStyle = 'rgba(3, 7, 18, 0.94)';
        ctx.fillRect(0, 0, cvs.width, cvs.height);

        ctx.fillStyle = '#f43f5e';
        ctx.font = 'bold 36px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('BẠN ĐÃ BỊ QUÁI VẬT TÚM TÓC!', cvs.width / 2, 180);

        ctx.fillStyle = '#fde047';
        ctx.font = '22px monospace';
        ctx.fillText('⭐ Điểm: ' + score + '  |  🪙 Vàng: ' + coins, cvs.width / 2, 240);

        ctx.fillStyle = '#94a3b8';
        ctx.font = '16px monospace';
        ctx.fillText('Nhấn nút bên dưới để chơi lại', cvs.width / 2, 300);

        document.getElementById('menu').style.display = 'flex';
        document.getElementById('menu').querySelector('h1').innerText = 'THUA MẤT RỒI!';
        document.querySelector('.play-btn').innerText = 'CHƠI LẠI NGAY';
    }

    document.getElementById('score').innerText = score;
    document.getElementById('coins').innerText = coins;
}

function mainLoop() {
    try {
        updateGame();
        renderGame();
    } catch(err) {
        console.error(err);
    }
    requestAnimationFrame(mainLoop);
}

mainLoop();
</script>

</body>
</html>
"""

components.html(game_code, height=580, scrolling=False)
