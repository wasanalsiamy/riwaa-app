import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="منظومة رِواء - التحكم الذكي", layout="wide", page_icon="🕋")

# --- تحسينات بصرية (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    /* كارت الحافظة */
    .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-top: 5px solid #ccc; transition: 0.3s; }
    .card-good { border-top-color: #2E7D32; }
    .card-bad { border-top-color: #C62828; }
    /* ستايل الملاحة */
    .route-step { background: #fff; padding: 15px; border-radius: 10px; border-right: 5px solid #8B7355; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# --- البيانات ---
if 'stations' not in st.session_state:
    st.session_state.stations = {
        "صحن المطاف": {"المستوى": 95, "الزحام": "منخفض", "lat": 21.4225, "lon": 39.8262},
        "المسعى": {"المستوى": 20, "الزحام": "عالي", "lat": 21.4230, "lon": 39.8270},
        "التوسعة الثالثة": {"المستوى": 12, "الزحام": "عالي جداً", "lat": 21.4240, "lon": 39.8255},
        "الساحات الخارجية": {"المستوى": 65, "الزحام": "مستقر", "lat": 21.4215, "lon": 39.8250}
    }

# --- القائمة الجانبية ---
with st.sidebar:
    st.title("🕋 رِواء الرقمية")
    page = st.radio("القائمة:", ["مراقبة الحافظات", "خريطة الملاحة والمسارات"])

# --- الصفحة 1: مراقبة الحافظات ---
if page == "مراقبة الحافظات":
    st.title("📦 لوحة مراقبة حافظات زمزم")
    st.write("عرض الحالة الفورية للحافظات في الحرم")
    
    cols = st.columns(4)
    for i, (name, info) in enumerate(st.session_state.stations.items()):
        status = "card-good" if info['المستوى'] > 30 else "card-bad"
        with cols[i % 4]:
            st.markdown(f"""
                <div class="card {status}">
                    <h3>{name}</h3>
                    <p style="font-size: 24px;">💧 {info['المستوى']}%</p>
                    <p><b>الزحام:</b> {info['الزحام']}</p>
                </div>
            """, unsafe_allow_html=True)

# --- الصفحة 2: الخريطة (Google Maps Style) ---
else:
    st.title("📍 نظام الملاحة الذكي")
    st.write("اختر الحافظة وسيقوم النظام بتوليد أفضل مسار للوصول إليها")
    
    selected = st.selectbox("حدد وجهتك:", list(st.session_state.stations.keys()))
    
    # تحضير بيانات الخريطة
    data = pd.DataFrame([
        {'name': name, 'lat': info['lat'], 'lon': info['lon'], 'status': info['المستوى']} 
        for name, info in st.session_state.stations.items()
    ])
    
    # الخريطة التفاعلية
    st.map(data, latitude='lat', longitude='lon', size=300)
    
    if st.button("🚀 ابدأ التوجيه الآن"):
        st.success(f"تم تفعيل المسار إلى: {selected}")
        
        # محاكاة خطوات جوجل ماب
        st.markdown(f"""
            <div class="route-step">
                <h4>🚶‍♂️ المسار المقترح:</h4>
                <p>1. ابدأ التحرك من موقعك الحالي تجاه <b>نقطة التجمع {selected}</b>.</p>
                <p>2. تجنب المسار المزدحم (المسعى) وخذ المسار الجانبي (التوسعة).</p>
                <p>3. الوقت المتوقع للوصول: <b>4 دقائق</b>.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # مؤشر بصري للزحام
        st.write("حالة الزحام على الطريق:")
        st.progress(70) # محاكاة لنسبة الزحام
