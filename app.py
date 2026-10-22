# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(
    page_title="Chạy Trốn Quái Vật - Rừng Đêm",
    page_icon="🌲",
    layout="centered"
)

st.markdown("""
<style>
.main { background-color: #050811; color: #ffffff; }
.stApp { max-width: 900px; margin: 0 auto; }
h1 { text-align: center; color: #00ffff; text-shadow: 0 0 15px rgba(0, 255, 255, 0.7); font-size: 26px; }
.menu-box {
    text-align: center;
    padding: 25px;
    background: rgba(3, 7, 18, 0.95);
    border-radius: 12px;
    border: 1px solid #38bdf8;
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
    margin-bottom: 20px;
}
.stButton>button {
    background-color: #0284c7;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 12px 20px;
    border: none;
    box-shadow: 0 0 10px #38bdf8;
    width: 100%;
    margin-top: 10px;
}
.stButton>button:hover {
    background-color: #38bdf8;
    color: #0f172a;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>CHẠY TRỐN QUÁI VẬT - RỪNG ĐÊM</h1>", unsafe_allow_html=True)

# Khởi tạo trạng thái game
if "game_state" not in st.session_state:
    st.session_state.game_state = "home"
if "coins" not in st.session_state:
    st.session_state.coins = 0
if "diamonds" not in st.session_state:
    st.session_state.diamonds = 100
if "equipped_skin" not in st.session_state:
    st.session_state.equipped_skin = "Thám Hiểm Tiêu Chuẩn"

# Điều hướng Menu chính
if st.session_state.game_state == "home":
    st.markdown(f"""
    <div class="menu-box">
        <h2 style="color: #38bdf8; margin-top:0;">SẴN SÀNG SINH TỒN</h2>
        <p style="color: #94a3b8; font-size: 14px;">Khám phá Rừng Đêm, né tránh quái vật và thu thập kim cương!</p>
        <div style="font-size: 16px; color: #fde047; margin-top: 15px;">
            🪙 Vàng: <b>{st.session_state.coins}</b> | 💎 Kim cương: <b>{st.session_state.diamonds}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 BẮT ĐẦU CHƠI NGAY"):
            st.session_state.game_state = "playing"
            st.rerun()
        if st.button("👕 CỬA HÀNG TRANG PHỤC"):
            st.session_state.game_state = "shop"
            st.rerun()
    with col2:
        if st.button("📖 HƯỚNG DẪN CÁCH CHƠI"):
            st.session_state.game_state = "tutorial"
            st.rerun()
        if st.button("🎯 NHIỆM VỤ NHẬN THƯỞNG"):
            st.session_state.game_state = "quests"
            st.rerun()

elif st.session_state.game_state == "tutorial":
    st.info("""### HƯỚNG DẪN CÁCH CHƠI
- **Di chuyển:** Sử dụng các phím mũi tên `Trái`, `Phải` để đổi làn đường, phím `Mũi tên lên` để nhảy tránh chướng ngại vật.
- **Mục tiêu:** Né tránh đá, khúc gỗ, thu thập vàng và kim cương, sống sót đến vạch đích 10.000 điểm!""")
    if st.button("⬅️ QUAY LẠI TRANG CHỦ"):
        st.session_state.game_state = "home"
        st.rerun()

elif st.session_state.game_state == "shop":
    st.success(f"""### CỬA HÀNG TRANG PHỤC
Kim cương hiện có: **{st.session_state.diamonds} 💎**  
Đang mặc: **{st.session_state.equipped_skin}**

* **Thám Hiểm Tiêu Chuẩn** (Đã sở hữu)
* **Hiệp Sĩ Áo Giáp Vàng** (50 💎)
* **Ninja Bóng Đêm** (100 💎)""")
    if st.button("⬅️ QUAY LẠI TRANG CHỦ"):
        st.session_state.game_state = "home"
        st.rerun()

elif st.session_state.game_state == "quests":
    st.warning("""### HỆ THỐNG NHIỆM VỤ
1. **Chạy sinh tồn đạt 500 điểm** - Tiến độ: 0/500 (Thưởng: 20 💎)
2. **Thu thập tổng cộng 10 vàng** - Tiến độ: 0/10 (Thưởng: 20 💎)""")
    if st.button("⬅️ QUAY LẠI TRANG CHỦ"):
        st.session_state.game_state = "home"
        st.rerun()

elif st.session_state.game_state == "playing":
    # Canvas trò chơi sinh tồn mượt mà chuẩn xác
    game_canvas_code = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
    <meta charset="UTF-8">
    <style>
    body {{ margin: 0; background: #030712; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; font-family: monospace; color: white; }}
    #canvas-wrap {{ position: relative; width: 100%; max-width: 800px; aspect-ratio: 8/5; box-shadow: 0 0 25px #38bdf8; border-radius: 8px; overflow: hidden; }}
    canvas {{ display: block; width: 100%; height: 100%; background: #030712; }}
    #hud {{ position: absolute; top: 15px; left: 15px; right: 15px; display: flex; justify-content: space-between; font-size: 15px; font-weight: bold; z-index: 20; pointer-events: none; }}
    .badge {{ background: rgba(15, 23, 42, 0.9); padding: 6px 12px; border-radius: 6px; border: 1px solid #38bdf8; box-shadow: 0 0 8px rgba(56,189,248,0.5); }}
    </style>
    </head>
    <body>
    <div id="canvas-wrap">
      <div id="hud">
        <div class="badge">ĐIỂM: <span id="score">0</span></div>
        <div class="badge" style="color: #fde047;">VÀNG: <span id="coins">{st.session_state.coins}</span></div>
        <div class="badge" style="color: #38bdf8;">KIM CƯƠNG: <span id="diamonds">{st.session_state.diamonds}</span></div>
      </div>
      <canvas id="cvs" width="800" height="500"></canvas>
    </div>
    <script>
    const cvs = document.getElementById('cvs');
    const ctx = cvs.getContext('2d');
    let score = 0, playing = true, currentLane = 1, jumpY = 0, isJumping = false, jumpVY = 0, frameCount = 0;
    const lanes = [280, 400, 520];
    let roadOffset = 0, obstacles = [], coins = [], diamonds = [];

    window.addEventListener('keydown', (e) => {{
      if (e.code === 'ArrowLeft' && currentLane > 0) currentLane--;
      if (e.code === 'ArrowRight' && currentLane < 2) currentLane++;
      if (e.code === 'ArrowUp' && !isJumping) {{ isJumping = true; jumpVY = -11; }}
      e.preventDefault();
    }});

    function spawnObjects() {{
      let lane = Math.floor(Math.random() * 3);
      let type = Math.random();
      if (type < 0.5) {{
        obstacles.push({{ lane: lane, y: -50, kind: Math.random() < 0.5 ? 'rock' : 'log' }});
      }} else if (type < 0.8) {{
        coins.push({{ lane: lane, y: -50 }});
      }} else {{
        diamonds.push({{ lane: lane, y: -50 }});
      }}
    }}

    function update() {{
      score++;
      frameCount++;
      roadOffset += 4.5;

      if (frameCount % 55 === 0) {{
        spawnObjects();
      }}

      if (isJumping) {{
        jumpY += jumpVY;
        jumpVY += 0.55;
        if (jumpY >= 0) {{ jumpY = 0; isJumping = false; }}
      }}

      // Cập nhật vị trí vật thể
      for (let i = obstacles.length - 1; i >= 0; i--) {{
        obstacles[i].y += 4.5;
        if (obstacles[i].y > 550) obstacles.splice(i, 1);
      }}
      for (let i = coins.length - 1; i >= 0; i--) {{
        coins[i].y += 4.5;
        if (coins[i].y > 550) coins.splice(i, 1);
      }}
      for (let i = diamonds.length - 1; i >= 0; i--) {{
        diamonds[i].y += 4.5;
        if (diamonds[i].y > 550) diamonds.splice(i, 1);
      }}
    }}

    function render() {{
      ctx.clearRect(0, 0, 800, 500);
      
      // Nền trời & rừng
      ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, 800, 500);

      // Cây hai bên đường
      for (let i = 0; i < 8; i++) {{
        let treeY = (i * 120 + roadOffset * 1.5) % 600 - 50;
        ctx.fillStyle = '#064e3b';
        ctx.beginPath(); ctx.arc(100, treeY, 35, 0, Math.PI*2); ctx.arc(700, treeY, 35, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#022c22';
        ctx.fillRect(92, treeY + 15, 16, 40); ctx.fillRect(692, treeY + 15, 16, 40);
      }}

      // Đường chạy
      ctx.fillStyle = '#1e293b'; ctx.fillRect(200, 0, 400, 500);
      ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 4;
      ctx.beginPath(); ctx.moveTo(200, 0); ctx.lineTo(200, 500); ctx.moveTo(600, 0); ctx.lineTo(600, 500); ctx.stroke();
      
      // Vạch kẻ đường
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.3)'; ctx.lineWidth = 2; ctx.setLineDash([15, 15]);
      ctx.beginPath(); ctx.moveTo(333, roadOffset % 500 - 500); ctx.lineTo(333, 500);
      ctx.moveTo(466, roadOffset % 500 - 500); ctx.lineTo(466, 500); ctx.stroke(); ctx.setLineDash([]);

      // Chướng ngại vật
      obstacles.forEach(o => {{
        let tX = lanes[o.lane];
        if (o.kind === 'rock') {{
          ctx.fillStyle = '#334155';
          ctx.beginPath(); ctx.arc(tX, o.y, 22, 0, Math.PI*2); ctx.fill();
          ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 2; ctx.stroke();
        }} else {{
          ctx.fillStyle = '#b45309';
          ctx.fillRect(tX - 35, o.y - 12, 70, 24);
          ctx.strokeStyle = '#451a03'; ctx.lineWidth = 2; ctx.stroke();
        }}
      }});

      // Vàng
      coins.forEach(c => {{
        let tX = lanes[c.lane];
        ctx.fillStyle = '#facc15';
        ctx.beginPath(); ctx.arc(tX, c.y, 14, 0, Math.PI*2); ctx.fill();
        ctx.strokeStyle = '#ca8a04'; ctx.lineWidth = 2; ctx.stroke();
        ctx.fillStyle = '#854d0e'; ctx.font = 'bold 14px sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText('$', tX, c.y);
      }});

      // Kim cương
      diamonds.forEach(d => {{
        let tX = lanes[d.lane];
        ctx.fillStyle = '#38bdf8';
        ctx.beginPath();
        ctx.moveTo(tX, d.y - 15); ctx.lineTo(tX + 12, d.y); ctx.lineTo(tX, d.y + 15); ctx.lineTo(tX - 12, d.y);
        ctx.closePath(); ctx.fill();
        ctx.strokeStyle = '#bae6fd'; ctx.lineWidth = 2; ctx.stroke();
      }});

      // Nhân vật chi tiết (có thân, tay, chân, đầu)
      let px = lanes[currentLane], py = 385 + jumpY;
      ctx.fillStyle = 'rgba(0,0,0,0.5)';
      ctx.beginPath(); ctx.ellipse(px, py + 38, 16, 6, 0, 0, Math.PI*2); ctx.fill();

      // Chân
      let legCycle = Math.cos(frameCount * 0.3) * 8;
      ctx.fillStyle = '#64748b';
      ctx.fillRect(px - 9, py + 12 + legCycle, 6, 20);
      ctx.fillRect(px + 3, py + 12 - legCycle, 6, 20);

      // Thân nhân vật
      ctx.fillStyle = '#38bdf8';
      ctx.fillRect(px - 13, py - 20, 26, 34);

      // Đầu & Mũ
      ctx.fillStyle = '#fbcfe8';
      ctx.beginPath(); ctx.arc(px, py - 28, 10, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#334155';
      ctx.beginPath(); ctx.arc(px, py - 31, 11, Math.PI, Math.PI * 2); ctx.fill();

      // Quái vật rượt đuổi phía sau
      let mX = px, mY = 460 + Math.sin(frameCount * 0.1) * 6;
      ctx.fillStyle = '#22c55e';
      ctx.beginPath();
      ctx.moveTo(mX, mY - 40); ctx.bezierCurveTo(mX + 35, mY - 20, mX + 40, mY + 15, mX + 20, mY + 30);
      ctx.bezierCurveTo(mX + 10, mY + 40, mX - 10, mY + 40, mX - 20, mY + 30);
      ctx.bezierCurveTo(mX - 40, mY + 15, mX - 35, mY - 20, mX, mY - 40); ctx.fill();

      document.getElementById('score').innerText = score;
    }}

    function loop() {{
      if (playing) {{ update(); render(); }}
      requestAnimationFrame(loop);
    }}
    loop();
    </script>
    </body>
    </html>
    """
    st.components.v1.html(game_canvas_code, height=520)
    if st.button("🏠 VỀ LẠI TRANG CHỦ"):
        st.session_state.game_state = "home"
        st.rerun()
