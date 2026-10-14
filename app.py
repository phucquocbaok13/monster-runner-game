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
        <div class="tip">💡 Mẹo: Dùng phím mũi tên điều khiển cực kỳ mượt mà, không sợ xung đột phím!</div>
    </div>
    """, unsafe_allow_html=True)

# Mã nguồn HTML/JS tinh gọn, chỉ nhận phím Mũi tên
game_code = (
    "<!DOCTYPE html>"
    "<html lang='vi'>"
    "<head>"
    "<meta charset='UTF-8'>"
    "<title>Night Forest 3D Runner</title>"
    "<style>"
    "body { margin: 0; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: monospace; color: white; overflow: hidden; }"
    "#game-wrap { position: relative; box-shadow: 0 0 25px rgba(0, 255, 255, 0.4); border-radius: 8px; overflow: hidden; }"
    "canvas { display: block; background: #030712; }"
    "#hud { position: absolute; top: 12px; left: 15px; right: 15px; display: flex; justify-content: space-between; font-size: 18px; font-weight: bold; text-shadow: 2px 2px #000; pointer-events: none; }"
    ".badge { background: rgba(15, 23, 42, 0.85); padding: 6px 14px; border-radius: 6px; border: 1px solid #38bdf8; }"
    "#menu { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 7, 18, 0.94); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 10; }"
    ".play-btn { background: #0284c7; color: white; border: none; padding: 14px 32px; font-size: 20px; font-weight: bold; border-radius: 8px; cursor: pointer; margin-top: 20px; box-shadow: 0 0 15px #38bdf8; transition: 0.2s; }"
    ".play-btn:hover { background: #38bdf8; color: #0f172a; transform: scale(1.05); }"
    "</style>"
    "</head>"
    "<body>"
    "<div id='game-wrap'>"
    "<div id='hud'>"
    "<div class='badge'>⭐ ĐIỂM: <span id='score'>0</span></div>"
    "<div class='badge' style='color: #fde047;'>🪙 VÀNG: <span id='coins'>0</span></div>"
    "<div class='badge' style='color: #f43f5e;'>⚡ TỐC ĐỘ BỨT PHÁ</div>"
    "</div>"
    "<div id='menu'>"
    "<h1 style='color: #38bdf8; margin-bottom: 10px; text-shadow: 0 0 15px #0284c7;'>RỪNG ĐÊM 3D: BỨT TỐC</h1>"
    "<p style='max-width: 450px; color: #94a3b8; font-size: 15px; line-height: 1.5;'>"
    "Sử dụng các phím mũi tên để điều khiển nhân vật!<br>"
    "<b>Mũi tên Lên</b> để nhảy, <b>Trái / Phải</b> để né tránh chướng ngại vật."
    "</p>"
    "<button class='play-btn' onclick='startTheGame()'>BẮT ĐẦU CHƠI</button>"
    "</div>"
    "<canvas id='cvs' width='800' height='500'></canvas>"
    "</div>"
    "<script>"
    "const cvs = document.getElementById('cvs');"
    "const ctx = cvs.getContext('2d');"
    "let playing = false, score = 0, coins = 0, speed = 6, timer = 0;"
    "const lanes = [260, 400, 540];"
    "let currentLane = 1, jumpY = 0, jumpVY = 0, isJumping = false;"
    "let obstacles = [], coinList = [], floatTexts = [], roadOffset = 0;"
    "window.addEventListener('keydown', (e) => {"
    "  if (!playing) return;"
    "  if (e.code === 'ArrowLeft') { if (currentLane > 0) currentLane--; e.preventDefault(); }"
    "  else if (e.code === 'ArrowRight') { if (currentLane < 2) currentLane++; e.preventDefault(); }"
    "  else if (e.code === 'ArrowUp') { if (!isJumping) { isJumping = true; jumpVY = -13; } e.preventDefault(); }"
    "});"
    "function startTheGame() {"
    "  playing = true; score = 0; coins = 0; speed = 6.5; currentLane = 1; jumpY = 0; isJumping = false; obstacles = []; coinList = []; floatTexts = [];"
    "  document.getElementById('menu').style.display = 'none';"
    "}"
    "function spawnObjects() {"
    "  if (!playing) return;"
    "  let lane = Math.floor(Math.random() * 3);"
    "  if (Math.random() < 0.6) {"
    "    let types = ['rock', 'log', 'tree'];"
    "    obstacles.push({ lane: lane, z: 0.05, type: types[Math.floor(Math.random() * types.length)] });"
    "  } else { coinList.push({ lane: lane, z: 0.05 }); }"
    "}"
    "setInterval(spawnObjects, 1200);"
    "function updateGame() {"
    "  if (!playing) return;"
    "  score++; timer += 0.25; speed = 6.5 + Math.floor(score / 300) * 0.35; roadOffset += speed * 4.5;"
    "  if (isJumping) { jumpY += jumpVY; jumpVY += 0.68; if (jumpY >= 0) { jumpY = 0; isJumping = false; } }"
    "  for (let i = floatTexts.length - 1; i >= 0; i--) {"
    "    let ft = floatTexts[i]; ft.y += ft.vy; ft.alpha -= 0.03; if (ft.alpha <= 0) floatTexts.splice(i, 1);"
    "  }"
    "  for (let i = obstacles.length - 1; i >= 0; i--) {"
    "    let obs = obstacles[i]; obs.z += speed * 0.0028;"
    "    if (obs.z >= 0.84 && obs.z <= 0.95 && obs.lane === currentLane) {"
    "      if (!(obs.type === 'log' && isJumping && jumpY < -38)) { playing = false; }"
    "    }"
    "    if (obs.z > 1.05) obstacles.splice(i, 1);"
    "  }"
    "  for (let i = coinList.length - 1; i >= 0; i--) {"
    "    let c = coinList[i]; c.z += speed * 0.0028;"
    "    if (c.z >= 0.84 && c.z <= 0.95 && c.lane === currentLane && jumpY > -50) {"
    "      coins++;"
    "      let targetX = (c.lane === 0) ? 260 : (c.lane === 2) ? 540 : 400;"
    "      floatTexts.push({ x: targetX, y: 360, text: '+1 🪙', alpha: 1.0, vy: -2.5 });"
    "      coinList.splice(i, 1); continue;"
    "    }"
    "    if (c.z > 1.05) coinList.splice(i, 1);"
    "  }"
    "}"
    "function renderGame() {"
    "  ctx.clearRect(0, 0, cvs.width, cvs.height);"
    "  let skyGrad = ctx.createLinearGradient(0, 0, 0, 160);"
    "  skyGrad.addColorStop(0, '#0f172a'); skyGrad.addColorStop(1, '#1e293b');"
    "  ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, cvs.width, 160);"
    "  ctx.fillStyle = '#f1f5f9'; ctx.beginPath(); ctx.arc(680, 50, 28, 0, Math.PI * 2); ctx.fill();"
    "  ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 160, cvs.width, 340);"
    "  ctx.beginPath(); ctx.moveTo(400, 160); ctx.lineTo(80, 500); ctx.lineTo(720, 500); ctx.closePath();"
    "  ctx.fillStyle = '#1e293b'; ctx.fill();"
    "  ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 4;"
    "  ctx.beginPath(); ctx.moveTo(400, 160); ctx.lineTo(250, 500); ctx.moveTo(400, 160); ctx.lineTo(550, 500); ctx.stroke();"
    "  for (let i = -2; i < 8; i++) {"
    "    let tProg = (i * 0.2 + (roadOffset * 0.0012)) % 1.0;"
    "    let tY = 160 + tProg * 340, lX = 400 - tProg * 400, rX = 400 + tProg * 400, s = 0.2 + tProg * 0.8;"
    "    ctx.fillStyle = '#334155'; ctx.fillRect(lX - 8*s, tY, 16*s, 48*s); ctx.fillRect(rX - 8*s, tY, 16*s, 48*s);"
    "    ctx.fillStyle = '#10b981'; ctx.beginPath(); ctx.arc(lX, tY - 12*s, 26*s, 0, Math.PI*2); ctx.fill();"
    "    ctx.beginPath(); ctx.arc(rX, tY - 12*s, 26*s, 0, Math.PI*2); ctx.fill();"
    "  }"
    "  obstacles.forEach(o => {"
    "    let z = o.z, screenY = 160 + z * 340, sc = 0.25 + z * 0.75;"
    "    let targetX = (o.lane === 0) ? 400 - z * 320 : (o.lane === 2) ? 400 + z * 320 : 400;"
    "    if (o.type === 'rock') {"
    "      ctx.fillStyle = '#475569'; ctx.beginPath(); ctx.arc(targetX, screenY, 42*sc, 0, Math.PI*2); ctx.fill();"
    "      ctx.fillStyle = '#94a3b8'; ctx.beginPath(); ctx.arc(targetX - 8*sc, screenY - 8*sc, 18*sc, 0, Math.PI*2); ctx.fill();"
    "    } else if (o.type === 'log') {"
    "      ctx.fillStyle = '#78350f'; ctx.fillRect(targetX - 60*sc, screenY - 20*sc, 120*sc, 30*sc);"
    "      ctx.fillStyle = '#15803d'; ctx.beginPath(); ctx.arc(targetX - 35*sc, screenY - 12*sc, 20*sc, 0, Math.PI*2); ctx.fill();"
    "    } else if (o.type === 'tree') {"
    "      ctx.fillStyle = '#451a03'; ctx.fillRect(targetX - 16*sc, screenY - 60*sc, 32*sc, 65*sc);"
    "      ctx.fillStyle = '#16a34a'; ctx.beginPath(); ctx.arc(targetX, screenY - 65*sc, 38*sc, 0, Math.PI*2); ctx.fill();"
    "    }"
    "  });"
    "  coinList.forEach(c => {"
    "    let z = c.z, screenY = 160 + z * 340, sc = 0.3 + z * 0.7;"
    "    let targetX = (c.lane === 0) ? 400 - z * 320 : (c.lane === 2) ? 400 + z * 320 : 400;"
    "    let bounce = Math.sin(timer * 4) * 6;"
    "    ctx.fillStyle = '#fde047'; ctx.beginPath(); ctx.arc(targetX, screenY - 25*sc + bounce, 20*sc, 0, Math.PI*2); ctx.fill();"
    "    ctx.strokeStyle = '#ca8a04'; ctx.lineWidth = 3; ctx.stroke();"
    "  });"
    "  floatTexts.forEach(ft => {"
    "    ctx.save(); ctx.globalAlpha = ft.alpha; ctx.fillStyle = '#fde047'; ctx.font = 'bold 22px monospace'; ctx.textAlign = 'center';"
    "    ctx.fillText(ft.text, ft.x, ft.y); ctx.restore();"
    "  });"
    "  let pX = lanes[currentLane], pY = 400 + jumpY;"
    "  let legMove = isJumping ? 0 : Math.sin(timer * 1.2) * 16;"
    "  ctx.fillStyle = 'rgba(255,255,255,0.3)'; ctx.beginPath(); ctx.arc(pX - 15, pY + 30, 10, 0, Math.PI*2); ctx.fill();"
    "  ctx.fillStyle = 'rgba(0,0,0,0.6)'; ctx.beginPath(); ctx.ellipse(pX, pY + 35, 28, 11, 0, 0, Math.PI*2); ctx.fill();"
    "  ctx.fillStyle = '#e2e8f0'; ctx.fillRect(pX - 24, pY - 65, 48, 65);"
    "  ctx.fillStyle = '#cbd5e1'; ctx.beginPath(); ctx.arc(pX, pY - 58, 22, Math.PI, Math.PI*2); ctx.fill();"
    "  ctx.fillStyle = '#fef08a'; ctx.beginPath(); ctx.arc(pX, pY - 80, 18, 0, Math.PI*2); ctx.fill();"
    "  ctx.fillStyle = '#0f172a'; ctx.fillRect(pX - 14, pY, 12, 32 + legMove); ctx.fillRect(pX + 2, pY, 12, 32 - legMove);"
    "  let mBreath = Math.sin(timer * 0.6) * 7, mX = pX, mY = 475 + mBreath;"
    "  ctx.fillStyle = '#15803d'; ctx.beginPath(); ctx.arc(mX, mY, 80, 0, Math.PI*2); ctx.fill();"
    "  ctx.fillStyle = '#22c55e'; ctx.beginPath(); ctx.arc(mX, mY - 28, 56, 0, Math.PI*2); ctx.fill();"
    "  ctx.fillStyle = '#fde047'; ctx.beginPath(); ctx.arc(mX - 18, mY - 36, 10, 0, Math.PI*2); ctx.arc(mX + 18, mY - 36, 10, 0, Math.PI*2); ctx.fill();"
    "  ctx.fillStyle = '#dc2626'; ctx.beginPath(); ctx.arc(mX - 18, mY - 36, 4.5, 0, Math.PI*2); ctx.arc(mX + 18, mY - 36, 4.5, 0, Math.PI*2); ctx.fill();"
    "  if (!playing && score > 0) {"
    "    ctx.fillStyle = 'rgba(3, 7, 18, 0.94)'; ctx.fillRect(0, 0, cvs.width, cvs.height);"
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
