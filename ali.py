import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة الفاخرة ---
st.set_page_config(page_title="ALI Growth Engine V20 - AI Visualizer", layout="wide", page_icon="🚀")

# --- 2. التصميم (CSS) لواجهة الأداة نفسها ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
html, body, [data-testid="stAppViewContainer"], .main {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
    background-color: #f8f9fa;
}
.main-header { 
    background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); 
    color: white; padding: 30px; border-radius: 20px; 
    text-align: center; margin-bottom: 30px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
}
.stButton>button {
    width: 100%; border-radius: 10px; height: 3em; 
    background-color: #3b82f6; color: white; font-weight: bold; border: none;
}
.status-box { background: white; padding: 20px; border-radius: 15px; border-right: 5px solid #3b82f6; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. تهيئة الذاكرة ---
for key in ['html_code', 'image_prompts', 'video_scripts', 'marketing_strategy', 'active_model']:
    if key not in st.session_state: st.session_state[key] = ""

# --- 4. دوال الذكاء الاصطناعي المطورة (V20) ---
def get_working_model(api_key):
    try:
        genai.configure(api_key=api_key)
        return "gemini-1.5-flash" # نستخدم Flash لقدرته العالية على التحليل السريع
    except: return "gemini-pro"

def generate_full_experience(api_key, product_url):
    model_name = get_working_model(api_key)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    # المرحلة الأولى: تحليل الرابط واستخراج الاستراتيجية والألوان
    analysis_prompt = f"""
    أنت خبير تسويق وتحليل بيانات. قم بزيارة وتحليل هذا الرابط: {product_url}
    المطلوب:
    1. استخرج اسم المنتج بدقة.
    2. استخرج "الآلية الفريدة" (Unique Mechanism) و"فجوة السوق".
    3. قرر لوحة ألوان احترافية (Primary, Secondary, Accent) بناءً على ألوان المنتج في الرابط.
    4. اكتب دراسة سوق قصيرة بنظام Agora (الحجة التي لا تقهر).
    رد باللغة العربية، ولكن اجعل الألوان في قسم منفصل بالإنجليزية.
    """
    strategy_res = model.generate_content(analysis_prompt).text
    st.session_state.marketing_strategy = strategy_res

    # المرحلة الثانية: توليد الكود البصري (المطابق للصور)
    html_prompt = f"""
    أنت أعظم مصمم صفحات هبوط (UI/UX) ومبرمج Tailwind CSS.
    بناءً على التحليل التالي: {strategy_res}
    وعلى الرابط: {product_url}

    المطلوب: كود HTML متكامل (Single File) يتضمن Tailwind CSS.
    ⚠️ المواصفات البصرية (إلزامي):
    1. التصميم (Mobile-First) بعرض 480px متمركز.
    2. استخدم ألوان المنتج المستخرجة للأزرار والخلفيات.
    3. الأقسام الـ 13 (Hero, Trust Bar, Problem, Solution, Mechanism, Grid, Comparison, Ingredients, Social Proof, Expert, Steps, Guarantee, Sticky CTA).
    4. اجعل الزوايا مستديرة (rounded-2xl) والظلال ناعمة (shadow-lg) كما في قوالب Shopify الاحترافية.
    5. استخدم صوراً تعبيرية عالية الجودة من Unsplash أو روابط صور المنتج إن وجدت.
    
    أعطني الكود فقط داخل علامتي ```html.
    """
    html_res = model.generate_content(html_prompt).text
    if "```html" in html_res: html_res = html_res.split("```html")[1].split("```")[0]
    st.session_state.html_code = html_res.strip()

# --- 5. الواجهة الجانبية ---
with st.sidebar:
    st.image("https://i.postimg.cc/xCt20gWj/image.png", width=100)
    st.title("محرك علي V20.0")
    api_key = st.text_input("🔑 Gemini API Key", type="password")
    product_url = st.text_input("🔗 رابط المنتج (URL)", placeholder="https://example.com/product")
    
    st.markdown("---")
    st.info("الأداة ستقوم الآن بتحليل الرابط تلقائياً، استخراج الألوان، وتصميم الصفحة دون تدخل منك.")

# --- 6. العرض الرئيسي ---
st.markdown('<div class="main-header"><h1>ALI Growth Engine V20: Auto-Link Visualizer</h1><p>توليد صفحات هبوط احترافية بناءً على روابط المنتجات</p></div>', unsafe_allow_html=True)

if not api_key or not product_url:
    st.warning("الرجاء إدخال API Key ورابط المنتج في القائمة الجانبية.")
else:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🚀 ابدأ التحليل والتوليد الكامل"):
            with st.spinner("جاري قراءة الرابط وتصميم الصفحة بصرياً..."):
                generate_full_experience(api_key, product_url)
                st.success("تم التوليد بنجاح!")

    tabs = st.tabs(["🎨 معاينة الصفحة", "🧠 الاستراتيجية المستخرجة", "💻 الكود البرمجي"])
    
    with tabs[0]:
        if st.session_state.html_code:
            st.markdown("### معاينة الصفحة (تصميم الموبايل)")
            components.html(st.session_state.html_code, height=900, scrolling=True)
        else: st.info("انتظر التوليد للمعاينة...")

    with tabs[1]:
        if st.session_state.marketing_strategy:
            st.markdown('<div class="status-box">', unsafe_allow_html=True)
            st.write(st.session_state.marketing_strategy)
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        if st.session_state.html_code:
            st.code(st.session_state.html_code, language='html')
