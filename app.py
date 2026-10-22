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
.game-container {
    position: relative;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    aspect-ratio: 8 / 5;
    background: #030712;
    border-radius: 12px;
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.4);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: monospace;
    color: white;
}
.menu-box {
    text-align: center;
    padding: 20px;
    background: rgba(3, 7, 18, 0.95);
    border-radius: 10px;
    border: 1px solid #38bdf8;
    width: 80%;
    max-width: 450px;
}
.stButton>button {
    background-color: #0284c7;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    box-shadow: 0 0 10px #38bdf8;
    width: 100%;
    margin-top: 8px;
}
.stButton>button:hover {
    background-color: #38bdf8;
    color: #0f172a;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>CHẠY TRỐN QUÁI VẬT - RỪNG ĐÊM</h1>", unsafe_allow_html=True)

# Khởi tạo trạng thái game trong Session State của Streamlit
if "game_state" not in st.session_state:
    st.session_state.game_state = "home"
if "coins" not in st.session_state:
    st.session_state.coins = 0
if "diamonds" not in st.session_state:
    st.session_state.diamonds = 100
if "equipped_skin" not in st.session_state:
    st.session_state.equipped_skin = "Thám Hiểm Tiêu Chuẩn"

# Giao diện điều hướng Menu chính trực tiếp trên Streamlit
if st.session_state.game_state == "home":
    st.markdown(f"""
    <div class="game-container">
        <div class="menu-box">
            <h2 style="color: #38bdf8; margin-top:0;">SẴN SÀNG SINH TỒN</h2>
            <p style="color: #94a3b8; font-size: 13px;">Khám phá Rừng Đêm, né tránh quái vật và thu thập kim cương!</p>
            <div style="font-size: 14px; color: #fde047; margin-bottom: 15px;">
                🪙 Vàng: <b>{st.session_state.coins}</b> | 💎 Kim cương: <b>{st.session_state.diamonds}</b>
            </div>
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
    st.info("### HƯỚNG DẪN CÁCH CHƠI\n- **Điện thoại / Máy tính:** Sử dụng các nút điều khiển hoặc phím Mũi tên để di chuyển.\n- **Mục tiêu:** Né tránh chướng ngại vật, thu thập vật phẩm và sống sót đến mốc 10.000 điểm!")
    if st.button("⬅️ QUAY LẠI TRANG CHỦ"):
        st.session_state.game_state = "home"
        st.rerun()

elif st.session_state.game_state == "shop":
    st.success(f"### CỬA HÀNG TRANG PHỤC\nKim cương hiện có: **{st.session_state.diamonds} 💎**\n\nĐang mặc: **{st.session_state.equipped_skin}**")
    if st.button("⬅️ QUAY LẠI TRANG CHỦ"):
        st.session_state.game_state = "home"
        st.rerun()

elif st.session_state.game_state == "quests":
    st.warning("### HỆ THỐNG NHIỆM VỤ\n1. Chạy sinh tồn đạt 500 điểm (Thưởng: 20 💎)\n2. Thu thập 10 vàng (Thưởng: 20 💎)")
    if st.button("⬅️ QUAY LẠI TRANG CHỦ"):
        st.session_state.game_state = "home"
        st.rerun()

elif st.session_state.game_state == "playing":
    game_canvas_code = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
    <meta charset="UTF-8">
    <style>
    body {{ margin: 0; background: #030712; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; font-family: monospace; color: white; }}
    #canvas-wrap {{ position: relative; width: 100%; max-width: 800px; aspect-ratio: 8/5; box-shadow: 0 0 20px #38bdf8; border-radius: 8px; overflow: hidden; }}
    canvas {{ display: block; width: 100%; height: 100%; background: #030712; }}
    #hud {{ position: absolute; top: 10px; left: 10px; right: 10px; display: flex; justify-content: space-between; font-size: 14px; font-weight: bold; pointer-events: none; }}
    .badge {{ background: rgba(15, 23, 42, 0.85); padding: 5px 10px; border-radius: 6px; border: 1px solid #38bdf8; }}
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
    let score = 0, playing = true, currentLane = 1, jumpY = 0, isJumping = false, jumpVY = 0;
    const lanes = [280, 400, 520];
    let obstacles = [], roadOffset = 0;

    window.addEventListener('keydown', (e) => {{
      if (e.code === 'ArrowLeft' && currentLane > 0) currentLane--;
      if (e.code === 'ArrowRight' && currentLane < 2) currentLane++;
      if (e.code === 'ArrowUp' && !isJumping) {{ isJumping = true; jumpVY = -11; }}
      e.preventDefault();
    }});

    function update() {{
      score++;
      roadOffset += 4;
      if (isJumping) {{
        jumpY += jumpVY;
        jumpVY += 0.55;
        if (jumpY >= 0) {{ jumpY = 0; isJumping = false; }}
      }}
    }}

    function render() {{
      ctx.clearRect(0, 0, 800, 500);
      ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, 800, 500);
      ctx.fillStyle = '#1e293b'; ctx.fillRect(200, 0, 400, 500);
      ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 4;
      ctx.beginPath(); ctx.moveTo(200, 0); ctx.lineTo(200, 500); ctx.moveTo(600, 0); ctx.lineTo(600, 500); ctx.stroke();
      
      let px = lanes[currentLane], py = 385 + jumpY;
      ctx.fillStyle = '#fbcfe8'; ctx.beginPath(); ctx.arc(px, py - 32, 11, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#38bdf8'; ctx.fillRect(px - 14, py - 24, 28, 38);

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
