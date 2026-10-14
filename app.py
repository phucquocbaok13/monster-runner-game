import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Chạy Trốn Quái Vật - Forest Runner",
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
    }
    .instructions {
        background-color: #1e2530;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 5px solid #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏃 CHẠY TRỐN QUÁI VẬT - VƯỢT CHƯỚNG NGẠI VẬT 🌳</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div class="instructions">
        <h3>🎮 Hướng dẫn điều khiển:</h3>
        <ul>
            <li><b>Phím SPACE (Dấu cách):</b> Nhảy qua chướng ngại vật thấp.</li>
            <li><b>Phím A:</b> Né sang làn bên TRÁI.</li>
            <li><b>Phím D:</b> Né sang làn bên PHẢI.</li>
        </ul>
        <p><i>Mẹo: Quái vật đang bám đuổi sát nút phía sau! Hãy tập trung cao độ, né tránh cây đổ, khúc cây và tảng đá lớn trong khu rừng u ám! Bật âm thanh để nghe nhạc nền căng thẳng.</i></p>
    </div>
    """, unsafe_allow_html=True)

# Mã nguồn HTML/JS của trò chơi
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Monster Forest Runner</title>
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
            box-shadow: 0 0 25px rgba(255, 0, 0, 0.5);
            border-radius: 8px;
            overflow: hidden;
            background: #111;
        }
        canvas {
            display: block;
            background: #1a2416;
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
            background: #ff3333;
            color: white;
            border: none;
            padding: 12px 25px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 15px;
            box-shadow: 0 0 10px #ff0000;
            transition: 0.2s;
        }
        .btn:hover {
            background: #ff5252;
            transform: scale(1.05);
        }
    </style>
</head>
<body>

<div id="game-container">
    <div id="ui">
        <span id="score-display">ĐIỂM: 0</span>
        <span id="danger-display" style="color: #ff4b4b;">⚠️ QUÁI VẬT: GẦN KỀ</span>
    </div>

    <div id="start-screen">
        <h1 style="color: #ff3333; margin-bottom: 5px; text-shadow: 0 0 10px red;">RỪNG SÂU TỬ THẦN</h1>
        <p style="max-width: 400px; color: #ccc; font-size: 14px; line-height: 1.4;">
            Quái vật ác mộng đang đuổi theo sau lưng bạn!<br>
            Sử dụng <b>A</b> (Trái), <b>D</b> (Phải) để đổi làn và <b>SPACE</b> để nhảy.
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
let gameSpeed = 6;

// Âm thanh căng thẳng bằng Web Audio API
let audioCtx = null;
let musicInterval = null;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
    // Nhạc nền hung dữ, căng thẳng (nhịp trống dồn dập + tiếng hú quái vật trầm)
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
        }, 180); // Nhịp điệu nhanh, dồn dập gây hồi hộp
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

// Làn đường (3 làn tương tự Subway Surfers: 0: Trái, 1: Giữa, 2: Phải)
const lanes = [260, 400, 540]; 
let playerLane = 1; 
let playerY = 380;
let playerJumpVY = 0;
let isJumping = false;

const player = {
    x: lanes[1],
    y: 380,
    width: 45,
    height: 70,
    targetX: lanes[1]
};

let obstacles = [];
let forestScrollY = 0;

// Xử lý phím bấm
window.addEventListener('keydown', (e) => {
    if (!gameStarted || gameOver) return;
    
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') {
        if (playerLane > 0) {
            playerLane--;
            player.targetX = lanes[playerLane];
        }
    } else if (e.code === 'KeyD' || e.code === 'ArrowRight') {
        if (playerLane < 2) {
            playerLane++;
            player.targetX = lanes[playerLane];
        }
    } else if (e.code === 'Space' && !isJumping) {
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
    gameSpeed = 6;
    obstacles = [];
    playerLane = 1;
    player.targetX = lanes[1];
    document.getElementById('start-screen').style.display = 'none';
    initAudio();
}

// Sinh chướng ngại vật ngẫu nhiên trên 3 làn
function spawnObstacle() {
    if (!gameStarted || gameOver) return;
    let lane = Math.floor(Math.random() * 3);
    // Các loại: 'rock' (tảng đá), 'fallen_tree' (cây đổ ngang), 'tree_stump' (gốc cây mọc trên đường)
    let types = ['rock', 'fallen_tree', 'tree_stump'];
    let type = types[Math.floor(Math.random() * types.length)];
    
    obstacles.push({
        lane: lane,
        x: lanes[lane],
        y: -50,
        type: type,
        width: 60,
        height: type === 'fallen_tree' ? 40 : 50
    });
}

setInterval(spawnObstacle, 1400);

function update() {
    if (!gameStarted || gameOver) return;

    // Tăng độ khó dần theo điểm
    score += 1;
    gameSpeed = 6 + Math.floor(score / 300);

    // Di chuyển mượt sang làn
    player.x += (player.targetX - player.x) * 0.2;

    // Xử lý nhảy
    if (isJumping) {
        player.y += playerJumpVY;
        playerJumpVY += 0.6; // trọng lực
        if (player.y >= 380) {
            player.y = 380;
            isJumping = false;
        }
    }

    // Cuộn cảnh rừng (hiệu ứng 3D góc nhìn từ trên xuống tương tự Subway Surfers)
    forestScrollY += gameSpeed * 1.5;

    // Cập nhật chướng ngại vật
    for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.y += gameSpeed;

        // Kiểm tra va chạm
        // Nhân vật nằm ở y khoảng 380
        let inSameLane = playerLane === obs.lane;
        let isHitY = (player.y + player.height > obs.y && player.y < obs.y + obs.height);
        
        if (inSameLane && isHitY) {
            // Nếu nhảy qua được chướng ngại vật thấp (như tảng đá nhỏ / gốc cây), không bị chết
            if (obs.type === 'rock' && isJumping && player.y < obs.y) {
                // Nhảy qua an toàn
            } else {
                // Va chạm! Game Over
                gameOver = true;
                playSound('hit');
            }
        }

        // Xóa vật cản khi ra ngoài màn hình
        if (obs.y > 550) {
            obstacles.splice(i, 1);
        }
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Vẽ nền rừng rậm u ám (phối cảnh 3 làn đường)
    // Màu nền đất rừng tối
    ctx.fillStyle = '#1c281d';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Vẽ 3 làn đường (hiệu ứng phối cảnh hẹp dần phía trên)
    // Vùng đường đi chính
    ctx.beginPath();
    ctx.moveTo(150, 0);
    ctx.lineTo(650, 0);
    ctx.lineTo(750, 500);
    ctx.lineTo(50, 500);
    ctx.fillStyle = '#263828';
    ctx.fill();

    // Vạch chia làn đường
    ctx.strokeStyle = '#3e5c40';
    ctx.lineWidth = 4;
    ctx.setLineDash([15, 15]);
    ctx.lineDashOffset = -forestScrollY;
    
    ctx.beginPath();
    ctx.moveTo(333, 0); ctx.lineTo(316, 500);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(466, 0); ctx.lineTo(483, 500);
    ctx.stroke();
    ctx.setLineDash([]); // Reset line dash

    // Cây cối 2 bên đường (tạo cảm giác rừng rậm u ám)
    ctx.fillStyle = '#0d140e';
    for (let i = -2; i < 6; i++) {
        let treeY = (i * 120 + forestScrollY) % 600 - 50;
        // Cây bên trái
        ctx.beginPath();
        ctx.arc(40, treeY, 45, 0, Math.PI * 2);
        ctx.fill();
        // Cây bên phải
        ctx.beginPath();
        ctx.arc(760, treeY + 60, 45, 0, Math.PI * 2);
        ctx.fill();
    }

    // 2. Vẽ Chướng ngại vật (Cây đổ, gốc cây, tảng đá lớn)
    obstacles.forEach(obs => {
        let renderX = obs.x;
        let renderY = obs.y;
        
        if (obs.type === 'rock') {
            // Tảng đá lớn xám rêu
            ctx.fillStyle = '#4a5568';
            ctx.beginPath();
            ctx.arc(renderX, renderY + 25, 28, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#718096';
            ctx.beginPath();
            ctx.arc(renderX - 5, renderY + 20, 12, 0, Math.PI * 2);
            ctx.fill();
        } else if (obs.type === 'fallen_tree') {
            // Cây đổ ngang đường
            ctx.fillStyle = '#5c4033';
            ctx.fillRect(renderX - 45, renderY + 10, 90, 25);
            ctx.fillStyle = '#2e7d32'; // lá cây
            ctx.beginPath();
            ctx.arc(renderX - 40, renderY + 20, 18, 0, Math.PI * 2);
            ctx.fill();
        } else if (obs.type === 'tree_stump') {
            // Cây mọc / gốc cây lớn trên đường
            ctx.fillStyle = '#6e4f3a';
            ctx.fillRect(renderX - 25, renderY + 15, 50, 35);
            ctx.fillStyle = '#3b2219';
            ctx.beginPath();
            ctx.ellipse(renderX, renderY + 15, 25, 10, 0, 0, Math.PI * 2);
            ctx.fill();
        }
    });

    // 3. Vẽ Nhân vật (Người chơi chạy trốn)
    ctx.fillStyle = '#ffcc00'; // Áo vàng nổi bật
    ctx.fillRect(player.x - player.width / 2, player.y, player.width, player.height);
    // Đầu nhân vật
    ctx.fillStyle = '#ffd1b3';
    ctx.beginPath();
    ctx.arc(player.x, player.y - 10, 15, 0, Math.PI * 2);
    ctx.fill();
    // Balo / Chi tiết
    ctx.fillStyle = '#e65100';
    ctx.fillRect(player.x - 12, player.y + 15, 24, 30);

    // 4. Vẽ Quái vật bám đuổi sát phía sau (ở đáy màn hình)
    ctx.fillStyle = '#b71c1c';
    ctx.beginPath();
    ctx.moveTo(250, 480);
    ctx.lineTo(400, 430);
    ctx.lineTo(550, 480);
    ctx.closePath();
    ctx.fill();
    // Mắt quái vật phát sáng đỏ hung dữ
    ctx.fillStyle = '#ffff00';
    ctx.beginPath();
    ctx.arc(360, 455, 6, 0, Math.PI * 2);
    ctx.arc(440, 455, 6, 0, Math.PI * 2);
    ctx.fill();

    // 5. Màn hình Game Over
    if (gameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#ff3333';
        ctx.font = 'bold 45px "Courier New"';
        ctx.textAlign = 'center';
        ctx.fillText('BẠN ĐÃ BỊ QUÁI VẬT BẮT!', canvas.width / 2, 200);
        
        ctx.fillStyle = '#ffffff';
        ctx.font = '24px "Courier New"';
        ctx.fillText('Điểm đạt được: ' + score, canvas.width / 2, 260);
        
        ctx.fillStyle = '#aaaaaa';
        ctx.font = '16px "Courier New"';
        ctx.fillText('Nhấn nút dưới để thử lại', canvas.width / 2, 310);
        
        document.getElementById('start-screen').style.display = 'flex';
        document.getElementById('start-screen').querySelector('h1').innerText = 'THUA MẤT RỒI!';
        document.getElementById('start-screen').querySelector('button').innerText = 'CHƠI LẠI NGAY';
    }

    // Cập nhật hiển thị điểm số trên UI
    document.getElementById('score-display').innerText = 'ĐIỂM: ' + score;
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// Khởi chạy vòng lặp game
gameLoop();
</script>

</body>
</html>
"""

# Hiển thị game vào Streamlit component (chiều cao 560px)
components.html(game_html, height=580, scrolling=False)
