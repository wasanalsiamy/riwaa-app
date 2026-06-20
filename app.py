import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعداد بروتوكول الهوية الرقمية للمنصة
st.set_page_config(page_title="منظومة رِواء الرقمية - الهيئة العامة للعناية بشؤون المسجد الحرام", page_icon="🕋", layout="wide")

# 2. هندسة المظهر البصري والسياسة الجمالية للمنصة (البيج الرخامي الملكي والبني النبوي الخشبي)
st.markdown("""
    <style>
    /* خلفية رخامية مريحة ومقاومة للتشتت البصري */
    .stApp {
        background-color: #FDFBF7;
        color: #1A1A1A;
    }
    
    /* الهوية البصرية للبوابة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #3E332A;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* ضبط معايير الخطوط والتباين العالي للنصوص الصريحة */
    h1, h2, h3, h4, p, span, label {
        color: #1A1A1A !important;
        font-family: 'Arial', sans-serif;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    /* أزرار الإجراءات التنفيذية والاعتماد والعودة للرئيسية */
    .stButton>button {
        background-color: #3E332A;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
        padding: 12px 20px;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #8B7355;
        color: #FFFFFF !important;
    }
    
    /* زر العودة المخصص باللون البني الفاتح لتميزه بلمسة جمالية */
    .home-btn>button {
        background-color: #8B7355 !important;
    }
    .home-btn>button:hover {
        background-color: #3E332A !important;
    }
    
    /* بطاقات المراقبة الجغرافية لنقاط السقيا */
    .station-card {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: #FFFFFF !important;
        font-weight: bold;
        box-shadow: 0 6px 15px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }
    .station-green { background-color: #2E7D32; border-right: 8px solid #1B5E20; } /* كفاية الإمداد */
    .station-red { background-color: #C62828; border-right: 8px solid #B71C1C; }   /* عجز تشغيلي وشيك */
    
    /* بطاقة النظام للمسارات التوجيهية */
    .route-box {
        background-color: #FFFFFF;
        border-right: 8px solid #8B7355;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. طبقة إدارة البيانات الجغرافية والتشغيلية الموحدة لخرائط الحرم
if 'stations' not in st.session_state:
    st.session_state.stations = {
        "صحن المطاف والأروقة المحيطة": {"المستوى": 95, "النوع": "حافظات نمطية معقمة", "الحشود": "آمن / مستقر", "lat": 21.4225, "lon": 39.8262},
        "المسعى بجميع أدواره": {"المستوى": 80, "النوع": "مشربيات رقمية مطورة", "الحشود": "متوسط الكثافة", "lat": 21.4230, "lon": 39.8270},
        "التوسعة السعودية الثالثة": {"المستوى": 12, "النوع": "حافظات نمطية معقمة", "الحشود": "ذروة تشغيلية حادة", "lat": 21.4240, "lon": 39.8255},
        "الساحات والمنحدرات الخارجية": {"المستوى": 65, "النوع": "عربات الإمداد الترددي", "الحشود": "آمن / مستقر", "lat": 21.4215, "lon": 39.8250}
    }
if 'active_page' not in st.session_state:
    st.session_state.active_page = "🏠 الرئيسية ودليل الاستخدام"

# 4. إدارة التنقل وحفظ الصفحة النشطة
def set_page(page_name):
    st.session_state.active_page = page_name

# 5. بوابة التحكم (القائمة الجانبية الإدارية المبسطة)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 26px; font-weight: bold;'>منظومة رِواء الرقمية</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 13px; opacity: 0.8;'>النظام الموحد لدعم القرار التنبؤي بسقيا زمزم</p>", unsafe_allow_html=True)
    st.write("---")
    
    # أسماء الصفحات بعد تبسيطها تماماً لتسهيل الفهم والملاحة
    options = [
        "🏠 الرئيسية ودليل الاستخدام",
        "📊 خريطة الحافظات الحية",
        "🗺️ محاكي مسار المعتمرين",
        "⚡ إرسال مهمة تعبئة ميدانية",
        "💬 اسأل النظام الذكي"
    ]
    
    sidebar_selection = st.radio(
        "اختر الشاشة المطلوبة:", 
        options, 
        index=options.index(st.session_state.active_page)
    )
    
    if sidebar_selection != st.session_state.active_page:
        st.session_state.active_page = sidebar_selection
        st.rerun()
        
    st.write("---")
    st.caption("هاكاثون جادة 30 - مكة المكرمة")

# ميزة زر العودة الموحد إلى الصفحة الرئيسية
def render_home_button():
    if st.session_state.active_page != "🏠 الرئيسية ودليل الاستخدام":
        st.write("---")
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🔙 العودة للشاشة الرئيسية"):
            set_page("🏠 الرئيسية ودليل الاستخدام")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- الشاشة الأولى: الرئيسية ودليل الاستخدام ---
if st.session_state.active_page == "🏠 الرئيسية ودليل الاستخدام":
    st.title("مرحباً بكم في منصة رِواء الرقمية")
    st.markdown("#### الحل الوطني الأتمت الذكي لإدارة عمليات سقيا زمزم بالمسجد الحرام")
    st.write("---")
    
    # شرح مبسط جداً للمنصة وفكرتها الأساسية
    st.subheader("💡 عن المنصة وفكرتها الأساسية")
    st.write("""
    منصة **رِواء** هي منظومة استباقية تلغي تماماً الطريقة اليدوية في مراقبة مستويات مياه زمزم داخل الحرم.
    عبر قراءة **8 محددات حيوية** (مثل كثافة الحشود من الكاميرات، ودرجات الحرارة، ومواعيد الصلوات)، يستطيع النظام **التنبؤ** بوقوع أي عجز أو نفاد للمياه قبل حدوثه بـ 20 دقيقة، مما يسمح للفرق الميدانية بالتحرك وإعادة التعبئة فوراً لمنع الازدحام والحفاظ على انسيابية حركة المعتمرين.
    """)
    
    st.write("---")
    
    # دليل الاستخدام المكتمل لشرح كيفية عمل المحاكاة أمام المحكمين
    st.subheader("📖 دليل الاستخدام السريع (كيف تستعرض المنصة أمام المحكمين؟)")
    
    st.markdown("""
    لتقديم عرض مبهر وخالٍ من التعقيد، تتبع الخطوات التالية عبر القائمة الجانبية:
    1. **الخطوة الأولى:** افتح صفحة **[📊 خريطة الحافظات الحية]** لتشاهد كيف تظهر المواقع باللون الأخضر (آمن) والتوسعة السعودية الثالثة باللون الأحمر (12% عجز وشيك) لإعطاء إنذار بصري فوري.
    2. **الخطوة الثانية:** انتقل إلى صفحة **[🗺️ محاكي مسار المعتمرين]** واضغط زر توليد المسار، لتلاحظ كيف يقوم النظام تلقائياً برسم مسار آمن للمعتمر وإبعاده عن المنطقة الحمراء المزدحمة وتوجيهه لأقرب مكان ممتلئ.
    3. **الخطوة الثالثة:** اذهب إلى صفحة **[⚡ إرسال مهمة تعبئة ميدانية]** واضغط على زر التعبئة الافتراضي، لترى كيف تكتمل المهمة ويعود المؤشر في الخريطة الرئيسية إلى 100% (أخضر آمن) تلقائياً!
    4. **الخطوة الرابعة:** استخدم شاشة **[💬 اسأل النظام الذكي]** لتوليد تقارير سريعة وفورية تناسب رؤساء الفترات والمشرفين.
    """)
    
    st.info("💡 يمكنك دائماً الضغط على زر 'العودة للشاشة الرئيسية' الموجود أسفل كل صفحة للتنقل السريع ومتابعة الشرح.")

# --- الشاشة الثانية: خريطة الحافظات الحية ---
elif st.session_state.active_page == "📊 خريطة الحافظات الحية":
    st.title("لوحة المراقبة الجغرافية اللحظية لمخزون مياه زمزم")
    st.write("المتابعة الحية لمستويات كفاية الإمداد المائي في نقاط التوزيع الاستراتيجية بالمسجد الحرام.")
    st.write("---")
    
    st.subheader("مؤشرات المراقبة الفنية لنقاط التوزيع")
    
    cols = st.columns(4)
    for i, (name, info) in enumerate(st.session_state.stations.items()):
        level = info["المستوى"]
        color_class = "station-green" if level > 20 else "station-red"
        status_text = "كفاية تامة" if level > 20 else "إنذار عجز تشغيلي وشيك"
        
        with cols[i]:
            st.markdown(f"""
                <div class="station-card {color_class}">
                    <div style="font-size: 32px; color: #FFFFFF !important;">🕋</div>
                    <div style="font-size: 16px; margin: 10px 0; color: #FFFFFF !important; font-weight: normal;">{name}</div>
                    <div style="font-size: 36px; font-weight: bold; color: #FFFFFF !important;">{level}%</div>
                    <div style="font-size: 13px; opacity: 0.9; color: #FFFFFF !important; font-weight: normal;">الوضع التشغيلي: {status_text}</div>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button(f"فحص نطاق {name}", key=f"det_{i}"):
                st.info(f"النوع الهندسي: {info['النوع']} | مؤشر الكثافة البشرية المحيطة: {info['الحشود']}")

    st.write("---")
    
    col_graph, col_summary = st.columns([2, 1])
    with col_graph:
        st.subheader("المنحنى التنبؤي لحجم الطلب المستقبلي (خلال الـ 60 دقيقة القادمة)")
        df_chart = pd.DataFrame({'الفترة الزمنية': ['أذان', 'الإقامة', 'الصلوات', 'خروج التدفقات'], 'معدل الطلب المتوقع (%)': [35, 55, 95, 70]})
        fig = px.area(df_chart, x='الفترة الزمنية', y='معدل الطلب المتوقع (%)')
        fig.update_traces(line_color='#8B7355', fillcolor='rgba(139, 115, 85, 0.15)')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        
    with col_summary:
        st.subheader("المحددات الحيوية الـ 8 للمنظومة")
        st.markdown("""
        تعتمد قراءة نظام دعم القرار على التكامل اللحظي بين المحددات التالية:
        1. **قراءات كثافة التدفق البشري** من الكاميرات الرقمية.
        2. **المطابقة الزمنية التلقائية** لجدول مواعيد الصلوات الخمس.
        3. **الحالة الجوية والبيئية** ومؤشرات الحرارة الحالية.
        4. **طبيعة وكثافة الموسم** (رمضان، الحج، الإجازات الرسمية).
        5. **الأنماط والسلوكيات التاريخية** للاستهلاك المخزنة رقمياً.
        6. **الإحداثيات الجغرافية الدقيقة** لنقاط التوزيع والتمركز الفعلي.
        7. **الوضع الجاهزي للآليات والكوادر الميدانية** المتاحة وعربات الخدمة.
        8. **مستويات القياس الرقمي اللحظي المتبقي** للمياه في خزانات التوزيع.
        """)
    render_home_button()

# --- الشاشة الثالثة: محاكي مسار المعتمرين ---
elif st.session_state.active_page == "🗺️ محاكي مسار المعتمرين":
    st.title("نظام محاكاة التوجيه والإرشاد الذكي لضيوف الرحمن")
    st.write("تطبيق إرشادي تفاعلي يهدف إلى توجيه المعتمرين لأماكن ونقاط السقيا الممتلئة والأقرب جغرافياً والأقل ازدحاماً.")
    st.write("---")
    
    st.subheader("تحديد خيارات المعتمر الافتراضية:")
    c1, c2 = st.columns(2)
    with c1:
        target_type = st.selectbox("1. حدد نوع السقيا المفضل:", [
            "تفضيل نقاط وموقع السقيا الأكثر وفرة وعشوائية", 
            "الحافظات النمطية المعقمة الثابتة", 
            "المشربيات الرقمية المحدثة", 
            "عربات الإمداد الترددي المتنقلة"
        ])
    with c2:
        current_loc = st.selectbox("2. حدد نقطة التواجد الحالية للمعتمر:", [
            "بوابة الملك عبدالعزيز (رقم 1)", 
            "بوابة الملك فهد (رقم 79)", 
            "بوابة الفتح", 
            "مجمع T3 (التوسعة السعودية الثالثة)"
        ])
        
    st.write("### تفعيل خوارزمية المسار الخالي من الكثافة البشري:")
    
    if st.button("🗺️ توليد الخريطة والمسار الإرشادي الفوري"):
        st.success("تمت معالجة القراءات الحية للموقع الجغرافي! تم توليد مسار فوري يوجه الزائر لأقرب نقطة مياه ممتلئة خالية تماماً من الكثافات والتكدسات.")
        
        st.subheader("📍 الخريطة الإرشادية اللحظية (نظام ملاحة رِواء المدمج):")
        
        map_data = []
        for name, info in st.session_state.stations.items():
            map_data.append({
                "النطاق الجغرافي": name,
                "lat": info["lat"],
                "lon": info["lon"],
                "نسبة الامتلاء (%)": info["المستوى"],
                "الحجم البصري للنقطة": info["المستوى"] * 5
            })
        df_map = pd.DataFrame(map_data)
        
        st.map(df_map, latitude="lat", longitude="lon", size="الحجم البصري للنقطة", zoom=16)
        
        st.markdown(f"""
        <div class="route-box">
            <h4 style="color: #3E332A !important; margin-bottom: 12px;">🛣️ مسار التوجيه الجغرافي الآمن لانسيابية الحشود:</h4>
            <p style="font-size: 16px; margin: 10px 0; line-height: 1.6;">
                الرجاء توجيه التدفقات والزوار عبر <b>"الممر الداخلي رقم 3"</b> المتصل مباشرة بـ <b>"صحن المطاف والأروقة المحيطة"</b> حيث تم رصده جغرافياً كأقرب نقطة إمداد مكتملة الوفرة بنسبة <b>95%</b> 🟢 ومؤشر الازدحام فيه: <b>مستقر وآمن</b>.
            </p>
            <p style="font-size: 13px; color: #555555 !important; border-top: 1px dashed #DDD; padding-top: 10px; margin-top: 10px;">
                * <b>ملاحظة الملاحة الذكية:</b> الخريطة قامت بعزل موقع "التوسعة السعودية الثالثة" (المعلم الأحمر المتدني 12% 🔴) تلقائياً لتحويل مسار الزوار وحمايتهم من مناطق التزاحم، وإتاحة النطاق لفرق التعبئة فقط.
            </p>
        </div>
        """, unsafe_allow_html=True)
    render_home_button()

# --- الشاشة الرابعة: إرسال مهمة تعبئة ميدانية ---
elif st.session_state.active_page == "⚡ إرسال مهمة تعبئة ميدانية":
    st.title("لوحة إدارة الأزمات والتحرك الميداني الاستباقي")
    st.write("عند رصد خوارزميات التنبؤ لانخفاض متوقع للمياه، يتم تفعيل بروتوكول التوجيه التلقائي لإمداد النطاق قبل نفاد المخزون بـ 20 دقيقة.")
    st.write("---")
    
    st.subheader("🚨 بروتوكول الاستجابة الاستباقية الفوري")
    st.error("تنبيه استباقي مركزي: تشير نماذج القياس إلى احتمالية حدوث عجز تشغيلي مائي تام في نطاق 'التوسعة السعودية الثالثة' في غضون 14 دقيقة تزامناً مع تدفق أفواج المصلين.")
    
    st.markdown("""
    <div style="background-color: #FFFFFF; padding: 25px; border-radius: 12px; border-left: 6px solid #C62828; box-shadow: 0 4px 10px rgba(0,0,0,0.02);">
        <h4 style="color: #C62828 !important; margin-bottom: 15px;">التوصية التشغيلية والقرار التنفيذي المقترح:</h4>
        • <b>فريق الإسناد المكلف جغرافياً:</b> فرقة الدعم والتشغيل الميداني (ب) - الممر المحوري رقم 2.<br>
        • <b>طبيعة التدخل المطلوبة:</b> تزويد وإسناد النطاق بـ 40 حافظة نمطية معقمة كاملة السعة.<br>
        • <b>المسار الترددي اللوجستي المقترح:</b> مسار الخدمة الغربي الجانبي (نسبة خلو الحركة وخلو الاختناقات فيه تبلغ 88%).
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### توجيه وتوثيق المهمة الميدانية:")
    if st.button("⚡ اعتماد وتفعيل بروتوكول التوجيه وتنبيه الفرق الميدانية"):
        st.session_state.active_logs.append("تم تفعيل بروتوكول التوجيه الاستباقي")
        st.success("تم إرسال الأمر وتوجيه التنبيه الفوري للأجهزة المحمولة المخصصة للكوادر الميدانية العاملة بالموقع.")
        
    st.write("---")
    st.subheader("⚙️ بوابة المحاكاة والفحص للمحكمين:")
    if st.button("🔄 محاكاة: قيام الكادر الميداني بتأكيد عملية إعادة التعبئة بنجاح"):
        st.session_state.stations["التوسعة السعودية الثالثة"]["المستوى"] = 100
        st.session_state.stations["التوسعة السعودية الثالثة"]["الحشود"] = "آمن / مستقر"
        st.success("تم استقبال التحديث الميداني بنجاح! عاد مخزون السقيا في 'التوسعة السعودية الثالثة' إلى وضع الأمان الكلي بنسبة 100%. تفضل بالانتقال الآن إلى 'خريطة الحافظات الحية' لتأكيد تحول البطاقة إلى اللون الأخضر.")
    render_home_button()

# --- الشاشة الخامسة: اسأل النظام الذكي ---
elif st.session_state.active_page == "💬 اسأل النظام الذكي":
    st.title("بوابة التقارير الفورية والاستعلام للمشرفين")
    st.write("الاستعلام عن البيانات التشغيلية لخدمات السقيا وتوليد التوجيهات الفورية الفنية عبر نظم المحادثة المدمجة.")
    st.write("---")
    
    st.subheader("بوابة المحادثة الموحدة للاستعلام:")
    user_query = st.text_input("اكتب سؤالك أو استفسارك الإداري المباشر هنا:", value="ما هي النطاقات الجغرافية المتوقع تسجيل أعلى استهلاك فيها خلال الساعة القادمة؟")
    
    if st.button("معالجة الاستعلام واستخراج التقرير الفني"):
        st.markdown("<div style='background-color: #EFEBE9; padding: 15px; border-radius: 8px; margin-bottom: 10px;'><strong>المستعلم المسؤول (رئيس الفترة):</strong> " + user_query + "</div>", unsafe_allow_html=True)
        st.markdown("<div style='background-color: #3E332A; padding: 15px; border-radius: 8px; color: #FFFFFF; line-height: 1.6;'><strong>منظومة رِواء الرقمية:</strong> بناءً على النماذج التنبؤية ومؤشرات كاميرات قياس الحشود الحالية، يُتوقع ارتفاع معدل الطلب والمخزون بنسبة 45% في نطاق 'صحن المطاف والأروقة المحيطة' فور انتهاء الصلاة مباشرة. يُوصى إدارياً بجدولة عربات الإمداد الترددي لتغذية المسار قبل الأذان بـ 20 دقيقة كاملة لضمان استمرارية الوفرة المائية وتجنب الاختناقات وتجمع الزوار حول نقط المشربيات.</div>", unsafe_allow_html=True)
        
    st.write("---")
    st.subheader("الأثر الاستراتيجي والمستهدفات الوطنية وفق رؤية المملكة 2030:")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("مؤشر استمرارية وضمان وفرة الخدمة", "99.9%", "مستهدف مستدام")
    c2.metric("تقليل زمن الاستجابة والتدخل الميداني", "40%-", "تحسين الكفاءة التشغيلية")
    c3.metric("خفض نسب الهدر وحماية الموارد المائية", "15%-", "استدامة بيئية")
    render_home_button()
