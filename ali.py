import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V11", layout="wide", page_icon="https://i.postimg.cc/xCt20gWj/image.png")

# --- 2. التصميم (CSS) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
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

# --- 3. دوال الذكاء الاصطناعي (مع الذاكرة المؤقتة لتجنب الاختفاء) ---
@st.cache_data(show_spinner=False)
def generate_html_page(api_key, product_name):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        أنت خبير برمجة واجهات (Front-end) ومسوق إلكتروني محترف للسوق الخليجي.
        المطلوب: برمجة صفحة هبوط كاملة وجاهزة (HTML & CSS مدمج) لمنتج اسمه: {product_name}.
        1. لغة الصفحة: العربية (RTL) بخط 'Tajawal'.
        2. التصميم: حديث وسريع التجاوب (Responsive).
        3. الأقسام: Hero Section مع صورة مؤقتة، 4 فوائد، 3 تقييمات خليجية، زر عائم للطلب.
        ⚠️ شرط صارم: أعطني فقط كود الـ HTML والـ CSS الكامل داخل علامتي ```html و ```.
        """
        response = model.generate_content(prompt)
        code = response.text
        if "```html" in code: code = code.split("```html")[1].split("```")[0]
        elif "```" in code: code = code.split("```")[1]
        return code.strip()
    except Exception as e: return f"<h3>خطأ: {str(e)}</h3>"

@st.cache_data(show_spinner=False)
def generate_image_prompts(api_key, product_name):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        اكتب 3 برومتات (Prompts) احترافية باللغة الإنجليزية لتوليد صور لمنتج: "{product_name}".
        1. صورة الهيرو (Hero Shot)
        2. صورة نمط الحياة (Lifestyle Shot)
        3. صورة تفصيلية (Macro Shot)
        افصل بينها بـ: "---PROMPT_SEPARATOR---"
        """
        response = model.generate_content(prompt)
        prompts = response.text.split("---PROMPT_SEPARATOR---")
        return [p.strip() for p in prompts if p.strip()]
    except: return []

@st.cache_data(show_spinner=False)
def ask_ai(api_key, prompt):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"أجب بالعربية الفصحى فقط: {prompt}")
        return response.text
    except: return "خطأ في الاتصال"

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.title("🏗️ محرك علي V11.0")
    api_key = st.text_input("🔑 API Key", type="password")
    product_name = st.text_input("📦 اسم المنتج")
    
    st.markdown("---")
    st.markdown("### 💰 إعدادات المالية")
    P = st.number_input("سعر البيع (P)", value=250.0)
    C = st.number_input("التكلفة (C)", value=50.0)
    CPL = st.number_input("تكلفة الليد (CPL)", value=15.0)
    
    uploaded_file = st.file_uploader("📊 ارفع ملف الإكسل", type=['xlsx', 'csv'])
    run_btn = st.button("🚀 تشغيل النظام الشامل")

# حفظ حالة التشغيل في الذاكرة (لحل مشكلة اختفاء النتائج)
if run_btn:
    st.session_state['app_is_running'] = True

# --- 5. الواجهة الرئيسية ---
st.markdown('<div class="main-header"><h1>ALI Growth Engine - مستقر 100%</h1></div>', unsafe_allow_html=True)

if st.session_state.get('app_is_running', False):
    if not api_key:
        st.error("الرجاء إدخال API Key للبدء.")
    else:
        # تم تصحيح ترتيب التبويبات هنا (0, 1, 2, 3)
        tabs = st.tabs(["📄 بناء الصفحة (HTML)", "🖼️ استوديو الصور (Prompts)", "🎯 الاستراتيجية", "💰 التحليل المالي الدقيق"])
        
        # التبويب الأول: HTML
        with tabs[0]:
            if product_name:
                with st.spinner("المهندس المعماري يعمل (قد يستغرق 15 ثانية)..."):
                    html_code = generate_html_page(api_key, product_name)
                    st.success("✅ تم بناء هيكل الصفحة!")
                    components.html(html_code, height=500, scrolling=True)
                    with st.expander("💻 عرض كود الـ HTML للنسخ"):
                        st.code(html_code, language='html')
            else:
                st.warning("أدخل اسم المنتج لتوليد الصفحة.")

        # التبويب الثاني: الصور
        with tabs[1]:
            if product_name:
                with st.spinner("المخرج الفني يكتب البرومتات..."):
                    prompts = generate_image_prompts(api_key, product_name)
                    if len(prompts) >= 3:
                        st.markdown(f'<div class="image-prompt-box"><strong>1️⃣ Hero Shot:</strong><br>{prompts[0]}</div>', unsafe_allow_html=True)
                        st.code(prompts[0], language="text")
                        st.markdown(f'<div class="image-prompt-box"><strong>2️⃣ Lifestyle Shot:</strong><br>{prompts[1]}</div>', unsafe_allow_html=True)
                        st.code(prompts[1], language="text")
                        st.markdown(f'<div class="image-prompt-box"><strong>3️⃣ Macro Shot:</strong><br>{prompts[2]}</div>', unsafe_allow_html=True)
                        st.code(prompts[2], language="text")
            else:
                 st.warning("أدخل اسم المنتج لتوليد البرومتات.")

        # التبويب الثالث: الاستراتيجية
        with tabs[2]:
             if product_name:
                with st.spinner("توليد الاستراتيجية..."):
                    st.markdown(ask_ai(api_key, f"اعطني استراتيجية تسويق لمنتج {product_name} للسوق الخليجي."))

        # التبويب الرابع: المالية
        with tabs[3]:
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
                            results.append({
                                "المنطقة": row[country_col],
                                "التسليم (DR)": f"{round(val_dr*100, 1)}%",
                                "التعادل المطلوب": f"{round(break_even_dr*100, 1)}%",
                                "الحالة": status
                            })
                        except: continue

                    if results:
                        st.table(pd.DataFrame(results))
                except Exception as e:
                    st.error(f"خطأ في قراءة ملف البيانات: {str(e)}")
            else:
                st.info("ارفع ملف البيانات المالي لعرض التحليل.")
