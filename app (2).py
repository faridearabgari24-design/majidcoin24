import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import argrelextrema

BRAND_NAME = "Majidcoin24"
BRAND_ICON = "🪙"
PURPLE = "#8B5CF6"
BLUE = "#3B82F6"
GREEN = "#10B981"
RED = "#EF4444"
DARK_BG = "#0B1120"
CARD_BG = "#1E293B"
CARD_BORDER = "#334155"
TEXT = "#F8FAFC"
TEXT_MUTED = "#94A3B8"

USERNAME = "admin"
PASSWORD = "Trader2026"

ASSETS = {"BTC-USD": "بیت‌کوین", "ETH-USD": "اتریوم", "GC=F": "طلای جهانی"}
TIMEFRAMES = {"15m": "۱۵ دقیقه", "1h": "۱ ساعت", "4h": "۴ ساعت", "1d": "روزانه"}

MUSIC_URL = "https://drive.google.com/uc?export=download&id=1dqN34S9uA-4nV6rLFzuORB58JbDS2Fvx"
MUSIC_URL_ALT = "https://docs.google.com/uc?export=download&id=1dqN34S9uA-4nV6rLFzuORB58JbDS2Fvx"

def play_welcome_music():
    st.markdown(f"""
        <div style="text-align:center;margin:0.5rem 0 1rem 0;">
            <audio autoplay controls style="width:70%;max-width:380px;border-radius:12px;">
                <source src="{MUSIC_URL}" type="audio/mpeg">
                <source src="{MUSIC_URL_ALT}" type="audio/mpeg">
            </audio>
            <p style="color:#94A3B8;font-size:0.85rem;">🎵 خوش آمدید</p>
        </div>
    """, unsafe_allow_html=True)

