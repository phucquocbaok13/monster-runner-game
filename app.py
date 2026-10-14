import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Chạy Trốn Quái Vật - Phong Cách Subway Surfers",
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

# Phần hướng dẫn điều khiển sáng rực Neon
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
        text-shadow: 0 0 5px rgba(255, 204, 0, 0.6);
    }
    </style>
    
    <div class="neon-instructions">
        <h3>🎮 HƯỚNG DẪN ĐIỀU KHIỂN:</h3>
        <ul>
            <li><b>Phím W:</b> Nhảy qua tảng đá / chướng ngại vật.</li>
            <li><b>Phím A:</b> Né sang làn TRÁI.</li>
            <li><b>Phím D:</b> Né sang làn PHẢI.</li>
        </ul>
        <p style="margin-bottom: 0;"><i>☀️ Mẹo: Thu thập tiền vàng, né tránh chướng ngại vật trong khung cảnh rừng xanh ngập tràn ánh nắng và âm thanh sống động!</i></p>
    </div>
    """, unsafe_allow_html=True)

# Đọc mã game từ file game.html độc lập
try:
    with open("game.html", "r", encoding="utf-8") as f:
        game_html = f.read()
    components.html(game_html, height=580, scrolling=False)
except FileNotFoundError:
    st.error("⚠️ Vui lòng tạo file `game.html` chứa mã nguồn giao diện game trong cùng thư mục!")
