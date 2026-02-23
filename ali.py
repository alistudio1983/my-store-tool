import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة (مع صورتك كأيقونة) ---
# تم استخدام رابط صورتك الشخصية كأيقونة للصفحة
st.set_page_config(page_title="ALI Growth Engine V10", layout="wide", page_icon="https://i.postimg.cc/xCt20gWj/image.png")

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
/* تنسيق الجداول لظهور الأرقام */
.stDataFrame div[data-testid="stTable"] { direction: ltr !important; }
.stDataFrame td, .stDataFrame th { text-align: center !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. دوال الذكاء الاصطناعي ---
def generate_html_page(api_key, product_name):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        أنت خبير برمجة واجهات (Front-end) ومسوق إلكتروني محترف للسوق الخليجي.
        المطلوب: برمجة صفحة هبوط كاملة وجاهزة (HTML & CSS مدمج) لمنتج اسمه: {product_name}.
        
        المواصفات الفنية والتسويقية:
        1. لغة الصفحة: العربية (RTL) بخط 'Tajawal' أو 'Cairo'.
        2. التصميم: حديث، نظيف، وسريع التجاوب (Responsive) للموبايل.
        3. الأقسام المطلوبة:
           - Hero Section: عنوان رئيسي يخطف الأنظار، وصف للحل، وزر "اطلب الآن". استخدم صورة مؤقتة (Placeholder) معبرة.
           - قسم الفوائد: 4 فوائد للمنتج مع إيموجي.
           - قسم التقييمات: 3 آراء لعملاء بأسماء خليجية.
           - زر عائم (Sticky Bottom Button) للطلب المباشر.
        4. الألوان: استخدم ألوان احترافية تزيد التحويل.
        
        ⚠️ شرط صارم: أعطني فقط كود الـ HTML والـ CSS الكامل داخل علامتي ```html و ``` بدون أي مقدمات.
        """
        response = model.generate_content(prompt)
        code = response.text
        if "```html" in code: code = code.split("```html")[1].split("```")[0]
        elif "```" in code: code = code.split("```")[1]
        return code.strip()
    except Exception as e: return f"<h3>خطأ: {str(e)}</h3>"

def generate_image_prompts(api_key, product_name):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        أنت مخرج فني (AI Art Director) متخصص في توليد صور المنتجات التجارية عالية الجودة.
        المهمة: اكتب 3 برومتات (Prompts) احترافية ومفصلة باللغة الإنجليزية لتوليد صور لمنتج: "{product_name}".
        هذه البرومتات ستستخدم في نموذج توليد صور متطور (مثل Nano Banana).

        المطلوب 3 أنواع من الصور:
        1. **صورة الهيرو (Hero Shot):** صورة سينمائية للمنتج في بيئة فاخرة، إضاءة استوديو، تركيز حاد.
        2. **صورة نمط الحياة (Lifestyle Shot):** المنتج قيد الاستخدام في بيئة واقعية وجذابة.
        3. **صورة تفصيلية (Macro Shot):** لقطة مقربة تظهر جودة الخامات والتفاصيل.

        ⚠️ التنسيق المطلوب للإجابة:
        افصل بين كل برومت والآخر باستخدام هذا الفاصل تماماً: "---PROMPT_SEPARATOR---"
        لا تكتب أي مقدمات، فقط البرومتات الإنجليزية الثلاثة مفصولة بالفاصل.
        """
        response = model.generate_content(prompt)
        prompts = response.text.split("---PROMPT_SEPARATOR---")
        return [p.strip() for p in prompts if p.strip()]
    except: return []

def ask_ai(api_key, prompt):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"أجب بالعربية الفصحى فقط: {prompt}")
        return response.text
    except: return "خطأ في الاتصال"

# --- 4. القائمة الجانبية (مع مدخلات المالية) ---
with st.sidebar:
    st.title("🏗️ محرك علي V10.0")
    api_key = st.text_input("🔑 API Key", type="password")
    product_name = st.text_input("📦 اسم المنتج (للصفحة والصور)")
    
    st.markdown("---")
    st.markdown("### 💰 إعدادات المالية (لحساب نقطة التعادل)")
    P = st.number_input("سعر البيع (P)", value=250.0)
    C = st.number_input("التكلفة (C)", value=50.0)
    CPL = st.number_input("تكلفة الليد (CPL)", value=15.0)
    
    st.markdown("---")
    uploaded_file = st.file_uploader("📊 ارفع ملف الإكسل للتحليل", type=['xlsx', 'csv'])
    run_btn = st.button("🚀 تشغيل النظام الشامل")

# --- 5. الواجهة الرئيسية ---
st.markdown('<div class="main-header"><h1>ALI Growth Engine - نظام البناء والتحليل الشامل</h1></div>', unsafe_allow_html=True)

