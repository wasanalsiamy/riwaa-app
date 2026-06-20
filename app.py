import streamlit as st
import pandas as pd
import numpy as np

# إعداد الصفحة
st.set_page_config(page_title="منصة رِواء الرقمية", layout="wide", page_icon="💧")

# --- تنسيق CSS لجعل الموقع يبدو كأنه تطبيق جوال/ويب احترافي ---
st.markdown("""
    <style>
    .card { background: #ffffff; padding: 20px; border-radius: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin: 10px; border-top: 5px solid #2e7d32; }
    .card-crowded { border-top-color: #c62828; }
    .water-icon { font-size: 40px; }
    .nav-instruction { background: #e8f5e9; padding: 15px; border-radius: 10px; border-right: 5px solid #2e7d32; }
    </style>
""", unsafe_allow_html=True)

# تهيئة بيانات الحافظات (المحاكاة)
if 'locations' not in st.session_state:
    st.session_state.locations = pd.DataFrame({
        'name': ['صحن المطاف', 'المسعى - الدور 1', 'التوسعة الثالثة', 'بوابة الملك عبدالعزيز', 'ساحة التوسعة'],
        'lat': [21.4225, 21.4230, 21.4245, 21.4210, 21.4235],
        'lon': [39.8262, 39.8270, 39.8255, 39.8250, 39.8265],
        'water_level': [85, 15, 60, 95, 45], # مستوى الماء
        'crowd_level': [30, 95, 50, 20, 80]  # مستوى الزحام
    })

# --- القائمة الجانبية ---
menu = st.sidebar.radio("القائمة الرئيسية", ["📦 لوحة الحافظات الحية", "📍 الملاحة الذكية (Google Maps)"])

# --- الصفحة الأولى: لوحة الحافظات (Visual Stations) ---
if menu == "📦 لوحة الحافظات الحية":
    st.title("🕋 رِواء - مراقبة الحافظات")
    st.write("عرض لحظي لحالة حافظات زمزم الموزعة")

    cols = st.columns(3)
    for i, row in st.session_state.locations.iterrows():
        is_crowded = row['crowd_level'] > 70 or row['water_level'] < 30
        card_class = "card card-crowded" if is_crowded else "card"
        
        with cols[i % 3]:
            st.markdown(f"""
                <div class="{card_class}">
                    <div class="water-icon">💧</div>
                    <h3>{row['name']}</h3>
                    <p><b>مستوى الماء:</b> {row['water_level']}%</p>
                    <p><b>حالة الزحام:</b> {'🚨 مزدحم' if is_crowded else '✅ متاح'}</p>
                </div>
            """, unsafe_allow_html=True)

# --- الصفحة الثانية: الملاحة الذكية (The "Google Maps" Feature) ---
else:
    st.title("📍 الملاحة الذكية إلى أقرب حافظة")
    
    # اختيار الموقع
    target = st.selectbox("إلى أين تود التوجه؟", st.session_state.locations['name'])
    selected_data = st.session_state.locations[st.session_state.locations['name'] == target].iloc[0]
    
    # الخريطة
    st.map(pd.DataFrame({'lat': [selected_data['lat']], 'lon': [selected_data['lon']]}))
    
    # محاكاة الطريق
    if st.button("بدء التوجيه الصوتي والمسار"):
        st.markdown(f"""
            <div class="nav-instruction">
                <h4>🚀 المسار إلى {target}</h4>
                <ul>
                    <li>1. اتجه شمالاً نحو المسار الرئيسي.</li>
                    <li>2. تجاوز المنطقة {np.random.choice(['A', 'B', 'C'])} (الطريق سالك).</li>
                    <li>3. ستصل إلى الحافظة خلال 3 دقائق مشياً.</li>
                    <li>4. مستوى الماء في الحافظة المستهدفة: {selected_data['water_level']}%</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.success("تم تشغيل التوجيه الصوتي.. تابع المسار على الخريطة.")
