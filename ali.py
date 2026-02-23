import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V15", layout="wide", page_icon="https://i.postimg.cc/xCt20gWj/image.png")

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
        
        # برومت "التصميم البصري" الإلزامي
        prompt = f"""أنت أعظم مصمم صفحات هبوط بصرية (Visual-First Landing Pages) في التجارة الإلكترونية.
        المطلوب: كتابة كود HTML و CSS متكامل لصفحة هبوط لمنتج: {product_name}.
        
        ⚠️ القاعدة الذهبية الجديدة (Visuals > Text):
        العملاء لا يقرؤون! لذلك يجب أن تكون الصفحة مبنية بنسبة 80% على الصور، الفيديوهات، وصور الـ GIF المتحركة، و20% فقط نصوص (عناوين قصيرة جداً ومباشرة).
        
        الهيكل الإلزامي (الـ 7 أقسام بأسلوب بصري):
        1. <section id="hero">: خلفية فيديو للمنتج. استخدم <video autoplay loop muted playsinline width="100%"> مع رابط مؤقت لفيديو (MP4 placeholder). فوق الفيديو ضع عنواناً من 5 كلمات فقط، وزر شراء ضخم.
        2. <section id="pas-framework">: قسم المشكلة والحل. استخدم صورة GIF تعبر عن المعاناة، بجانبها أو تحتها GIF للحل السحري بالمنتج. النص عبارة عن سطرين كحد أقصى.
        3. <section id="unique-mechanism">: صورة مقطعية (Macro Image Placeholder) توضح كيف يعمل المنتج، مع 3 نقاط نصية (Bullet points) قصيرة جداً تشرح الآلية.
        4. <section id="fab-framework">: شبكة بصرية (Grid). ضع 3 صور أو أيقونات كبيرة، تحت كل منها 3 كلمات فقط تشرح الفائدة العاطفية (Benefit) وليس الميزة المعقدة.
        5. <section id="social-proof">: قسم "آراء العملاء بالفيديو". صمم 3 مساحات طولية (مستطيلات عمودية تشبه الريلز) لوضع فيديوهات مراجعات العملاء (Video Testimonials).
        6. <section id="risk-reversal">: تصميم بأسلوب "ختم ذهبي" ضخم يملأ الشاشة لضمان الاسترجاع، تحته سطر واحد: "جرب بدون مخاطرة".
        7. <section id="urgency-cta">: زر عائم بالأسفل (Sticky CTA) يتحرك ببطء (Pulse Animation) مع نص "اطلب الآن - الكمية محدودة".
        
        التصميم: CSS حديث، متجاوب تماماً للموبايل (Mobile First)، مساحات واسعة للوسائط المتعددة (Media Containers)، نصوص عريضة بخط 'Cairo' وقليلة جداً.
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
        prompt = f"""أنت خبير محتوى تسويقي و Copywriter محترف. 
        اكتب 5 سكريبتات مفصلة لفيديوهات (UGC) قصيرة لمنتج: {product_name}.
        المنصات: 1. تيك توك، 2. انستجرام ريلز، 3. يوتيوب شورتس، 4. سناب شات، 5. فيسبوك.
        ⚠️ أوامر صارمة لكل سكريبت بناءً على قواعد Copywriting:
        1. الإطار الإلزامي: (انتباه Attention، اهتمام Interest، رغبة Desire، إجراء Action).
        2. الثواني الأولى (Hook/Attention): يجب أن تخطف الانتباه بصدمة أو سؤال يمس المشكلة.
        3. الرغبة (Desire): ركز على (النتيجة العاطفية) التي سيحصل عليها العميل.
        4. الإجراء (Action): ادمج محفز (الندرة) في الثواني الأخيرة.
        أعطني السكريبتات منسقة بشكل احترافي وواضح."""
        return model.generate_content(prompt).text
    except Exception as e: return f"خطأ: {str(e)}"

def generate_strategy(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""أنت خبير أبحاث تسويقية من مدرسة Agora العملاقة.
        المطلوب: دراسة سوق لمنتج: {product_name}.
        ⚠️ يجب أن تغطي دراستك بدقة:
        1. الآلية الفريدة (Unique Mechanism): ما هو الشيء الفريد في منتجنا؟
        2. الحجة التي لا تقهر (The Magnificent Argument): التسلسل المنطقي والعاطفي.
        3. المعتقدات الأساسية (Necessary Beliefs): اكتب 4 معتقدات حتمية بصيغة "يجب أن يعتقد العميل أن...".
        4. فجوات السوق (Market Gaps): نقاط الضعف في إعلانات المنافسين."""
        return model.generate_content(prompt).text
    except Exception as e: return f"خطأ: {str(e)}"

