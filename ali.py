import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components
import re

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V19", layout="wide", page_icon="🚀")

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
.image-prompt-box { background: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ffbd45; direction: ltr; text-align: left; }
.stDataFrame div[data-testid="stTable"] { direction: ltr !important; }
.stDataFrame td, .stDataFrame th { text-align: center !important; }
div.stTextArea textarea { font-family: 'Cairo', sans-serif !important; font-size: 16px; direction: rtl; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- 3. تهيئة الذاكرة ---
if 'html_code' not in st.session_state:
    st.session_state.html_code = ""
if 'image_prompts' not in st.session_state:
    st.session_state.image_prompts = []
if 'video_scripts' not in st.session_state:
    st.session_state.video_scripts = ""
if 'marketing_strategy' not in st.session_state:
    st.session_state.marketing_strategy = ""
if 'active_model' not in st.session_state:
    st.session_state.active_model = None

# --- 4. دوال الذكاء الاصطناعي ---
def get_working_model(api_key):
    if st.session_state.active_model:
        return st.session_state.active_model
    try:
        genai.configure(api_key=api_key)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name.lower():
                st.session_state.active_model = m.name
                return m.name
        st.session_state.active_model = "gemini-pro"
        return "gemini-pro"
    except:
        return "gemini-pro"

def generate_strategy(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""أنت خبير أبحاث تسويقية من مدرسة Agora العملاقة.
        المطلوب: دراسة سوق لمنتج: {product_name}.
        ⚠️ ركز على: 1. الآلية الفريدة، 2. الحجة التي لا تقهر، 3. المعتقدات الأساسية، 4. فجوات السوق.
        اكتب باللغة العربية الفصحى بشكل منظم وواضح."""
        return model.generate_content(prompt).text
    except Exception as e:
        return f"خطأ: {str(e)}"

def generate_html_page(api_key, product_name, strategy_text, product_color):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""أنت أعظم مبرمج ومصمم لصفحات الهبوط البصرية (Visual-First) وخبير Copywriting بمستوى دان كينيدي.
        المطلوب: برمجة كود HTML و CSS متكامل لصفحة هبوط لمنتج: {product_name}.
        ألوان الهوية المطلوبة للمنتج: {product_color}.
        
        🧠 **[قانون تسويقي صارم جداً]:** يجب أن تُبنى جميع النصوص (العناوين، الفقرات، وزوايا البيع) حرفياً وبذكاء تسويقي عالي بناءً على هذا التقرير الاستراتيجي:
        --- بداية التقرير ---
        {strategy_text}
        --- نهاية التقرير ---
        ⚠️ تأكد من دمج (الآلية الفريدة، الحجة التي لا تقهر، وفجوات السوق) داخل نصوص الصفحة لكسر كل اعتراضات العميل الشرائية. لا تكتب نصوصاً عشوائية، بل اجعل كل كلمة تخدم زاوية بيع من التقرير.
        
        ⚠️ قوانين التصميم الإلزامية (تحديث CRO):
        - ابدأ الكود بـ <html lang="ar" dir="rtl"> إجبارياً.
        - تناسق الألوان: صمم الـ CSS بحيث تكون ألوان الأزرار، الخلفيات، والعناصر متوافقة تماماً وبشكل أنيق مع الألوان المحددة: ({product_color}).
        - شريط الثقة: أضف <div id="top-trust-bar"> في أعلى الصفحة تماماً.
        - التصميم (Mobile First) بعرض أقصى 480px متمركز في المنتصف.
        
        ⚠️ الأقسام الـ 13 الإلزامية (يجب أن تتسلسل بهذا الترتيب لتشكيل قمع مبيعات متكامل، استخدم روابط وهمية للصور/الفيديوهات):
        1. <section id="hero">: فيديو خلفية (البطل)، تحته العنوان الصغير الجذاب (مستوحى من الحجة التي لا تقهر)، وزر طلب.
        2. <section id="trust-icons"> (القسم 13 الجديد): قسم الأيقونات السريعة أسفل الهيرو (مثل: جودة أصلية 100%، آمن ومجرب، توصيل سريع). 3 أو 4 أيقونات دائرية صغيرة.
        3. <section id="problem">: صورة GIF توضح المشكلة (اضرب على ألم العميل المذكور في التقرير).
        4. <section id="solution">: صورة GIF توضح الحل.
        5. <section id="unique-mechanism">: صورة تشرح الآلية الفريدة (Agora) المذكورة في التقرير.
        6. <section id="benefits-grid">: 4 صور مربعة للنتائج المرغوبة.
        7. <section id="comparison">: صورتين متجاورتين للمقارنة (توضح فجوة السوق للماسكات التقليدية).
        8. <section id="ingredients">: 3 أيقونات للخصائص والمكونات.
        9. <section id="social-proof">: 3 فيديوهات ريلز لآراء العملاء.
        10. <section id="expert-authority">: اقتباس لخبير يثبت المعتقدات الأساسية.
        11. <section id="how-to-use">: 3 خطوات مصورة بسيطة.
        12. <section id="risk-reversal">: ختم ضمان ضخم يزيل المخاطرة تماماً.
        13. <section id="urgency-cta">: زر عائم بالأسفل (Sticky CTA) مع عداد ندرة.
        
        أعطني فقط كود الـ HTML والـ CSS المدمج داخل علامتي ```html و ```."""
        
        response = model.generate_content(prompt)
        code = response.text
        
        # تنظيف الكود لضمان عرضه في Streamlit
        clean_code = re.sub(r'
