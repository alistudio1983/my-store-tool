import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re
import pandas as pd
import requests
import random
import urllib.parse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine Pro - Real Images System", layout="wide", page_icon="🚀")

# --- التصميم العبقري (Premium UI/UX CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] { 
        font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; background-color: #f8fafc;
    }
    
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

    .main-header { 
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white; padding: 40px 20px; border-radius: 20px; text-align: center; margin-bottom: 35px; 
        box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.3); border-bottom: 5px solid #3b82f6; position: relative; overflow: hidden;
    }
    .main-header::before {
        content: ""; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(59,130,246,0.1) 0%, transparent 60%); animation: rotate 20s linear infinite;
    }
    .main-header h1 {
        font-weight: 900; font-size: 3rem; margin-bottom: 5px;
        background: linear-gradient(to right, #93c5fd, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; position: relative; z-index: 1;
    }
    .main-header p { color: #94a3b8; font-size: 1.2rem; font-weight: 600; position: relative; z-index: 1; }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important; color: white !important; font-weight: 800 !important;
        font-size: 1.1rem !important; border: none !important; border-radius: 12px !important; padding: 15px 30px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3) !important; width: 100%;
    }
    .stButton > button:hover { transform: translateY(-3px) scale(1.01) !important; box-shadow: 0 15px 25px -5px rgba(59, 130, 246, 0.4) !important; }

    [data-testid="stMetric"] { 
        background: white; padding: 25px 20px; border-radius: 16px; border: 1px solid #e2e8f0; text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); border-color: #cbd5e1; }
    [data-testid="stMetricValue"] { font-weight: 900 !important; color: #0f172a !important; }

    .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
        border-radius: 10px !important; border: 1px solid #cbd5e1 !important; transition: border-color 0.3s !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🚀 ALI Growth Engine Pro</h1><p>منصة العمليات التسويقية المتكاملة | صور حقيقية 100% (Pexels Integration)</p></div>', unsafe_allow_html=True)

# ==========================================================
# 🧠 دوال جلب الصور الحقيقية (Real Image Engine)
# ==========================================================
def get_real_or_ai_image(keyword, pexels_key, width, height, orientation="landscape"):
    """
    هذا المحرك يحاول جلب صورة حقيقية من Pexels أولاً.
    إذا لم ينجح، يستخدم الذكاء الاصطناعي مع أمر صارم (صورة هاتف عفوية) لكي لا تبدو مصطنعة.
    """
    safe_keyword = str(keyword).strip()
    if not safe_keyword or safe_keyword.lower() == "none":
        safe_keyword = "product"

    # 1. محاولة جلب صورة حقيقية من Pexels (الخيار الذهبي)
    if pexels_key:
        try:
            url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(safe_keyword)}&per_page=5&orientation={orientation}"
            headers = {"Authorization": pexels_key}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("photos") and len(data["photos"]) > 0:
                    photo = random.choice(data["photos"])
                    # إرجاع صورة بدقة عالية
                    return photo["src"]["large"]
        except Exception as e:
            pass # في حال فشل الاتصال، انتقل للخيار البديل
            
    # 2. الخيار البديل: الذكاء الاصطناعي بنمط كاميرا الهاتف (لتبدو حقيقية وليست 3D)
    prompt = f"candid authentic smartphone amateur photo of {safe_keyword}, real life, unedited, realistic, no CGI"
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 100000)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={seed}"

# ==========================================================
# 🧱 القوالب الهيكلية (بدمج الصور الحقيقية)
# ==========================================================

