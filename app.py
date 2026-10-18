# -*- coding: utf-8 -*-
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
.main { background-color: #050811; color: #ffffff; }
.stApp { max-width: 900px; margin: 0 auto; }
h1 { text-align: center; color: #00ffff; text-shadow: 0 0 15px rgba(0, 255, 255, 0.7); font-size: 24px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>CHẠY TRỐN QUÁI VẬT - RỪNG ĐÊM</h1>", unsafe_allow_html=True)

html_code = r'''
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Night Forest RPG</title>
<style>
body { margin: 0; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: monospace; color: white; overflow: hidden; touch-action: none; }
#game-wrap { position: relative; width: 100%; max-width: 800px; box-shadow: 0 0 25px rgba(0, 255, 255, 0.4); border-radius: 8px; overflow: hidden; }
canvas { display: block; width: 100%; height: auto; background: #030712; }
#hud { position: absolute; top: 10px; left: 10px; right: 10px; display: flex; justify-content: space-between; font-size: 14px; font-weight: bold; text-shadow: 2px 2px #000; pointer-events: none; z-index: 5; }
.badge { background: rgba(15, 23, 42, 0.85); padding: 5px 10px; border-radius: 6px; border: 1px solid #38bdf8; }
.screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 7, 18, 0.96); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 10; padding: 20px; box-sizing: border-box; }
.hidden { display: none !important; }
.btn { background: #0284c7; color: white; border: none; padding: 12px 28px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; margin: 6px; box-shadow: 0 0 15px #38bdf8; transition: 0.2s; width: 260px; max-width: 100%; }
.btn:hover { background: #38bdf8; color: #0f172a; transform: scale(1.03); }
.btn-secondary { background: #475569; box-shadow: 0 0 10px #94a3b8; }
.btn-secondary:hover { background: #94a3b8; color: #0f172a; }
.panel-grid { display: flex; flex-direction: column; gap: 10px; width: 100%; max-width: 460px; max-height: 280px; overflow-y: auto; margin: 10px 0; padding: 5px; }
.item-card { background: rgba(30, 41, 59, 0.85); border: 1px solid #38bdf8; border-radius: 8px; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.preview-cvs { width: 50px; height: 60px; border-radius: 6px; border: 1px solid #38bdf8; background: #0f172a; flex-shrink: 0; }
</style>
</head>
<body>
<div id="game-wrap">
  <div id="hud" class="hidden">
    <div class="badge">ĐIỂM: <span id="score">0</span></div>
    <div class="badge" style="color: #fde047;">V
