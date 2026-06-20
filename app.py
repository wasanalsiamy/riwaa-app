import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="منظومة رِواء الرقمية", layout="wide", page_icon="🕋")

# --- CSS الاحترافي ---
st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; }
    [data-testid="stSidebar"] { background-color: #3E332A; }
    .kpi-card { background: white; padding: 20px; border-radius: 10px; border-top: 5px solid #8B7355; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- إدارة الحالة ---
if 'stations' not in st.session_state:
    st.session_state.stations = {
        "صحن المطاف": {"level": 95, "lat": 21.4225, "lon": 39.8262},
        "المسعى": {"level": 40, "lat": 21.4230, "lon": 39.8270},
        "التوسعة الثالثة": {"level": 12, "lat": 21.4240, "lon": 39.8255}
    }

# --- القائمة الجانبية ---
with st.sidebar:
    st.title("🕋 رِواء الرقمية")
    mode = st.radio("الوضع:", ["لوحة المشرف", "واجهة العامل", "التحليلات (AI)"])
    st.write("---")
    if st.button("🚀 تشغيل وضع المحاكاة (Demo)"):
        with st.spinner("جاري محاكاة ضغط الحشود..."):
            time.sleep(2)
            st.session_state.stations["صحن المطاف"]["level"] -= 20
            st.success("تم تحديث البيانات لحظياً!")

# --- لوحة المشرف ---
if mode == "لوحة المشرف":
    st.title("📊 لوحة تحكم المشرف")
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الحافظات", "1850", "مستقر")
    c2.metric("تحتاج تعبئة", "430", "عاجل", delta_color="inverse")
    c3.metric("نسبة الامتلاء", "76%", "-2%")

    st.subheader("📍 خريطة التغطية الميدانية")
    df = pd.DataFrame([{'name': k, **v} for k, v in st.session_state.stations.items()])
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", size="level", color="level", zoom=16)
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)

# --- واجهة العامل ---
elif mode == "واجهة العامل":
    st.title("🛠️ مهام العامل الميداني")
    task = st.checkbox("تعبئة الحافظة #152 - صحن المطاف")
    if task:
        st.success("تم إرسال بلاغ الإنجاز للمشرف ✅")
    st.checkbox("تعبئة الحافظة #84 - التوسعة الثالثة")

# --- التحليلات (AI Prediction) ---
else:
    st.title("🤖 التنبؤ الذكي بالطلب")
    data = pd.DataFrame({'الفترة': ['بعد العصر', 'بعد المغرب', 'بعد العشاء'], 'التنبؤ': [35, 60, 90]})
    fig = px.bar(data, x='الفترة', y='التنبؤ', color='التنبؤ', color_continuous_scale='OrRd')
    st.plotly_chart(fig, use_container_width=True)
    st.info("توصية الذكاء الاصطناعي: يرجى توجيه 15 عامل إضافي للتوسعة الثالثة قبل صلاة العشاء.")