def generate_image_prompts(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""اكتب 3 برومتات احترافية باللغة الإنجليزية لتوليد صور لمنتج: "{product_name}".
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
    st.title("🏗️ محرك علي V15.0")
    api_key = st.text_input("🔑 API Key", type="password")
    product_name = st.text_input("📦 اسم المنتج")
    st.markdown("---")
    st.markdown("### 💰 إعدادات المالية (نقطة التعادل)")
    P = st.number_input("سعر البيع (P)", value=250.0)
    C = st.number_input("التكلفة (C)", value=50.0)
    CPL = st.number_input("تكلفة الليد (CPL)", value=15.0)
    uploaded_file = st.file_uploader("📊 ارفع ملف الإكسل", type=['xlsx', 'csv'])

# --- 6. الواجهة الرئيسية ---
st.markdown('<div class="main-header"><h1>ALI Growth Engine - القالب البصري (V15)</h1></div>', unsafe_allow_html=True)

if not api_key:
    st.warning("الرجاء إدخال API Key في القائمة الجانبية للبدء.")
else:
    tabs = st.tabs(["🎯 الاستراتيجية (Agora)", "📱 صفحة الهبوط (Visual First)", "🎬 سكريبتات الفيديو", "🖼️ استوديو الصور", "💰 التحليل المالي"])
    
    with tabs[0]:
        st.subheader("دراسة السوق وبناء الحجة")
        if st.button("🧠 استخراج الاستراتيجية"):
            if product_name:
                with st.spinner("جاري التحليل..."):
                    st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
            else: st.error("أدخل اسم المنتج!")
        if st.session_state.marketing_strategy: st.markdown(st.session_state.marketing_strategy)

    with tabs[1]:
        st.subheader("بناء صفحة هبوط بصرية (صور و GIF وفيديوهات)")
        if st.button("🚀 توليد الصفحة البصرية"):
            if product_name:
                with st.spinner("جاري بناء هيكل الوسائط المتعددة..."):
                    st.session_state.html_code = generate_html_page(api_key, product_name)
            else: st.error("أدخل اسم المنتج!")
        if st.session_state.html_code:
            st.success("✅ الصفحة البصرية جاهزة! ستلاحظ وجود مساحات لرفع فيديوهات وصور GIF.")
            components.html(st.session_state.html_code, height=700, scrolling=True)
            with st.expander("💻 عرض كود الـ HTML للنسخ"):
                st.code(st.session_state.html_code, language='html')

    with tabs[2]:
        st.subheader("توليد 5 سكريبتات فيديو")
        if st.button("🎬 توليد السكريبتات"):
            if product_name:
                with st.spinner("جاري الكتابة..."):
                    st.session_state.video_scripts = generate_video_scripts(api_key, product_name)
            else: st.error("أدخل اسم المنتج!")
        if st.session_state.video_scripts: st.markdown(st.session_state.video_scripts)

    with tabs[3]:
        st.subheader("أوامر توليد الصور")
        if st.button("🖼️ توليد البرومتات"):
            if product_name:
                with st.spinner("المخرج الفني يعمل..."):
                    st.session_state.image_prompts = generate_image_prompts(api_key, product_name)
            else: st.error("أدخل اسم المنتج!")
        if st.session_state.image_prompts and len(st.session_state.image_prompts) >= 3:
            for i, p in enumerate(st.session_state.image_prompts):
                st.markdown(f'<div class="image-prompt-box"><strong>البرومت {i+1}:</strong><br>{p}</div>', unsafe_allow_html=True)
                st.code(p, language="text")

    with tabs[4]:
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
                break_even_dr = (C + CPL) / P
                st.info(f"💡 نقطة التعادل المحسوبة: **{round(break_even_dr * 100, 2)}%** من نسبة التسليم (DR).")
                col_a, col_b = st.columns(2)
                with col_a: country_col = st.selectbox("عمود الدولة:", df.columns)
                with col_b: dr_col = st.selectbox("عمود نسبة التسليم:", df.columns)
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
        else: st.info("ارفع ملف البيانات المالي لعرض التحليل.")