if run_btn:
    if not api_key:
        st.error("الرجاء إدخال API Key للبدء.")
    else:
        tabs = st.tabs(["📄 بناء الصفحة (HTML)", "🖼️ استوديو الصور (Prompts)", "🎯 الاستراتيجية", "💰 التحليل المالي الدقيق"])
        
        # 1. بناء الصفحة
        with tabs[0]:
            if product_name:
                st.subheader(f"✨ جاري بناء الهيكل لـ: {product_name}...")
                with st.spinner("المهندس المعماري يعمل..."):
                    html_code = generate_html_page(api_key, product_name)
                    st.success("✅ تم بناء هيكل الصفحة! (يحتوي على صور مؤقتة)")
                    st.markdown("### 📱 معاينة الصفحة:")
                    components.html(html_code, height=500, scrolling=True)
                    with st.expander("💻 عرض كود الـ HTML للنسخ"):
                        st.code(html_code, language='html')
            else:
                st.warning("أدخل اسم المنتج في القائمة الجانبية لتوليد الصفحة.")

        # 2. استوديو الصور
        with tabs[1]:
            if product_name:
                st.subheader("🖼️ أوامر توليد الصور (لنانو بنانا)")
                st.info("انسخ هذه الأوامر (Prompts) وأعطها لمولد الصور الخاص بك، ثم استبدل الروابط في الكود.")
                with st.spinner("المخرج الفني يكتب البرومتات..."):
                    prompts = generate_image_prompts(api_key, product_name)
                    if len(prompts) >= 3:
                        st.markdown(f'<div class="image-prompt-box"><strong>1️⃣ صورة الهيرو (Hero Shot):</strong><br>{prompts[0]}</div>', unsafe_allow_html=True)
                        st.code(prompts[0], language="text")
                        st.markdown(f'<div class="image-prompt-box"><strong>2️⃣ صورة نمط الحياة (Lifestyle Shot):</strong><br>{prompts[1]}</div>', unsafe_allow_html=True)
                        st.code(prompts[1], language="text")
                        st.markdown(f'<div class="image-prompt-box"><strong>3️⃣ صورة تفصيلية (Macro Shot):</strong><br>{prompts[2]}</div>', unsafe_allow_html=True)
                        st.code(prompts[2], language="text")
                    else:
                        st.error("لم نتمكن من توليد البرومتات بدقة، حاول مرة أخرى.")
            else:
                 st.warning("أدخل اسم المنتج في القائمة الجانبية لتوليد البرومتات.")

        # 3. الاستراتيجية
        with tabs[3]:
             if product_name:
                with st.spinner("توليد الاستراتيجية..."):
                    st.markdown(ask_ai(api_key, f"اعطني استراتيجية تسويق مختصرة لمنتج {product_name} للسوق الخليجي."))
             else:
                 st.warning("أدخل اسم المنتج في القائمة الجانبية لتوليد الاستراتيجية.")

        # 4. التحليل المالي الدقيق (الجديد!)
        with tabs[3]:
            if uploaded_file:
                try:
                    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
                    
                    # --- حساب نقطة التعادل الدقيقة ---
                    # المعادلة: Break-Even DR = (Cost + CPL) / Price
                    break_even_dr = (C + CPL) / P

                    st.subheader("📊 نتائج التحليل المالي الدقيق")
                    st.info(f"💡 نقطة التعادل المحسوبة بناءً على مدخلاتك هي: **{round(break_even_dr * 100, 2)}%** من نسبة التسليم (DR).")

                    st.info("👈 اختر الأعمدة الصحيحة للتحليل من ملفك:")
                    col_a, col_b = st.columns(2)
                    with col_a: country_col = st.selectbox("اختر عمود الدولة/المنطقة:", df.columns)
                    with col_b: dr_col = st.selectbox("اختر عمود نسبة التسليم (DR):", df.columns)
                    
                    results = []
                    for _, row in df.iterrows():
                        try:
                            # تنظيف وتحويل قيمة نسبة التسليم من الملف
                            raw_dr = str(row[dr_col]).replace('%', '').strip()
                            val_dr = float(raw_dr)
                            if val_dr > 1: val_dr /= 100 # تحويل النسبة المئوية إلى كسر عشري (مثلاً 70% تصبح 0.70)
                            
                            # مقارنة نسبة التسليم بنقطة التعادل لتحديد الحالة
                            status = "✅ رابح" if val_dr >= break_even_dr else "🚨 خاسر"
                            
                            results.append({
                                "المنطقة": row[country_col],
                                "التسليم (DR)": f"{round(val_dr*100, 1)}%",
                                "نقطة التعادل المطلوبة": f"{round(break_even_dr*100, 1)}%",
                                "الحالة": status
                            })
                        except: continue # تخطي الصفوف التي تحتوي على أخطاء في البيانات

                    if results:
                        st.table(pd.DataFrame(results)) # عرض النتائج في جدول
                    else:
                        st.warning("لم يتم العثور على بيانات صالحة للتحليل في الأعمدة المختارة.")

                except Exception as e:
                    st.error(f"خطأ في قراءة ملف البيانات: {str(e)}")
            else:
                st.info("ارفع ملف البيانات المالي لعرض تحليل نقطة التعادل الدقيق.")
