import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Chạy Trốn Quái Vật - Rừng Đêm",
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

st.markdown("<h1>🌲 CHẠY TRỐN QUÁI VẬT - RỪNG ĐÊM 🌙</h1>", unsafe_allow_html=True)

# Hướng dẫn điều khiển chỉ dùng phím mũi tên
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
            <li><b>Mũi tên Lên (⬆️):</b> Nhảy lên tránh chướng ngại vật.</li>
            <li><b>Mũi tên Trái (⬅️):</b> Chuyển sang làn TRÁI.</li>
            <li><b>Mũi tên Phải (➡️):</b> Chuyển sang làn PHẢI.</li>
        </ul>
        <div class="tip">💡 Mẹo: Chạy được 2 giây, quái vật Grinch sẽ tự động lùi lại tạo khoảng cách!</div>
    </div>
    """, unsafe_allow_html=True)

# Mã nguồn HTML/JS hoàn chỉnh
game_code = (
    "<!DOCTYPE html>"
    "<html lang='vi'>"
    "<head>"
    "<meta charset='UTF-8'>"
    "<title>Night Forest Straight Road</title>"
    "<style>"
    "body { margin: 0; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: monospace; color: white; overflow: hidden; }"
    "#game-wrap { position: relative; box-shadow: 0 0 25px rgba(0, 255, 255, 0.4); border-radius: 8px; overflow: hidden; }"
    "canvas { display: block; background: #030712; }"
    "#hud { position: absolute; top: 12px; left: 15px; right: 15px; display: flex; justify-content: space-between; font-size: 18px; font-weight: bold; text-shadow: 2px 2px #000; pointer-events: none; }"
    ".badge { background: rgba(15, 23, 42, 0.85); padding: 6px 14px; border-radius: 6px; border: 1px solid #38bdf8; }"
    "#menu { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 7, 18, 0.95); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 10; }"
    ".play-btn { background: #0284c7; color: white; border: none; padding: 14px 32px; font-size: 20px; font-weight: bold; border-radius: 8px; cursor: pointer; margin-top: 20px; box-shadow: 0 0 15px #38bdf8; transition: 0.2s; }"
    ".play-btn:hover { background: #38bdf8; color: #0f172a; transform: scale(1.05); }"
    "</style>"
    "</head>"
    "<body>"
    "<div id='game-wrap'>"
    "<div id='hud'>"
    "<div class='badge'>⭐ ĐIỂM: <span id='score'>0</span></div>"
    "<div class='badge' style='color: #fde047;'>🪙 VÀNG: <span id='coins'>0</span></div>"
    "<div class='badge' style='color: #f43f5e;'>🌲 RỪNG ĐÊM</div>"
    "</div>"
    "<div id='menu'>"
    "<h1 style='color: #38bdf8; margin-bottom: 10px; text-shadow: 0 0 15px #0284c7;'>RỪNG ĐÊM: ĐƯỜNG THẲNG</h1>"
    "<p style='max-width: 450px; color: #94a3b8; font-size: 15px; line-height: 1.5;'>"
    "Sau 2 giây chạy, quái vật sẽ tự động lùi lại!<br>"
    "Dùng phím <b>Mũi tên Lên</b> để nhảy, <b>Trái / Phải</b> để đổi làn."
    "</p>"
    "<button class='play-btn' onclick='startTheGame()'>BẮT ĐẦU CHƠI</button>"
    "</div>"
    "<canvas id='cvs' width='800' height='500'></canvas>"
    "</div>"
    "<script>"
    "const cvs = document.getElementById('cvs');"
    "const ctx = cvs.getContext('2d');"
    "let playing = false, score = 0, coins = 0, speed = 3.5, timer = 0, frameCount = 0, currentMY = 460;"
    "const lanes = [280, 400, 520];"
    "let currentLane = 1, jumpY = 0, jumpVY = 0, isJumping = false;"
    "let obstacles = [], coinList = [], floatTexts = [], roadOffset = 0;"
    "window.addEventListener('keydown', (e) => {"
    "  if (!playing) return;"
    "  if (e.code === 'ArrowLeft') { if (currentLane > 0) currentLane--; e.preventDefault(); }"
    "  else if (e.code === 'ArrowRight') { if (currentLane < 2) currentLane++; e.preventDefault(); }"
    "  else if (e.code === 'ArrowUp') { if (!isJumping) { isJumping = true; jumpVY = -11; } e.preventDefault(); }"
    "});"
    "function startTheGame() {"
    "  playing = true; score = 0; coins = 0; speed = 3.5; currentLane = 1; jumpY = 0; isJumping = false; frameCount = 0; currentMY = 460; obstacles = []; coinList = []; floatTexts = [];"
    "  document.getElementById('menu').style.display = 'none';"
    "}"
    "function spawnObjects() {"
    "  if (!playing) return;"
    "  let lane = Math.floor(Math.random() * 3);"
    "  if (Math.random() < 0.6) {"
    "    let types = ['rock', 'log', 'tree'];"
    "    obstacles.push({ lane: lane, y: -50, type: types[Math.floor(Math.random() * types.length)] });"
    "  } else { coinList.push({ lane: lane, y: -50 }); }"
    "}"
    "setInterval(spawnObjects, 1600);"
    "function updateGame() {"
    "  if (!playing) return;"
    "  score++; frameCount++; timer += 0.15; speed = 3.5 + Math.floor(score / 400) * 0.2; roadOffset += speed;"
    "  if (isJumping) { jumpY += jumpVY; jumpVY += 0.55; if (jumpY >= 0) { jumpY = 0; isJumping = false; } }"
    "  for (let i = floatTexts.length - 1; i >= 0; i--) {"
    "    let ft = floatTexts[i]; ft.y += ft.vy; ft.alpha -= 0.025; if (ft.alpha <= 0) floatTexts.splice(i, 1);"
    "  }"
    "  for (let i = obstacles.length - 1; i >= 0; i--) {"
    "    let obs = obstacles[i]; obs.y += speed;"
    "    if (obs.y >= 350 && obs.y <= 420 && obs.lane === currentLane) {"
    "      if (!(obs.type === 'log' && isJumping && jumpY < -35)) { playing = false; }"
    "    }"
    "    if (obs.y > 550) obstacles.splice(i, 1);"
    "  }"
    "  for (let i = coinList.length - 1; i >= 0; i--) {"
    "    let c = coinList[i]; c.y += speed;"
    "    if (c.y >= 350 && c.y <= 420 && c.lane === currentLane && jumpY > -45) {"
    "      coins++;"
    "      floatTexts.push({ x: lanes[c.lane], y: 360, text: '+1coin', alpha: 1.0, vy: -2 });"
    "      coinList.splice(i, 1); continue;"
    "    }"
    "    if (c.y > 550) coinList.splice(i, 1);"
    "  }"
    "}"
    "function renderGame() {"
    "  ctx.clearRect(0, 0, cvs.width, cvs.height);"
    "  let skyGrad = ctx.createLinearGradient(0, 0, 0, 500);"
    "  skyGrad.addColorStop(0, '#020617'); skyGrad.addColorStop(1, '#0f172a');"
    "  ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, cvs.width, 500);"
    "  ctx.fillStyle = '#f1f5f9'; ctx.beginPath(); ctx.arc(700, 70, 30, 0, Math.PI * 2); ctx.fill();"
    "  ctx.fillStyle = '#1e293b'; ctx.fillRect(200, 0, 400, 500);"
    "  ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 4;"
    "  ctx.beginPath(); ctx.moveTo(200, 0); ctx.lineTo(200, 500); ctx.moveTo(600, 0); ctx.lineTo(600, 500); ctx.stroke();"
    "  ctx.strokeStyle = 'rgba(56, 189, 248, 0.3)'; ctx.lineWidth = 2; ctx.setLineDash([15, 15]);"
    "  ctx.beginPath(); ctx.moveTo(333, roadOffset % 500 - 500); ctx.lineTo(333, 500);"
    "  ctx.moveTo(466, roadOffset % 500 - 500); ctx.lineTo(466, 500); ctx.stroke(); ctx.setLineDash([]);"
    "  for (let i = 0; i < 10; i++) {"
    "    let tY = (i * 120 + roadOffset * 1.5) % 600 - 50;"
    "    ctx.fillStyle = '#064e3b'; ctx.beginPath(); ctx.arc(100, tY, 35, 0, Math.PI*2); ctx.arc(700, tY, 35, 0, Math.PI*2); ctx.fill();"
    "    ctx.fillStyle = '#022c22'; ctx.fillRect(92, tY + 15, 16, 40); ctx.fillRect(692, tY + 15, 16, 40);"
    "  }"
    "  obstacles.forEach(o => {"
    "    let targetX = lanes[o.lane];"
    "    if (o.type === 'rock') {"
    "      ctx.fillStyle = '#475569'; ctx.beginPath(); ctx.arc(targetX, o.y, 35, 0, Math.PI*2); ctx.fill();"
    "      ctx.fillStyle = '#94a3b8'; ctx.beginPath(); ctx.arc(targetX - 6, o.y - 6, 15, 0, Math.PI*2); ctx.fill();"
    "    } else if (o.type === 'log') {"
    "      ctx.fillStyle = '#78350f'; ctx.fillRect(targetX - 50, o.y - 12, 100, 24);"
    "      ctx.fillStyle = '#15803d'; ctx.beginPath(); ctx.arc(targetX - 25, o.y - 6, 16, 0, Math.PI*2); ctx.fill();"
    "    } else if (o.type === 'tree') {"
    "      ctx.fillStyle = '#451a03'; ctx.fillRect(targetX - 12, o.y - 45, 24, 50);"
    "      ctx.fillStyle = '#16a34a'; ctx.beginPath(); ctx.arc(targetX, o.y - 50, 32, 0, Math.PI*2); ctx.fill();"
    "    }"
    "  });"
    "  coinList.forEach(c => {"
    "    let targetX = lanes[c.lane];"
    "    let bounce = Math.sin(timer * 5) * 5;"
    "    ctx.fillStyle = '#fde047'; ctx.beginPath(); ctx.arc(targetX, c.y + bounce, 18, 0, Math.PI*2); ctx.fill();"
    "    ctx.strokeStyle = '#ca8a04'; ctx.lineWidth = 3; ctx.stroke();"
    "  });"
    "  floatTexts.forEach(ft => {"
    "    ctx.save(); ctx.globalAlpha = ft.alpha; ctx.fillStyle = '#fde047'; ctx.font = 'bold 20px monospace'; ctx.textAlign = 'center';"
    "    ctx.fillText(ft.text, ft.x, ft.y); ctx.restore();"
    "  });"
    "  let pX = lanes[currentLane], pY = 390 + jumpY;"
    "  let armSwing = Math.sin(timer * 0.4) * 15;"
    "  let legSwing = Math.cos(timer * 0.4) * 12;"
    "  ctx.fillStyle = 'rgba(0,0,0,0.6)'; ctx.beginPath(); ctx.ellipse(pX, pY + 30, 22, 8, 0, 0, Math.PI*2); ctx.fill();"
    "  ctx.fillStyle = '#334155'; ctx.fillRect(pX - 12 - legSwing, pY + 15, 8, 20); ctx.fillRect(pX + 4 + legSwing, pY + 15, 8, 20);"
    "  ctx.fillStyle = '#e2e8f0'; ctx.fillRect(pX - 16, pY - 25, 32, 40);"
    "  ctx.fillStyle = '#94a3b8'; ctx.fillRect(pX - 22, pY - 20 + armSwing, 8, 22); ctx.fillRect(pX + 14, pY - 20 - armSwing, 8, 22);"
    "  ctx.fillStyle = '#fef08a'; ctx.beginPath(); ctx.arc(pX, pY - 38, 14, 0, Math.PI*2); ctx.fill();"
    "  let targetMY = (frameCount > 120) ? 520 : 460;"
    "  currentMY += (targetMY - currentMY) * 0.05;"
    "  let mX = pX, mY = currentMY + Math.sin(timer * 0.6) * 6;"
    "  ctx.fillStyle = '#22c55e';"
    "  ctx.beginPath(); ctx.moveTo(mX, mY - 60); ctx.bezierCurveTo(mX + 45, mY - 40, mX + 50, mY + 10, mX + 30, mY + 40);"
    "  ctx.bezierCurveTo(mX + 15, mY + 55, mX - 15, mY + 55, mX - 30, mY + 40);"
    "  ctx.bezierCurveTo(mX - 50, mY + 10, mX - 45, mY - 40, mX, mY - 60); ctx.fill();"
    "  ctx.strokeStyle = '#22c55e'; ctx.lineWidth = 4;"
    "  ctx.beginPath(); ctx.moveTo(mX, mY - 60); ctx.quadraticCurveTo(mX + 10, mY - 80, mX + 5, mY - 90);"
    "  ctx.moveTo(mX + 2, mY - 70); ctx.quadraticCurveTo(mX + 15, mY - 85, mX + 20, mY - 88); ctx.stroke();"
    "  ctx.strokeStyle = '#14532d'; ctx.lineWidth = 5;"
    "  ctx.beginPath(); ctx.moveTo(mX - 32, mY - 30); ctx.lineTo(mX - 5, mY - 20);"
    "  ctx.moveTo(mX + 32, mY - 30); ctx.lineTo(mX + 5, mY - 20); ctx.stroke();"
    "  ctx.fillStyle = '#fef08a';"
    "  ctx.beginPath(); ctx.ellipse(mX - 18, mY - 20, 10, 6, -0.2, 0, Math.PI * 2);"
    "  ctx.ellipse(mX + 18, mY - 20, 10, 6, 0.2, 0, Math.PI * 2); ctx.fill();"
    "  ctx.fillStyle = '#1e293b';"
    "  ctx.beginPath(); ctx.arc(mX - 16, mY - 20, 3, 0, Math.PI * 2); ctx.arc(mX + 20, mY - 20, 3, 0, Math.PI * 2); ctx.fill();"
    "  ctx.fillStyle = '#14532d'; ctx.beginPath(); ctx.arc(mX, mY - 8, 4, 0, Math.PI * 2); ctx.fill();"
    "  ctx.strokeStyle = '#14532d'; ctx.lineWidth = 3;"
    "  ctx.beginPath(); ctx.moveTo(mX - 18, mY + 10); ctx.quadraticCurveTo(mX, mY + 22, mX + 20, mY + 8); ctx.stroke();"
    "  if (!playing && score > 0) {"
    "    ctx.fillStyle = 'rgba(3, 7, 18, 0.95)'; ctx.fillRect(0, 0, cvs.width, cvs.height);"
    "    ctx.fillStyle = '#f43f5e'; ctx.font = 'bold 36px monospace'; ctx.textAlign = 'center';"
    "    ctx.fillText('BẠN ĐÃ BỊ QUÁI VẬT TÚM TÓC!', cvs.width / 2, 180);"
    "    ctx.fillStyle = '#fde047'; ctx.font = '22px monospace'; ctx.fillText('⭐ Điểm: ' + score + '  |  🪙 Vàng: ' + coins, cvs.width / 2, 240);"
    "    ctx.fillStyle = '#94a3b8'; ctx.font = '16px monospace'; ctx.fillText('Nhấn nút bên dưới để chơi lại', cvs.width / 2, 300);"
    "    document.getElementById('menu').style.display = 'flex';"
    "    document.getElementById('menu').querySelector('h1').innerText = 'THUA MẤT RỒI!';"
    "    document.querySelector('.play-btn').innerText = 'CHƠI LẠI NGAY';"
    "  }"
    "  document.getElementById('score').innerText = score;"
    "  document.getElementById('coins').innerText = coins;"
    "}"
    "function mainLoop() {"
    "  try { updateGame(); renderGame(); } catch(err) { console.error(err); }"
    "  requestAnimationFrame(mainLoop);"
    "}"
    "mainLoop();"
    "</script>"
    "</body>"
    "</html>"
)

components.html(game_code, height=580, scrolling=False)
