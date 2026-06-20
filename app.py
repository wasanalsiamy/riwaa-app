import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. إعدادات الهوية الرسمية للمنصة
st.set_page_config(page_title="منظومة رِواء الوطنية", page_icon="🕋", layout="wide")

# 2. هندسة المظهر البصري (بيج رخامي وبني خشبي بنصوص سوداء وبيضاء صريحة)
st.markdown("""
    <style>
    /* الخلفية العامة: بيج رخامي مريح للعين */
    .stApp {
        background-color: #FDFBF7;
        color: #1A1A1A;
    }
    
    /* القائمة الجانبية: بني داكن بنصوص بيضاء */
    [data-testid="stSidebar"] {
        background-color: #3E332A;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* توحيد لون النصوص العامة بالأسود الصريح لراحة العين */
    h1, h2, h3, h4, p, span, label {
        color: #1A1A1A !important;
        font-family: 'Arial', sans-serif;
    }
    
    /* الحفاظ على نصوص القائمة الجانبية باللون الأبيض */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    /* صناديق المؤشرات التشغيلية */
    .stMetric {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border-right: 6px solid #8B7355;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    
    /* التبويبات الفاخرة */
    .stTabs [data-baseweb="tab"] {
        color: #3E332A;
        font-size: 18px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        color: #8B7355 !important;
        border-bottom-color: #8B7355 !important;
    }

    /* الأزرار التنفيذية */
    .stButton>button {
        background-color: #3E332A;
        color: #FFFFFF !important;
        border-radius: 6px;
        border: none;
        padding: 12px 30px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #8B7355;
        color: #FFFFFF !important;
    }
    
    /* التنبيهات الإدارية */
    .stAlert {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات الافتراضية للنظام (مستويات التعبئة اللحظية)
if 'water_levels' not in st.session_state:
    st.session_state.water_levels = {"أروقة المطاف": 88, "المسعى الأرضي": 42, "توسعة الملك فهد": 14, "الساحات الخارجية": 65}
if 'active_tasks' not in st.session_state:
    st.session_state.active_tasks = []

# 4. القائمة الجانبية للتوجيه والتحكم
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 28px; font-weight: bold;'>منظومة رِواء</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 14px; opacity: 0.8;'>الإدارة الرقمية لسقيا زمزم بالمسجد الحرام</p>", unsafe_allow_html=True)
    st.write("---")
    page = st.radio("أقسام المنصة التشغيلية:", [
        "التعريف بالمنظومة", 
        "مركز العمليات والتنبؤ اللحظي", 
        "نظام دعم القرار والتوجيه الذكي", 
        "المساعد اللغوي للمشرفين", 
        "تطبيق الكوادر الميدانية", 
        "مؤشرات الأثر والاستدامة"
    ])
    st.write("---")
    st.caption("مسار: التنقل الذكي وإدارة الحشود")

# --- 1. التعريف بالمنظومة ---
if page == "التعريف بالمنظومة":
    st.title("منظومة رِواء الرقمية")
    st.markdown("#### الحل الوطني الذكي لأتمتة ورفع كفاءة عمليات السقيا داخل الحرم المكي الشريف")
    st.write("---")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("رؤية المنصة")
        st.write("""
        تأتي منصة **رِواء** لإنهاء العمليات التشغيلية التقليدية القائمة على الجولات الدورية أو البلاغات المتأخرة، والتي قد تتسبب في نفاد المياه المفاجئ وتكدس الحشود في نقاط التوزيع خلال أوقات الذروة.
        
        تعتمد المنصة على ربط البيانات اللحظية وإخضاعها لخوارزميات متقدمة تتنبأ بحجم الاستهلاك البشري ومعدلات نفاد المياه قبل حدوثها بـ 20 دقيقة، مما يتيح للإدارة العامة للسقيا التحرك الاستباقي وتوجيه الموارد البشرية والعربات بمرونة تامة لضمان انسيابية الحشود.
        """)
        st.info("يتكامل النظام بصورة مباشرة مع أهداف الهيئة العامة للعناية بشؤون المسجد الحرام والمسجد النبوي.")
    with col2:
        # صورة تعبيرية راقية تعكس تفاصيل وهوية الحرم المكي الشريف
        st.image("https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=600&q=80", caption="المسجد الحرام - مكة المكرمة", use_container_width=True)

# --- 2. مركز العمليات والتنبؤ اللحظي ---
elif page == "مركز العمليات والتنبؤ اللحظي":
    st.title("لوحة تحكم مركز العمليات")
    st.write("متابعة حية ومباشرة لحالة نقاط التوزيع في كافة أروقة وتوسعات الحرم المكي الشريف.")
    st.write("---")
    
    st.subheader("مستويات تعبئة المياه اللحظية الحالية")
    cols = st.columns(4)
    locations = list(st.session_state.water_levels.keys())
    for i, loc in enumerate(locations):
        level = st.session_state.water_levels[loc]
        status = "مستقر" if level > 50 else ("متوسط" if level > 20 else "حرِج: يتطلب تدخل")
        cols[i].metric(label=loc, value=f"{level}%", delta=status, delta_color="normal" if level > 20 else "inverse")
        
    st.write("---")
    
    col_factors, col_chart = st.columns([1, 1])
    with col_factors:
        st.subheader("المحددات والمؤشرات الـ 8 للتحليل:")
        st.write("""
        يقوم النظام بتحليل هذه العوامل الثمانية بالتوازي لإصدار التوقعات:
        1. الكثافة العددية وتدفقات الحشود البشرية في الممرات.
        2. التوقيت الزمني وربطه بمواعيد الصلوات الخمس.
        3. درجات الحرارة الحالية والمتوقعة خلال اليوم.
        4. طبيعة الموسم التشغيلي الحالي (رمضان، الحج، الإجازات).
        5. الأنماط التاريخية للاستهلاك في كل جناح بالمستودعات.
        6. التوزيع الجغرافي ونقاط التموضع الثابتة للحافظات.
        7. الحالة التشغيلية ومواقع عربات التعبئة المتحركة.
        8. القياس اللحظي للمياه المتبقية داخل كل نقطة توزيع.
        """)
        
    with col_chart:
        st.subheader("منحنى الاستهلاك والتنبؤ بالطلب (الساعة القادمة)")
        time_slots = ['10:00', '11:00', '12:00', '13:00', '14:00']
        demand_forecast = [35, 50, 95, 70, 40]
        df_chart = pd.DataFrame({'الوقت': time_slots, 'معدل الطلب المتوقع (%)': demand_forecast})
        fig = px.area(df_chart, x='الوقت', y='معدل الطلب المتوقع (%)')
        fig.update_traces(line_color='#8B7355', fillcolor='rgba(139, 115, 85, 0.15)')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# --- 3. نظام دعم القرار والتوجيه الذكي ---
elif page == "نظام دعم القرار والتوجيه الذكي":
    st.title("نظام دعم القرار والتحرك الاستباقي")
    st.write("توليد التوصيات التشغيلية التلقائية لتفادي نفاد المياه ومنع التكدس البشري حول نقاط السقيا.")
    st.write("---")
    
    st.subheader("حالة التنبؤ والتحليل الجاري")
    
    st.error("🚨 إشعار استباقي: تشير التوقعات لنفاد مياه زمزم بالكامل في 'توسعة الملك فهد' خلال 15 دقيقة القادمة نتيجة تدفق بشري كثيف.")
    
    st.write("### التوصية والقرار التشغيلي المقترح:")
    st.info("""
    - **المركبة التشغيلية المرشحة:** عربة التعبئة رقم 4.
    - **الفريق الميداني الأقرب جغرافياً:** فريق ب - ممر رقم 2.
    - **القدرة الاستيعابية المطلوبة:** شحن وإمداد 40 حافظة نمطية.
    - **المسار الترددي المقترح:** ممر الملك فهد الجانبي (نسبة خلو المسار من التكدس البشري تبلغ 88%).
    - **زمن الوصول المقدر:** 6 دقائق (مما يضمن الإمداد قبل النفاد بـ 9 دقائق كاملة).
    """)
    
    if st.button("اعتماد التوصية وتوجيه الفريق الميداني فوراً"):
        if "مهمة توسعة الملك فهد" not in st.session_state.active_tasks:
            st.session_state.active_tasks.append("مهمة توسعة الملك فهد")
            st.success("تم تسجيل القرار بنجاح، وتحويل المهمة تلقائياً إلى الأجهزة المحمولة للفرق الميدانية.")

# --- 4. المساعد اللغوي للمشرفين ---
elif page == "المساعد اللغوي للمشرفين":
    st.title("المساعد الفوري للمشرفين ورؤساء الفترات")
    st.write("تسهيل استعلام مسؤولي التشغيل عن الوضع الميداني عبر واجهة محادثة ذكية ومباشرة.")
    st.write("---")
    
    st.subheader("استعلم عن الحالة التشغيلية:")
    user_query = st.text_input("اكتب استفسارك هنا كمسؤول تشغيل:", value="ما هي المناطق المتوقع تشهد أعلى استهلاك بعد صلاة المغرب؟")
    
    if st.button("تحليل الاستفسار واستخراج التقرير"):
        st.markdown("<div style='background-color: #EFEBE9; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #1A1A1A;'><strong>المستعلم (رئيس الفترة):</strong> " + user_query + "</div>", unsafe_allow_html=True)
        st.markdown("<div style='background-color: #3E332A; padding: 15px; border-radius: 8px; color: #FFFFFF;'><strong>منصة رِواء:</strong> تشير القراءات إلى ارتفاع الطلب بنسبة 42% في صحن المطاف والأروقة القريبة منه فور انتهاء الصلاة. يُوصى بجدولة وتوجيه عربات الدعم قبل الأذان بـ 20 دقيقة لضمان استمرار الخدمة وتفادي حدوث أي اختناقات في حركة المشاة حول المشربيات.</div>", unsafe_allow_html=True)

# --- 5. تطبيق الكوادر الميدانية ---
elif page == "تطبيق الكوادر الميدانية":
    st.title("واجهة الفرق الميدانية التنفيذية")
    st.write("محاكاة لشاشة الأجهزة المحمولة الخاصة بالكوادر التشغيلية في الميدان لتلقي التوجيهات.")
    st.write("---")
    
    col_app, col_img = st.columns([3, 2])
    
    with col_app:
        if not st.session_state.active_tasks:
            st.info("لا توجد مهمات معلقة حالياً. مؤشرات الأداء مستقرة وجميع نقاط السقيا مغطاة.")
        else:
            for task in st.session_state.active_tasks:
                st.warning("⚠️ مهمة عمل مستعجلة صادرة من الإدارة المركزية")
                st.write(f"**طبيعة العمل:** إعادة تعبئة وإمداد حافظات مياه زمزم")
                st.write(f"**الموقع المستهدف:** توسعة الملك فهد")
                st.write(f"**الحجم المطلوب:** 40 حافظة معقمة")
                st.write(f"**المسار الموصى به:** اسلك ممر الملك فهد الجانبي (مسار خالٍ من الكثافة البشري الحالية)")
                st.write(f"**مستوى الأهمية:** عاجل جداً")
                
                if st.button("تأكيد إتمام عملية الإعادة والتعبئة بنجاح"):
                    st.session_state.water_levels["توسعة الملك فهد"] = 100
                    st.session_state.active_tasks.remove(task)
                    st.success("تم تحديث قاعدة البيانات المركزية فوراً وعودة المؤشر للوضع المستقر.")
                    st.rerun()
    with col2:
        # صورة تعبيرية لحافظات المياه والعمل التنظيمي في الحرم
        st.image("https://images.unsplash.com/photo-1591604129939-f1edd4d9f7fa?auto=format&fit=crop&w=600&q=80", caption="تنظيم وإمداد خدمات السقيا بالحرم المكي", use_container_width=True)

# --- 6. مؤشرات الأثر والاستدامة ---
elif page == "مؤشرات الأثر والاستدامة":
    st.title("الأثر الإستراتيجي والاستدامة")
    st.write("تحقيق الأهداف الوطنية وقياس جودة الخدمات المقدمة لضيوف الرحمن.")
    st.write("---")
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("استمرارية وضمان توفر الخدمة", "99.9%", "مستهدف مستدام")
    col_kpi2.metric("خفْض زمن الاستجابة للمهمات", "40%-", "تحسين كفاءة")
    col_kpi3.metric("خفْض الهدر في عمليات التعبئة", "15%-", "حماية الموارد المائية")
    
    st.write("---")
    st.subheader("المساهمة في تحقيق مستهدفات رؤية المملكة 2030:")
    st.write("""
    - **التحول الرقمي الذكي للخدمات:** أتمتة إدارة البنية التحتية لمنظومة السقيا بالاعتماد على علم البيانات التنبؤية المتطور.
    - **تحسين إدارة الحشود وتنقل المركبات:** تقليل الاختناقات وحظر تعارض عربات الخدمة مع حركة المشاة والمصلين بتوجيهها عبر مسارات رقمية دقيقة وخالية.
    - **جودة الحياة وإثراء تجربة ضيوف الرحمن:** ضمان التوزيع العادل والمستمر للمياه المباركة بكفاءة تليق بالمكانة المقدسة للمملكة وبأعلى المعايير العالمية.
    """)
