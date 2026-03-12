import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re
import urllib.parse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine - 1-Click Magic", layout="wide", page_icon="⚡")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: linear-gradient(90deg, #1e293b, #0f172a); color: white; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>⚡ ALI Growth Engine (بضغطة زر)</h1><p style="color:#94a3b8; margin:0;">صفحات هبوط كاملة (نصوص + صور ذكية) ببرومت واحد فقط</p></div>', unsafe_allow_html=True)

# ==========================================================
# 🧱 الخطوة 2: القالب الشامل (1-Click Template)
# ==========================================================

MASTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: {{COLOR_PRIMARY}};
            --secondary: {{COLOR_SECONDARY}};
            --accent: {{COLOR_ACCENT}};
        }
        body { font-family: 'Cairo', sans-serif; background-color: #e5e7eb; scroll-behavior: smooth; }
        .bg-primary { background-color: var(--primary); }
        .bg-secondary { background-color: var(--secondary); }
        .bg-accent { background-color: var(--accent); }
        .text-primary { color: var(--primary); }
        .text-accent { color: var(--accent); }
        section { position: relative; padding: 3rem 1.5rem; }
        .no-pad { padding: 0 !important; }
    </style>
</head>
<body class="text-gray-800 antialiased pb-24 flex justify-center">
    <div class="w-full max-w-lg bg-white shadow-2xl relative overflow-hidden">
        
        <!-- Trust Bar -->
        <div class="bg-gray-900 text-white text-center py-2 text-xs font-bold flex justify-center gap-4">
            <span>🚚 شحن سريع مجاني</span><span>🔒 دفع آمن 100%</span>
        </div>

        <!-- Hero Section -->
        <section class="no-pad relative w-full bg-gray-900">
            <img src="https://image.pollinations.ai/prompt/{{IMAGE_HERO}}?width=800&height=1000&nologo=true" class="w-full h-[500px] object-cover opacity-90">
            <div class="absolute bottom-0 left-0 w-full h-3/4 bg-gradient-to-t from-[var(--primary)] to-transparent"></div>
            <div class="absolute bottom-0 left-0 w-full p-6 text-white text-center z-10">
                <div class="inline-block bg-accent text-white px-4 py-1 rounded-full text-xs font-black mb-4 shadow-lg animate-pulse">عرض حصري</div>
                <h1 class="text-4xl font-black mb-3 leading-tight drop-shadow-md">{{HERO_HEADLINE}}</h1>
                <p class="text-lg font-bold text-gray-100 mb-6 drop-shadow">{{HERO_SUB}}</p>
                <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-8 rounded-full text-xl w-full block shadow-lg transition transform hover:scale-105">{{CTA_BUTTON}}</a>
            </div>
        </section>

        <!-- Problem Section -->
        <section class="bg-white text-center">
            <h2 class="text-2xl font-black mb-5 text-red-600">⚠️ {{PROBLEM_TITLE}}</h2>
            <img src="https://image.pollinations.ai/prompt/{{IMAGE_PROBLEM}}?width=600&height=400&nologo=true" class="w-full h-56 object-cover rounded-2xl shadow-md mb-5">
            <p class="text-lg font-bold text-gray-700 leading-relaxed">{{PROBLEM_DESC}}</p>
        </section>

        <!-- Solution Section -->
        <section class="bg-primary text-white text-center rounded-3xl shadow-lg relative z-20 mx-2">
            <h2 class="text-3xl font-black text-accent mb-4 drop-shadow-sm">✨ {{SOLUTION_TITLE}}</h2>
            <p class="text-lg font-bold mb-6 text-gray-100">{{SOLUTION_DESC}}</p>
            <img src="https://image.pollinations.ai/prompt/{{IMAGE_SOLUTION}}?width=800&height=600&nologo=true" class="w-full h-64 object-cover rounded-2xl shadow-xl border-4 border-white">
        </section>

        <!-- Benefits & Features -->
        <section class="bg-secondary mt-4">
            <h2 class="text-3xl font-black text-center text-gray-900 mb-8 drop-shadow-sm">لماذا نحن الخيار الأفضل؟</h2>
            <div class="grid grid-cols-1 gap-4 mb-8">
                {{BENEFITS_HTML}}
            </div>
            <div class="bg-white p-5 rounded-2xl border border-gray-200 text-right shadow-sm">
                <h3 class="font-black text-gray-900 text-xl mb-3 flex items-center gap-2"><span>⚙️</span> {{MECHANISM_TITLE}}</h3>
                <p class="text-base font-bold text-gray-600 leading-relaxed">{{MECHANISM_DESC}}</p>
            </div>
        </section>

        <!-- Dynamic Section (Ingredients or Steps) -->
        <section class="bg-white border-t border-gray-100">
             {{DYNAMIC_SECTION_HTML}}
        </section>

        <!-- Reviews -->
        <section class="bg-secondary border-t border-gray-200">
            <h2 class="text-3xl font-black text-center text-primary mb-8">تجارب حقيقية لعملائنا</h2>
            <div class="space-y-5">
                {{REVIEWS_HTML}}
            </div>
        </section>

        <!-- FAQ -->
        <section class="bg-white border-t border-gray-100">
            <h2 class="text-3xl font-black text-center text-gray-900 mb-8">❓ الأسئلة الشائعة</h2>
            <div class="space-y-4 text-right">
                {{FAQ_HTML}}
            </div>
        </section>

        <!-- Guarantee -->
        <section class="bg-primary text-center pb-20 text-white rounded-t-3xl mt-4">
            <div class="text-6xl mb-4">🛡️</div>
            <h3 class="text-3xl font-black text-accent mb-4">ضمان جودة 100%</h3>
            <p class="text-lg font-bold text-gray-100">{{GUARANTEE}}</p>
        </section>

        <!-- Sticky CTA -->
        <div id="buy" class="fixed bottom-0 left-0 w-full bg-white/95 backdrop-blur-sm p-4 shadow-[0_-15px_30px_rgba(0,0,0,0.15)] flex justify-center z-50 border-t-4 border-accent">
            <div class="w-full max-w-lg flex flex-col items-center">
                 <div class="text-gray-800 text-sm font-black mb-2 flex items-center gap-2 bg-gray-100 px-4 py-1 rounded-full border border-gray-200">
                    <span class="w-3 h-3 rounded-full bg-red-600 animate-ping"></span>
                    العرض ينتهي قريباً! الدفع عند الاستلام
                </div>
                <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-6 rounded-xl text-2xl w-full text-center shadow-lg transition transform hover:scale-[1.02] flex justify-center items-center gap-3">
                    <span>🛒</span> {{CTA_BUTTON}}
                </a>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ==========================================================
# 🧠 الخطوة 1: المحرك اللفظي (One-Prompt Magic)
# ==========================================================
def get_fast_working_model(api_key):
    if 'valid_model_name' in st.session_state:
        return st.session_state.valid_model_name
    genai.configure(api_key=api_key, transport="rest")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name.lower():
                st.session_state.valid_model_name = m.name
                return m.name
    except: pass
    st.session_state.valid_model_name = "gemini-pro"
    return "gemini-pro"

def generate_landing_page_json(api_key, product, category):
    genai.configure(api_key=api_key, transport="rest")
    model_name = get_fast_working_model(api_key)
    model = genai.GenerativeModel(model_name)
    
    # برومت ذكي يجمع بين التسويق وتوليد الصور
    prompt = f"""
    أنت أعظم خبير تسويق لصفحات الهبوط (Infographic Sales Pages).
    المنتج: "{product}". 
    الفئة: {"مستحضرات تجميل وعناية" if "Cosmetics" in category else "أدوات وأجهزة ذكية"}.
    
    ⚠️ قانون صارم: جميع النصوص للعميل يجب أن تكون بـ "العربية الفصحى". 
    حقول الصور (image_prompts) فقط بالإنجليزية لوصف الصورة لمولد الصور.

    رد بصيغة JSON صالحة بهذا الهيكل الدقيق:
    {{
        "hero_headline": "عنوان رئيسي قصير وصادم (عربي)",
        "hero_subheadline": "عنوان فرعي (عربي)",
        "image_hero_prompt": "English prompt for AI image showing the {product} in a beautiful studio shot, highly detailed, 4k",
        "problem_title": "عنوان المشكلة (عربي)",
        "problem_description": "وصف المشكلة بشكل عاطفي (عربي)",
        "image_problem_prompt": "English prompt for AI image showing a person frustrated with the problem that {product} solves",
        "solution_title": "عنوان الحل (عربي)",
        "solution_description": "كيف يحل المنتج المشكلة (عربي)",
        "image_solution_prompt": "English prompt for AI image showing a happy person enjoying the results of {product}",
        "mechanism_title": "كيف يعمل؟ (عربي)",
        "mechanism_description": "وصف الآلية باختصار (عربي)",
        "benefits": ["فائدة 1 (عربي)", "فائدة 2 (عربي)", "فائدة 3 (عربي)"],
        "dynamic_items": [
            {{"title": "اسم المكون أو الخطوة (عربي)", "desc": "شرح (عربي)", "image_prompt": "English prompt for macro photo or illustration of this item"}}
        ],
        "reviews": [
            {{"name": "اسم عميل", "rating": 5, "comment": "تعليق إيجابي (عربي)"}}
        ],
        "faq": [
            {{"q": "سؤال شائع؟ (عربي)", "a": "إجابة (عربي)"}}
        ],
        "guarantee": "نص ضمان (عربي)",
        "call_to_action": "نص الزر (عربي)"
    }}
    """
    
    response = model.generate_content(prompt, request_options={"timeout": 45.0})
    tb = chr(96) * 3 
    clean_text = re.sub(f'{tb}(?:json|JSON)?', '', response.text, flags=re.IGNORECASE)
    clean_text = clean_text.replace(tb, '').strip()
    match = re.search(r'\{.*\}', clean_text, re.DOTALL)
    if match: return match.group(0)
    return clean_text

# ==========================================================
# 💉 الخطوة 3: محرك الحقن (تجميع الصفحة)
# ==========================================================
def safe_quote(text):
    return urllib.parse.quote(str(text).replace('\n', ' ').strip())

def inject_data_into_template(json_data, category, colors):
    final_html = MASTER_TEMPLATE
    
    # 1. الفوائد
    benefits_html = ""
    for benefit in json_data.get('benefits', [])[:4]:
        benefits_html += f'''
        <div class="bg-white p-4 rounded-xl flex items-center gap-4 shadow-sm border border-gray-200">
            <div class="w-10 h-10 flex-shrink-0 bg-green-100 rounded-full flex items-center justify-center">
                <span class="text-xl text-green-600">✓</span>
            </div>
            <p class="font-bold text-gray-800 text-right">{benefit}</p>
        </div>'''

    # 2. القسم الديناميكي (مكونات أو خطوات مع صور ذكية)
    dynamic_html = ""
    section_title = "السر في مكوناتنا الطبيعية" if "Cosmetics" in category else "طريقة الاستخدام بخطوات بسيطة"
    dynamic_html += f'<h2 class="text-3xl font-black text-center text-primary mb-8">{section_title}</h2><div class="grid grid-cols-1 gap-5">'
    
    for item in json_data.get('dynamic_items', [])[:3]:
        title = item.get('title', '')
        desc = item.get('desc', '')
        img_prompt = safe_quote(item.get('image_prompt', f"macro photography of {title}"))
        dynamic_html += f'''
        <div class="bg-gray-50 p-4 rounded-2xl border border-gray-200 flex items-center gap-4 text-right shadow-sm">
            <img src="https://image.pollinations.ai/prompt/{img_prompt}?width=200&height=200&nologo=true" class="w-20 h-20 rounded-full shadow-md border-2 border-accent object-cover flex-shrink-0">
            <div>
                <h4 class="font-black text-primary text-lg mb-1">{title}</h4>
                <p class="text-sm font-medium text-gray-600">{desc}</p>
            </div>
        </div>'''
    dynamic_html += '</div>'

    # 3. التقييمات والأسئلة الشائعة
    reviews_html = ""
    for rev in json_data.get('reviews', [])[:3]:
        stars = '⭐' * int(rev.get('rating', 5))
        reviews_html += f'''
        <div class="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
            <div class="flex justify-between items-center mb-2">
                <span class="font-black text-primary">{rev.get('name')}</span>
                <span class="text-accent text-sm">{stars}</span>
            </div>
            <p class="text-gray-700 font-bold italic leading-relaxed text-sm">"{rev.get('comment')}"</p>
        </div>'''

    faq_html = ""
    for faq in json_data.get('faq', [])[:3]:
        faq_html += f'''
        <div class="bg-gray-50 p-4 rounded-xl shadow-sm border-r-4 border-primary">
            <h4 class="font-black text-gray-900 mb-1 text-base">❓ {faq.get('q')}</h4>
            <p class="text-gray-600 text-sm font-bold">{faq.get('a')}</p>
        </div>'''

    # حقن البيانات
    final_html = final_html.replace("{{BENEFITS_HTML}}", benefits_html)
    final_html = final_html.replace("{{DYNAMIC_SECTION_HTML}}", dynamic_html)
    final_html = final_html.replace("{{REVIEWS_HTML}}", reviews_html)
    final_html = final_html.replace("{{FAQ_HTML}}", faq_html)
    
    final_html = final_html.replace("{{COLOR_PRIMARY}}", colors['primary'])
    final_html = final_html.replace("{{COLOR_SECONDARY}}", colors['secondary'])
    final_html = final_html.replace("{{COLOR_ACCENT}}", colors['accent'])

    final_html = final_html.replace("{{IMAGE_HERO}}", safe_quote(json_data.get("image_hero_prompt", "product high quality")))
    final_html = final_html.replace("{{IMAGE_PROBLEM}}", safe_quote(json_data.get("image_problem_prompt", "problem frustration")))
    final_html = final_html.replace("{{IMAGE_SOLUTION}}", safe_quote(json_data.get("image_solution_prompt", "solution happiness")))
    
    final_html = final_html.replace("{{HERO_HEADLINE}}", json_data.get("hero_headline", ""))
    final_html = final_html.replace("{{HERO_SUB}}", json_data.get("hero_subheadline", ""))
    final_html = final_html.replace("{{PROBLEM_TITLE}}", json_data.get("problem_title", ""))
    final_html = final_html.replace("{{PROBLEM_DESC}}", json_data.get("problem_description", ""))
    final_html = final_html.replace("{{SOLUTION_TITLE}}", json_data.get("solution_title", ""))
    final_html = final_html.replace("{{SOLUTION_DESC}}", json_data.get("solution_description", ""))
    final_html = final_html.replace("{{MECHANISM_TITLE}}", json_data.get("mechanism_title", ""))
    final_html = final_html.replace("{{MECHANISM_DESC}}", json_data.get("mechanism_description", ""))
    final_html = final_html.replace("{{GUARANTEE}}", json_data.get("guarantee", ""))
    final_html = final_html.replace("{{CTA_BUTTON}}", json_data.get("call_to_action", "اطلب الآن"))
    
    return final_html

# --- واجهة المستخدم ---
with st.sidebar:
    st.header("⚙️ إعدادات بضغطة زر")
    api_key = st.text_input("🔑 Gemini API Key", type="password")
    product_name = st.text_area("📦 تفاصيل المنتج", placeholder="اكتب اسم المنتج ووصف بسيط له هنا... \nمثال: شامبو بخلاصة الصبار لعلاج تساقط الشعر.")
    
    product_category = st.selectbox("📦 الفئة", ["💄 مستحضرات تجميل وعناية (Cosmetics)", "⚙️ أدوات وأجهزة ذكية (Gadgets)"])

    st.subheader("🎨 الألوان")
    col1, col2 = st.columns(2)
    with col1: color_primary = st.color_picker("أساسي", "#0f766e" if "Cosmetics" in product_category else "#1f2937")
    with col2: color_accent = st.color_picker("الزر", "#eab308" if "Cosmetics" in product_category else "#ef4444")
    color_secondary = st.color_picker("ثانوي", "#f8fafc")
    
    colors_dict = {'primary': color_primary, 'secondary': color_secondary, 'accent': color_accent}
    
    start_btn = st.button("🚀 توليد صفحة كاملة (سحر!)", use_container_width=True)

if start_btn:
    if not api_key or not product_name:
        st.error("أدخل المفتاح ووصف المنتج.")
    else:
        with st.spinner("🤖 جاري كتابة المحتوى وتوليد الصور بالذكاء الاصطناعي... (قد يستغرق 30 ثانية)"):
            try:
                raw_json = generate_landing_page_json(api_key, product_name, product_category)
                parsed_data = json.loads(raw_json)
                st.session_state.final_page = inject_data_into_template(parsed_data, product_category, colors_dict)
                st.session_state.json_data = parsed_data
                st.success("🎉 نجاح! تم بناء الصفحة بالكامل.")
            except Exception as e:
                st.error(f"🛑 خطأ: {str(e)}")

# --- العرض ---
if 'final_page' in st.session_state:
    tab1, tab2 = st.tabs(["📱 المعاينة (نصوص + صور)", "💻 كود HTML للنسخ"])
    with tab1:
        st.info("💡 يتم الآن توليد وجلب الصور الحية من الذكاء الاصطناعي بناءً على وصف منتجك. انتظر قليلاً لتكتمل.")
        components.html(st.session_state.final_page, height=1200, scrolling=True)
    with tab2:
        st.code(st.session_state.final_page, language="html")