TEMPLATES = {
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
            body { font-family: 'Cairo', sans-serif; background-color: #f3f4f6; scroll-behavior: smooth; }
            .bg-primary { background-color: var(--primary); }
            .text-primary { color: var(--primary); }
            .bg-accent { background-color: var(--accent); }
            .text-accent { color: var(--accent); }
            section { padding: 3rem 1.5rem; }
            .no-pad { padding: 0 !important; }
            .img-container { background-color: #e5e7eb; display: flex; align-items: center; justify-content: center; }
        </style>
    </head>
    <body class="text-gray-800 antialiased pb-24 flex justify-center">
        <div class="w-full max-w-lg bg-white shadow-2xl relative overflow-hidden">
            <div class="bg-gray-900 text-white text-center py-2 text-xs font-bold flex justify-center gap-4">
                <span>🚚 شحن سريع مجاني</span><span>🔒 الدفع عند الاستلام</span>
            </div>
            
            <section class="!p-0 relative w-full bg-gray-900 img-container h-[500px]">
                <img src="{{IMAGE_HERO_URL}}" class="w-full h-full object-cover opacity-90 absolute top-0 left-0" alt="Hero" loading="lazy">
                <div class="absolute bottom-0 left-0 w-full h-3/4 bg-gradient-to-t from-[var(--primary)] to-transparent"></div>
                <div class="absolute bottom-0 left-0 w-full p-6 text-white text-center z-10">
                    <h1 class="text-4xl font-black mb-3 leading-tight drop-shadow-md">{{HERO_HEADLINE}}</h1>
                    <p class="text-lg font-bold text-gray-100 mb-6 drop-shadow">{{HERO_SUB}}</p>
                    <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-8 rounded-full text-xl w-full block shadow-lg transition transform hover:scale-105">{{CTA_BUTTON}}</a>
                </div>
            </section>
            
            <section class="bg-white text-center border-b border-gray-100">
                <h2 class="text-2xl font-black mb-5 text-red-600">⚠️ {{PROBLEM_TITLE}}</h2>
                <img src="{{IMAGE_PROBLEM_URL}}" class="w-full h-56 object-cover rounded-2xl mb-5 shadow-md border-2 border-red-100" alt="Problem" loading="lazy">
                <p class="text-lg font-bold text-gray-700 leading-relaxed">{{PROBLEM_DESC}}</p>
            </section>
            
            <section class="bg-primary text-white text-center relative z-20">
                <h2 class="text-3xl font-black text-accent mb-4">✨ {{SOLUTION_TITLE}}</h2>
                <p class="text-lg font-bold mb-6 text-gray-100">{{SOLUTION_DESC}}</p>
                <img src="{{IMAGE_SOLUTION_URL}}" class="w-full h-64 object-cover rounded-2xl border-4 border-white shadow-xl" alt="Solution" loading="lazy">
            </section>
            
            <section class="bg-gray-50 text-center border-b border-gray-200">
                <h2 class="text-3xl font-black text-gray-900 mb-6">تحول مذهل تلاحظه فوراً!</h2>
                <div class="flex gap-2 relative">
                    <div class="w-1/2 relative h-48 rounded-r-2xl border-2 border-red-300 overflow-hidden bg-white">
                        <img src="{{IMAGE_BEFORE_URL}}" class="w-full h-full object-cover opacity-90" loading="lazy">
                        <div class="absolute bottom-2 right-2 bg-red-600 text-white px-2 py-1 text-xs font-bold rounded">قبل</div>
                    </div>
                    <div class="w-1/2 relative h-48 rounded-l-2xl border-2 border-green-300 overflow-hidden bg-white">
                        <img src="{{IMAGE_AFTER_URL}}" class="w-full h-full object-cover" loading="lazy">
                        <div class="absolute bottom-2 left-2 bg-green-600 text-white px-2 py-1 text-xs font-bold rounded">بعد</div>
                    </div>
                    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-accent text-white w-10 h-10 flex items-center justify-center rounded-full border-4 border-white shadow-lg font-black text-xl z-10">></div>
                </div>
            </section>

            <section class="bg-gray-50 border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-primary mb-8">السر في مكوناتنا</h2>
                <div class="grid grid-cols-1 gap-4">{{DYNAMIC_SECTION_HTML}}</div>
            </section>
            
            <section class="bg-white border-b border-gray-200 text-center">
                <h2 class="text-3xl font-black text-primary mb-2">شاهد تجارب عملائنا</h2>
                <p class="text-gray-500 font-bold mb-8">لا تأخذ كلمتنا، شاهد الفيديوهات بنفسك!</p>
                <div class="flex gap-3 overflow-x-auto pb-4 snap-x">
                    <div class="min-w-[80%] snap-center"><div class="w-full h-64 bg-gray-200 rounded-xl overflow-hidden relative shadow-md img-container"><span class="text-red-500 text-4xl mb-2">▶️</span><span>ضع فيديو يوتيوب هنا</span></div></div>
                </div>
            </section>
            
            <section class="bg-white border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">آراء العملاء</h2>
                <div class="space-y-4">{{REVIEWS_HTML}}</div>
            </section>
            
            <section class="bg-gray-50 border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">❓ الأسئلة الشائعة</h2>
                <div class="space-y-3 text-right">{{FAQ_HTML}}</div>
            </section>
            
            <section class="bg-primary text-center pb-20 text-white rounded-t-3xl mt-4">
                <div class="text-6xl mb-4 drop-shadow-lg">🛡️</div>
                <h3 class="text-3xl font-black text-accent mb-4">{{GUARANTEE_TITLE}}</h3>
                <p class="text-lg font-bold text-gray-100">{{GUARANTEE_TEXT}}</p>
            </section>
            
            <div id="buy" class="fixed bottom-0 left-0 w-full bg-white/95 backdrop-blur-sm p-4 shadow-[0_-15px_30px_rgba(0,0,0,0.15)] flex justify-center z-50 border-t-4 border-accent">
                <div class="w-full max-w-lg flex flex-col items-center">
                    <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-6 rounded-xl text-2xl w-full text-center shadow-lg transition transform hover:scale-[1.02] flex justify-center items-center gap-3"><span>🛒</span> {{CTA_BUTTON}}</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """,
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
            body { font-family: 'Cairo', sans-serif; background-color: #f3f4f6; scroll-behavior: smooth; }
            .bg-primary { background-color: var(--primary); }
            .text-primary { color: var(--primary); }
            .bg-accent { background-color: var(--accent); }
            .text-accent { color: var(--accent); }
            section { padding: 3rem 1.5rem; }
            .no-pad { padding: 0 !important; }
            .img-container { background-color: #e5e7eb; display: flex; align-items: center; justify-content: center; }
        </style>
    </head>
    <body class="text-gray-800 antialiased pb-24 flex justify-center">
        <div class="w-full max-w-lg bg-white shadow-2xl relative overflow-hidden">
            <div class="bg-gray-900 text-white text-center py-2 text-xs font-bold flex justify-center gap-4">
                <span>🚚 توصيل سريع </span><span>🔒 جودة مضمونة</span>
            </div>
            
            <section class="no-pad relative w-full bg-gray-900 img-container h-[500px]">
                <img src="{{IMAGE_HERO_URL}}" class="w-full h-full object-cover opacity-90 absolute top-0 left-0" alt="Hero" loading="lazy">
                <div class="absolute bottom-0 left-0 w-full h-3/4 bg-gradient-to-t from-[var(--primary)] to-transparent"></div>
                <div class="absolute bottom-0 left-0 w-full p-6 text-white text-center z-10">
                    <h1 class="text-4xl font-black mb-3 leading-tight drop-shadow-md">{{HERO_HEADLINE}}</h1>
                    <p class="text-lg font-bold text-gray-100 mb-6 drop-shadow">{{HERO_SUB}}</p>
                    <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-8 rounded-full text-xl w-full block shadow-lg transition transform hover:scale-105">{{CTA_BUTTON}}</a>
                </div>
            </section>
            
            <section class="bg-white text-center border-b border-gray-100">
                <h2 class="text-2xl font-black mb-5 text-red-600">⚠️ {{PROBLEM_TITLE}}</h2>
                <img src="{{IMAGE_PROBLEM_URL}}" class="w-full h-56 object-cover rounded-2xl mb-5 shadow-md border-2 border-red-100" alt="Problem" loading="lazy">
                <p class="text-lg font-bold text-gray-700 leading-relaxed">{{PROBLEM_DESC}}</p>
            </section>
            
            <section class="bg-primary text-white text-center relative z-20">
                <h2 class="text-3xl font-black text-accent mb-4">✨ {{SOLUTION_TITLE}}</h2>
                <p class="text-lg font-bold mb-6 text-gray-100">{{SOLUTION_DESC}}</p>
                <img src="{{IMAGE_SOLUTION_URL}}" class="w-full h-64 object-cover rounded-2xl border-4 border-white shadow-xl" alt="Solution" loading="lazy">
            </section>
            
            <section class="bg-gray-100 border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-primary mb-6">⚙️ المقاسات والمواصفات</h2>
                <div class="flex flex-col gap-4">
                    <img src="{{IMAGE_DIMENSIONS_URL}}" class="w-full h-48 object-cover rounded-xl shadow-md" alt="Dimensions" loading="lazy">
                    <ul class="space-y-3 bg-white p-4 rounded-xl shadow-sm border border-gray-200 text-right">{{DIMENSIONS_HTML}}</ul>
                </div>
            </section>
            
            <section class="bg-white border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-primary mb-8">سهولة تامة في الاستخدام</h2>
                <div class="grid grid-cols-1 gap-4">{{DYNAMIC_SECTION_HTML}}</div>
            </section>
            
            <section class="bg-gray-50 border-b border-gray-200 text-center">
                <h2 class="text-3xl font-black text-primary mb-2">تجارب عملائنا المباشرة</h2>
                <p class="text-gray-500 font-bold mb-6">شاهد المنتج وهو يعمل على أرض الواقع</p>
                <div class="space-y-4">
                    <div class="w-full h-56 bg-gray-200 rounded-xl overflow-hidden relative shadow-md img-container"><span class="text-red-500 text-4xl mb-2">▶️</span><span>ضع رابط فيديو يوتيوب هنا</span></div>
                </div>
            </section>
            
            <section class="bg-white border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">التقييمات الكتابية</h2>
                <div class="space-y-4">{{REVIEWS_HTML}}</div>
            </section>
            
            <section class="bg-gray-50 border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">❓ أسئلة متكررة</h2>
                <div class="space-y-3 text-right">{{FAQ_HTML}}</div>
            </section>
            
            <section class="bg-gray-900 text-center pb-20 text-white rounded-t-3xl mt-4">
                <div class="text-6xl mb-4">🛡️</div>
                <h3 class="text-3xl font-black text-accent mb-4">{{GUARANTEE_TITLE}}</h3>
                <p class="text-lg font-bold text-gray-300">{{GUARANTEE_TEXT}}</p>
            </section>
            
            <div id="buy" class="fixed bottom-0 left-0 w-full bg-white/95 backdrop-blur-sm p-4 shadow-[0_-15px_30px_rgba(0,0,0,0.15)] flex justify-center z-50 border-t-4 border-accent">
                <div class="w-full max-w-lg flex flex-col items-center">
                    <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-6 rounded-xl text-2xl w-full text-center shadow-lg transition transform hover:scale-[1.02] flex justify-center items-center gap-3"><span>🛒</span> {{CTA_BUTTON}}</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
}

# ==========================================================
# 🧠 دوال الذكاء الاصطناعي الأساسية
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
    
    prompt = f"""
    أنت خبير Copywriter لصفحات الهبوط.
    المنتج: "{product}". الفئة: "{category}".
    النصوص الموجهة للعميل بـ "العربية الفصحى".
    ⚠️ الحقول المنتهية بـ _search هي كلمات مفتاحية بالإنجليزية فقط للبحث عن صور حقيقية (كلمة إلى 3 كلمات كحد أقصى). مثال: "smiling woman", "acne face", "skincare serum".

    رد بصيغة JSON صالحة بهذا الهيكل:
    {{
        "hero_headline": "عنوان رئيسي يخطف الانتباه",
        "hero_subheadline": "عنوان فرعي يقدم وعداً بالحل",
        "image_hero_search": "english keyword for product or happy person",
        "problem_title": "عنوان قسم الألم",
        "problem_description": "فقرة تصف الإحباط بدقة",
        "image_problem_search": "english keyword for frustrated person or bad skin/mess",
        "solution_title": "عنوان قسم الحل",
        "solution_description": "فقرة تشرح كيف يقدم المنتج الحل",
        "image_solution_search": "english keyword for happy relieved person or clean result",
        "image_before_search": "english keyword for before result (bad)",
        "image_after_search": "english keyword for after result (good)",
        "dynamic_items": [
            {{"title": "اسم ميزة 1", "desc": "الفائدة", "image_search": "english keyword for feature 1"}},
            {{"title": "اسم ميزة 2", "desc": "الفائدة", "image_search": "english keyword for feature 2"}},
            {{"title": "اسم ميزة 3", "desc": "الفائدة", "image_search": "english keyword for feature 3"}}
        ],
        "dimensions": ["الطول: ..", "الوزن: ..", "الخامة: .."],
        "image_dimensions_search": "english keyword for ruler or measurement",
        "reviews": [
            {{"name": "سارة م.", "rating": 5, "comment": "تعليق واقعي"}}
        ],
        "faq": [
            {{"q": "متى سألاحظ النتائج؟", "a": "إجابة مقنعة"}}
        ],
        "guarantee_title": "عنوان الضمان",
        "guarantee_text": "نص تفصيلي للضمان",
        "call_to_action": "نص زر الشراء"
    }}
    """
    response = model.generate_content(prompt, request_options={"timeout": 45.0})
    tb = chr(96) * 3 
    clean_text = re.sub(f'{tb}(?:json|JSON)?', '', response.text, flags=re.IGNORECASE)
    clean_text = clean_text.replace(tb, '').strip()
    match = re.search(r'\{.*\}', clean_text, re.DOTALL)
    if match: return match.group(0)
    return clean_text

def generate_deep_research(api_key, product_name, category):
    genai.configure(api_key=api_key, transport="rest")
    model_name = get_fast_working_model(api_key)
    model = genai.GenerativeModel(model_name)
    prompt = f"""
    أنت أداة "Deep Research" متطورة وخبير استراتيجي في الـ (Direct Response Copywriting).
    المنتج: "{product_name}". الفئة: "{category}".
    استند إلى منهجية SOP-1 وبناء الوثائق التأسيسية الأربعة. أخرج تقريراً شاملاً بالعربية الفصحى بتنسيق Markdown.
    1. وثيقة شخصية العميل (Avatar Sheet) - الآلام، الرغبات، الاعتراضات الخفية.
    2. وثيقة بحث السوق والمنافسين - فجوة السوق، أخطاء المنافسين.
    3. وثيقة ملخص العرض (Offer Brief) - الوعد الأساسي، الآلية الفريدة.
    4. وثيقة المعتقدات الضرورية - 4 إلى 6 معتقدات تبدأ بـ "أنا أؤمن أن...".
    5. زوايا البيع الجاهزة - تطبيق إطار PAS وإطار FAB.
    """
    response = model.generate_content(prompt, request_options={"timeout": 60.0})
    return response.text

# ==========================================================
# 💉 دالة الحقن وبناء الـ HTML بالصور الحقيقية
# ==========================================================
def inject_data_into_template(json_data, category, colors, pexels_key):
    template_key = "Cosmetics" if "Cosmetics" in category else "Gadgets"
    final_html = TEMPLATES[template_key]
    
    # استخراج وتوليد روابط الصور الحقيقية
    hero_url = get_real_or_ai_image(json_data.get('image_hero_search', 'product'), pexels_key, 800, 1000, "portrait")
    prob_url = get_real_or_ai_image(json_data.get('image_problem_search', 'sad person'), pexels_key, 600, 400, "landscape")
    sol_url = get_real_or_ai_image(json_data.get('image_solution_search', 'happy person'), pexels_key, 800, 600, "landscape")
    before_url = get_real_or_ai_image(json_data.get('image_before_search', 'sad face'), pexels_key, 400, 500, "portrait")
    after_url = get_real_or_ai_image(json_data.get('image_after_search', 'clean face'), pexels_key, 400, 500, "portrait")
    dim_url = get_real_or_ai_image(json_data.get('image_dimensions_search', 'ruler measurement'), pexels_key, 600, 400, "landscape")

    dynamic_html = ""
    for item in json_data.get('dynamic_items', [])[:3]:
        item_img = get_real_or_ai_image(item.get('image_search', 'feature'), pexels_key, 200, 200, "square")
        dynamic_html += f'''
        <div class="bg-white p-4 rounded-2xl border border-gray-100 flex items-center gap-4 text-right shadow-sm">
            <img src="{item_img}" class="w-16 h-16 rounded-full object-cover shadow-sm border-2 border-accent flex-shrink-0" loading="lazy">
            <div><h4 class="font-black text-gray-900 text-lg mb-1">{item.get('title')}</h4><p class="text-sm font-bold text-gray-600 leading-relaxed">{item.get('desc')}</p></div>
        </div>'''

    dimensions_html = ""
    for dim in json_data.get('dimensions', [])[:4]:
        dimensions_html += f'<li class="flex items-center gap-3 font-bold text-gray-700"><span class="text-accent text-xl">📏</span> {dim}</li>'

    reviews_html = ""
    for rev in json_data.get('reviews', [])[:3]:
        stars = '⭐' * int(rev.get('rating', 5))
        reviews_html += f'''
        <div class="bg-gray-50 p-5 rounded-2xl border border-gray-100 shadow-sm text-right">
            <div class="flex justify-between items-center mb-2"><span class="font-black text-primary">{rev.get('name')}</span><span class="text-accent text-sm tracking-tighter">{stars}</span></div>
            <p class="text-gray-700 font-bold italic leading-relaxed text-sm">"{rev.get('comment')}"</p>
            <div class="mt-3 text-xs text-green-600 font-black flex items-center gap-1"><span>✅</span> مشتري موثق</div>
        </div>'''

    faq_html = ""
    for faq in json_data.get('faq', [])[:4]:
        faq_html += f'''
        <details class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 group cursor-pointer mb-2">
            <summary class="font-black text-gray-900 text-base flex justify-between items-center outline-none">{faq.get('q')}<span class="text-accent group-open:rotate-180 transition-transform">▼</span></summary>
            <p class="text-gray-600 text-sm font-bold mt-3 border-t pt-3 border-gray-100">{faq.get('a')}</p>
        </details>'''

    # حقن الروابط والنصوص
    final_html = final_html.replace("{{IMAGE_HERO_URL}}", hero_url)
    final_html = final_html.replace("{{IMAGE_PROBLEM_URL}}", prob_url)
    final_html = final_html.replace("{{IMAGE_SOLUTION_URL}}", sol_url)
    final_html = final_html.replace("{{IMAGE_BEFORE_URL}}", before_url)
    final_html = final_html.replace("{{IMAGE_AFTER_URL}}", after_url)
    final_html = final_html.replace("{{IMAGE_DIMENSIONS_URL}}", dim_url)
    
    final_html = final_html.replace("{{DYNAMIC_SECTION_HTML}}", dynamic_html)
    final_html = final_html.replace("{{DIMENSIONS_HTML}}", dimensions_html)
    final_html = final_html.replace("{{REVIEWS_HTML}}", reviews_html)
    final_html = final_html.replace("{{FAQ_HTML}}", faq_html)
    
    final_html = final_html.replace("{{COLOR_PRIMARY}}", colors['primary'])
    final_html = final_html.replace("{{COLOR_SECONDARY}}", colors['secondary'])
    final_html = final_html.replace("{{COLOR_ACCENT}}", colors['accent'])

    final_html = final_html.replace("{{HERO_HEADLINE}}", json_data.get("hero_headline", ""))
    final_html = final_html.replace("{{HERO_SUB}}", json_data.get("hero_subheadline", ""))
    final_html = final_html.replace("{{PROBLEM_TITLE}}", json_data.get("problem_title", ""))
    final_html = final_html.replace("{{PROBLEM_DESC}}", json_data.get("problem_description", ""))
    final_html = final_html.replace("{{SOLUTION_TITLE}}", json_data.get("solution_title", ""))
    final_html = final_html.replace("{{SOLUTION_DESC}}", json_data.get("solution_description", ""))
    final_html = final_html.replace("{{GUARANTEE_TITLE}}", json_data.get("guarantee_title", "ضمان الجودة"))
    final_html = final_html.replace("{{GUARANTEE_TEXT}}", json_data.get("guarantee_text", ""))
    final_html = final_html.replace("{{CTA_BUTTON}}", json_data.get("call_to_action", "اطلب الآن"))
    
    return final_html

# ==========================================================
# 🎛️ واجهة المستخدم والقائمة الجانبية
# ==========================================================
with st.sidebar:
    st.header("⚙️ الإعدادات العامة")
    global_api_key = st.text_input("🔑 Gemini API Key", type="password")
    global_product_name = st.text_area("📦 تفاصيل واسم المنتج", placeholder="مثال: جهاز تنظيف الوجه الحديث مع فرشتين.")
    global_category = st.selectbox("📦 فئة المنتج", ["💄 مستحضرات تجميل وعناية (Cosmetics)", "⚙️ أدوات وأجهزة ذكية (Gadgets)"])
    
    st.markdown("---")
    st.subheader("📸 الصور الحقيقية (Real Images)")
    pexels_key = st.text_input("🔑 Pexels API Key (اختياري)", type="password", help="احصل عليه مجاناً من Pexels.com لتعطيك الأداة صوراً فوتوغرافية حقيقية 100% لأشخاص ومنتجات بدلاً من الذكاء الاصطناعي.")
    
    st.markdown("---")
    st.header("🛠️ اختر الأداة")
    app_mode = st.radio("قائمة التحكم:", ["🏗️ منشئ صفحات الهبوط", "🔍 بحث السوق المعمق (SOP-1)", "💰 حاسبة التعادل المالي (Matrix)"])
    st.markdown("---")

# ---------------------------------------------------------
# أداة 1: منشئ صفحات الهبوط
# ---------------------------------------------------------
if app_mode == "🏗️ منشئ صفحات الهبوط":
    with st.sidebar:
        with st.expander("🎨 تخصيص ألوان صفحة الهبوط", expanded=True):
            col1, col2 = st.columns(2)
            with col1: color_primary = st.color_picker("أساسي", "#0f766e" if "Cosmetics" in global_category else "#1f2937")
            with col2: color_accent = st.color_picker("الزر", "#eab308" if "Cosmetics" in global_category else "#ef4444")
            color_secondary = st.color_picker("ثانوي", "#f8fafc")
            colors_dict = {'primary': color_primary, 'secondary': color_secondary, 'accent': color_accent}
        
        start_btn = st.button("🚀 توليد الصفحة (سحر حقيقي!)")

    if start_btn:
        if not global_api_key or not global_product_name:
            st.error("الرجاء إدخال المفتاح واسم المنتج في القائمة الجانبية.")
        else:
            with st.spinner("🤖 جاري الهندسة، كتابة المحتوى، وجلب الصور الفوتوغرافية الحقيقية..."):
                try:
                    raw_json = generate_landing_page_json(global_api_key, global_product_name, global_category)
                    parsed_data = json.loads(raw_json)
                    st.session_state.final_page = inject_data_into_template(parsed_data, global_category, colors_dict, pexels_key)
                    st.success("🎉 اكتمل البناء بنجاح! لاحظ احترافية الصور وواقعيتها.")
                except Exception as e:
                    st.error(f"🛑 خطأ: {str(e)}")

    if 'final_page' in st.session_state:
        tab1, tab2 = st.tabs(["📱 المعاينة البصرية", "💻 كود HTML (للنسخ)"])
        with tab1:
            if pexels_key:
                st.success("📸 تم تفعيل محرك Pexels! الصور المعروضة أدناه هي صور فوتوغرافية حقيقية 100% تم جلبها من أرشيف Pexels.")
            else:
                st.info("💡 تم تفعيل محرك الذكاء الاصطناعي بنمط (كاميرا الهاتف) لتبدو الصور عفوية وحقيقية قدر الإمكان. لصور حقيقية 100%، أضف مفتاح Pexels في الجانب.")
            components.html(st.session_state.final_page, height=1000, scrolling=True)
        with tab2:
            st.code(st.session_state.final_page, language="html")

# ---------------------------------------------------------
# أداة 2: بحث السوق المعمق (Deep Research)
# ---------------------------------------------------------
elif app_mode == "🔍 بحث السوق المعمق (SOP-1)":
    st.markdown("### 🔍 البحث المعمق في السوق والمنافسين")
    st.write(f"تحليل صارم لـ: **{global_product_name if global_product_name else '[يرجى إدخال المنتج]'}**")
    
    start_research_btn = st.button("🧠 استخراج وثائق البيع الاستراتيجية")

    if start_research_btn:
        if not global_api_key or not global_product_name:
            st.error("الرجاء إدخال المفتاح واسم المنتج أولاً.")
        else:
            with st.spinner("🕵️‍♂️ جاري الغوص في أعماق السوق وبناء الوثائق التأسيسية الأربعة..."):
                try:
                    research_result = generate_deep_research(global_api_key, global_product_name, global_category)
                    st.session_state.research_output = research_result
                    st.success("✅ اكتمل البحث! إليك التقرير السري لمنتجك.")
                except Exception as e:
                    st.error(f"🛑 حدث خطأ: {str(e)}")

    if 'research_output' in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state.research_output)
        with st.expander("💾 عرض التقرير الخام للنسخ"):
            st.text_area("التقرير:", value=st.session_state.research_output, height=300)

# ---------------------------------------------------------
# أداة 3: حاسبة التعادل والمصفوفة المالية
# ---------------------------------------------------------
elif app_mode == "💰 حاسبة التعادل المالي (Matrix)":
    st.markdown("### 💰 حاسبة نقطة التعادل والمصفوفة المالية")
    
    COUNTRIES = {
        "السعودية (KSA)": {"currency": "SAR", "P": 199.0, "C": 85.0, "CPL": 25.0},
        "الإمارات (UAE)": {"currency": "AED", "P": 149.0, "C": 60.0, "CPL": 30.0},
        "الكويت (KWT)": {"currency": "KWD", "P": 19.0, "C": 8.0, "CPL": 2.5},
        "سلطنة عمان (OMN)": {"currency": "OMR", "P": 19.0, "C": 8.0, "CPL": 3.0},
        "قطر (QAT)": {"currency": "QAR", "P": 199.0, "C": 80.0, "CPL": 35.0},
        "البحرين (BHD)": {"currency": "BHD", "P": 19.0, "C": 8.0, "CPL": 3.0},
        "المغرب (MAD)": {"currency": "MAD", "P": 299.0, "C": 120.0, "CPL": 40.0},
        "مصر (EGP)": {"currency": "EGP", "P": 500.0, "C": 200.0, "CPL": 50.0},
        "أخرى (Custom)": {"currency": "USD", "P": 50.0, "C": 20.0, "CPL": 5.0},
    }

    col_country, col_currency = st.columns(2)
    with col_country: selected_country = st.selectbox("🌍 الدولة:", list(COUNTRIES.keys()))
    with col_currency: currency = st.text_input("💱 العملة:", value=COUNTRIES[selected_country]["currency"])

    default_vals = COUNTRIES[selected_country]

    st.markdown("##### 💵 البيانات المالية")
    col1, col2, col3 = st.columns(3)
    P = col1.number_input(f"سعر البيع (P) [{currency}]", value=default_vals["P"], step=1.0)
    C = col2.number_input(f"تكلفة المنتج+الشحن (C) [{currency}]", value=default_vals["C"], step=1.0)
    actual_cpl = col3.number_input(f"تكلفة الليد (CPL) [{currency}]", value=default_vals["CPL"], step=0.5)

    st.markdown("##### 📈 معدلات الأداء المتوقعة")
    col4, col5 = st.columns(2)
    CR_percent = col4.slider("نسبة التأكيد (CR) %", min_value=10, max_value=100, value=60)
    DR_percent = col5.slider("نسبة التسليم (DR) %", min_value=10, max_value=100, value=55)
    
    CR, DR = CR_percent / 100.0, DR_percent / 100.0
    gross_margin = P - C
    max_cpl = gross_margin * CR * DR
    max_cpa = gross_margin * DR
    profit_per_lead = max_cpl - actual_cpl

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(f"هامش الربح", f"{gross_margin:.2f} {currency}")
    m2.metric(f"أقصى CPL", f"{max_cpl:.2f} {currency}")
    m3.metric(f"أقصى CPA", f"{max_cpa:.2f} {currency}")
    if profit_per_lead >= 0: m4.metric("حالة الإعلان", "✅ رابح", f"+ {profit_per_lead:.2f} صافي")
    else: m4.metric("حالة الإعلان", "🚨 خاسر", f"{profit_per_lead:.2f} خسارة")

    st.markdown("---")
    st.markdown("#### 🧮 مصفوفة أقصى تكلفة لليد (Max CPL Matrix)")
    
    dr_list = [x/100.0 for x in range(30, 100, 5)]
    cr_list = [x/100.0 for x in range(30, 100, 5)]
    matrix_data = []
    for cr_val in cr_list:
        row = {'CR \\ DR': f"{int(cr_val*100)}%"}
        for dr_val in dr_list: row[f"{int(dr_val*100)}%"] = round(gross_margin * cr_val * dr_val, 2)
        matrix_data.append(row)

    df_matrix = pd.DataFrame(matrix_data)
    try:
        st.dataframe(df_matrix.style.background_gradient(cmap='RdYlGn', subset=df_matrix.columns[1:]), use_container_width=True)
    except Exception:
        st.dataframe(df_matrix, use_container_width=True)
