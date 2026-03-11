import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import re

# --- إعدادات صارمة ---
st.set_page_config(page_title="ALI Growth Engine V27", layout="wide")

def clean_html_output(raw_text):
    """تنظيف الكود من أي نصوص زائدة أو علامات ماركداون"""
    # البحث عن محتوى بين وسمي <html> أو علامات الكود
    code_match = re.search(r'<html>.*</html>', raw_text, re.DOTALL | re.IGNORECASE)
    if code_match:
        return code_match.group(0)
    # إذا لم يجد وسوم html، نبحث عن علامات الماركداون
    clean_code = raw_text.replace("```html", "").replace("```", "").strip()
    return clean_code

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج")
    
    st.divider()
    st.header("📊 مصفوفة البريك ايفنت")
    price = st.number_input("سعر البيع", value=250)
    cost = st.number_input("التكلفة الإجمالية (منتج + شحن + CPL)", value=100)
    # المعادلة: (التكاليف / سعر البيع) * 100
    be_rate = (cost / price) * 100 if price > 0 else 0

# --- الواجهة الرئيسية ---
st.title("🚀 المحرك الجبار V27")

if st.button("🔥 توليد الآن"):
    if api_key and product_url:
        with st.spinner("جاري بناء الإمبراطورية..."):
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # برومت صارم جداً يركز على SOP-1 و Copywriting Mastery
            prompt = f"""
            بصفتك خبير CRO و Copywriter (نظام Agora):
            المنتج: {product_url}
            المطلوب: كود HTML متكامل لصفحة هبوط بـ 13 قسم (SOP-1).
            شروط بصرية: استخدم Tailwind CSS، خط Cairo، ألوان المنتج، Mobile-First.
            يجب أن يبدأ الكود بـ <html> وينتهي بـ </html>.
            لا تكتب أي كلمة خارج الكود.
            """
            
            response = model.generate_content(prompt)
            st.session_state.raw_res = response.text
            st.session_state.clean_html = clean_html_output(response.text)
            st.success("تم التوليد!")

# --- عرض النتائج ---
tab1, tab2 = st.tabs(["📱 المعاينة الحية", "📊 التحليل المالي"])

with tab1:
    if 'clean_html' in st.session_state:
        # استخدام iframe بخصائص تسمح بالتحميل الصحيح
        components.html(st.session_state.clean_html, height=1200, scrolling=True)
        with st.expander("💻 عرض الكود المصدري"):
            st.code(st.session_state.clean_html, language="html")

with tab2:
    st.metric("نقطة التعادل (Delivery Rate)", f"{be_rate}%")
    st.write(f"لتحقيق الربح، يجب أن تتجاوز نسبة التسليم لديك **{be_rate}%**.")
