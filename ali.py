import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re
import urllib.parse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine - Ultimate Categorized", layout="wide", page_icon="💎")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: linear-gradient(90deg, #1e293b, #0f172a); color: white; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>💎 ALI Growth Engine (الذكاء الصوري + الفئات)</h1><p style="color:#94a3b8; margin:0;">قوالب مخصصة للأدوات الذكية (Gadgets) ومستحضرات التجميل (Cosmetics)</p></div>', unsafe_allow_html=True)

# ==========================================================
# 🧱 الخطوة 2: نظام القوالب المنفصلة (تجميل vs أدوات ذكية)
# ==========================================================

TEMPLATES = {
    # ---------------------------------------------------------
    # 💄 قالب مستحضرات التجميل (مكونات، مقارنة، نتائج قبل وبعد)
    # ---------------------------------------------------------
    "Cosmetics": """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            :root { --primary: {{COLOR_PRIMARY}}; --secondary: {{COLOR_SECONDARY}}; --accent: {{COLOR_ACCENT}}; }
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
            
            <div class="bg-gray-900 text-white text-center py-2 text-xs font-bold flex justify-center gap-4">
                <span>🚚 شحن سريع مجاني</span><span>🔒 دفع آمن 100%</span>
            </div>

            <!-- Hero Section -->
            <section class="no-pad relative w-full bg-gray-900">
                <img src="https://image.pollinations.ai/prompt/{{IMAGE_HERO}}?width=800&height=1000&nologo=true" class="w-full h-[500px] object-cover opacity-90">
                <div class="absolute bottom-0 left-0 w-full h-3/4 bg-gradient-to-t from-[var(--primary)] to-transparent"></div>
                <div class="absolute bottom-0 left-0 w-full p-6 text-white text-center z-10">
                    <div class="inline-block bg-accent text-white px-4 py-1 rounded-full text-xs font-black mb-4 shadow-lg animate-pulse">سر الجمال</div>
                    <h1 class="text-4xl font-black mb-3 leading-tight">{{HERO_HEADLINE}}</h1>
                    <p class="text-lg font-bold text-gray-100 mb-6">{{HERO_SUB}}</p>
                </div>
            </section>

            <!-- Problem -->
            <section class="bg-primary text-white text-center rounded-b-3xl shadow-md z-20">
                <h2 class="text-2xl font-black mb-5 text-accent">⚠️ {{PROBLEM_TITLE}}</h2>
                <img src="https://image.pollinations.ai/prompt/{{IMAGE_PROBLEM}}?width=600&height=400&nologo=true" class="w-full h-56 object-cover rounded-2xl border-4 border-white shadow-lg mb-5">
                <p class="text-lg font-bold leading-relaxed">{{PROBLEM_DESC}}</p>
            </section>

            <!-- Solution -->
            <section class="bg-white text-center">
                <h2 class="text-3xl font-black text-primary mb-4">✨ {{SOLUTION_TITLE}}</h2>
                <p class="text-lg text-gray-700 font-bold mb-8">{{SOLUTION_DESC}}</p>
                <img src="https://image.pollinations.ai/prompt/{{IMAGE_SOLUTION}}?width=800&height=600&nologo=true" class="w-full h-64 object-cover rounded-2xl shadow-lg border border-gray-200">
            </section>

            <!-- Results (Before & After) -->
            <section class="bg-secondary text-center">
                <h2 class="text-3xl font-black text-gray-900 mb-6">{{RESULTS_TITLE}}</h2>
                <div class="flex gap-2 relative">
                    <div class="w-1/2 relative">
                        <img src="https://image.pollinations.ai/prompt/{{IMAGE_BEFORE}}?width=400&height=500&nologo=true" class="w-full h-48 object-cover rounded-r-2xl border-2 border-red-500">
                        <div class="absolute bottom-2 right-2 bg-red-600 text-white px-2 py-1 text-xs font-bold rounded">قبل</div>
                    </div>
                    <div class="w-1/2 relative">
                        <img src="https://image.pollinations.ai/prompt/{{IMAGE_AFTER}}?width=400&height=500&nologo=true" class="w-full h-48 object-cover rounded-l-2xl border-2 border-green-500">
                        <div class="absolute bottom-2 left-2 bg-green-600 text-white px-2 py-1 text-xs font-bold rounded">بعد</div>
                    </div>
                    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-accent text-white w-10 h-10 flex items-center justify-center rounded-full border-4 border-white shadow-lg font-black text-xl z-10">></div>
                </div>
            </section>

            <!-- Ingredients -->
            <section class="bg-primary text-white text-center">
                <h2 class="text-3xl font-black text-accent mb-8">السر في مكوناتنا الطبيعية</h2>
                <div class="grid grid-cols-1 gap-5">
                    {{INGREDIENTS_HTML}}
                </div>
            </section>

            <!-- Comparison -->
            <section class="bg-white">
                <h2 class="text-3xl font-black text-center text-primary mb-8">لماذا نحن الأفضل؟</h2>
                {{COMPARISON_HTML}}
            </section>

            <!-- Reviews -->
            <section class="bg-secondary border-t border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">تجارب حقيقية لعملائنا</h2>
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
                    <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-6 rounded-xl text-2xl w-full text-center shadow-lg transition transform hover:scale-[1.02] flex justify-center items-center gap-3">
                        <span>🛒</span> {{CTA_BUTTON}}
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """,

    # ---------------------------------------------------------
    # ⚙️ قالب الأدوات الذكية (Gadgets - مقاسات، كيفية الاستعمال)
    # ---------------------------------------------------------
    "Gadgets": """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            :root { --primary: {{COLOR_PRIMARY}}; --secondary: {{COLOR_SECONDARY}}; --accent: {{COLOR_ACCENT}}; }
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
            
            <div class="bg-gray-900 text-white text-center py-2 text-xs font-bold flex justify-center gap-4">
                <span>🚚 توصيل مجاني</span><span>💳 الدفع عند الاستلام</span>
            </div>

            <!-- Hero -->
            <section class="no-pad relative w-full bg-gray-900">
                <img src="https://image.pollinations.ai/prompt/{{IMAGE_HERO}}?width=800&height=1000&nologo=true" class="w-full h-[500px] object-cover opacity-90">
                <div class="absolute bottom-0 left-0 w-full h-3/4 bg-gradient-to-t from-[var(--primary)] to-transparent"></div>
                <div class="absolute bottom-0 left-0 w-full p-6 text-white text-center z-10">
                    <div class="inline-block bg-accent text-gray-900 px-4 py-1 rounded-full text-xs font-black mb-4 shadow-lg animate-pulse border border-white/30">تصميم عصري متطور</div>
                    <h1 class="text-4xl font-black mb-3 leading-tight">{{HERO_HEADLINE}}</h1>
                    <p class="text-lg font-bold text-gray-100 mb-6">{{HERO_SUB}}</p>
                </div>
            </section>

            <!-- Problem -->
            <section class="bg-white text-center pb-10 pt-8 px-6">
                <h2 class="text-2xl font-black mb-5 text-red-600">⚠️ {{PROBLEM_TITLE}}</h2>
                <img src="https://image.pollinations.ai/prompt/{{IMAGE_PROBLEM}}?width=600&height=400&nologo=true" class="w-full h-56 object-cover rounded-2xl shadow-md mb-5">
                <p class="text-lg font-bold text-gray-700">{{PROBLEM_DESC}}</p>
            </section>

            <!-- Solution -->
            <section class="bg-primary text-white text-center rounded-t-3xl shadow-[0_-10px_20px_rgba(0,0,0,0.1)] relative z-20">
                <h2 class="text-3xl font-black text-accent mb-4 drop-shadow-sm">✨ {{SOLUTION_TITLE}}</h2>
                <p class="text-lg font-bold mb-8">{{SOLUTION_DESC}}</p>
                <img src="https://image.pollinations.ai/prompt/{{IMAGE_SOLUTION}}?width=800&height=600&nologo=true" class="w-full h-64 object-cover rounded-2xl shadow-xl border-4 border-white">
            </section>

            <!-- How to Use (GIF placeholder & Steps) -->
            <section class="bg-secondary text-center border-b border-gray-200">
                <h2 class="text-3xl font-black text-gray-900 mb-6">{{HOW_TO_USE_TITLE}}</h2>
                <div class="relative w-full mb-8 group">
                    <img src="https://image.pollinations.ai/prompt/{{IMAGE_USAGE}}?width=600&height=400&nologo=true" class="w-full rounded-2xl shadow-md border-2 border-accent object-cover opacity-90 group-hover:opacity-100 transition">
                    <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                        <div class="bg-black/60 text-white rounded-full w-16 h-16 flex items-center justify-center text-3xl border-2 border-white">▶</div>
                    </div>
                </div>
                <div class="space-y-4 text-right">
                    {{STEPS_HTML}}
                </div>
            </section>

            <!-- Dimensions & Specs -->
            <section class="bg-white border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-primary mb-8">⚙️ {{DIMENSIONS_TITLE}}</h2>
                <div class="flex flex-col gap-6">
                    <img src="https://image.pollinations.ai/prompt/{{IMAGE_DIMENSIONS}}?width=600&height=400&nologo=true" class="w-full h-48 rounded-2xl shadow-md border border-gray-100 object-cover">
                    <ul class="space-y-3 w-full text-right">
                        {{DIMENSIONS_HTML}}
                    </ul>
                </div>
            </section>

            <!-- Benefits Grid -->
            <section class="bg-gray-50 border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">ميزات تجعله الأفضل</h2>
                <div class="grid grid-cols-1 gap-4">
                    {{BENEFITS_HTML}}
                </div>
            </section>

            <!-- Reviews -->
            <section class="bg-white border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-primary mb-8">تقييمات العملاء</h2>
                <div class="space-y-5">
                    {{REVIEWS_HTML}}
                </div>
            </section>

            <!-- FAQ -->
            <section class="bg-secondary border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">❓ أسئلة متكررة</h2>
                <div class="space-y-4 text-right">
                    {{FAQ_HTML}}
                </div>
            </section>

            <!-- Guarantee -->
            <section class="bg-gray-900 text-center pb-20 text-white rounded-t-3xl mt-4">
                <div class="text-6xl mb-4">🛡️</div>
                <h3 class="text-3xl font-black text-accent mb-4">ضمان جودة</h3>
                <p class="text-lg font-bold text-gray-300">{{GUARANTEE}}</p>
            </section>

            <!-- Sticky CTA -->
            <div id="buy" class="fixed bottom-0 left-0 w-full bg-white/95 backdrop-blur-sm p-4 shadow-[0_-15px_30px_rgba(0,0,0,0.15)] flex justify-center z-50 border-t-4 border-accent">
                <div class="w-full max-w-lg flex flex-col items-center">
                    <a href="#buy" class="bg-accent hover:opacity-90 text-gray-900 font-black py-4 px-6 rounded-xl text-2xl w-full text-center shadow-lg transition transform hover:scale-[1.02] flex justify-center items-center gap-3">
                        <span>🛒</span> {{CTA_BUTTON}}
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
}

# ==========================================================
# 🧠 الخطوة 1: المحرك اللفظي المعزز (حسب الفئة المختارة)
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
    
    if "Cosmetics" in category:
        prompt = f"""
        أنت أعظم خبير تسويق لصفحات الهبوط. المنتج: "{product}". الفئة: مستحضرات تجميل وعناية.
        ⚠️ قانون صارم: جميع النصوص التي يقرأها العميل يجب أن تكون بـ "العربية الفصحى". حقول الصور (image_prompts) فقط بالإنجليزية.
        رد بصيغة JSON صالحة بهذا الهيكل:
        {{
            "hero_headline": "عنوان رئيسي قصير وصادم (عربي)",
            "hero_subheadline": "عنوان فرعي (عربي)",
            "image_hero_prompt": "English prompt for AI image showing the cosmetic product in a beautiful studio shot. highly detailed",
            "problem_title": "عنوان المشكلة (عربي)",
            "problem_description": "وصف المشكلة بشكل عاطفي (عربي)",
            "image_problem_prompt": "English prompt for AI image showing a person frustrated with skin or hair problem.",
            "solution_title": "عنوان الحل (عربي)",
            "solution_description": "كيف يحل المنتج المشكلة (عربي)",
            "image_solution_prompt": "English prompt for AI image showing a happy person with perfect glowing skin or hair.",
            "results_title": "عنوان لنتائج قبل وبعد (عربي)",
            "image_before_prompt": "English prompt for before image (bad skin or messy hair).",
            "image_after_prompt": "English prompt for after image (perfect skin or beautiful hair).",
            "ingredients": [
                {{"name": "اسم المكون (عربي)", "desc": "فائدته (عربي)", "image_prompt": "English prompt for macro photo of this natural ingredient"}}
            ],
            "comparison": {{
                "our_product": "اسم منتجنا (عربي)",
                "others": "المنتجات التقليدية (عربي)",
                "rows": [
                    {{"feature": "ميزة 1 طبيعية (عربي)", "us": "نعم", "them": "لا"}},
                    {{"feature": "ميزة 2 سريعة (عربي)", "us": "نعم", "them": "لا"}}
                ]
            }},
            "reviews": [
                {{"name": "سارة م.", "rating": 5, "comment": "تعليق إيجابي (عربي)"}}
            ],
            "faq": [
                {{"q": "سؤال شائع؟ (عربي)", "a": "إجابة (عربي)"}}
            ],
            "guarantee": "نص ضمان (عربي)",
            "call_to_action": "نص الزر (عربي)"
        }}
        """
    else:
        prompt = f"""
        أنت أعظم خبير تسويق لصفحات الهبوط. المنتج: "{product}". الفئة: أدوات وأجهزة ذكية (Gadgets).
        ⚠️ قانون صارم: جميع النصوص التي يقرأها العميل يجب أن تكون بـ "العربية الفصحى". حقول الصور (image_prompts) فقط بالإنجليزية.
        رد بصيغة JSON صالحة بهذا الهيكل:
        {{
            "hero_headline": "عنوان رئيسي قصير وصادم (عربي)",
            "hero_subheadline": "عنوان فرعي (عربي)",
            "image_hero_prompt": "English prompt for AI image showing the modern smart gadget, sleek design, studio lighting",
            "problem_title": "عنوان المشكلة (عربي)",
            "problem_description": "وصف المشكلة بشكل عاطفي (عربي)",
            "image_problem_prompt": "English prompt for AI image showing someone struggling with a daily task.",
            "solution_title": "عنوان الحل (عربي)",
            "solution_description": "كيف يحل المنتج المشكلة بسهولة (عربي)",
            "image_solution_prompt": "English prompt for AI image showing someone easily doing the task using the gadget.",
            "how_to_use_title": "كيفية الاستعمال (عربي)",
            "image_usage_prompt": "English prompt for AI image illustrating the gadget in action.",
            "steps": ["الخطوة 1 (عربي)", "الخطوة 2 (عربي)", "الخطوة 3 (عربي)"],
            "dimensions_title": "المقاسات والمواصفات (عربي)",
            "image_dimensions_prompt": "English prompt for an infographic image showing the gadget with measurement lines.",
            "dimensions_list": ["الطول: ..", "الوزن: ..", "الخامة: .."],
            "benefits": ["ميزة ذكية 1 (عربي)", "ميزة ذكية 2 (عربي)"],
            "reviews": [
                {{"name": "أحمد خ.", "rating": 5, "comment": "تعليق إيجابي (عربي)"}}
            ],
            "faq": [
                {{"q": "سؤال شائع حول الأداة؟ (عربي)", "a": "إجابة (عربي)"}}
            ],
            "guarantee": "نص ضمان الجودة (عربي)",
            "call_to_action": "نص الزر (عربي)"
        }}
        """
    
    response = model.generate_content(prompt, request_options={"timeout": 30.0})
    tb = chr(96) * 3 
    clean_text = re.sub(f'{tb}(?:json|JSON)?', '', response.text, flags=re.IGNORECASE)
    clean_text = clean_text.replace(tb, '').strip()
    match = re.search(r'\{.*\}', clean_text, re.DOTALL)
    if match: return match.group(0)
    return clean_text

# ==========================================================
# 💉 الخطوة 3: محرك الحقن المتقدم (ألوان + نصوص + صور مخصصة للفئات)
# ==========================================================
def safe_quote(text):
    return urllib.parse.quote(str(text).replace('\n', ' ').strip())

def inject_data_into_template(json_data, category, colors):
    template_key = "Cosmetics" if "Cosmetics" in category else "Gadgets"
    final_html = TEMPLATES[template_key]
    
    # 1. الأسئلة الشائعة (مشتركة)
    faq_html = ""
    for faq in json_data.get('faq', [])[:3]:
        faq_html += f'''
        <div class="bg-white p-5 rounded-2xl shadow-sm border-r-4 border-primary">
            <h4 class="font-black text-gray-900 mb-2 text-lg">❓ {faq.get('q')}</h4>
            <p class="text-gray-700 text-sm font-bold leading-relaxed">{faq.get('a')}</p>
        </div>'''

    # 2. التقييمات (مشتركة)
    reviews_html = ""
    for rev in json_data.get('reviews', [])[:3]:
        stars = '⭐' * int(rev.get('rating', 5))
        reviews_html += f'''
        <div class="bg-gray-50 p-6 rounded-2xl border border-gray-200 shadow-sm">
            <div class="flex justify-between items-center mb-3">
                <span class="font-black text-primary text-lg">{rev.get('name')}</span>
                <span class="text-accent text-sm">{stars}</span>
            </div>
            <p class="text-gray-700 font-bold italic leading-relaxed">"{rev.get('comment')}"</p>
            <div class="mt-3 text-xs text-green-600 font-black flex items-center gap-1"><span>✅</span> مشتري موثق</div>
        </div>'''
        
    final_html = final_html.replace("{{FAQ_HTML}}", faq_html)
    final_html = final_html.replace("{{REVIEWS_HTML}}", reviews_html)

    # ----------------------------------------------------
    # حقن بيانات التجميل (Cosmetics)
    # ----------------------------------------------------
    if template_key == "Cosmetics":
        ingredients_html = ""
        for ing in json_data.get('ingredients', [])[:3]:
            name, desc = ing.get('name', ''), ing.get('desc', '')
            ing_prompt = safe_quote(ing.get('image_prompt', f"macro photography of {name}"))
            ingredients_html += f'''
            <div class="bg-white/10 backdrop-blur-sm p-4 rounded-2xl border border-white/20 flex items-center gap-5 text-right shadow-lg">
                <img src="https://image.pollinations.ai/prompt/{ing_prompt}?width=200&height=200&nologo=true" class="w-24 h-24 rounded-full shadow-lg border-2 border-accent object-cover flex-shrink-0 bg-white">
                <div><h4 class="font-black text-accent text-xl mb-1">{name}</h4><p class="text-sm font-medium text-gray-100">{desc}</p></div>
            </div>'''
            
        comparison_html = ""
        comp = json_data.get('comparison', {})
        if comp:
            our_name = comp.get('our_product', 'منتجنا')
            others_name = comp.get('others', 'المنتجات العادية')
            rows_html = ""
            for row in comp.get('rows', []):
                us_icon = "✅" if row.get('us') == "نعم" else "❌"
                them_icon = "✅" if row.get('them') == "نعم" else "❌"
                rows_html += f'''<tr class="border-b border-gray-100">
                    <td class="p-4 text-gray-800 font-bold">{row.get('feature')}</td>
                    <td class="p-4 text-center bg-green-50 border-x text-green-600 font-black">{us_icon}</td>
                    <td class="p-4 text-center text-red-500 font-black">{them_icon}</td>
                </tr>'''
            comparison_html = f'''
            <div class="overflow-x-auto rounded-2xl shadow-md border border-gray-200 bg-white">
                <table class="w-full text-right border-collapse">
                    <thead>
                        <tr class="bg-gray-100 text-gray-700">
                            <th class="p-4 font-bold border-b">الميزة</th>
                            <th class="p-4 font-black text-accent bg-green-50 border-b border-x">{our_name}</th>
                            <th class="p-4 font-bold border-b">{others_name}</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>'''
            
        final_html = final_html.replace("{{RESULTS_TITLE}}", json_data.get("results_title", "تحول مذهل تلاحظه فوراً!"))
        final_html = final_html.replace("{{IMAGE_BEFORE}}", safe_quote(json_data.get("image_before_prompt", "bad condition skin or hair")))
        final_html = final_html.replace("{{IMAGE_AFTER}}", safe_quote(json_data.get("image_after_prompt", "perfect condition skin or hair")))
        final_html = final_html.replace("{{INGREDIENTS_HTML}}", ingredients_html)
        final_html = final_html.replace("{{COMPARISON_HTML}}", comparison_html)

    # ----------------------------------------------------
    # حقن بيانات الأدوات الذكية (Gadgets)
    # ----------------------------------------------------
    else:
        steps_html = ""
        for i, step in enumerate(json_data.get('steps', [])[:3], 1):
            steps_html += f'''
            <div class="flex items-center gap-4 bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                <div class="w-12 h-12 flex items-center justify-center bg-[var(--primary)] text-white font-black rounded-full flex-shrink-0 text-xl shadow-md">{i}</div>
                <p class="font-bold text-gray-800 text-lg">{step}</p>
            </div>'''
            
        dimensions_html = ""
        for dim in json_data.get('dimensions_list', [])[:4]:
            dimensions_html += f'''
            <li class="flex items-center gap-3 bg-gray-50 p-3 rounded-lg border border-gray-100">
                <span class="text-accent text-xl">📏</span><span class="font-bold text-gray-700">{dim}</span>
            </li>'''
            
        benefits_html = ""
        for benefit in json_data.get('benefits', [])[:4]:
            benefits_html += f'''
            <div class="bg-white p-5 rounded-xl flex items-center gap-4 shadow-sm border border-gray-200">
                <div class="w-12 h-12 flex-shrink-0 bg-blue-50 rounded-full flex items-center justify-center border border-blue-100">
                    <span class="text-2xl text-blue-500">⚡</span>
                </div>
                <p class="font-bold text-gray-800 text-lg text-right">{benefit}</p>
            </div>'''

        final_html = final_html.replace("{{HOW_TO_USE_TITLE}}", json_data.get("how_to_use_title", "سهولة تامة في الاستخدام"))
        final_html = final_html.replace("{{IMAGE_USAGE}}", safe_quote(json_data.get("image_usage_prompt", "using the gadget easily")))
        final_html = final_html.replace("{{STEPS_HTML}}", steps_html)
        final_html = final_html.replace("{{DIMENSIONS_TITLE}}", json_data.get("dimensions_title", "المقاسات والمواصفات"))
        final_html = final_html.replace("{{IMAGE_DIMENSIONS}}", safe_quote(json_data.get("image_dimensions_prompt", "gadget size dimensions infographic")))
        final_html = final_html.replace("{{DIMENSIONS_HTML}}", dimensions_html)
        final_html = final_html.replace("{{BENEFITS_HTML}}", benefits_html)

    # ----------------------------------------------------
    # حقن النصوص المشتركة الأساسية
    # ----------------------------------------------------
    final_html = final_html.replace("{{COLOR_PRIMARY}}", colors['primary'])
    final_html = final_html.replace("{{COLOR_SECONDARY}}", colors['secondary'])
    final_html = final_html.replace("{{COLOR_ACCENT}}", colors['accent'])

    final_html = final_html.replace("{{IMAGE_HERO}}", safe_quote(json_data.get("image_hero_prompt", "product high quality")))
    final_html = final_html.replace("{{IMAGE_PROBLEM}}", safe_quote(json_data.get("image_problem_prompt", "problem frustration")))
    final_html = final_html.replace("{{IMAGE_SOLUTION}}", safe_quote(json_data.get("image_solution_prompt", "solution happiness")))
    
    final_html = final_html.replace("{{HERO_HEADLINE}}", json_data.get("hero_headline", "اكتشف الحل الأمثل"))
    final_html = final_html.replace("{{HERO_SUB}}", json_data.get("hero_subheadline", "المنتج الذي سيغير حياتك."))
    final_html = final_html.replace("{{PROBLEM_TITLE}}", json_data.get("problem_title", "هل تعاني من هذه المشكلة؟"))
    final_html = final_html.replace("{{PROBLEM_DESC}}", json_data.get("problem_description", "وصف المشكلة..."))
    final_html = final_html.replace("{{SOLUTION_TITLE}}", json_data.get("solution_title", "الحل النهائي"))
    final_html = final_html.replace("{{SOLUTION_DESC}}", json_data.get("solution_description", "وصف الحل..."))
    final_html = final_html.replace("{{GUARANTEE}}", json_data.get("guarantee", "ضمان استرجاع الأموال."))
    final_html = final_html.replace("{{CTA_BUTTON}}", json_data.get("call_to_action", "اطلب الآن"))
    
    return final_html

# --- واجهة المستخدم (Sidebar & Main) ---
with st.sidebar:
    st.header("⚙️ إعدادات المحرك")
    api_key = st.text_input("🔑 أدخل API Key", type="password")
    product_name = st.text_input("📦 اسم/وصف المنتج", placeholder="مثال: شامبو طبيعي لنمو الشعر")
    
    st.markdown("---")
    st.subheader("📦 فئة المنتج (تحدد هيكل الصفحة)")
    product_category = st.selectbox("اختر فئة المنتج:", [
        "💄 مستحضرات تجميل وعناية (Cosmetics)", 
        "⚙️ أدوات وأجهزة ذكية (Gadgets)"
    ])

    st.markdown("---")
    st.subheader("🎨 تخصيص ألوان المنتج")
    col1, col2 = st.columns(2)
    with col1:
        color_primary = st.color_picker("اللون الأساسي", "#0f766e" if "Cosmetics" in product_category else "#1f2937")
    with col2:
        color_accent = st.color_picker("لون الزر", "#eab308" if "Cosmetics" in product_category else "#ef4444")
    color_secondary = st.color_picker("اللون الثانوي", "#f8fafc")
    
    colors_dict = {'primary': color_primary, 'secondary': color_secondary, 'accent': color_accent}
    
    st.markdown("---")
    start_btn = st.button("⚡ توليد الصفحة الذكية", use_container_width=True)
    
    if 'json_data' in st.session_state:
        st.markdown("---")
        change_theme_btn = st.button("🔄 تحديث الألوان/التصميم فقط", use_container_width=True)
        if change_theme_btn:
            st.session_state.final_page = inject_data_into_template(st.session_state.json_data, product_category, colors_dict)
            st.rerun()

if start_btn:
    if not api_key or not product_name:
        st.error("يرجى إدخال المفتاح واسم المنتج أولاً.")
    else:
        with st.spinner("1️⃣ جاري هندسة المحتوى وكتابة أوامر الصور (يستغرق 15 ثانية)..."):
            try:
                raw_json = generate_landing_page_json(api_key, product_name, product_category)
                parsed_data = json.loads(raw_json)
                
                with st.spinner("2️⃣ جاري تجميع الصفحة وتوليد الصور تلقائياً..."):
                    st.session_state.final_page = inject_data_into_template(parsed_data, product_category, colors_dict)
                    st.session_state.json_data = parsed_data
                    st.session_state.current_colors = colors_dict
                    st.session_state.current_category = product_category
                    
                st.success("🎉 اكتمل بناء صفحة الإنفوجرافيك الخارقة! انظر التبويبات.")
            except json.JSONDecodeError:
                st.error("⚠️ حدث خطأ في قراءة الاستجابة. المحاولة مرة أخرى ستحلها.")
            except Exception as e:
                st.error(f"🛑 خطأ: {str(e)}")

# --- العرض (التبويبات) ---
if 'final_page' in st.session_state:
    tab1, tab2 = st.tabs(["📱 المعاينة البصرية الحية", "💻 كود HTML للنسخ"])
    
    with tab1:
        st.info(f"💡 الفئة المحددة: **{st.session_state.get('current_category', product_category)}**. الصور تولد حالياً عبر الذكاء الاصطناعي بناءً على وصف منتجك.")
        components.html(st.session_state.final_page, height=1200, scrolling=True)
        
    with tab2:
        st.write("انسخ هذا الكود بالكامل، ستجد أن روابط الصور قد تم توليدها برمجياً بالفعل.")
        st.code(st.session_state.final_page, language="html")
