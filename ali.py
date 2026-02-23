import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V14", layout="wide", page_icon="https://i.postimg.cc/xCt20gWj/image.png")

# --- 2. التصميم (CSS) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
html, body, [data-testid="stAppViewContainer"], .main {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}
.main-header { background: #182848; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
.image-prompt-box { background: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ffbd45; }
.stDataFrame div[data-testid="stTable"] { direction: ltr !important; }
.stDataFrame td, .stDataFrame th { text-align: center !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. تهيئة الذاكرة ---
if 'html_code' not in st.session_state: st.session_state.html_code = ""
if 'image_prompts' not in st.session_state: st.session_state.image_prompts = []
if 'video_scripts' not in st.session_state: st.session_state.video_scripts = ""
if 'marketing_strategy' not in st.session_state: st.session_state.marketing_strategy = ""
if 'active_model' not in st.session_state: st.session_state.active_model = None

# --- 4. دوال الذكاء الاصطناعي ---
def get_working_model(api_key):
    if st.session_state.active_model: return st.session_state.active_model
    try:
        genai.configure(api_key=api_key)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name.lower():
                st.session_state.active_model = m.name
                return m.name
        st.session_state.active_model = "gemini-pro"
        return "gemini-pro"
    except: return "gemini-pro"

def generate_html_page(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        # البرومت الإلزامي الصارم بناءً على الملفات
        prompt = f"""أنت أعظم كاتب إعلانات (Copywriter) ومصمم صفحات هبوط.
        يجب عليك كتابة كود HTML و CSS متكامل في ملف واحد لصفحة هبوط لمنتج: {product_name}.
        
        ⚠️ أوامر معمارية صارمة: يجب أن يحتوي كود HTML الخاص بك على 7 أقسام متتالية (Sections)، مبرمجة ومصممة بدقة، ولا يجوز حذف أي قسم منها:
        
        1. <section id="hero">: عنوان رئيسي يعتمد على الوضوح (Clarity)، يليه عنوان فرعي يركز على الفائدة النهائية (Benefit)، ثم زر اتخاذ إجراء (CTA) قوي مثل "اطلب الآن".
        2. <section id="pas-framework">: تطبيق حرفي لنموذج PAS. فقرة تصف المشكلة (Problem)، فقرة تضخم الألم (Agitate)، ثم الإعلان عن المنتج كحل نهائي (Solution).
        3. <section id="unique-mechanism">: (طريقة Agora). قسم يشرح "الآلية الفريدة" للمنتج، ولماذا هو مختلف تماماً وأفضل من أي حل آخر في السوق.
        4. <section id="fab-framework">: تطبيق حرفي لنموذج FAB. عرض 3 مميزات للمنتج، بحيث تذكر الميزة (Feature)، ثم أفضليتها (Advantage)، ثم النتيجة العاطفية (Benefit).
        5. <section id="social-proof">: محفز الدليل الاجتماعي. تصميم 3 بطاقات لتقييمات عملاء (بأسماء عربية) مع 5 نجوم.
        6. <section id="risk-reversal">: محفز عكس المخاطر. قسم مخصص يبرز "الضمان الذهبي" (مثال: ضمان استرجاع لمدة 30 يوماً).
        7. <section id="urgency-cta">: محفز الإلحاح والندرة. قسم سفلي يذكر أن "الكمية محدودة" مع زر الطلب النهائي (Sticky CTA Button).
        
        التصميم: استخدم خط 'Cairo'، ألوان جذابة ومتباينة (تباين عالي للأزرار)، واجعل التصميم متجاوباً (Mobile First).
        أعطني فقط كود الـ HTML والـ CSS الكامل داخل علامتي ```html و ```."""
        
        response = model.generate_content(prompt)
        code = response.text
        if "```html" in code: code = code.split("```html")[1].split("```")[0]
        elif "```" in code: code = code.split("```")[1]
        return code.strip()
    except Exception as e: return f"<h3>خطأ في التوليد: {str(e)}</h3>"

def generate_video_scripts(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        # برومت السكريبتات الإلزامي بـ AIDA
        prompt = f"""أنت خبير محتوى تسويقي و Copywriter محترف. 
        اكتب 5 سكريبتات مفصلة لفيديوهات (UGC) قصيرة لمنتج: {product_name}.
        المنصات: 1. تيك توك، 2. انستجرام ريلز، 3. يوتيوب شورتس، 4. سناب شات، 5. فيسبوك.
        
        ⚠️ أوامر صارمة لكل سكريبت بناءً على قواعد Copywriting:
        1. الإطار الإلزامي: قسم كل سكريبت بوضوح إلى 4 مراحل: (انتباه Attention، اهتمام Interest، رغبة Desire، إجراء Action).
        2. الثواني الأولى (Hook/Attention): يجب أن تخطف الانتباه بصدمة أو سؤال يمس المشكلة (Pain Point).
        3. الرغبة (Desire): ركز على (النتيجة العاطفية - Emotional Outcome) التي سيحصل عليها العميل وليس المواصفات الجافة.
        4. الإجراء (Action): ادمج محفز (الندرة - Scarcity) في الثواني الأخيرة مثل "باقي 50 قطعة فقط".
        
        أعطني السكريبتات منسقة بشكل احترافي وواضح."""
        return model.generate_content(prompt).text
    except Exception as e: return f"خطأ: {str(e)}"

def generate_strategy(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        # برومت الاستراتيجية بـ Agora
        prompt = f"""أنت خبير أبحاث تسويقية من مدرسة Agora العملاقة لكتابة الإعلانات.
        المطلوب: دراسة سوق واستراتيجية اختراق لمنتج: {product_name}.
        
        ⚠️ يجب أن تغطي دراستك بدقة وإلزامية العناوين التالية:
        1. الآلية الفريدة (Unique Mechanism): ما هو الشيء الفريد في منتجنا الذي يجعله الحل الوحيد الفعال؟
        2. الحجة التي لا تقهر (The Magnificent Argument): التسلسل المنطقي والعاطفي لإقناع العميل.
        3. المعتقدات الأساسية (Necessary Beliefs): اكتب 4 معتقدات حتمية بصيغة "يجب أن يعتقد العميل أن...".
        4. فجوات السوق (Market Gaps): نقاط الضعف في إعلانات المنافسين التي سنستغلها."""
        return model.generate_content(prompt).text
    except Exception as e: return f"خطأ: {str(e)}"

def generate_image_prompts(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""اكتب 3 برومتات (Prompts) احترافية باللغة الإنجليزية لتوليد صور لمنتج: "{product_name}".
        1. Hero Shot
        2. Lifestyle Shot
        3. Macro Shot
        افصل بينها بـ: "---PROMPT_SEPARATOR---" """
        response = model.generate_content(prompt)
        prompts = response.text.split("---PROMPT_SEPARATOR---")
        return [p.strip() for p in prompts if p.strip()]
    except: return []

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.title("🏗️ محرك علي V14.0")
    api_key = st.text_input("🔑 API Key", type="password")
    product_name = st.text_input("📦 اسم المنتج")
    st.markdown("---")
    st.markdown("### 💰 إعدادات المالية (نقطة التعادل)")
    P = st.number_input("سعر البيع (P)", value=250.0)
    C = st.number_input("التكلفة (C)", value=50.0)
    CPL = st.number_input("تكلفة الليد (CPL)", value=15.0)
    uploaded_file = st.file_uploader("📊 ارفع ملف الإكسل (المالية)", type=['xlsx', 'csv'])

# --- 6. الواجهة الرئيسية ---
st.markdown('<div class="main-header"><h1>ALI Growth Engine - القالب الصارم (V14)</h1></div>', unsafe_allow_html=True)

if not api_key:
    st.warning("الرجاء إدخال API Key في القائمة الجانبية للبدء.")
else:
    tabs = st.tabs(["🎯 الاستراتيجية (Agora)", "📄 صفحة الهبوط (7 أقسام صارمة)", "🎬 سكريبتات الفيديو (AIDA)", "🖼️ استوديو الصور", "💰 التحليل المالي"])
    
    # --- التبويب 1: الاستراتيجية ---
    with tabs[0]:
        st.subheader("دراسة السوق وبناء الحجة (طريقة Agora)")
        if st.button("🧠 استخراج الاستراتيجية والآلية الفريدة"):
            if product_name:
                with st.spinner("جاري تحليل السوق وبناء الحجة..."):
                    st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
            else: st.error("أدخل اسم المنتج أولاً!")
        if st.session_state.marketing_strategy:
            st.markdown(st.session_state.marketing_strategy)

    # --- التبويب 2: صفحة الهبوط ---
    with tabs[1]:
        st.subheader("بناء صفحة الهبوط (قالب الـ 7 أقسام)")
        if st.button("🚀 توليد صفحة الهبوط الإلزامية"):
            if product_name:
                with st.spinner("جاري بناء الهيكل الإلزامي (Hero, PAS, Unique Mech, FAB, Social Proof, Risk, Urgency)..."):
                    st.session_state.html_code = generate_html_page(api_key, product_name)
            else: st.error("أدخل اسم المنتج أولاً!")
        if st.session_state.html_code:
            st.success("✅ الصفحة جاهزة وتم تطبيق الهياكل التسويقية بالحرف!")
            components.html(st.session_state.html_code, height=600, scrolling=True)
            with st.expander("💻 عرض كود الـ HTML للنسخ"):
                st.code(st.session_state.html_code, language='html')

    # --- التبويب 3: سكريبتات الفيديو ---
    with tabs[2]:
        st.subheader("توليد 5 سكريبتات فيديو (نموذج AIDA الإلزامي)")
        if st.button("🎬 توليد السكريبتات البيعية"):
            if product_name:
                with st.spinner("جاري كتابة السكريبتات..."):
                    st.session_state.video_scripts = generate_video_scripts(api_key, product_name)
            else: st.error("أدخل اسم المنتج أولاً!")
        if st.session_state.video_scripts:
            st.markdown(st.session_state.video_scripts)

    # --- التبويب 4: استوديو الصور ---
    with tabs[3]:
        st.subheader("أوامر توليد الصور")
        if st.button("🖼️ توليد البرومتات"):
            if product_name:
                with st.spinner("المخرج الفني يعمل..."):
                    st.session_state.image_prompts = generate_image_prompts(api_key, product_name)
            else: st.error("أدخل اسم المنتج أولاً!")
        if st.session_state.image_prompts and len(st.session_state.image_prompts) >= 3:
            for i, p in enumerate(st.session_state.image_prompts):
                st.markdown(f'<div class="image-prompt-box"><strong>البرومت {i+1}:</strong><br>{p}</div>', unsafe_allow_html=True)
                st.code(p, language="text")

    # --- التبويب 5: التحليل المالي ---
    with tabs[4]:
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
                break_even_dr = (C + CPL) / P
                st.info(f"💡 نقطة التعادل المحسوبة: **{round(break_even_dr * 100, 2)}%** من نسبة التسليم (DR).")
                col_a, col_b = st.columns(2)
                with col_a: country_col = st.selectbox("عمود الدولة/المنطقة:", df.columns)
                with col_b: dr_col = st.selectbox("عمود نسبة التسليم (DR):", df.columns)
                
                results = []
                for _, row in df.iterrows():
                    try:
                        raw_dr = str(row[dr_col]).replace('%', '').strip()
                        val_dr = float(raw_dr)
                        if val_dr > 1: val_dr /= 100 
                        status = "✅ رابح" if val_dr >= break_even_dr else "🚨 خاسر"
                        results.append({"المنطقة": row[country_col], "التسليم (DR)": f"{round(val_dr*100, 1)}%", "التعادل المطلوب": f"{round(break_even_dr*100, 1)}%", "الحالة": status})
                    except: continue
                if results: st.table(pd.DataFrame(results))
            except Exception as e: st.error(f"خطأ: {str(e)}")
        else:
            st.info("ارفع ملف البيانات المالي لعرض التحليل.")

