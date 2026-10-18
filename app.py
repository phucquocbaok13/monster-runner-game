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

html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Night Forest RPG</title>
<style>
body { margin: 0; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: monospace; color: white; overflow: hidden; }
#game-wrap { position: relative; width: 100%; max-width: 800px; aspect-ratio: 8 / 5; box-shadow: 0 0 25px rgba(0, 255, 255, 0.4); border-radius: 8px; overflow: hidden; background: #030712; }
canvas { display: block; width: 100%; height: 100%; background: #030712; }
#hud { position: absolute; top: 10px; left: 10px; right: 10px; display: flex; justify-content: space-between; font-size: 14px; font-weight: bold; z-index: 5; pointer-events: none; }
.badge { background: rgba(15, 23, 42, 0.85); padding: 5px 10px; border-radius: 6px; border: 1px solid #38bdf8; }
.screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 7, 18, 0.98); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 10; padding: 20px; box-sizing: border-box; }
.hidden { display: none !important; }
.btn { background: #0284c7; color: white; border: none; padding: 12px 28px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; margin: 6px; width: 260px; max-width: 100%; box-shadow: 0 0 10px #38bdf8; }
.btn:hover { background: #38bdf8; color: #0f172a; }
.btn-secondary { background: #475569; }
.btn-secondary:hover { background: #94a3b8; color: #0f172a; }
.panel-grid { display: flex; flex-direction: column; gap: 10px; width: 100%; max-width: 460px; max-height: 220px; overflow-y: auto; margin: 10px 0; padding: 5px; }
.item-card { background: rgba(30, 41, 59, 0.85); border: 1px solid #38bdf8; border-radius: 8px; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.preview-cvs { width: 40px; height: 50px; border-radius: 6px; border: 1px solid #38bdf8; background: #0f172a; flex-shrink: 0; }
</style>
</head>
<body>
<div id="game-wrap">
  <div id="hud" class="hidden">
    <div class="badge">ĐIỂM: <span id="score">0</span></div>
    <div class="badge" style="color: #fde047;">VÀNG: <span id="coins">0</span></div>
    <div class="badge" style="color: #38bdf8;">KIM CƯƠNG: <span id="diamonds">0</span></div>
  </div>

  <!-- MÀN HÌNH CHÍNH -->
  <div id="screen-home" class="screen">
    <h1 style="color: #38bdf8; font-size: 24px; margin-bottom: 5px; text-shadow: 0 0 10px #0284c7;">CHẠY TRỐN QUÁI VẬT</h1>
    <p style="color: #94a3b8; font-size: 13px; margin-bottom: 12px;">Khám phá Rừng Đêm, thu thập tài nguyên và sinh tồn!</p>
    <div style="margin-bottom: 12px; font-size: 14px; color: #fde047;">🪙 Vàng: <span id="home-coins">0</span> | 💎 Kim cương: <span id="home-diamonds">0</span></div>
    <button class="btn" onclick="safelyStartGame()">BẮT ĐẦU CHƠI</button>
    <button class="btn btn-secondary" onclick="showScreen('screen-tutorial')">HƯỚNG DẪN CÁCH CHƠI</button>
    <button class="btn btn-secondary" onclick="showScreen('screen-shop')">CỬA HÀNG TRANG PHỤC</button>
    <button class="btn btn-secondary" onclick="showScreen('screen-quests')">NHIỆM VỤ NHẬN THƯỞNG</button>
  </div>

  <!-- HƯỚNG DẪN -->
  <div id="screen-tutorial" class="screen hidden">
    <h2 style="color: #38bdf8; margin-top:0; font-size: 20px;">HƯỚNG DẪN CÁCH CHƠI</h2>
    <div style="text-align: left; max-width: 420px; font-size: 12px; line-height: 1.4; color: #f8fafc; background: rgba(15, 23, 42, 0.9); padding: 12px; border-radius: 8px; border: 1px solid #38bdf8; margin-bottom: 10px;">
      <p style="margin:0 0 6px 0;"><b>📱 Điện thoại:</b> Vuốt màn hình (Trái/Phải: Đổi làn, Lên: Nhảy)</p>
      <p style="margin:0 0 6px 0;"><b>💻 Máy tính:</b> Phím Mũi tên (Trái/Phải: Đổi làn, Lên: Nhảy)</p>
      <p style="margin:0;"><b>🎯 Mục tiêu:</b> Đạt 3000 điểm tăng tốc, chạm mốc 10.000 điểm để tìm cổng thoát thân!</p>
    </div>
    <button class="btn btn-secondary" onclick="showScreen('screen-home')">QUAY LẠI</button>
  </div>

  <!-- CỬA HÀNG -->
  <div id="screen-shop" class="screen hidden">
    <h2 style="color: #38bdf8; margin-top:0; font-size: 20px;">CỬA HÀNG TRANG PHỤC</h2>
    <div style="font-size: 13px; color: #fde047; margin-bottom: 3px;">💎 Kim cương hiện có: <span id="shop-diamonds">0</span></div>
    <div class="panel-grid" id="shop-list"></div>
    <button class="btn btn-secondary" onclick="showScreen('screen-home')">QUAY LẠI</button>
  </div>

  <!-- NHIỆM VỤ -->
  <div id="screen-quests" class="screen hidden">
    <h2 style="color: #38bdf8; margin-top:0; font-size: 20px;">HỆ THỐNG NHIỆM VỤ</h2>
    <div class="panel-grid" id="quest-list"></div>
    <button class="btn btn-secondary" onclick="showScreen('screen-home')">QUAY LẠI</button>
  </div>

  <!-- GAME OVER -->
  <div id="screen-gameover" class="screen hidden">
    <h1 style="color: #f43f5e; font-size: 24px; margin-bottom: 8px;">BẠN ĐÃ BỊ TÚM TÓC!</h1>
    <p style="color: #fde047; font-size: 15px; margin: 3px;">⭐ Điểm đạt được: <span id="go-score">0</span></p>
    <p style="color: #fde047; font-size: 13px; margin: 3px;">🪙 Vàng nhặt: +<span id="go-coins">0</span> | 💎 Kim cương: +<span id="go-diamonds">0</span></p>
    <button class="btn" onclick="safelyStartGame()" style="margin-top: 10px;">CHƠI LẠI NGAY</button>
    <button class="btn btn-secondary" onclick="showScreen('screen-home')">VỀ TRANG CHỦ</button>
  </div>

  <!-- VICTORY -->
  <div id="screen-victory" class="screen hidden">
    <h1 style="color: #34d399; font-size: 22px; margin-bottom: 8px;">CHÚC MỪNG BẠN SỐNG SÓT!</h1>
    <p style="color: #fde047; font-size: 15px; margin: 3px;">⭐ Điểm hoàn thành: <span id="vic-score">10000</span></p>
    <p style="color: #38bdf8; font-size: 14px; margin: 3px; font-weight: bold;">🎁 Thưởng: +100 💎 Kim cương!</p>
    <button class="btn" onclick="safelyStartGame()" style="margin-top: 10px;">CHƠI LẠI</button>
    <button class="btn btn-secondary" onclick="showScreen('screen-home')">VỀ TRANG CHỦ</button>
  </div>

  <canvas id="cvs" width="800" height="500"></canvas>
</div>

<script>
let playerData = {
  coins: 0,
  diamonds: 100,
  unlockedSkins: ['default'],
  equippedSkin: 'default',
  questTier: 1,
  quests: [
    { id: 1, title: 'Chạy sinh tồn đạt 500 điểm', target: 500, progress: 0, reward: 20, claimed: false },
    { id: 2, title: 'Thu thập tổng cộng 10 vàng', target: 10, progress: 0, reward: 20, claimed: false },
    { id: 3, title: 'Thu thập 3 viên kim cương', target: 3, progress: 0, reward: 30, claimed: false }
  ]
};

function saveGame() { updateUI(); }

function checkAndRotateQuests() {
  try {
    if (!playerData.quests || playerData.quests.length === 0) return;
    let allClaimed = playerData.quests.every(q => q.claimed);
    if (allClaimed) {
      playerData.questTier = (Number(playerData.questTier) || 1) + 1;
      let t = playerData.questTier;
      playerData.quests = [
        { id: t * 100 + 1, title: 'Chạy sinh tồn đạt ' + (t * 1500) + ' điểm', target: t * 1500, progress: 0, reward: t * 30, claimed: false },
        { id: t * 100 + 2, title: 'Thu thập tổng cộng ' + (t * 20) + ' vàng', target: t * 20, progress: 0, reward: t * 25, claimed: false },
        { id: t * 100 + 3, title: 'Thu thập ' + (t * 8) + ' viên kim cương', target: t * 8, progress: 0, reward: t * 40, claimed: false }
      ];
      saveGame();
    }
  } catch(e) {}
}

const skins = {
  'default': { name: 'Thám Hiểm Tiêu Chuẩn', cost: 0, color: '#94a3b8', accent: '#64748b', hat: '#334155', glow: '#60a5fa' },
  'gold':    { name: 'Hiệp Sĩ Áo Giáp Vàng', cost: 50, color: '#fde047', accent: '#ca8a04', hat: '#eab308', glow: '#facc15' },
  'ninja':   { name: 'Ninja Bóng Đêm', cost: 100, color: '#38bdf8', accent: '#0284c7', hat: '#0f172a', glow: '#38bdf8' },
  'fire':    { name: 'Chiến Binh Lửa Đỏ', cost: 150, color: '#ef4444', accent: '#b91c1c', hat: '#7f1d1d', glow: '#f87171' },
  'cyber':   { name: 'Robot Tương Lai', cost: 200, color: '#c084fc', accent: '#7e22ce', hat: '#a855f7', glow: '#e879f9' },
  'wizard':  { name: 'Phù Thủy Tối Thượng', cost: 250, color: '#a855f7', accent: '#581c87', hat: '#3b0764', glow: '#c084fc' },
  'neon':    { name: 'Siêu Tốc Độ Neon', cost: 300, color: '#22c55e', accent: '#15803d', hat: '#4ade80', glow: '#48bb78' },
  'ice':     { name: 'Chiến Binh Băng Giá', cost: 350, color: '#e0f2fe', accent: '#0284c7', hat: '#7dd3fc', glow: '#bae6fd' },
  'king':    { name: 'Đế Vương Hoàng Gia', cost: 400, color: '#fbbf24', accent: '#b45309', hat: '#dc2626', glow: '#f6e05e' },
  'cosmic':  { name: 'Hành Tinh Vũ Trụ', cost: 500, color: '#ec4899', accent: '#831843', hat: '#6366f1', glow: '#f472b6' }
};

function updateUI() {
  try {
    let el = document.getElementById('home-coins'); if (el) el.innerText = playerData.coins;
    let el2 = document.getElementById('home-diamonds'); if (el2) el2.innerText = playerData.diamonds;
    let el3 = document.getElementById('shop-diamonds'); if (el3) el3.innerText = playerData.diamonds;
    let el4 = document.getElementById('coins'); if (el4) el4.innerText = playerData.coins;
    let el5 = document.getElementById('diamonds'); if (el5) el5.innerText = playerData.diamonds;
  } catch(e) {}
}
updateUI();

function showScreen(screenId) {
  try {
    document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
    let target = document.getElementById(screenId);
    if (target) target.classList.remove('hidden');
    if (screenId === 'screen-shop') renderShop();
    if (screenId === 'screen-quests') {
      checkAndRotateQuests();
      renderQuests();
    }
  } catch(e) {
    alert("Lỗi hiển thị màn hình: " + e.message);
  }
}

function drawDetailedPlayer(ctx, px, py, skin, isJumpingState, animTimer) {
  try {
    ctx.save();
    let armCycle = Math.sin(animTimer * 0.6) * 8;
    let legCycle = Math.cos(animTimer * 0.6) * 10;
    ctx.fillStyle = 'rgba(0,0,0,0.5)';
    ctx.beginPath(); ctx.ellipse(px, py + 38, 18, 7, 0, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = skin.accent;
    ctx.fillRect(px - 10, py + 12 + legCycle, 7, 24);
    ctx.fillRect(px + 3, py + 12 - legCycle, 7, 24);
    let bodyGrad = ctx.createLinearGradient(px - 15, py - 20, px + 15, py + 20);
    bodyGrad.addColorStop(0, skin.color);
    bodyGrad.addColorStop(1, skin.accent);
    ctx.fillStyle = bodyGrad;
    ctx.beginPath();
    if (ctx.roundRect) { ctx.roundRect(px - 14, py - 24, 28, 38, 6); } else { ctx.rect(px - 14, py - 24, 28, 38); }
    ctx.fill();
    ctx.strokeStyle = skin.glow; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.fillStyle = '#1e293b'; ctx.fillRect(px - 14, py - 2, 28, 5);
    ctx.fillStyle = '#fde047'; ctx.fillRect(px - 3, py - 3, 6, 7);
    ctx.fillStyle = skin.accent;
    ctx.fillRect(px - 22, py - 20 + armCycle, 7, 20);
    ctx.fillRect(px + 15, py - 20 - armCycle, 7, 20);
    ctx.fillStyle = '#fbcfe8';
    ctx.beginPath(); ctx.arc(px, py - 32, 11, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(px - 5, py - 35, 3, 4);
    ctx.fillRect(px + 2, py - 35, 3, 4);
    ctx.fillStyle = skin.hat;
    ctx.beginPath(); ctx.arc(px, py - 35, 12, Math.PI, Math.PI * 2); ctx.fill();
    ctx.fillRect(px - 14, py - 43, 28, 7);
    ctx.shadowColor = skin.glow; ctx.shadowBlur = 10;
    ctx.fillStyle = skin.glow; ctx.fillRect(px - 2, py - 46, 4, 4);
    ctx.shadowBlur = 0;
    ctx.restore();
  } catch(e) {
    ctx.fillStyle = skin.color || '#fff';
    ctx.fillRect(15, 10, 20, 30);
  }
}

function drawSkinPreview(canvasId, skin) {
  let pCvs = document.getElementById(canvasId);
  if (!pCvs) return;
  let pCtx = pCvs.getContext('2d');
  if (!pCtx) return;
  pCtx.clearRect(0, 0, 40, 50);
  drawDetailedPlayer(pCtx, 20, 26, skin, false, 0);
}

function renderShop() {
  let list = document.getElementById('shop-list');
  if (!list) return;
  list.innerHTML = '';
  for (let key in skins) {
    let skin = skins[key];
    let unlocked = playerData.unlockedSkins.includes(key);
    let equipped = playerData.equippedSkin === key;
    let cvsId = 'cvs-skin-' + key;
    let html = "<div class='item-card'>";
    html += "<canvas id='" + cvsId + "' width='40' height='50' class='preview-cvs'></canvas>";
    html += "<div style='text-align: left; flex-grow: 1;'><b>" + skin.name + "</b><br><small style='color:#fde047;'>" + (skin.cost > 0 ? skin.cost + " 💎" : "Miễn phí") + "</small></div>";
    if (equipped) {
      html += "<span style='color: #34d399; font-weight:bold; font-size:12px;'>Đang mặc</span>";
    } else if (unlocked) {
      html += "<button class='btn' style='padding:4px 10px; font-size:12px; width:auto; margin:0;' onclick='equipSkin(\"" + key + "\")'>Chọn</button>";
    } else {
      html += "<button class='btn' style='padding:4px 10px; font-size:12px; width:auto; margin:0;' onclick='buySkin(\"" + key + "\")'>Mua</button>";
    }
    html += "</div>";
    list.innerHTML += html;
  }
  setTimeout(() => {
    for (let key in skins) { drawSkinPreview('cvs-skin-' + key, skins[key]); }
  }, 100);
}

function buySkin(key) {
  let skin = skins[key];
  if (playerData.diamonds >= skin.cost) {
    playerData.diamonds -= skin.cost;
    playerData.unlockedSkins.push(key);
    playerData.equippedSkin = key;
    saveGame();
    renderShop();
    alert('Mua thành công trang phục mới!');
  } else {
    alert('Bạn không đủ kim cương!');
  }
}

function equipSkin(key) {
  playerData.equippedSkin = key;
  saveGame();
  renderShop();
}

function renderQuests() {
  let list = document.getElementById('quest-list');
  if (!list) return;
  list.innerHTML = '';
  playerData.quests.forEach(q => {
    let target = Number(q.target) || 500;
    let progress = Number(q.progress) || 0;
    let reward = Number(q.reward) || 20;
    let completed = progress >= target;
    let html = "<div class='item-card'>";
    html += "<div style='text-align: left;'><b>" + (q.title || 'Nhiệm vụ') + "</b><br><small style='color:#94a3b8;'>Tiến độ: " + progress + " / " + target + "</small></div>";
    if (q.claimed) {
      html += "<span style='color: #94a3b8; font-size: 12px;'>Đã nhận</span>";
    } else if (completed) {
      html += "<button class='btn' style='padding:4px 10px; font-size:12px; width:auto; margin:0; background:#34d399;' onclick='claimQuest(" + q.id + ")'>Nhận " + reward + " 💎</button>";
    } else {
      html += "<span style='color: #fde047; font-size:12px;'>Thưởng " + reward + " 💎</span>";
    }
    html += "</div>";
    list.innerHTML += html;
  });
}

function claimQuest(id) {
  let q = playerData.quests.find(x => x.id === id);
  if (q && !q.claimed && Number(q.progress) >= Number(q.target)) {
    q.claimed = true;
    playerData.diamonds = (Number(playerData.diamonds) || 0) + (Number(q.reward) || 20);
    saveGame();
    checkAndRotateQuests();
    renderQuests();
    alert('Nhận thưởng thành công!');
  }
}

const cvs = document.getElementById('cvs');
const ctx = cvs ? cvs.getContext('2d') : null;
let playing = false, score = 0, runCoins = 0, runDiamonds = 0, speed = 3.5, timer = 0, frameCount = 0, spawnTimer = 0, currentMY = 460;
const lanes = [280, 400, 520];
let currentLane = 1, jumpY = 0, jumpVY = 0, isJumping = false;
let obstacles = [], coinList = [], diamondList = [], gateObj = null, floatTexts = [], roadOffset = 0;

function goLeft() { if (playing && currentLane > 0) currentLane--; }
function goRight() { if (playing && currentLane < 2) currentLane++; }
function goJump() { if (playing && !isJumping) { isJumping = true; jumpVY = -11; } }

window.addEventListener('keydown', (e) => {
  if (!playing) return;
  if (e.code === 'ArrowLeft') { goLeft(); e.preventDefault(); }
  else if (e.code === 'ArrowRight') { goRight(); e.preventDefault(); }
  else if (e.code === 'ArrowUp') { goJump(); e.preventDefault(); }
});

let touchStartX = 0, touchStartY = 0;
if (cvs) {
  cvs.addEventListener('touchstart', (e) => { touchStartX = e.changedTouches[0].screenX; touchStartY = e.changedTouches[0].screenY; }, {passive: true});
  cvs.addEventListener('touchend', (e) => {
    if (!playing) return;
    let diffX = e.changedTouches[0].screenX - touchStartX;
    let diffY = e.changedTouches[0].screenY - touchStartY;
    if (Math.abs(diffX) > Math.abs(diffY)) {
      if (diffX > 30) goRight(); else if (diffX < -30) goLeft();
    } else {
      if (diffY < -30) goJump();
    }
  }, {passive: true});
}

function safelyStartGame() {
  try {
    document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
    let hud = document.getElementById('hud');
    if (hud) hud.classList.remove('hidden');
    playing = true; 
    score = 0; 
    runCoins = 0; 
    runDiamonds = 0; 
    speed = 3.5; 
    currentLane = 1; 
    jumpY = 0; 
    isJumping = false; 
    frameCount = 0; 
    spawnTimer = 0; 
    currentMY = 460;
    obstacles = []; 
    coinList = []; 
    diamondList = []; 
    gateObj = null; 
    floatTexts = [];
  } catch(e) {
    alert("Không thể bắt đầu trò chơi: " + e.message);
  }
}

function spawnObjects() {
  if (!playing) return;
  if (score >= 10000 && !gateObj) return;
  let types = ['rock', 'log', 'tree'];
  let lane = Math.floor(Math.random() * 3);

  if (score >= 3000) {
    obstacles.push({ lane: lane, y: -50, type: types[Math.floor(Math.random() * types.length)] });
    let lane2 = (lane + 1) % 3;
    obstacles.push({ lane: lane2, y: -80, type: types[Math.floor(Math.random() * types.length)] });
  } else if (score >= 2000) {
    obstacles.push({ lane: lane, y: -50, type: types[Math.floor(Math.random() * types.length)] });
    if (Math.random() < 0.4) {
      let lane2 = (lane + 1) % 3;
      coinList.push({ lane: lane2, y: -50 });
    }
  } else {
    let rand = Math.random();
    if (rand < 0.5) {
      obstacles.push({ lane: lane, y: -50, type: types[Math.floor(Math.random() * types.length)] });
    } else if (rand < 0.8) {
      coinList.push({ lane: lane, y: -50 });
    } else {
      diamondList.push({ lane: lane, y: -50 });
    }
  }
}

function updateGame() {
  if (!playing) return;
  score++;
  frameCount++;
  timer += 0.15;

  let baseSpeed = 3.5;
  if (score >= 3000) baseSpeed = 7.0;
  else if (score >= 2000) baseSpeed = 5.2;
  
  speed = baseSpeed + Math.floor(score / 500) * 0.25;
  roadOffset += speed;

  spawnTimer++;
  let currentSpawnThreshold = score >= 3000 ? 35 : (score >= 2000 ? 50 : 75);
  if (spawnTimer >= currentSpawnThreshold) {
    spawnTimer = 0;
    spawnObjects();
  }

  if (isJumping) { 
    jumpY += jumpVY; 
    jumpVY += 0.55; 
    if (jumpY >= 0) { jumpY = 0; isJumping = false; } 
  }

  playerData.quests.forEach(q => {
    if ((q.id === 1 || q.id === 101 || q.id % 100 === 1) && score > q.progress) q.progress = score;
  });

  if (score >= 10000 && !gateObj) {
    gateObj = { lane: 1, y: -100 };
  }

  if (gateObj) {
    gateObj.y += speed;
    if (gateObj.y >= 350 && gateObj.y <= 430 && gateObj.lane === currentLane) {
      victoryGame();
      return;
    }
  }

  for (let i = floatTexts.length - 1; i >= 0; i--) {
    let ft = floatTexts[i]; ft.y += ft.vy; ft.alpha -= 0.025; if (ft.alpha <= 0) floatTexts.splice(i, 1);
  }

  for (let i = obstacles.length - 1; i >= 0; i--) {
    let obs = obstacles[i]; obs.y += speed;
    if (obs.y >= 350 && obs.y <= 420 && obs.lane === currentLane) {
      if (!(obs.type === 'log' && isJumping && jumpY < -35)) {
        gameOver();
      }
    }
    if (obs.y > 550) obstacles.splice(i, 1);
  }

  for (let i = coinList.length - 1; i >= 0; i--) {
    let c = coinList[i]; c.y += speed;
    if (c.y >= 350 && c.y <= 420 && c.lane === currentLane && jumpY > -45) {
      runCoins++; playerData.coins++;
      playerData.quests.forEach(q => { if (q.id === 2 || q.id === 102 || q.id % 100 === 2) q.progress++; });
      floatTexts.push({ x: lanes[c.lane], y: 360, text: '+1 vàng', alpha: 1.0, vy: -2 });
      coinList.splice(i, 1); continue;
    }
    if (c.y > 550) coinList.splice(i, 1);
  }

  for (let i = diamondList.length - 1; i >= 0; i--) {
    let d = diamondList[i]; d.y += speed;
    if (d.y >= 350 && d.y <= 420 && d.lane === currentLane && jumpY > -45) {
      runDiamonds++; playerData.diamonds++;
      playerData.quests.forEach(q => { if (q.id === 3 || q.id === 103 || q.id % 100 === 3) q.progress++; });
      floatTexts.push({ x: lanes[d.lane], y: 360, text: '+1 kim cương', alpha: 1.0, vy: -2 });
      diamondList.splice(i, 1); continue;
    }
    if (d.y > 550) diamondList.splice(i, 1);
  }
}

function gameOver() {
  playing = false;
  saveGame();
  let hud = document.getElementById('hud');
  if (hud) hud.classList.add('hidden');
  let goScore = document.getElementById('go-score'); if (goScore) goScore.innerText = score;
  let goCoins = document.getElementById('go-coins'); if (goCoins) goCoins.innerText = runCoins;
  let goDiamonds = document.getElementById('go-diamonds'); if (goDiamonds) goDiamonds.innerText = runDiamonds;
  let screenGo = document.getElementById('screen-gameover'); if (screenGo) screenGo.classList.remove('hidden');
}

function victoryGame() {
  playing = false;
  playerData.diamonds = (Number(playerData.diamonds) || 0) + 100;
  saveGame();
  let hud = document.getElementById('hud');
  if (hud) hud.classList.add('hidden');
  let vicScore = document.getElementById('vic-score'); if (vicScore) vicScore.innerText = score;
  let screenVic = document.getElementById('screen-victory'); if (screenVic) screenVic.classList.remove('hidden');
}

function renderGame() {
  if (!ctx || !cvs) return;
  ctx.clearRect(0, 0, cvs.width, cvs.height);
  let skyGrad = ctx.createLinearGradient(0, 0, 0, 500);
  skyGrad.addColorStop(0, '#020617'); skyGrad.addColorStop(1, '#0f172a');
  ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, cvs.width, 500);

  ctx.fillStyle = '#f1f5f9'; ctx.beginPath(); ctx.arc(700, 70, 30, 0, Math.PI * 2); ctx.fill();

  ctx.fillStyle = '#1e293b'; ctx.fillRect(200, 0, 400, 500);
  ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.moveTo(200, 0); ctx.lineTo(200, 500); ctx.moveTo(600, 0); ctx.lineTo(600, 500); ctx.stroke();
  ctx.strokeStyle = 'rgba(56, 189, 248, 0.3)'; ctx.lineWidth = 2; ctx.setLineDash([15, 15]);
  ctx.beginPath(); ctx.moveTo(333, roadOffset % 500 - 500); ctx.lineTo(333, 500);
  ctx.moveTo(466, roadOffset % 500 - 500); ctx.lineTo(466, 500); ctx.stroke(); ctx.setLineDash([]);

  for (let i = 0; i < 10; i++) {
    let tY = (i * 120 + roadOffset * 1.5) % 600 - 50;
    ctx.fillStyle = '#064e3b'; ctx.beginPath(); ctx.arc(100, tY, 35, 0, Math.PI*2); ctx.arc(700, tY, 35, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = '#022c22'; ctx.fillRect(92, tY + 15, 16, 40); ctx.fillRect(692, tY + 15, 16, 40);
  }

  if (gateObj) {
    let gX = lanes[gateObj.lane], gY = gateObj.y;
    ctx.save();
    ctx.shadowColor = '#38bdf8'; ctx.shadowBlur = 25;
    ctx.fillStyle = 'rgba(56, 189, 248, 0.3)';
    ctx.fillRect(gX - 55, gY - 60, 110, 110);
    ctx.strokeStyle = '#00ffff'; ctx.lineWidth = 4;
    ctx.strokeRect(gX - 55, gY - 60, 110, 110);
    ctx.fillStyle = '#ffffff'; ctx.font = 'bold 14px monospace'; ctx.textAlign = 'center';
    ctx.fillText('THOÁT THÂN', gX, gY - 70);
    ctx.restore();
  }

  obstacles.forEach(o => {
    let targetX = lanes[o.lane];
    if (o.type === 'rock') {
      ctx.save();
      let rx = targetX, ry = o.y;
      ctx.fillStyle = '#334155'; ctx.beginPath();
      ctx.moveTo(rx - 32, ry + 16); ctx.lineTo(rx - 36, ry - 6); ctx.lineTo(rx - 14, ry - 28);
      ctx.lineTo(rx + 12, ry - 22); ctx.lineTo(rx + 36, ry - 6); ctx.lineTo(rx + 30, ry + 18);
      ctx.closePath(); ctx.fill();
      ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 2; ctx.stroke();
      ctx.restore();
    } else if (o.type === 'log') {
      ctx.save();
      let logGrad = ctx.createLinearGradient(targetX - 45, o.y - 14, targetX - 45, o.y + 14);
      logGrad.addColorStop(0, '#d97706'); logGrad.addColorStop(0.5, '#b45309'); logGrad.addColorStop(1, '#78350f');
      ctx.fillStyle = logGrad; ctx.beginPath();
      if (ctx.roundRect) { ctx.roundRect(targetX - 45, o.y - 12, 90, 24, 6); } else { ctx.rect(targetX - 45, o.y - 12, 90, 24); }
      ctx.fill(); ctx.strokeStyle = '#451a03'; ctx.lineWidth = 2; ctx.stroke();
      ctx.fillStyle = '#fef08a'; ctx.beginPath(); ctx.ellipse(targetX - 45, o.y, 7, 12, 0, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    } else if (o.type === 'tree') {
      ctx.fillStyle = '#451a03'; ctx.fillRect(targetX - 12, o.y - 45, 24, 50);
      ctx.fillStyle = '#16a34a'; ctx.beginPath(); ctx.arc(targetX, o.y - 50, 32, 0, Math.PI*2); ctx.fill();
    }
  });

  coinList.forEach(c => {
    let targetX = lanes[c.lane];
    let bounce = Math.sin(timer * 5) * 5;
    let cX = targetX, cY = c.y + bounce;
    ctx.save();
    ctx.fillStyle = '#b45309'; ctx.beginPath(); ctx.arc(cX, cY + 3, 18, 0, Math.PI * 2); ctx.fill();
    let coinGrad = ctx.createRadialGradient(cX - 4, cY - 4, 2, cX, cY, 18);
    coinGrad.addColorStop(0, '#fef08a'); coinGrad.addColorStop(0.5, '#facc15'); coinGrad.addColorStop(1, '#ca8a04');
    ctx.fillStyle = coinGrad; ctx.beginPath(); ctx.arc(cX, cY, 17, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#a16207'; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = '#854d0e'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('$', cX, cY + 1); ctx.restore();
  });

  diamondList.forEach(d => {
    let targetX = lanes[d.lane];
    let bounce = Math.sin(timer * 6) * 6;
    let dX = targetX, dY = d.y + bounce;
    ctx.save();
    ctx.fillStyle = '#38bdf8'; ctx.beginPath();
    ctx.moveTo(dX, dY - 16); ctx.lineTo(dX + 14, dY - 4); ctx.lineTo(dX, dY + 16); ctx.lineTo(dX - 14, dY - 4);
    ctx.closePath(); ctx.fill();
    ctx.strokeStyle = '#bae6fd'; ctx.lineWidth = 2; ctx.stroke();
    ctx.restore();
  });

  floatTexts.forEach(ft => {
    ctx.save(); ctx.globalAlpha = ft.alpha; ctx.fillStyle = '#38bdf8'; ctx.font = 'bold 16px monospace'; ctx.textAlign = 'center';
    ctx.fillText(ft.text, ft.x, ft.y); ctx.restore();
  });

  let skin = skins[playerData.equippedSkin] || skins['default'];
  let pX = lanes[currentLane], pY = 385 + jumpY;
  drawDetailedPlayer(ctx, pX, pY, skin, isJumping, timer);

  let targetMY = (frameCount > 120) ? 520 : 460;
  currentMY += (targetMY - currentMY) * 0.05;
  let mX = pX, mY = currentMY + Math.sin(timer * 0.6) * 6;
  
  ctx.fillStyle = '#22c55e'; ctx.beginPath();
  ctx.moveTo(mX, mY - 60); ctx.bezierCurveTo(mX + 45, mY - 40, mX + 50, mY + 10, mX + 30, mY + 40);
  ctx.bezierCurveTo(mX + 15, mY + 55, mX - 15, mY + 55, mX - 30, mY + 40);
  ctx.bezierCurveTo(mX - 50, mY + 10, mX - 45, mY - 40, mX, mY - 60); ctx.fill();

  let elScore = document.getElementById('score'); if (elScore) elScore.innerText = score;
  let elCoins = document.getElementById('coins'); if (elCoins) elCoins.innerText = playerData.coins;
  let elDiamonds = document.getElementById('diamonds'); if (elDiamonds) elDiamonds.innerText = playerData.diamonds;
}

function mainLoop() {
  if (playing) { updateGame(); renderGame(); }
  requestAnimationFrame(mainLoop);
}
mainLoop();
</script>
</body>
</html>
"""

components.html(html_code, height=520, scrolling=False)