def brand_logo_svg(size=80):
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 140 140" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="g1{size}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#A78BFA"/>
                <stop offset="100%" stop-color="#7C3AED"/>
            </linearGradient>
            <linearGradient id="g2{size}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#60A5FA"/>
                <stop offset="100%" stop-color="#2563EB"/>
            </linearGradient>
        </defs>
        <g transform="translate(70,70)">
            <ellipse cx="-12" cy="0" rx="34" ry="44" fill="none" stroke="url(#g1{size})" stroke-width="4.5" transform="rotate(-30)"/>
            <ellipse cx="-4" cy="3" rx="32" ry="42" fill="none" stroke="url(#g1{size})" stroke-width="4.5" transform="rotate(-15)"/>
            <ellipse cx="16" cy="0" rx="36" ry="44" fill="none" stroke="url(#g2{size})" stroke-width="4.5" transform="rotate(20)"/>
        </g>
    </svg>
    """

def inject_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap');
        * {{ font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif !important; }}
        html, body, [class*="css"] {{ font-family: 'Vazirmatn', sans-serif !important; direction: rtl; }}
        .stApp {{ background: radial-gradient(ellipse at top, #1a1f3a 0%, {DARK_BG} 50%); color: {TEXT}; }}
        .brand-header {{ display: flex; align-items: center; justify-content: center; gap: 24px; padding: 1.5rem 0 0.5rem 0; flex-wrap: wrap; }}
        .brand-logo-wrap {{ filter: drop-shadow(0 0 30px rgba(139, 92, 246, 0.5)); animation: float 4s ease-in-out infinite; }}
        @keyframes float {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-8px); }} }}
        .brand-title {{ font-size: 3rem; font-weight: 900; background: linear-gradient(135deg, {PURPLE} 0%, {BLUE} 50%, {PURPLE} 100%); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shine 3s linear infinite; margin: 0; letter-spacing: 1px; }}
        @keyframes shine {{ to {{ background-position: 200% center; }} }}
        .brand-tagline {{ text-align: center; color: {TEXT_MUTED}; font-size: 1.05rem; margin-bottom: 1.5rem; font-weight: 500; }}
        .glass-card {{ background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(59, 130, 246, 0.05)); border: 1px solid rgba(139, 92, 246, 0.25); border-radius: 20px; padding: 1.5rem; backdrop-filter: blur(10px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }}
        div[data-testid="stMetric"] {{ background: linear-gradient(135deg, {CARD_BG} 0%, #253047 100%); border: 1px solid {CARD_BORDER}; border-radius: 16px; padding: 1.2rem; }}
        div[data-testid="stMetric"] label {{ color: {TEXT_MUTED} !important; }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{ color: {TEXT} !important; font-weight: 700 !important; }}
        .stButton > button {{ background: linear-gradient(135deg, {PURPLE}, {BLUE}) !important; color: white !important; font-weight: 700 !important; font-family: 'Vazirmatn' !important; border: none !important; border-radius: 12px !important; padding: 0.7rem 1.8rem !important; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important; }}
        section[data-testid="stSidebar"] {{ background: linear-gradient(180deg, {DARK_BG} 0%, #0F1629 100%); border-left: 1px solid {CARD_BORDER}; }}
        section[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
        .stSelectbox > div > div, .stTextInput > div > div > input {{ background: {CARD_BG} !important; color: {TEXT} !important; border-radius: 10px !important; }}
        h1, h2, h3, h4, h5, p, span, div, label {{ font-family: 'Vazirmatn' !important; color: {TEXT} !important; }}
        .brand-footer {{ text-align: center; color: {TEXT_MUTED}; padding: 2rem 0 1rem 0; border-top: 1px solid {CARD_BORDER}; margin-top: 3rem; }}
        .stTabs [data-baseweb="tab-list"] {{ gap: 8px; border-bottom: 2px solid {CARD_BORDER}; }}
        .stTabs [data-baseweb="tab"] {{ background: transparent; color: {TEXT_MUTED}; font-family: 'Vazirmatn'; padding: 10px 20px; }}
        .stTabs [aria-selected="true"] {{ background: linear-gradient(135deg, {PURPLE}, {BLUE}) !important; color: white !important; }}
        #MainMenu, footer, header {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

def brand_header():
    st.markdown(f"""
        <div class="brand-header">
            <div class="brand-logo-wrap">{brand_logo_svg(90)}</div>
            <h1 class="brand-title">Majidcoin<span style="background:linear-gradient(135deg,{BLUE},{PURPLE});-webkit-background-clip:text;-webkit-text-fill-color:transparent;">24</span></h1>
        </div>
        <p class="brand-tagline">پلتفرم تحلیل هوشمند بازار</p>
    """, unsafe_allow_html=True)

def brand_footer():
    st.markdown(f"""
        <div class="brand-footer">
            <strong style="background:linear-gradient(135deg,{PURPLE},{BLUE});-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Majidcoin24</strong> © 2026
        </div>
    """, unsafe_allow_html=True)

def safe(v, default=0.0):
    try:
        if v is None or (isinstance(v, float) and np.isnan(v)):
            return default
        return float(v)
    except:
        return default

def calculate_atr(df, period=14):
    high, low, close = df['High'], df['Low'], df['Close']
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def calculate_ichimoku(df, tenkan=9, kijun=26, senkou=52):
    high, low, close = df['High'], df['Low'], df['Close']
    t = (high.rolling(tenkan).max() + low.rolling(tenkan).min()) / 2
    k = (high.rolling(kijun).max() + low.rolling(kijun).min()) / 2
    sa = ((t + k) / 2).shift(kijun)
    sb = ((high.rolling(senkou).max() + low.rolling(senkou).min()) / 2).shift(kijun)
    return {'tenkan': t, 'kijun': k, 'senkou_a': sa, 'senkou_b': sb}

def find_zigzag(df, order=5, min_pct=0.02):
    highs, lows = df['High'].values, df['Low'].values
    hi = argrelextrema(highs, np.greater_equal, order=order)[0]
    lo = argrelextrema(lows, np.less_equal, order=order)[0]
    all_idx = sorted(set(hi).union(set(lo)))
    pivots, last_price, last_type = [], None, None
    for i in all_idx:
        if i < order or i >= len(df) - order:
            continue
        ih, il = i in hi, i in lo
        if ih and not il:
            pt, pr = 'high', highs[i]
        elif il and not ih:
            pt, pr = 'low', lows[i]
        else:
            mid = (highs[i] + lows[i]) / 2
            pt, pr = ('high', highs[i]) if df['Close'].iloc[i] >= mid else ('low', lows[i])
        if pt == last_type:
            if pt == 'high' and pr > (pivots[-1]['price'] if pivots else pr):
                pivots[-1] = {'index': i, 'price': pr, 'type': pt}
            elif pt == 'low' and pr < (pivots[-1]['price'] if pivots else pr):
                pivots[-1] = {'index': i, 'price': pr, 'type': pt}
            continue
        if last_price is not None and abs(pr - last_price) / last_price < min_pct:
            continue
        pivots.append({'index': i, 'price': pr, 'type': pt})
        last_price, last_type = pr, pt
    return pivots

def detect_wave(pivots):
    if len(pivots) < 4:
        return {'signal': "در حال شکل‌گیری", 'dir': 0, 'reason': "ساختار موج هنوز کامل نشده."}
    recent = pivots[-6:] if len(pivots) >= 6 else pivots
    highs = [p for p in recent if p['type'] == 'high']
    lows = [p for p in recent if p['type'] == 'low']
    if len(highs) < 2 or len(lows) < 2:
        return {'signal': "در حال شکل‌گیری", 'dir': 0, 'reason': "داده کافی نیست."}
    lh, ph = highs[-1]['price'], highs[-2]['price']
    ll, pl = lows[-1]['price'], lows[-2]['price']
    if lh > ph and ll > pl:
        return {'signal': "موج صعودی", 'dir': 1, 'reason': f"سقف بالاتر و کف بالاتر."}
    if lh < ph and ll < pl:
        return {'signal': "موج نزولی", 'dir': -1, 'reason': f"سقف پایین‌تر و کف پایین‌تر."}
    if lh > ph and ll < pl:
        return {'signal': "انبساط", 'dir': 0, 'reason': "نوسان در حال افزایش."}
    if lh < ph and ll > pl:
        return {'signal': "انقباض", 'dir': 0, 'reason': "فشار فشرده."}
    return {'signal': "اصلاح", 'dir': 0, 'reason': "ساختار اصلاحیه."}

def check_cross(tenkan, kijun, lookback=5):
    if len(tenkan) < lookback + 1:
        return 'none'
    t = tenkan.iloc[-(lookback+1):].values
    k = kijun.iloc[-(lookback+1):].values
    for i in range(1, len(t)):
        if any(np.isnan(x) for x in [t[i], k[i], t[i-1], k[i-1]]):
            continue
        if t[i] > k[i] and t[i-1] <= k[i-1]:
            return 'up'
        if t[i] < k[i] and t[i-1] >= k[i-1]:
            return 'down'
    if not np.isnan(t[-1]) and not np.isnan(k[-1]):
        return 'above' if t[-1] > k[-1] else 'below'
    return 'none'

def analyze(df, ichimoku, wave, asset_name, tf_name):
    close = safe(df['Close'].iloc[-1])
    tenkan = safe(ichimoku['tenkan'].iloc[-1])
    kijun = safe(ichimoku['kijun'].iloc[-1])
    sa = safe(ichimoku['senkou_a'].iloc[-1])
    sb = safe(ichimoku['senkou_b'].iloc[-1])
    atr = safe(calculate_atr(df).iloc[-1], close * 0.01)
    cloud_ok = sa > 0 and sb > 0
    cloud_top = max(sa, sb) if cloud_ok else close
    cloud_bot = min(sa, sb) if cloud_ok else close
    if not cloud_ok: pos = 'unknown'
    elif close > cloud_top: pos = 'above'
    elif close < cloud_bot: pos = 'below'
    else: pos = 'inside'
    cta = abs(cloud_top - cloud_bot) / atr if atr > 0 and cloud_ok else 0
    cs = "ضعیف" if cta < 0.5 else ("متوسط" if cta < 1.5 else "قوی")
    cross = check_cross(ichimoku['tenkan'], ichimoku['kijun'], 5)
    above = pos == 'above'; below = pos == 'below'
    tk_bull = cross in ('up', 'above'); tk_bear = cross in ('down', 'below')
    wb = wave['dir'] == 1; ws = wave['dir'] == -1
    buy_c = sum([above, tk_bull and wb, wb])
    sell_c = sum([below, tk_bear and ws, ws])
    if buy_c >= 3 and cta >= 0.5: dec, dr = "🟢 خرید قوی", "buy"
    elif buy_c == 3: dec, dr = "🟢 خرید (ابر ضعیف)", "buy"
    elif sell_c >= 3 and cta >= 0.5: dec, dr = "🔴 فروش قوی", "sell"
    elif sell_c == 3: dec, dr = "🔴 فروش (ابر ضعیف)", "sell"
    elif buy_c == 2 and wb: dec, dr = "🟡 صبر — تمایل صعودی", "wait_bull"
    elif sell_c == 2 and ws: dec, dr = "🟡 صبر — تمایل نزولی", "wait_bear"
    elif pos == 'inside': dec, dr = "⛔ وارد نشو — داخل ابر", "no"
    else: dec, dr = "⛔ وارد نشو — نامشخص", "no"
    entry = close
    if dr == "buy":
        sl = min(kijun, cloud_bot) if cloud_ok else close - atr * 1.5
        tp1 = cloud_top + atr if cloud_ok else close + atr * 2
        tp2 = tp1 + atr * 1.5
        if tp1 <= entry: tp1 = entry + atr * 1.5
        if tp2 <= tp1: tp2 = tp1 + atr * 1.5
    elif dr == "sell":
        sl = max(kijun, cloud_top) if cloud_ok else close + atr * 1.5
        tp1 = cloud_bot - atr if cloud_ok else close - atr * 2
        tp2 = tp1 - atr * 1.5
        if tp1 >= entry: tp1 = entry - atr * 1.5
        if tp2 >= tp1: tp2 = tp1 - atr * 1.5
    else:
        sl = kijun if kijun > 0 else close - atr
        tp1 = cloud_top if cloud_ok else close + atr
        tp2 = close + atr * 2
    L = []
    L.append(f"📊 **تحلیل {asset_name} — تایم‌فریم {tf_name}**\n")
    L.append(f"**💰 قیمت فعلی:** `${close:,.2f}`\n")
    L.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    L.append("**🌊 ساختار موج (نئوویو):**")
    L.append(f"• وضعیت: **{wave['signal']}**")
    L.append(f"• {wave['reason']}\n")
    L.append("**☁️ وضعیت ایچیموکو:**")
    pf = {'above': 'بالای ابر ✅', 'below': 'زیر ابر ❌', 'inside': 'داخل ابر ⚠️', 'unknown': 'نامشخص'}[pos]
    L.append(f"• موقعیت قیمت: **{pf}**")
    L.append(f"• تنکان: `${tenkan:,.2f}` | کیجون: `${kijun:,.2f}`")
    cf = {'up': '✅ کراس صعودی تازه', 'down': '❌ کراس نزولی تازه', 'above': '➖ تنکان بالای کیجون', 'below': '➖ تنکان زیر کیجون', 'none': '➖ نامشخص'}[cross]
    L.append(f"• کراس: {cf}")
    L.append(f"• قدرت ابر: **{cs}**")
    L.append(f"• ATR: `${atr:,.2f}`\n")
    L.append("**⚖️ نتیجه‌گیری:**")
    L.append(f"• تأیید خرید: **{buy_c}/3**")
    L.append(f"• تأیید فروش: **{sell_c}/3**\n")
    L.append("**🎯 تصمیم نهایی:**")
    L.append(f"### {dec}")
    if dr in ("buy", "sell"): L.append("✅ شرایط کامل تأیید شد.")
    elif dr == "wait_bull": L.append("⏸️ تمایل صعودی. صبر کن.")
    elif dr == "wait_bear": L.append("⏸️ تمایل نزولی. صبر کن.")
    else: L.append("⛔ شرایط مناسب نیست.")
    L.append("")
    L.append("**📌 سطوح کلیدی:**\n")
    L.append("| سطح | قیمت |")
    L.append("|-----|------|")
    if cloud_ok:
        L.append(f"| مقاومت | `${cloud_top:,.2f}` |")
        L.append(f"| حمایت | `${cloud_bot:,.2f}` |")
    L.append(f"| 🎯 ورود | `${entry:,.2f}` |")
    L.append(f"| 🛑 حد ضرر | `${sl:,.2f}` |")
    L.append(f"| ✅ هدف ۱ | `${tp1:,.2f}` |")
    L.append(f"| 🚀 هدف ۲ | `${tp2:,.2f}` |")
    return {'decision': dec, 'direction': dr, 'entry': entry, 'sl': sl, 'tp1': tp1, 'tp2': tp2,
            'buy_conf': buy_c, 'sell_conf': sell_c, 'analysis_text': "\n".join(L),
            'pos': pos, 'cross': cross, 'atr': atr, 'cta': cta}

st.set_page_config(page_title=BRAND_NAME, page_icon=BRAND_ICON, layout="wide")
inject_css()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="text-align:center;padding:1rem 0;">
                <div class="brand-logo-wrap" style="display:inline-block;">{brand_logo_svg(140)}</div>
                <h1 class="brand-title" style="font-size:2.8rem;margin-top:1rem;">Majidcoin<span style="background:linear-gradient(135deg,{BLUE},{PURPLE});-webkit-background-clip:text;-webkit-text-fill-color:transparent;">24</span></h1>
                <p class="brand-tagline">پلتفرم تحلیل هوشمند بازار</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align:center;margin-bottom:1.5rem;'>🔐 ورود به حساب کاربری</h4>", unsafe_allow_html=True)
        username = st.text_input("👤 نام کاربری")
        password = st.text_input("🔑 رمز عبور", type="password")
        if st.button("🚀 ورود به پلتفرم", use_container_width=True):
            if username == USERNAME and password == PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ نام کاربری یا رمز اشتباهه")
        st.markdown('</div>', unsafe_allow_html=True)

def main_page():
    play_welcome_music()
    with st.sidebar:
        st.markdown(f"""
            <div style="text-align:center;padding:1rem 0;">
                <div class="brand-logo-wrap" style="display:inline-block;">{brand_logo_svg(80)}</div>
                <h3 class="brand-title" style="font-size:1.6rem;margin-top:0.5rem;">Majidcoin<span style="background:linear-gradient(135deg,{BLUE},{PURPLE});-webkit-background-clip:text;-webkit-text-fill-color:transparent;">24</span></h3>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:{TEXT_MUTED};'>👤 {USERNAME}</p>", unsafe_allow_html=True)
        if st.button("🚪 خروج", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        st.markdown("---")
        st.markdown(f"<h4>⚙️ تنظیمات</h4>", unsafe_allow_html=True)
        asset = st.selectbox("📊 بازار", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
        tf = st.selectbox("⏱️ تایم‌فریم", list(TIMEFRAMES.keys()), format_func=lambda x: TIMEFRAMES[x])
        st.markdown("---")
        st.markdown(f"<h4>🧠 استراتژی</h4>", unsafe_allow_html=True)
        st.caption("ترکیب ایچیموکو + نئوویو")
    
    brand_header()
    
    with st.spinner("🔄 در حال تحلیل..."):
        period_map = {"15m": "1mo", "1h": "3mo", "4h": "1y", "1d": "2y"}
        period = period_map.get(tf, "6mo")
        df = yf.download(asset, period=period, interval=tf, progress=False)
        if df.empty:
            st.error(f"❌ داده‌ای یافت نشد")
            return
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        ichimoku = calculate_ichimoku(df)
        zo = {"15m": 5, "1h": 5, "4h": 4, "1d": 3}[tf]
        zp = {"15m": 0.005, "1h": 0.01, "4h": 0.015, "1d": 0.02}[tf]
        pivots = find_zigzag(df, order=zo, min_pct=zp)
        wave = detect_wave(pivots)
        result = analyze(df, ichimoku, wave, ASSETS[asset], TIMEFRAMES[tf])
    
    d = result['decision']
    if "خرید قوی" in d: st.success(f"## {d}")
    elif "خرید" in d: st.info(f"## {d}")
    elif "فروش قوی" in d: st.error(f"## {d}")
    elif "فروش" in d: st.warning(f"## {d}")
    elif "صبر" in d: st.warning(f"## {d}")
    else: st.error(f"## {d}")
    
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📝 تحلیل", "📊 چک‌لیست", "📈 نمودار"])
    
    with tab1:
        st.markdown(result['analysis_text'])
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ✅ وضعیت")
            p = result['pos']
            st.write(f"{'✅' if p=='above' else '❌' if p=='below' else '⚠️'} موقعیت: {p}")
            c = result['cross']
            st.write(f"{'✅' if c=='up' else '❌' if c=='down' else '➖'} کراس: {c}")
            st.write(f"🌊 موج: {wave['signal']}")
        with col2:
            st.markdown("### 📊 آمار")
            st.metric("تأیید خرید", f"{result['buy_conf']}/3")
            st.metric("تأیید فروش", f"{result['sell_conf']}/3")
            st.metric("ATR", f"${result['atr']:,.2f}")
    
    with tab3:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.75, 0.25])
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="قیمت", increasing_line_color=GREEN, decreasing_line_color=RED), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ichimoku['tenkan'], name="تنکان", line=dict(color=BLUE, width=1.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ichimoku['kijun'], name="کیجون", line=dict(color=PURPLE, width=1.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ichimoku['senkou_a'], name="سنکو A", line=dict(color=GREEN, width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ichimoku['senkou_b'], name="سنکو B", line=dict(color=RED, width=1), fill='tonexty', fillcolor='rgba(139,92,246,0.1)'), row=1, col=1)
        for p in pivots[-15:]:
            fig.add_trace(go.Scatter(x=[df.index[p['index']]], y=[p['price']], mode='markers', marker=dict(color=PURPLE if p['type']=='high' else BLUE, size=11, symbol='diamond'), showlegend=False), row=1, col=1)
        colors = [GREEN if df['Close'].iloc[i] >= df['Open'].iloc[i] else RED for i in range(len(df))]
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="حجم", marker_color=colors), row=2, col=1)
        fig.update_layout(height=650, template="plotly_dark", xaxis_rangeslider_visible=False, hovermode='x unified', paper_bgcolor=DARK_BG, plot_bgcolor=CARD_BG, font=dict(family="Vazirmatn"))
        st.plotly_chart(fig, use_container_width=True)
    
    brand_footer()

if st.session_state.logged_in:
    main_page()
else:
    login_page()