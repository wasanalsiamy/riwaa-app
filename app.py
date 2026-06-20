import streamlit as st
import pandas as pd
import plotly.express as px

# 1. بروتوكول الهوية الرقمية للمنصة
st.set_page_config(
    page_title="منظومة رِواء الرقمية - الهيئة العامة للعناية بشؤون المسجد الحرام", 
    page_icon="🕋", 
    layout="wide"
)

# 2. هندسة المظهر البصري لغرف التحكم (تباير عالي، خلفيات بيج مريحة، نصوص سوداء صريحة)
st.markdown("""
    <style>
    /* الخلفية العامة للمنصة */
    .stApp {
        background-color: #FDFBF7;
        color: #1A1A1A;
    }
    
    /* الهوية البصرية للقائمة الجانبية (بني خشبي داكن) */
    [data-testid="stSidebar"] {
        background-color: #3E332A;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* توحيد الخطوط والتباين اللوني */
    h1, h2, h3, h4, p, span, label {
        color: #1A1A1A !important;
        font-family: 'Arial', sans-serif;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    /* أزرار النظام التشغيلية الموحدة */
    .stButton>button {
        background-color: #3E332A;
        color: #FFFFFF !important;
        border-radius: 6px;
        border: none;
        padding: 10px 18px;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #8B7355;
        color: #FFFFFF !important;
    }
    
    /* بطاقات مؤشرات المراقبة اللحظية */
    .station-card {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: #FFFFFF !important;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 12px;
    }
    .station-green { background-color: #2E7D32; border-right: 6px solid #1B5E20; }
    .station-red { background-color: #C62828; border-right: 6px solid #B71C1C; }
    
    /* لوحات توجيه المسارات */
    .route-box {
        background-color: #FFFFFF;
        border-right: 6px solid #8B7355;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قائمة التبويب والخيارات الموحدة للمنصة
options = [
    "الرئيسية ودليل المنظومة",
    "لوحة المراقبة الجغرافية اللحظية",
    "نظام محاكاة المسارات الإرشادية",
    "مركز إدارة التعبئة والإرسال الميداني",
    "نظام معالجة الاستعلامات والتقارير"
]

# 4. إدارة الحالة والذاكرة المؤقتة لقواعد البيانات الافتراضية
if 'stations' not in st.session_state:
    st.session_state.stations = {
        "صحن المطاف والأروقة": {"المستوى": 95, "النوع": "حافظات نمطية معقمة", "الحشود": "مستقر", "lat": 21.4225, "lon": 39.8262},
        "المسعى بجميع أدواره": {"المستوى": 80, "النوع": "مشربيات رقمية مطورة", "الحشود": "متوسط الكثافة", "lat": 21.4230, "lon": 39.8270},
        "التوسعة السعودية الثالثة": {"المستوى": 12, "النوع": "حافظات نمطية معقمة", "الحشود": "ذروة حادة", "lat": 21.4240, "lon": 39.8255},
        "الساحات الخارجية والمنحدرات": {"المستوى": 65, "النوع": "عربات الإمداد الترددي", "الحشود": "مستقر", "lat": 21.4215, "lon": 39.8250}
    }

if 'active_page' not in st.session_state or st.session_state.active_page not in options:
    st.session_state.active_page = "الرئيسية ودليل المنظومة"

# 5. التوجيه والانتقال بين الواجهات
def set_page(page_name):
    st.session_state.active_page = page_name

# 6. البوابة الجانبية للتحكم المركزي
with st.sidebar:
    st.markdown("<h2 style='text-align: center; font-size: 22px; font-weight: bold;'>منظومة رِواء الرقمية</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 13px; opacity: 0.8;'>إدارة عمليات السقيا بالذكاء الاصطناعي</p>", unsafe_allow_html=True)
    st.write("---")
    
    sidebar_selection = st.radio(
        "نطاق العمليات:", 
        options, 
        index=options.index(st.session_state.active_page)
    )
    
    if sidebar_selection != st.session_state.active_page:
        st.session_state.active_page = sidebar_selection
        st.rerun()
        
    st.write("---")
    st.caption("بروتوكول إدارة البيانات والمخزون المائي")

# زاوية الملاحة السريعة - زر العودة للرئيسية
def render_home_button():
    if st.session_state.active_page != "الرئيسية ودليل المنظومة":
        st.write("---")
        if st.button("العودة إلى واجهة الاستقبال الرئيسية"):
            st.session_state.active_page = "الرئيسية ودليل المنظومة"
            st.rerun()

# --- الشاشة الأولى: الرئيسية ودليل المنظومة ---
if st.session_state.active_page == "الرئيسية ودليل المنظومة":
    st.title("منصة رِواء الرقمية")
    st.markdown("##### النظام الوطني الموحد لإدارة ومراقبة كفاية الإمداد المائي بالحرم المكي الشريف")
    st.write("---")
    
    st.subheader("الغرض التشغيلي للمنصة")
    st.write("""
    تعمل منصة **رِواء** كلوحة تحكم ذكية تهدف إلى أتمتة حوكمة خدمات السقيا ومراقبة مستويات مياه زمزم بشكل استباقي. 
    يرتبط النظام بخوارزميات تقرأ كثافة التدفق البشري، جداول الصلوات، والمحددات البيئية للتنبؤ باحتماليات نفاد المخزون المائي في أي نطاق قبل حدوثه بـ 20 دقيقة، مما يتيح إسناد وإمداد المواقع آلياً دون تداخل بشري أو تأخير في الخدمة.
    """)
    
    st.write("---")
    st.subheader("مسار مراجعة وتقييم المنظومة")
    st.markdown("""
    تتوزع وظائف النظام في القائمة الجانبية وفق الدورة التشغيلية الفنية التالية:
    * **لوحة المراقبة الجغرافية اللحظية:** رصد مستويات كفاية المياه الفورية ونماذج التنبؤ بالطلب.
    * **نظام محاكاة المسارات الإرشادية:** رسم خريطة النطاقات الممتلئة وتوجيه الحشود للموقع الأقرب والأفضل.
    * **مركز إدارة التعبئة والإرسال الميداني:** تفعيل بروتوكول التدخل السريع ومحاكاة الاستجابة الميدانية.
    * **نظام معالجة الاستعلامات والتقارير:** بوابة استخراج الإحصاءات الفورية والتحليل التشغيلي للمشرفين.
    """)

# --- الشاشة الثانية: لوحة المراقبة الجغرافية اللحظية ---
elif st.session_state.active_page == "لوحة المراقبة الجغرافية اللحظية":
    st.title("لوحة المراقبة الجغرافية اللحظية لمخزون مياه زمزم")
    st.write("---")
    
    st.subheader("مؤشرات الطاقة الاستيعابية والامتلاء الحالية")
    cols = st.columns(4)
    for i, (name, info) in enumerate(st.session_state.stations.items()):
        level = info["المستوى"]
        color_class = "station-green" if level > 20 else "station-red"
        status_text = "كفاية تامة" if level > 20 else "إنذار عجز تشغيلي وشيك"
        
        with cols[i]:
            st.markdown(f"""
                <div class="station-card {color_class}">
                    <div style="font-size: 16px; margin-bottom: 8px; color: #FFFFFF !important;">{name}</div>
                    <div style="font-size: 34px; font-weight: bold; color: #FFFFFF !important;">{level}%</div>
                    <div style="font-size: 12px; opacity: 0.9; color: #FFFFFF !important; font-weight: normal;">{status_text}</div>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("عرض تقرير الكثافة", key=f"det_{i}"):
                st.info(f"النمط الفني: {info['النوع']} | مستوى الحشود في النطاق: {info['الحشود']}")

    st.write("---")
    col_graph, col_summary = st.columns([2, 1])
    with col_graph:
        st.subheader("المنحنى التنبؤي لحجم الطلب المتوقع (خلال الـ 60 دقيقة القادمة)")
        df_chart = pd.DataFrame({'الفترة الزمنية': ['أذان', 'الإقامة', 'الصلوات', 'خروج التدفقات'], 'معدل الطلب (%)': [35, 55, 95, 70]})
        fig = px.area(df_chart, x='الفترة الزمنية', y='معدل الطلب (%)')
        fig.update_traces(line_color='#8B7355', fillcolor='rgba(139, 115, 85, 0.12)')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
    with col_summary:
        st.subheader("المحددات التشغيلية الحيوية")
        st.markdown("""
        * رصد كثافة الحشود اللحظية عبر الكاميرات الرقمية.
        * ربط جدول التوقيت التلقائي لمواعيد الصلوات.
        * تتبع قراءات المستشعرات البيئية والحرارية.
        * مطابقة الأنماط التاريخية لمعدلات الاستهلاك اليومية.
        """)
    render_home_button()

# --- الشاشة الثالثة: نظام محاكاة المسارات الإرشادية ---
elif st.session_state.active_page == "نظام محاكاة المسارات الإرشادية":
    st.title("نظام التوجيه والملاحة الإرشادية للزوار")
    st.write("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("نمط السقيا المطلوب رصده:", ["كافة النطاقات المتاحة والممتلئة", "الحافظات النمطية الثابتة", "المشربيات الرقمية المحدثة"])
    with c2:
        st.selectbox("نقطة قياس التدفق والوصول الحالية:", ["بوابة الملك عبدالعزيز", "بوابة الملك فهد", "بوابة الفتح"])
        
    if st.button("توليد مسار الملاحة الرقمي الموصى به"):
        st.success("تمت المعالجة الجغرافية للموقع بنجاح. تم تحديد أقصر مسار متاح متصل بنقاط الوفرة المائية.")
        
        # عرض الملاحة الجغرافية لنقاط الحرم
        map_data = [{"النطاق الجغرافي": k, "lat": v["lat"], "lon": v["lon"], "المخزون": v["المستوى"]*4} for k, v in st.session_state.stations.items()]
        st.map(pd.DataFrame(map_data), latitude="lat", longitude="lon", size="المخزون", zoom=16)
        
        st.markdown("""
        <div class="route-box">
            <h4 style="color: #3E332A !important;">توصية مسار انسيابية الحركة البشري:</h4>
            <p>يوصى بتوجيه الكتل البشرية عبر <b>الممر المحوري رقم 3</b> المؤدي إلى <b>صحن المطاف والأروقة</b> (معدل كفاية مخزون المياه: <b>95%</b>، حالة التكدس: <b>مستقر</b>).</p>
            <p style="font-size: 13px; color: #555555 !important;">* يقوم النظام تلقائياً بحجب وحذف النقاط المتدنية أو الخاضعة لإعادة التعبئة لتأمين انسيابية الحركة البصرية والميدانية.</p>
        </div>
        """, unsafe_allow_html=True)
    render_home_button()

# --- الشاشة الرابعة: مركز إدارة التعبئة والإرسال الميداني ---
elif st.session_state.active_page == "مركز إدارة التعبئة والإرسال الميداني":
    st.title("لوحة قيادة وتحريك الكوادر التشغيلية")
    st.write("---")
    st.error("إنذار تنبؤي: يرجى اتخاذ الإجراء الاستباقي قبل نفاد المخزون المائي في التوسعة السعودية الثالثة (المتبقي الحالي 12%).")
    
    if st.button("اعتماد أمر الإسناد وتنبيه الفرق الميدانية"):
        st.success("تم تفعيل إرسال أمر التزويد الرقمي للأجهزة المحمولة الخاصة بالفرقة الميدانية المكلفة جغرافياً بالنطاق.")
        
    if st.button("محاكاة اكتمال الإمداد الميداني"):
        st.session_state.stations["التوسعة السعودية الثالثة"]["المستوى"] = 100
        st.session_state.stations["التوسعة السعودية الثالثة"]["الحشود"] = "مستقر"
        st.success("تم تحديث البيانات الرقمية بنجاح. عاد مؤشر الطاقة الاستيعابية في التوسعة السعودية الثالثة إلى وضع الأمان الكلي بنسبة 100%.")
    render_home_button()

# --- الشاشة الخامسة: نظام معالجة الاستعلامات والتقارير ---
elif st.session_state.active_page == "نظام معالجة الاستعلامات والتقارير":
    st.title("نظام الاستعلام التشغيلي والتحليلي")
    st.write("---")
    user_query = st.text_input("إدخال الاستفسار الإداري المباشر للرصد والتحليل:", value="ما هي النطاقات الجغرافية المتوقع تسجيل أعلى استهلاك فيها خلال الساعة القادمة؟")
    
    if st.button("تحليل ومعالجة التقرير"):
        st.markdown("<div style='background-color: #3E332A; padding: 15px; border-radius: 6px; color: #FFFFFF;'><strong>التوجيه التحليلي الصادر عن النظام:</strong> تشير النمذجة التنبؤية لحساب الحشود الحالية إلى توقع ارتفاع الطلب المائي بنسبة 45% في نطاق صحن المطاف فور الانتهاء من أداء الصلاة مباشرة، يوصى بجدولة عربات الدعم الترددي مسبقاً.</div>", unsafe_allow_html=True)
        
    st.write("---")
    st.subheader("مؤشرات الأداء الاستراتيجية")
    c1, c2, c3 = st.columns(3)
    c1.metric("معدل استمرارية وفرة الخدمة", "99.9%", "مستهدف مستدام")
    c2.metric("تقليل زمن الاستجابة للمهمات", "40%-", "تحسين كفاءة التشغيل")
    c3.metric("خفض نسب هدر الموارد المائية", "15%-", "استدامة الموارد")
    render_home_button()
