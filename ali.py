import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine - Template System", layout="wide", page_icon="⚙️")

st.markdown("""
<style>
    body { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: #1e293b; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>⚙️ ALI Growth Engine (نظام القوالب الصاروخي)</h1></div>', unsafe_allow_html=True)

# ==========================================================
# 🧱 الخطوة 2: القالب الصلب (Hard-Coded HTML Template)
# هذا القالب مخزن في النظام، مستحيل أن ينكسر، ومبني بـ Tailwind
# ==========================================================
MASTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>body { font-family: 'Cairo', sans-serif; background-color: #f8fafc; }</style>
</head>
<body class="text-gray-800 antialiased">
    
    <!-- شريط الثقة -->
    <div class="bg-gray-900 text-white text-center py-2 text-sm font-bold tracking-wide">
        🚚 شحن مجاني اليوم | 💳 دفع آمن | 🛡️ ضمان ذهبي
    </div>

    <!-- Hero Section -->
    <section class="bg-white py-16 px-4 shadow-sm">
        <div class="max-w-3xl mx-auto text-center">
            <h1 class="text-4xl md:text-5xl font-black text-blue-900 mb-6 leading-tight">{{HERO_HEADLINE}}</h1>
            <p class="text-xl text-gray-600 mb-8">{{HERO_SUB}}</p>
            <a href="#buy" class="bg-red-600 hover:bg-red-700 text-white font-bold py-4 px-12 rounded-full text-xl inline-block shadow-lg transition transform hover:-translate-y-1 animate-pulse">{{CTA_BUTTON}}</a>
        </div>
    </section>

    <!-- Problem Section (Agitation) -->
    <section class="py-16 px-4 bg-red-50 text-center">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl font-bold text-red-600 mb-4">⚠️ {{PROBLEM_TITLE}}</h2>
            <p class="text-lg text-gray-700 font-medium">{{PROBLEM_DESC}}</p>
        </div>
    </section>

    <!-- Solution Section (The Savior) -->
    <section class="py-16 px-4 bg-green-50 text-center">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl font-bold text-green-600 mb-4">✨ {{SOLUTION_TITLE}}</h2>
            <p class="text-lg text-gray-700 font-medium">{{SOLUTION_DESC}}</p>
        </div>
    </section>

    <!-- Benefits Grid -->
    <section class="py-16 px-4">
        <div class="max-w-5xl mx-auto">
            <h2 class="text-3xl font-black text-center text-gray-800 mb-10">لماذا يختاره الجميع؟</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                {{BENEFITS_HTML}}
            </div>
        </div>
    </section>

    <!-- Guarantee & Sticky CTA -->
    <section class="bg-blue-900 text-white py-16 px-4 text-center pb-32">
        <div class="max-w-3xl mx-auto">
            <div class="text-6xl mb-4">🛡️</div>
            <h3 class="text-2xl font-bold text-yellow-400 mb-4">ضمان ذهبي 100%</h3>
            <p class="text-lg mb-8">{{GUARANTEE}}</p>
        </div>
    </section>

    <!-- Sticky Footer CTA -->
    <div class="fixed bottom-0 left-0 w-full bg-white p-4 shadow-[0_-10px_15px_-3px_rgba(0,0,0,0.1)] text-center flex justify-center border-t-2 border-gray-100">
        <a href="#buy" class="bg-green-600 text-white font-black py-3 px-10 rounded-xl text-lg w-full max-w-md shadow-lg animate-bounce">{{CTA_BUTTON}}</a>
    </div>

</body>
</html>
"""

# ==========================================================
# 🧠 الخطوة 1: المحرك اللفظي (JSON Generator)
# ==========================================================
def generate_landing_page_json(api_key, product):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash") # موديل سريع جداً
    
    prompt = f"""
    أنت أعظم Copywriter. اكتب محتوى تسويقي قوي لمنتج: "{product}".
    رد حصراً بـ JSON صالح (Valid JSON) بهذا الهيكل:
    {{
        "hero_headline": "عنوان رئيسي صادم",
        "hero_subheadline": "عنوان فرعي مقنع",
        "problem_title": "عنوان المشكلة",
        "problem_description": "وصف ألم العميل",
        "solution_title": "عنوان الحل",
        "solution_description": "وصف الآلية الفريدة",
        "benefits": ["فائدة قوية 1", "فائدة قوية 2", "فائدة قوية 3"],
        "guarantee": "نص عكس المخاطرة",
        "call_to_action": "نص زر الشراء القوي"
    }}
    لا تكتب أي حرف خارج الـ JSON.
    """
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(response_mime_type="application/json")
    )
    return response.text

