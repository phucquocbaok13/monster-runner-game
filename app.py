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
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌲 CHẠY TRỐN QUÁI VẬT - RỪNG ĐÊM 🌙</h1>", unsafe_allow_html=True)

# Hướng dẫn điều khiển gọn gàng
with st.container():
    st.markdown("""
    <style>
    .box-hd {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
        margin-bottom: 15px;
    }
    .box-hd h3 { color: #38bdf8; margin-top: 0; font-size: 16px; }
    .box-hd li { color: #f8fafc; font-size: 14px; margin-bottom: 4px; }
    .box-hd b { color: #fde047; }
    </style>
    <div class="box-hd">
        <h3>🎮 HƯỚNG DẪN ĐIỀU KHIỂN:</h3>
        <ul>
            <li><b>Điện thoại:</b> Vuốt màn hình (Vuốt trái/phải để đổi làn, vuốt lên để nhảy).</li>
            <li><b>Máy tính:</b> Dùng các phím <b>Mũi tên</b> (Lên để nhảy, Trái/Phải để đổi làn).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Mã nguồn HTML, CSS và JavaScript hoàn chỉnh
game_html = [
    "<!DOCTYPE html>",
    "<html lang='vi'>",
    "<head>",
    "<meta charset='UTF-8'>",
    "<meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'>",
    "<title>Night Forest Mobile</title>",
    "<style>",
    "body { margin: 0; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: monospace; color: white; overflow: hidden; touch-action: none; }",
    "#game-wrap { position: relative; width: 100%; max-width: 800px; box-shadow: 0 0 25px rgba(0, 255, 255, 0.4); border-radius: 8px; overflow: hidden; }",
    "canvas { display: block; width: 100%; height: auto; background: #030712; }",
    "#hud { position: absolute; top: 10px; left: 10px; right: 10px; display: flex; justify-content: space-between; font-size: 14px; font-weight: bold; text-shadow: 2px 2px #000; pointer-events: none; }",
    ".badge { background: rgba(15, 23, 42, 0.85); padding: 5px 10px; border-radius: 6px; border: 1px solid #38bdf8; }",
    "#menu { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 7, 18, 0.95); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 10; padding: 20px; box-sizing: border-box; }",
    ".play-btn { background: #0284c7; color: white; border: none; padding: 12px 28px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; margin-top: 15px; box-shadow: 0 0 15px #38bdf8; }",
    "</style>",
    "</head>",
    "<body>",
    "<div id='game-wrap'>",
    "<div id='hud'>",
    "<div class='badge'>⭐ ĐIỂM:
