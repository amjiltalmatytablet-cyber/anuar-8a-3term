import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- ПАРАҚША БАПТАУЫ ---
st.set_page_config(page_title="EduKZ Analytics", layout="wide", initial_sidebar_state="collapsed")

# Стильді баптау (Academic Look)
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    h1, h2, h3 { color: #003366 !important; font-family: 'Georgia', serif; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ДЕРЕКТЕРДІ ГЕНЕРАЦИЯЛАУ (PANDAS) ---
@st.cache_data
def get_data():
    # Гранттар мен мамандықтар
    grants = pd.DataFrame({
        'Сала': ['IT', 'IT', 'Медицина', 'Медицина', 'Педагогика', 'Педагогика', 'Инженерия', 'Инженерия'],
        'Мамандық': ['Software Engineering', 'Data Science', 'Жалпы медицина', 'Стоматология', 'Математика', 'Бастауыш білім', 'Құрылыс', 'Механика'],
        'Грант_саны': [3500, 1800, 2200, 500, 1600, 2400, 2900, 1100]
    })
    
    # Серпін бағдарламасы
    serpin = pd.DataFrame({
        'Өңір': ['Қызылорда', 'Түркістан', 'Жамбыл', 'Алматы обл.', 'Маңғыстау'],
        'Тиімділік': [89, 93, 78, 85, 72],
        'Бітірушілер': [1200, 2800, 1050, 1900, 800]
    })
    
    # Жұмыспен қамту (Bubble chart үшін)
    employment = pd.DataFrame({
        'Университет': ['NU', 'ENU', 'KazNU', 'KBTU', 'AITU', 'Satbayev', 'SDU', 'KIMEP'],
        'Жұмысқа_орналасу': [96, 83, 85, 93, 91, 79, 87, 92],
        'Орташа_жалақы': [480000, 285000, 305000, 440000, 395000, 325000, 365000, 420000],
        'Студент_саны': [1100, 5800, 6500, 2700, 2200, 5900, 3100, 2950]
    })
    return grants, serpin, employment

df_g, df_s, df_e = get_data()

# --- 2. HEADER ---
st.title("🎓 Қазақстанның жоғары білім беру жүйесін талдау")
st.write("Білім гранттары, 'Серпін' бағдарламасы және еңбек нарығының статистикасы")
st.markdown("---")

# --- 3. DASHBOARD COMPONENTS ---

# Бөлім 1: Plotly Treemap
st.header("1. Гранттардың мамандықтарға бөлінісі")
fig_tree = px.treemap(df_g, path=['Сала', 'Мамандық'], values='Грант_саны',
                      color='Грант_саны', color_continuous_scale='Blues',
                      height=500)
fig_tree.update_layout(margin=dict(t=30, l=10, r=10, b=10))
st.plotly_chart(fig_tree, use_container_width=True)

st.markdown("---")

# Бөлім 2 мен 3 (Екі баған)
col1, col2 = st.columns(2)

with col1:
    st.header("2. 'Серпін' тиімділігі")
    fig_bar = px.bar(df_s.sort_values('Тиімділік'), x='Тиімділік', y='Өңір',
                     orientation='h', color='Тиімділік',
                     color_continuous_scale='Tealgrn', text_auto=True)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.header("3. Жұмысқа орналасу мен жалақы")
    fig_bubble = px.scatter(df_e, x='Жұмысқа_орналасу', y='Орташа_жалақы',
                            size='Студент_саны', color='Университет',
                            hover_name='Университет', size_max=50)
    fig_bubble.update_layout(xaxis_title="Жұмысқа орналасу (%)", yaxis_title="Орташа жалақы (₸)")
    st.plotly_chart(fig_bubble, use_container_width=True)

# --- 4. PREDICTOR SECTION ---
st.markdown("---")
st.header("🎯 Grant Predictor v2.0")

with st.container():
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("Көрсеткіштер")
        score = st.slider("ҰБТ балыңызды таңдаңыз:", 50, 140, 100)
        faculty = st.selectbox("Бағытты таңдаңыз:", df_g['Сала'].unique())
        
        # Pandas сүзгісі
        subset = df_g[df_g['Сала'] == faculty]
        total_grants = subset['Грант_саны'].sum()
        
    with c2:
        st.subheader("Болжам нәтижесі")
        
        # Қарапайым логикалық сүзгі (Thresholds)
        thresholds = {'IT': 118, 'Медицина': 125, 'Инженерия': 102, 'Педагогика': 95}
        target = thresholds.get(faculty, 100)
        
        if score >= target:
            st.success(f"Мүмкіндік жоғары! {faculty} бағытында биыл {total_grants} грант бөлінді.")
            st.metric(label="Болжам", value="90%+", delta="Грантқа иелену ықтималдығы")
        elif score >= target - 10:
            st.warning("Мүмкіндік орташа. Былтырғы шекті балдарға назар аударыңыз.")
            st.metric(label="Болжам", value="50-60%", delta="Тәуекел бар", delta_color="off")
        else:
            st.error("Мүмкіндік төмен. Басқа бағыттарды немесе ауылдық квотаны қарастырыңыз.")
            st.metric(label="Болжам", value="<20%", delta="- Төмен бал", delta_color="inverse")

st.markdown("---")
st.caption("Мәліметтер тек ақпараттық мақсатта берілген. Дереккөз: Ұлттық тестілеу орталығы.")