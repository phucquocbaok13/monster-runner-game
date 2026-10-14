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

# Đọc mã nguồn game từ file game.html độc lập
try:
    with open("game.html", "r", encoding="utf-8") as f:
        game_html = f.read()
    components.html(game_html, height=580, scrolling=False)
except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file `game.html`! Vui lòng tải file `game.html` lên cùng thư mục với `app.py` trên GitHub.")
