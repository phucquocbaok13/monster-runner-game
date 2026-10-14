import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Chạy Trốn Quái Vật - Rừng Đêm 3D",
    page_icon="🌙",
    layout="centered"
)

st.markdown("""
    <style>
    .main {
        background-color: #080c10;
        color: #ffffff;
    }
    .stApp {
        max-width: 900px;
        margin: 0 auto;
    }
    h1 {
        text-align: center;
        color: #00e5ff;
        text-shadow: 0 0 12px rgba(0, 229, 255, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌙 CHẠY TRỐN QUÁI VẬT - RỪNG ĐÊM 3D 🌲</h1>", unsafe_allow_html=True)

# Phần hướng dẫn điều khiển với thiết kế huyền bí
with st.container():
    st.markdown("""
    <style>
    .neon-instructions {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 2px solid #00b4d8;
        box-shadow: 0 0 15px rgba(0, 180, 216, 0.5);
    }
    .neon-instructions h3 {
        color: #90e0ef;
        text-shadow: 0 0 8px rgba(144, 224, 239, 0.8);
        margin-top: 0;
    }
    .neon-instructions li {
        color: #ffffff;
        font-size: 16px;
        margin-bottom: 8px;
    }
    .neon-instructions b {
        color: #ffeb3b;
    }
    .glow-tip {
        color: #00f5d4 !important;
        font-size: 16px;
        font-weight: bold;
        text-shadow: 0 0 10px #00f5d4, 0 0 20px #00b4d8;
        background: rgba(0, 245, 212, 0.1);
        padding: 8px 12px;
        border-radius: 6px;
        border-left: 4px solid #00f5d4;
        margin-top: 10px;
    }
    </style>
    
    <div class="neon-instructions">
        <h3>🎮 HƯỚNG DẪN ĐIỀU KHIỂN:</h3>
        <ul>
            <li><b>Phím W:</b> Nhảy qua cây đổ ngang và tảng đá thấp.</li>
            <li><b>Phím A:</b> Né sang làn TRÁI.</li>
            <li><b>Phím D:</b> Né sang làn PHẢI.</li>
        </ul>
        <div class="glow-tip">🌕 Mẹo: Né tránh cây đổ ngang, gốc cây mọc giữa đường và tảng đá lớn dưới ánh trăng mờ u uất của rừng đêm!</div>
    </div>
    """, unsafe_allow_html=True)

# Mã nguồn trò chơi 3D Rừng Đêm (Dark Night Forest)
game_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Night Forest 3D Runner</title>
    <style>
        body {
            margin: 0;
            background: #020406;
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
            box-shadow: 0 0 30px rgba(0, 180, 216, 0.35);
            border-radius: 10px;
            overflow: hidden;
            background: #000;
        }
        canvas {
            display: block;
            background: #03070d;
        }
        #ui {
            position: absolute;
            top: 10px;
            left: 15px;
            right: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 2px 2px #000;
            pointer-events: none;
            z-index: 5;
        }
        .score-badge {
            background: rgba(3, 11, 20, 0.7);
            padding: 6px 14px;
            border-radius: 8px;
            border: 1px solid rgba(0, 180, 216, 0.5