# ==========================================================
# 💉 الخطوة 3: محرك الحقن (Data Binding Engine)
# ==========================================================
def inject_data_into_template(json_data):
    # تجهيز كود الفوائد (Benefits) ديناميكياً
    benefits_html = ""
    for benefit in json_data.get('benefits', []):
        benefits_html += f"""
        <div class="bg-white p-6 rounded-2xl shadow-md border border-gray-100 text-center hover:shadow-lg transition">
            <div class="text-3xl mb-3">✅</div>
            <p class="font-bold text-gray-800">{benefit}</p>
        </div>
        """
    
    # استبدال المتغيرات في القالب الصلب
    final_html = MASTER_TEMPLATE
    final_html = final_html.replace("{{HERO_HEADLINE}}", json_data.get("hero_headline", ""))
    final_html = final_html.replace("{{HERO_SUB}}", json_data.get("hero_subheadline", ""))
    final_html = final_html.replace("{{PROBLEM_TITLE}}", json_data.get("problem_title", ""))
    final_html = final_html.replace("{{PROBLEM_DESC}}", json_data.get("problem_description", ""))
    final_html = final_html.replace("{{SOLUTION_TITLE}}", json_data.get("solution_title", ""))
    final_html = final_html.replace("{{SOLUTION_DESC}}", json_data.get("solution_description", ""))
    final_html = final_html.replace("{{GUARANTEE}}", json_data.get("guarantee", ""))
    final_html = final_html.replace("{{CTA_BUTTON}}", json_data.get("call_to_action", ""))
    final_html = final_html.replace("{{BENEFITS_HTML}}", benefits_html)
    
    return final_html

# --- واجهة المستخدم (Sidebar & Main) ---
with st.sidebar:
    st.header("⚙️ إعدادات المحرك")
    api_key = st.text_input("🔑 أدخل API Key", type="password")
    product_name = st.text_input("📦 اسم/وصف المنتج")
    start_btn = st.button("⚡ توليد الصفحة (5 ثوانٍ)")

if start_btn:
    if not api_key or not product_name:
        st.error("يرجى إدخال المفتاح واسم المنتج.")
    else:
        with st.spinner("1️⃣ جاري استخراج العقول التسويقية (JSON)..."):
            try:
                # 1. جلب الكلمات
                raw_json = generate_landing_page_json(api_key, product_name)
                parsed_data = json.loads(raw_json)
                
                # 2. الحقن في القالب
                with st.spinner("2️⃣ جاري حقن البيانات في القالب الصلب..."):
                    st.session_state.final_page = inject_data_into_template(parsed_data)
                    st.session_state.json_data = parsed_data
                    
                st.success("🎉 اكتمل بناء الصفحة في ثوانٍ معدودة وبدون أخطاء تصميم!")
            except Exception as e:
                st.error(f"حدث خطأ في جلب البيانات: {str(e)}")

# --- العرض (التبويبات) ---
if 'final_page' in st.session_state:
    tab1, tab2, tab3 = st.tabs(["📱 المعاينة الحية (Template Engine)", "💻 كود HTML للنسخ", "📝 البيانات الخام (JSON)"])
    
    with tab1:
        st.info("💡 هذه الصفحة مبنية بنظام القوالب. لا يمكن أن تظهر شاشة بيضاء أبداً!")
        # تم تصغير العرض ليحاكي شاشة الجوال (Mobile View)
        components.html(st.session_state.final_page, height=850, scrolling=True)
        
    with tab2:
        st.code(st.session_state.final_page, language="html")
        
    with tab3:
        st.json(st.session_state.json_data)
