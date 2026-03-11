import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine V30 - Final", layout="wide")

# نصوص المنهجية المدمجة (SOP & Copywriting)
SOP_RULES = "13 Sections: Hero, Trust, Problem, Solution, Mechanism, Grid, Comparison, Specs, Social, Expert, Steps, Guarantee, Footer."

# --- 2. دالة التوليد ---
def generate_master_lp(api_key, url):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    Create a professional Landing Page for: {url}
    Rules: Use Tailwind CSS, Cairo Font, 13 Sections based on SOP: {SOP_RULES}.
    Style: High-end E-commerce (Like Shopify Plus).
    Output: ONLY raw HTML/CSS code. No talking.
    """
    return model.generate_content(prompt).text

# --- 3. الواجهة ---
st.title("🏗️ ALI Growth Engine V30 (The Final Solution)")

with st.sidebar:
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج")
    
    st.divider()
    st.header("💰 حساب البريك ايفنت (Matrix)")
    p_price = st.number_input("سعر البيع", value=250)
    p_cost = st.number_input("التكلفة (منتج+شحن+CPL)", value=100)
    # المعادلة: التكلفة تقسيم سعر البيع
    be_rate = (p_cost / p_price) * 100 if p_price > 0 else 0

if st.button("🚀 توليد النظام الكامل وتجهيز الملف"):
    if api_key and product_url:
        with st.spinner("جاري استخراج البيانات وبناء الصفحة..."):
            raw_html = generate_master_lp(api_key, product_url)
            clean_html = raw_html.replace("```html", "").replace("```", "").strip()
            
            # حفظ في ذاكرة الجلسة
            st.session_state.v30_html = clean_html
            st.success("✅ تم التوليد بنجاح! استخدم الأزرار بالأسفل.")

# --- 4. العرض (الحل الجذري للمساحة الفارغة) ---
t1, t2 = st.tabs(["💎 لوحة التحكم والعرض", "📊 مصفوفة الأرقام"])

with t1:
    if 'v30_html' in st.session_state:
        # الحل 1: زر تحميل الملف (أضمن طريقة لرؤية النتيجة)
        st.download_button(
            label="📥 تحميل صفحة الهبوط (HTML File)",
            data=st.session_state.v30_html,
            file_name="landing_page.html",
            mime="text/html"
        )
        
        # الحل 2: عرض الكود مباشرة للنسخ
        with st.expander("📄 انسخ الكود من هنا (في حال لم يفتح الملف)"):
            st.code(st.session_state.v30_html, language="html")
        
        # الحل 3: محاولة العرض المباشر (للتجربة فقط)
        st.markdown("---")
        st.subheader("👀 معاينة سريعة (إذا ظهرت فارغة استخدم زر التحميل أعلاه)")
        components.html(st.session_state.v30_html, height=600, scrolling=True)

with t2:
    st.metric("نقطة التعادل (Delivery Rate)", f"{be_rate:.2f}%")
    st.info(f"يجب أن تكون نسبة تسليم الطلبيات أعلى من {be_rate:.2f}% لتحقيق أي ربح.")
