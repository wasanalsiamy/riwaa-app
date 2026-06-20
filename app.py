import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الهوية الرسمية
st.set_page_config(page_title="منظومة رِواء الوطنية", page_icon="🕋", layout="wide")

# 2. هندسة المظهر البصري (بيج رخامي وبني خشبي)
st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; color: #1A1A1A; }
    [data-testid="stSidebar"] { background-color: #3E332A; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    h1, h2, h3, h4, p, span, label { color: #1A1A1A !important; font-family: 'Arial', sans-serif; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label { color: #FFFFFF !important; }
    .stMetric { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border-right: 6px solid #8B7355; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }
    .stButton>button { background-color: #3E332A; color: #FFFFFF !important; border-radius: 6px; padding: 12px 30px; font-weight: bold; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #8B7355; }
    
    /* تنسيق الحافظات (علب زمزم) */
    .container-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white !important;
        font-weight: bold;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .status-green { background-color: #2E7D32; } /* أخضر: متوفر */
    .status-red { background-color: #C62828; }   /* أحمر: إنذار بنفاد المياه */
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات
if 'water_levels' not in st.session_state:
    st.session_state.water_levels = {"أروقة المطاف": 85, "المسعى الأرضي": 45, "توسعة الملك فهد": 12, "الساحات الخارجية": 70}
if 'active_tasks' not in st.session_state:
    st.session_state.active_tasks = []

# 4. القائمة الجانبية
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 28px; font-weight: bold;'>منظومة رِواء</h1>", unsafe_allow_html=True)
    st.write("---")
    page = st.radio("أقسام المنصة:", ["التعريف بالمنظومة", "مركز العمليات والتنبؤ اللحظي", "نظام دعم القرار والتوجيه", "تطبيق الكوادر الميدانية", "مؤشرات الأثر 2030"])
    st.write("---")
    st.caption("هاكاثون جادة 30 - مكة المكرمة")

# --- 1. التعريف بالمنظومة ---
if page == "التعريف بالمنظومة":
    st.title("منظومة رِواء الرقمية")
    st.markdown("#### الحل الوطني الذكي لأتمتة ورفع كفاءة عمليات السقيا داخل الحرم المكي الشريف")
    st.write("---")
    st.subheader("رؤية المنصة")
    st.write("""
    منصة **رِواء** تهدف إلى إلغاء العمليات اليدوية في مراقبة مستويات مياه زمزم. من خلال تحليل 8 عوامل حيوية تشمل كثافة الحشود ودرجات الحرارة، يتنبأ النظام بحاجة كل نقطة توزيع للمياه قبل نفادها، مما يمنع التكدس البشري ويضمن استمرارية الخدمة لضيوف الرحمن.
    """)
    st.info("فلسفة رِواء: التواجد المسبق في المكان الصحيح قبل طلب الخدمة.")

# --- 2. مركز العمليات والتنبؤ اللحظي ---
elif page == "مركز العمليات والتنبؤ اللحظي":
    st.title("لوحة تحكم مركز العمليات")
    st.write("متابعة حية لحالة نقاط التوزيع (الحافظات والمشربيات) في كافة أروقة الحرم.")
    st.write("---")
    
    st.subheader("التمثيل البصري لحالة نقاط التوزيع (الحافظات)")
    cols = st.columns(4)
    locations = list(st.session_state.water_levels.keys())
    for i, loc in enumerate(locations):
        level = st.session_state.water_levels[loc]
        color_class = "status-green" if level > 20 else "status-red"
        status_text = "متوفر" if level > 20 else "إنذار: نفاد وشيك"
        
        with cols[i]:
            st.markdown(f"""
                <div class="container-box {color_class}">
                    <div style="font-size: 40px;">🕋</div>
                    <div style="font-size: 18px; margin-top:10px;">{loc}</div>
                    <div style="font-size: 24px; margin: 10px 0;">{level}%</div>
                    <div style="font-size: 14px; opacity: 0.9;">الحالة: {status_text}</div>
                </div>
                """, unsafe_allow_html=True)
            if level <= 20:
                st.warning(f"تنبيه: يتوقع نفاد المياه في {loc} خلال 12 دقيقة")

    st.write("---")
    st.subheader("منحنى التنبؤ الاستباقي بالطلب")
    df_chart = pd.DataFrame({'الوقت': ['10م', '11م', '12ص', '1ص'], 'الطلب المتوقع': [30, 45, 95, 60]})
    fig = px.area(df_chart, x='الوقت', y='الطلب المتوقع')
    fig.update_traces(line_color='#8B7355', fillcolor='rgba(139, 115, 85, 0.2)')
    st.plotly_chart(fig, use_container_width=True)

# --- 3. نظام دعم القرار والتوجيه ---
elif page == "نظام دعم القرار والتوجيه":
    st.title("نظام دعم القرار والتوجيه")
    st.write("تحويل التوقعات إلى مهمات ميدانية فورية.")
    st.write("---")
    
    if st.session_state.water_levels["توسعة الملك فهد"] <= 20:
        st.error("🚨 إشعار استباقي: تم رصد انخفاض حاد في 'توسعة الملك فهد'")
        st.info("**التوجيه الذكي:** يُنصح بتوجيه عربة التعبئة رقم 4 عبر ممر الملك فهد الجانبي (المسار الأقل زحاماً حالياً).")
        if st.button("اعتماد التوجيه وإرسال المهمة"):
            if "مهمة التوسعة" not in st.session_state.active_tasks:
                st.session_state.active_tasks.append("مهمة التوسعة")
                st.success("تم إرسال المهمة لجهاز الكادر الميداني بنجاح.")

# --- 4. تطبيق الكوادر الميدانية ---
elif page == "تطبيق الكوادر الميدانية":
    st.title("واجهة الكوادر الميدانية")
    if not st.session_state.active_tasks:
        st.info("لا توجد مهمات معلقة. جميع الحافظات في نطاق العمل خضراء (متوفرة).")
    else:
        for task in st.session_state.active_tasks:
            st.warning("⚠️ مهمة عمل: إعادة تعبئة حافظات 'توسعة الملك فهد'")
            if st.button("تأكيد إتمام المهمة ✅"):
                st.session_state.water_levels["توسعة الملك فهد"] = 100
                st.session_state.active_tasks.remove(task)
                st.success("تم تحديث الحالة. ستظهر الحافظة الآن باللون الأخضر في مركز العمليات.")
                st.rerun()

# --- 5. مؤشرات الأثر 2030 ---
elif page == "مؤشرات الأثر 2030":
    st.title("الأثر والاستدامة")
    c1, c2, c3 = st.columns(3)
    c1.metric("استمرارية الخدمة", "99.9%")
    c2.metric("خفْض زمن الاستجابة", "40%-")
    c3.metric("منع التكدس البشري", "تحسن ملحوظ")
    st.write("---")
    st.subheader("الارتباط برؤية 2030")
    st.write("- تحسين تجربة ضيوف الرحمن عبر التحول الرقمي.\n- الاستدامة المائية وإدارة الموارد بذكاء.\n- رفع كفاءة التشغيل في الحرم المكي.")
