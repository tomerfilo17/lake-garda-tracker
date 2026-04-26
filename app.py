"""
גארדה וילה - מעקב אחר וילות בלייק גארדה
גרסה מלאה עם עברית, פרופילים אישיים ומרחקי נסיעה
"""

import streamlit as st
import requests
import time
import os
import math
from datetime import datetime

st.set_page_config(
    page_title="🏡 גארדה וילה",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@400;700;900&family=Heebo:wght@300;400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Heebo', sans-serif; direction: rtl; }
h1,h2,h3 { font-family: 'Frank Ruhl Libre', serif; }
.main { background: #f7f2ea; }

.deal-banner {
  background: linear-gradient(135deg, #c8420a, #e85d20);
  color: white; border-radius: 16px; padding: 20px 28px;
  margin-bottom: 24px; animation: glow 2s ease-in-out infinite;
}
@keyframes glow {
  0%,100% { box-shadow: 0 0 0 0 rgba(200,66,10,0.4); }
  50%      { box-shadow: 0 0 0 8px rgba(200,66,10,0); }
}
.deal-banner h3 { color: white; margin: 0 0 6px; font-size: 1.3rem; }
.deal-banner p  { color: rgba(255,255,255,0.88); margin: 0; font-size: 0.9rem; }
.deal-price { font-size: 2rem; font-weight: 900; }

.hero {
  background: linear-gradient(135deg, #2d5a3d 0%, #1a3d2a 100%);
  border-radius: 20px; padding: 36px 32px 28px;
  color: white; margin-bottom: 28px;
}
.hero h1 { color: white; font-size: 2rem; margin: 0 0 6px; }
.hero-sub { color: rgba(255,255,255,0.75); font-size: 0.9rem; }
.hero-badge {
  background: rgba(255,255,255,0.15); border-radius: 12px;
  padding: 10px 18px; text-align: center;
}
.hero-badge .em { font-size: 1.8rem; }
.hero-badge .nm { font-size: 0.85rem; color: rgba(255,255,255,0.8); }

.stats-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 28px; }
.stat-card {
  background: white; border-radius: 12px; padding: 16px 20px;
  border: 1px solid #e8e0d0; text-align: center;
}
.stat-num { font-size: 1.7rem; font-weight: 700; color: #1a3d2a; }
.stat-lbl { font-size: 0.75rem; color: #8a7a6a; margin-top: 2px; }

.villa-card {
  background: white; border-radius: 18px; margin-bottom: 24px;
  overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.07);
  border: 1.5px solid #e8e0d0;
  transition: transform 0.2s, box-shadow 0.2s;
}
.villa-card:hover { transform: translateY(-4px); box-shadow: 0 12px 36px rgba(0,0,0,0.13); }
.card-img { width: 100%; height: 210px; object-fit: cover; }
.card-body { padding: 18px 20px 20px; }
.card-title { font-family: 'Frank Ruhl Libre', serif; font-size: 1.15rem; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; }
.card-loc { color: #8a7a6a; font-size: 0.82rem; margin-bottom: 10px; }

.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 500; margin: 2px 3px 2px 0; }
.bg   { background:#e6f4ea; color:#1e6e2e; }
.bb   { background:#e3f0fc; color:#1a5fa8; }
.bo   { background:#fff3e0; color:#b85c00; }
.bt   { background:#e0f5f0; color:#0a6e56; }
.br   { background:#fce8e8; color:#b01c1c; }
.bpu  { background:#eeedfe; color:#3c3489; }

.drive-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; margin: 8px 0; }
.drive-table th { color: #8a7a6a; padding: 4px 6px; text-align: right; font-weight: 500; border-bottom: 1px solid #e8e0d0; }
.drive-table td { padding: 5px 6px; color: #2a2a2a; border-bottom: 1px solid #f0ebe0; }
.drive-table tr:last-child td { border-bottom: none; }
.dkm { font-weight: 600; color: #2d5a3d; }
.dtm { color: #8a7a6a; }

.price-row { display: flex; justify-content: space-between; align-items: flex-end; margin-top: 14px; flex-wrap: wrap; gap: 10px; }
.price-tag { font-size: 1.5rem; font-weight: 700; color: #1a1a1a; }
.price-sub { font-size: 0.78rem; color: #8a7a6a; }
.free-cancel { color: #1e6e2e; font-size: 0.8rem; font-weight: 500; margin-top: 3px; }
.book-btn {
  display: inline-block; background: #2d5a3d; color: white !important;
  padding: 10px 22px; border-radius: 10px; text-decoration: none !important;
  font-weight: 600; font-size: 0.88rem; transition: background 0.2s;
}
.book-btn:hover { background: #1e3d2a; }

.rating-row { display: flex; align-items: center; gap: 6px; margin: 8px 0; }
.stars { color: #f4a700; }
.rnum { font-weight: 600; font-size: 0.9rem; }
.rcnt { color: #8a7a6a; font-size: 0.78rem; }

.sec-hdr {
  font-family: 'Frank Ruhl Libre', serif;
  font-size: 1rem; font-weight: 700; color: #2d5a3d;
  border-right: 4px solid #2d5a3d; padding-right: 10px;
  margin: 14px 0 8px;
}
.deal-star { color: #e85d20; font-size: 0.85rem; font-weight: 700; }
.no-res { text-align:center; padding:60px 20px; color:#8a7a6a; font-size:1.1rem; }

div[data-testid="stSidebar"] { background: #1a3d2a !important; }
div[data-testid="stSidebar"] label,
div[data-testid="stSidebar"] p,
div[data-testid="stSidebar"] span,
div[data-testid="stSidebar"] div { color: white !important; }
.stButton>button {
  background: #2d5a3d !important; color: white !important;
  border: none !important; border-radius: 8px !important; font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Config ───────────────────────────────────────────────────────────────────
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")
try:
    RAPIDAPI_KEY = RAPIDAPI_KEY or st.secrets.get("RAPIDAPI_KEY", "")
except Exception:
    pass

ITINERARY = [
    {"date": "18 מאי", "desc": "הגעה + סירמיונה", "lat": 45.4952, "lon": 10.6088},
    {"date": "19 מאי", "desc": "גרדה + לאציזה", "lat": 45.5046, "lon": 10.7361},
    {"date": "20 מאי", "desc": "גארדלנד + Caneva", "lat": 45.4452, "lon": 10.7136},
    {"date": "21 מאי", "desc": "ורונה (יום עיר)", "lat": 45.4386, "lon": 10.9944},
    {"date": "22 מאי", "desc": "מאלצ'זינה + כבל רכבל", "lat": 45.7661, "lon": 10.8059},
    {"date": "23 מאי", "desc": "ריבה דל גארדה + קיאקים", "lat": 45.8853, "lon": 10.8439},
]

PROFILES = {
    "shimon": {
        "name": "שמעון",
        "emoji": "🚗",
        "title": "אבא – מצב נהג",
        "desc": "מרחקי נסיעה + חוויות מהאזור",
        "focus": "distance",
        "welcome": "שלום שמעון! כל מרחקי הנסיעה מחושבים עבורך 🚗",
    },
    "shachar": {
        "name": "שחר",
        "emoji": "👶",
        "title": "אחות – פעילויות לילדים",
        "desc": "מה יש לילדים הקטנים",
        "focus": "kids",
        "welcome": "היי שחר! הכל ידידותי לפעוטות 👶🎡",
    },
    "ima": {
        "name": "אמא",
        "emoji": "✨",
        "title": "אמא – נקיון ויופי",
        "desc": "וילות יפות, נקיות ומעוצבות",
        "focus": "beauty",
        "welcome": "שלום אמא! רק הכי יפות ונקיות 🌸",
    },
}

DEMO = [
    {
        "id":"d1","name":"אגריטוריזמו וילה אולנדרו – לאציזה",
        "area":"לאציזה (חוף מזרחי)","address":"Via Gardesana, Lazise",
        "lat":45.5046,"lon":10.7361,
        "photo":"https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=700",
        "rating":4.7,"reviews":138,
        "eur_n":390,"eur_t":2340,
        "beds":4,"baths":3,"free_cancel":True,"is_deal":True,
        "deal_reason":"מחיר נמוך ב-30% מהממוצע עם דירוג 4.7 – מבצע אמיתי!",
        "tags":["🌿 אגריטוריזמו","🏊 בריכה","🌊 נוף לאגם","✅ ביטול חינם","👶 ידידותי לילדים","🧹 נקי מאוד","⭐ חדש ומעוצב"],
        "kids":["גינה מוקפת גדר","חדר משחקים","מיטות תינוק","בריכה רדודה"],
        "clean":"10/10 – אורחים כותבים 'נקי להפליא', שופץ 2023",
        "exp":["טעימות יין בכרמים","טיולי אופניים לאגם","שוק שבועי בלאציזה"],
        "url":"https://www.booking.com/searchresults.en-gb.html?ss=Lazise&checkin=2025-05-18&checkout=2025-05-24&group_adults=7&no_rooms=1&group_children=2",
    },
    {
        "id":"d2","name":"וילה רוסטיקה סירמיונה – חצי האי",
        "area":"סירמיונה (חוף דרומי)","address":"Loc. Lugana, Sirmione",
        "lat":45.4948,"lon":10.6082,
        "photo":"https://images.unsplash.com/photo-1613977257363-707ba9348227?w=700",
        "rating":4.5,"reviews":87,
        "eur_n":510,"eur_t":3060,
        "beds":4,"baths":4,"free_cancel":True,"is_deal":False,"deal_reason":"",
        "tags":["🏊 בריכה","🌊 נוף לאגם","✅ ביטול חינם","🧹 נקי מאוד","⭐ יוקרתי"],
        "kids":["בריכה פרטית מגודרת","גינה נרחבת"],
        "clean":"9.5/10 – עיצוב מודרני ושמור היטב",
        "exp":["גלישת מים באגם","סיור ב-Castello Scaligero","ספא מקומי"],
        "url":"https://www.booking.com/searchresults.en-gb.html?ss=Sirmione&checkin=2025-05-18&checkout=2025-05-24&group_adults=7&no_rooms=1&group_children=2",
    },
    {
        "id":"d3","name":"קאזאלה דלי אוליבי – גבעות בארדולינו",
        "area":"בארדולינו (חוף מזרחי)","address":"Via del Oliveto 12, Bardolino",
        "lat":45.5468,"lon":10.7225,
        "photo":"https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=700",
        "rating":4.3,"reviews":62,
        "eur_n":340,"eur_t":2040,
        "beds":5,"baths":3,"free_cancel":True,"is_deal":False,"deal_reason":"",
        "tags":["🌿 אגריטוריזמו","✅ ביטול חינם","👶 ידידותי לילדים","🧹 נקי"],
        "kids":["חצר גדולה","עגלת ילדים זמינה","שלב ונדנדה"],
        "clean":"8.5/10 – כפרי ומסורתי, נקי ומסודר",
        "exp":["כרמי יין בארדולינו","אופניים לאגם","פיקניק בזיתייה"],
        "url":"https://www.booking.com/searchresults.en-gb.html?ss=Bardolino&checkin=2025-05-18&checkout=2025-05-24&group_adults=7&no_rooms=1&group_children=2",
    },
    {
        "id":"d4","name":"טנוטה לה קוורצ'ה – מאלצ'זינה",
        "area":"מאלצ'זינה (חוף מזרחי)","address":"Loc. Navene, Malcesine",
        "lat":45.7661,"lon":10.8059,
        "photo":"https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=700",
        "rating":4.8,"reviews":211,
        "eur_n":455,"eur_t":2730,
        "beds":4,"baths":3,"free_cancel":True,"is_deal":True,
        "deal_reason":"דירוג 4.8 + מחיר טוב ביחס לאיכות – ערך מעולה!",
        "tags":["🌿 אגריטוריזמו","🏊 בריכה","🌊 נוף לאגם","✅ ביטול חינם","👶 ידידותי לילדים","⭐ חדש ומעוצב","🧹 נקי מאוד"],
        "kids":["גינה מגודרת 1,500מ\"ר","מגלשה ונדנדות","כלי שחייה לילדים"],
        "clean":"10/10 – שופצה 2023 מהיסוד, עיצוב חדש לחלוטין",
        "exp":["כבל-רכבל מונטה באלדו","שייט בקיאק","כפר מאלצ'זינה ההיסטורי"],
        "url":"https://www.booking.com/searchresults.en-gb.html?ss=Malcesine&checkin=2025-05-18&checkout=2025-05-24&group_adults=7&no_rooms=1&group_children=2",
    },
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d1 = math.radians(lat2-lat1)
    d2 = math.radians(lon2-lon1)
    a  = math.sin(d1/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(d2/2)**2
    return round(R * 2 * math.asin(math.sqrt(a)), 1)

def drive_time(km):
    mins = int(km/60*60 + 8)
    return f"{mins}דק'" if mins < 60 else f"{mins//60}ש'{mins%60:02d}דק'"

def stars_str(r):
    return "★"*int(r) + ("" if (r-int(r)) < 0.5 else "½") + "☆"*(5-int(r)-(1 if (r-int(r))>=0.5 else 0))

def eur_to_usd(e):
    return round(e * 1.08)

# ─── Login ────────────────────────────────────────────────────────────────────
def show_login():
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        st.markdown("""
        <div style="text-align:center;margin:48px 0 32px">
          <div style="font-family:'Frank Ruhl Libre',serif;font-size:3rem;font-weight:900;color:#1a3d2a;line-height:1">🌊 גארדה וילה</div>
          <p style="color:#6a8a6a;margin:8px 0 36px;font-size:1.05rem">חופשת משפחה · לייק גארדה · 18–24 מאי 2025</p>
          <p style="color:#8a7a6a;font-size:0.9rem;margin-bottom:20px">מי אתה/את? בחר/י פרופיל אישי</p>
        </div>
        """, unsafe_allow_html=True)

        for key, p in PROFILES.items():
            if st.button(
                f"{p['emoji']}   {p['name']} — {p['title']}",
                key=f"login_{key}",
                use_container_width=True,
                help=p['desc']
            ):
                st.session_state["profile"] = key
                st.session_state["props"] = DEMO
                st.session_state["ts"] = datetime.now().strftime("%H:%M:%S")
                st.rerun()

        st.markdown("<div style='text-align:center;color:#8a7a6a;font-size:0.78rem;margin-top:24px'>ניתן לעבור בין פרופילים בכל שלב מהתפריט הצידי</div>", unsafe_allow_html=True)

# ─── Card ─────────────────────────────────────────────────────────────────────
def render_card(p, focus):
    badges = "".join(f'<span class="badge bg">{t}</span>' for t in p["tags"])
    deal   = '<span class="deal-star"> 🔥 מבצע</span>' if p.get("is_deal") else ""
    cancel = '<div class="free-cancel">✅ ביטול חינם – החזר מלא עד 24 שעות לפני</div>' if p["free_cancel"] else ""
    usd_n  = eur_to_usd(p["eur_n"])
    usd_t  = eur_to_usd(p["eur_t"])

    # Section extras
    extra = ""

    if focus == "distance":
        rows = drive_distances_html(p["lat"], p["lon"])
        exp  = " · ".join(p.get("exp", []))
        extra = f"""
        <div class="sec-hdr">🚗 מרחקי נסיעה יומיים</div>
        <table class="drive-table">
          <thead><tr><th>תאריך</th><th>יעד</th><th>מרחק</th><th>זמן נסיעה</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
        <p style="font-size:0.78rem;color:#6a8a6a;margin:6px 0 0">🎯 {exp}</p>
        """

    elif focus == "kids":
        items = "".join(f'<span class="badge bt">{f}</span>' for f in p.get("kids",[]))
        extra = f'<div class="sec-hdr">👶 מה יש לילדים</div><div style="line-height:2.2">{items}</div>'

    elif focus == "beauty":
        extra = f'<div class="sec-hdr">✨ נקיון ומראה</div><p style="font-size:0.88rem;color:#2a2a2a;margin:0">{p.get("clean","")}</p>'

    st.markdown(f"""
    <div class="villa-card">
      <img class="card-img" src="{p['photo']}" alt="{p['name']}"
           onerror="this.src='https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600'">
      <div class="card-body">
        <div class="card-title">{p['name']}{deal}</div>
        <div class="card-loc">📍 {p['area']} &nbsp;·&nbsp; {p['address']}</div>
        <div class="rating-row">
          <span class="stars">{stars_str(p['rating'])}</span>
          <span class="rnum">{p['rating']}/5</span>
          <span class="rcnt">({p['reviews']} ביקורות)</span>
          <span class="badge bb">{p['beds']} חד' שינה · {p['baths']} אמבטיות</span>
        </div>
        {badges}
        {extra}
        <div class="price-row">
          <div>
            <div class="price-tag">${usd_n}<span style="font-size:1rem;font-weight:400">/לילה</span></div>
            <div class="price-sub">סה"כ: ${usd_t} (6 לילות) · 7 מבוגרים + 2 פעוטות</div>
            {cancel}
          </div>
          <a class="book-btn" href="{p['url']}" target="_blank">הזמן עכשיו ←</a>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def drive_distances_html(vlat, vlon):
    trs = ""
    for day in ITINERARY:
        km = haversine(vlat, vlon, day["lat"], day["lon"])
        t  = drive_time(km)
        trs += f"<tr><td>{day['date']}</td><td>{day['desc']}</td><td class='dkm'>{km} ק\"מ</td><td class='dtm'>{t}</td></tr>"
    return trs

# ─── Dashboard ────────────────────────────────────────────────────────────────
def show_dashboard():
    profile = st.session_state.get("profile", "shimon")
    prof    = PROFILES[profile]
    focus   = prof["focus"]

    with st.sidebar:
        st.markdown(f"## {prof['emoji']} שלום {prof['name']}!")
        st.markdown(f"*{prof['welcome']}*")
        st.markdown("---")
        st.markdown("### 🔍 סינון")
        min_r  = st.slider("דירוג מינימלי", 4.0, 5.0, 4.0, 0.1)
        max_p  = st.slider("מחיר מקסימלי ללילה ($)", 500, 1400, 1200, 50)
        st.markdown("### 🏷️ פילטרים")
        req_pool = st.checkbox("🏊 בריכה")
        req_agri = st.checkbox("🌿 אגריטוריזמו")
        req_lake = st.checkbox("🌊 נוף לאגם")
        req_kids = st.checkbox("👶 ידידותי לילדים") if profile == "shachar" else False
        req_cln  = st.checkbox("🧹 נקי מאוד") if profile == "ima" else False
        st.markdown("---")
        st.markdown("### 👤 החלף פרופיל")
        for k, p in PROFILES.items():
            if k != profile:
                if st.button(f"{p['emoji']} {p['name']}", key=f"sw_{k}", use_container_width=True):
                    st.session_state["profile"] = k
                    st.rerun()
        st.markdown("---")
        auto_ref = st.checkbox("⏱️ רענון כל 5 דקות")
        if st.button("🔄 רענן עכשיו", use_container_width=True):
            st.session_state["props"] = DEMO
            st.session_state["ts"] = datetime.now().strftime("%H:%M:%S")
            st.rerun()
        if RAPIDAPI_KEY:
            st.success("✅ API מחובר")
        else:
            st.warning("⚠️ מצב דמו")

    # Deal banner – show on entry
    all_p = st.session_state.get("props", DEMO)
    deals = [p for p in all_p if p.get("is_deal")]
    if deals and not st.session_state.get("dismissed_deal"):
        d = deals[0]
        usd_n = eur_to_usd(d["eur_n"])
        col_b, col_x = st.columns([10,1])
        with col_b:
            st.markdown(f"""
            <div class="deal-banner">
              <h3>🔥 מבצע חם בכניסה – {d['name']}</h3>
              <p>{d['deal_reason']}</p>
              <div style="margin-top:10px;display:flex;align-items:baseline;gap:14px;flex-wrap:wrap">
                <span class="deal-price">${usd_n}/לילה</span>
                <a href="{d['url']}" target="_blank" style="background:white;color:#c8420a;padding:8px 20px;border-radius:8px;text-decoration:none;font-weight:700">הזמן עכשיו →</a>
              </div>
            </div>
            """, unsafe_allow_html=True)
        with col_x:
            if st.button("✕", key="dismiss_deal"):
                st.session_state["dismissed_deal"] = True
                st.rerun()

    # Hero
    ts = st.session_state.get("ts","—")
    st.markdown(f"""
    <div class="hero">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px">
        <div>
          <h1>🏡 גארדה וילה</h1>
          <div class="hero-sub">חוף דרומי ומזרחי · 18–24 מאי · 7 מבוגרים + 2 פעוטות · עדכון: {ts}</div>
        </div>
        <div class="hero-badge">
          <div class="em">{prof['emoji']}</div>
          <div class="nm">{prof['name']}</div>
          <div style="font-size:0.72rem;color:rgba(255,255,255,0.55)">{prof['title']}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Filter
    filtered = []
    for p in all_p:
        usd_n = eur_to_usd(p["eur_n"])
        if p["rating"] < min_r:                             continue
        if usd_n > max_p:                                   continue
        if not p["free_cancel"]:                            continue
        if req_pool and "🏊 בריכה"          not in p["tags"]: continue
        if req_agri and "🌿 אגריטוריזמו"    not in p["tags"]: continue
        if req_lake and "🌊 נוף לאגם"       not in p["tags"]: continue
        if req_kids and "👶 ידידותי לילדים" not in p["tags"]: continue
        if req_cln  and "🧹 נקי מאוד"       not in p["tags"]: continue
        filtered.append(p)

    # Stats
    showing = len(filtered)
    avg_p   = int(sum(eur_to_usd(p["eur_n"]) for p in filtered)/showing) if showing else 0
    avg_r   = round(sum(p["rating"] for p in filtered)/showing,1) if showing else 0

    st.markdown(f"""
    <div class="stats-grid">
      <div class="stat-card"><div class="stat-num">{len(all_p)}</div><div class="stat-lbl">וילות נמצאו</div></div>
      <div class="stat-card"><div class="stat-num">{showing}</div><div class="stat-lbl">אחרי סינון</div></div>
      <div class="stat-card"><div class="stat-num">${avg_p}</div><div class="stat-lbl">ממוצע ללילה</div></div>
      <div class="stat-card"><div class="stat-num">{avg_r} ⭐</div><div class="stat-lbl">דירוג ממוצע</div></div>
    </div>
    """, unsafe_allow_html=True)

    sort_by = st.selectbox("מיון:", ["דירוג (גבוה→נמוך)","מחיר (נמוך→גבוה)","מחיר (גבוה→נמוך)","מבצעים קודם"], label_visibility="collapsed")
    if sort_by == "דירוג (גבוה→נמוך)":
        filtered.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "מחיר (נמוך→גבוה)":
        filtered.sort(key=lambda x: x["eur_n"])
    elif sort_by == "מחיר (גבוה→נמוך)":
        filtered.sort(key=lambda x: x["eur_n"], reverse=True)
    else:
        filtered.sort(key=lambda x: (not x.get("is_deal"), -x["rating"]))

    st.markdown("---")

    if not filtered:
        st.markdown('<div class="no-res">😔 לא נמצאו וילות – נסה להרחיב את הסינון</div>', unsafe_allow_html=True)
    else:
        cols = st.columns(2)
        for i, prop in enumerate(filtered):
            with cols[i % 2]:
                render_card(prop, focus)

    # Map
    if filtered:
        st.markdown("---")
        st.markdown("### 🗺️ מפת הוילות")
        import pandas as pd
        st.map(pd.DataFrame([{"lat":p["lat"],"lon":p["lon"]} for p in filtered]), zoom=10)

    # Itinerary
    st.markdown("---")
    st.markdown("### 📅 מסלול הטיול")
    cols2 = st.columns(3)
    for i, day in enumerate(ITINERARY):
        with cols2[i%3]:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:14px 16px;border:1px solid #e8e0d0;margin-bottom:12px">
              <div style="font-weight:700;font-size:0.85rem;color:#2d5a3d">{day['date']}</div>
              <div style="font-size:0.95rem;font-weight:700;margin:3px 0;color:#1a1a1a">{day['desc']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='text-align:center;color:#8a7a6a;font-size:0.78rem'>🌊 גארדה וילה · Streamlit + Booking.com API</div>", unsafe_allow_html=True)

    if auto_ref:
        time.sleep(300)
        st.rerun()

# ─── Entry ────────────────────────────────────────────────────────────────────
def main():
    if "profile" not in st.session_state:
        show_login()
    else:
        if "props" not in st.session_state:
            st.session_state["props"] = DEMO
            st.session_state["ts"] = datetime.now().strftime("%H:%M:%S")
        show_dashboard()

if __name__ == "__main__":
    main()
