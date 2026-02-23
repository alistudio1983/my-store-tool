import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V17", layout="wide", page_icon="https://i.postimg.cc/xCt20gWj/image.png")

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

# --- 4. دوال الذكاء الاصطناعي (محدثة بنظام الربط) ---
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

def generate_strategy(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""أنت خبير أبحاث تسويقية من مدرسة Agora العملاقة.
        المطلوب: دراسة سوق لمنتج: {product_name}.
        ⚠️ ركز على: 1. الآلية الفريدة، 2. الحجة التي لا تقهر، 3. المعتقدات الأساسية، 4. فجوات السوق."""
        return model.generate_content(prompt).text
    except Exception as e: return f"خطأ: {str(e)}"

# تم تمرير الاستراتيجية كمتغير داخل الدالة لربط العقول
def generate_html_page(api_key, product_name, strategy_text):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""أنت أعظم مبرمج ومصمم لصفحات الهبوط البصرية (Visual-First Landing Pages).
        المطلوب: برمجة كود HTML و CSS متكامل لصفحة هبوط لمنتج: {product_name}.
        
        🧠 **[هام جداً]: يجب أن تُبنى نصوص وأفكار الصفحة حصرياً على نتائج هذه الاستراتيجية التسويقية (طريقة Agora):**
        {strategy_text}
        استخدم "الآلية الفريدة" في قسم المكونات، و"الحجة" في قسم المشكلة والحل، و"المعتقدات" كفوائد.
        
        ⚠️ قوانين التصميم الصارمة (Visuals > Text):
        - النصوص لا تتعدى 15% من الصفحة. الباقي صور، فيديوهات، و GIF (استخدم روابط وهمية Placeholders).
        - التصميم للموبايل أولاً (Mobile First) بعرض أقصى 480px.
        
        ⚠️ الأقسام الـ 7 الإلزامية:
        1. <section id="hero">: فيديو خلفية، تحته عنوان مبني على "الحجة القوية"، وزر طلب نابض.
        2. <section id="pas-framework">: 2 صور GIF (واحدة للمشكلة والأخرى للحل) مبنية على الاستراتيجية، مع جمل قصيرة جداً.
        3. <section id="unique-mechanism">: صورة مقطعية (Diagram Placeholder). اكتب تحتها "الآلية الفريدة" التي استخرجتها من الاستراتيجية بـ 3 نقاط.
        4. <section id="fab-framework">: شبكة من 4 صور مربعة تبرز "النتائج العاطفية" بناءً على معتقدات العميل.
        5. <section id="social-proof">: 3 حاويات فيديوهات (ريلز) لتقييمات تدعم الحجة التي لا تقهر.
        6. <section id="risk-reversal">: ختم ضمان ذهبي كبير جداً (Risk Reversal).
        7. <section id="urgency-cta">: عداد تنازلي GIF، وزر عائم بالأسفل (Sticky CTA).
        
        أعطني فقط كود الـ HTML والـ CSS المدمج داخل علامتي ```html و ```."""
        
        response = model.generate_content(prompt)
        code = response.text
        if "```html" in code: code = code.split("```html")[1].split("```")[0]
        elif "```" in code: code = code.split("```")[1]
        return code.strip()
    except Exception as e: return f"<h3>خطأ في التوليد: {str(e)}</h3>"

def generate_video_scripts(api_key, product_name, strategy_text):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""أنت خبير محتوى تسويقي و Copywriter محترف. 
        اكتب 5 سكريبتات مفصلة لفيديوهات (UGC) قصيرة لمنتج: {product_name}.
        المنصات: تيك توك، انستجرام ريلز، يوتيوب شورتس، سناب شات، فيسبوك.
        
        🧠 **[هام جداً]: يجب أن تُبنى حوارات السكريبتات وزواياها حصرياً على هذه الاستراتيجية التسويقية:**
        {strategy_text}
        استخدم "الآلية الفريدة" كعنصر الجذب الرئيسي في منتصف الفيديو.
        
        ⚠️ الإطار الإلزامي: (انتباه Attention، اهتمام Interest، رغبة Desire، إجراء Action).
        ركز على المشكلة في أول 3 ثواني، والنتيجة العاطفية في المنتصف."""
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
    st.title("🏗️ محرك علي V17.0")
    api_key = st.text_input("🔑 API Key", type="password")
    product_name = st.text_input("📦 اسم المنتج")
    st.markdown("---")
    st.markdown("### 💰 إعدادات المالية (نقطة التعادل)")
    P = st.number_input("سعر البيع (P)", value=250.0)
    C = st.number_input("التكلفة (C)", value=50.0)
    CPL = st.number_input("تكلفة الليد (CPL)", value=15.0)
    uploaded_file = st.file_uploader("📊 ارفع ملف الإكسل", type=['xlsx', 'csv'])

# --- 6. الواجهة الرئيسية ---
st.markdown('<div class="main-header"><h1>ALI Growth Engine - محرك الربط الاستراتيجي (V17)</h1></div>', unsafe_allow_html=True)

if not api_key:
    st.warning("الرجاء إدخال API Key في القائمة الجانبية للبدء.")
else:
    tabs = st.tabs(["🎯 الاستراتيجية (الأساس)", "📱 صفحة الهبوط (Visual)", "🎬 سكريبتات الفيديو", "🖼️ استوديو الصور", "💰 التحليل المالي"])
    
    with tabs[0]:
        st.subheader("دراسة السوق وبناء الحجة (Agora)")
        if st.button("🧠 استخراج الاستراتيجية (إلزامي للخطوات القادمة)"):
            if product_name:
                with st.spinner("جاري التحليل واستخراج الآلية الفريدة..."):
                    st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
            else: st.error("أدخل اسم المنتج!")
        if st.session_state.marketing_strategy: st.markdown(st.session_state.marketing_strategy)

    with tabs[1]:
        st.subheader("بناء صفحة هبوط بصرية مبنية على الاستراتيجية")
        if st.button("🚀 توليد الصفحة المتكاملة"):
            if product_name:
                # التحقق الذكي: إذا لم تكن الاستراتيجية موجودة، يولدها أولاً ثم يولد الصفحة
                if not st.session_state.marketing_strategy:
                    with st.spinner("جاري بناء الاستراتيجية كأساس لتصميم الصفحة..."):
                        st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
                
                with st.spinner("جاري برمجة وتصميم الصفحة البصرية بناءً على الاستراتيجية..."):
                    st.session_state.html_code = generate_html_page(api_key, product_name, st.session_state.marketing_strategy)
            else: st.error("أدخل اسم المنتج!")
        
        if st.session_state.html_code:
            st.success("✅ الصفحة جاهزة! نصوصها مبنية حرفياً على معتقدات وحجة الاستراتيجية.")
            components.html(st.session_state.html_code, height=750, scrolling=True)
            with st.expander("💻 عرض كود الـ HTML للنسخ"):
                st.code(st.session_state.html_code, language='html')

    with tabs[2]:
        st.subheader("توليد 5 سكريبتات فيديو مبنية على الاستراتيجية")
        if st.button("🎬 توليد السكريبتات"):
            if product_name:
                if not st.session_state.marketing_strategy:
                    with st.spinner("جاري بناء الاستراتيجية كأساس للسكريبتات..."):
                        st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
                        
                with st.spinner("جاري كتابة السكريبتات التسويقية..."):
                    st.session_state.video_scripts = generate_video_scripts(api_key, product_name, st.session_state.marketing_strategy)
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
        if
