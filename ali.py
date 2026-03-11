import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- إعدادات الواجهة الأصلية ---
st.set_page_config(page_title="ALI Engine V19 - Original", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    body, p, h1, h2, h3 { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
</style>
""", unsafe_allow_html=True)

# --- محرك التوليد المستقر ---
def generate_v19(api_key, url):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # البرومت الأصلي الذي أعطاك نتائج جيدة في البداية
    prompt = f"""
    صمم صفحة هبوط احترافية لمنتج من الرابط التالي: {url}
    المواصفات المطلوبة:
    1. استخدام Tailwind CSS.
    2. تطبيق منهجية SOP-1 (13 قسم).
    3. لغة تسويقية قوية (Copywriting Mastery).
    4. الخط: Cairo.
    أعطني كود HTML فقط يبدأ بـ <!DOCTYPE html>.
    """
    response = model.generate_content(prompt)
    return response.text

# --- واجهة المستخدم ---
st.title("🚀 ALI Growth Engine - نسخة V19 المستقرة")

with st.sidebar:
    st.header("🔑 الإعدادات")
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج")
    st.divider()
    st.info("💡 هذه النسخة تعتمد على البساطة لضمان ظهور التصميم.")

if st.button("توليد الصفحة"):
    if api_key and product_url:
        with st.spinner("جاري التوليد..."):
            res = generate_v19(api_key, product_url)
            
            # حجر الزاوية: تنظيف الكود لضمان الرندرة البصرية
            clean_html = res.replace("```html", "").replace("```", "").strip()
            st.session_state.v19_res = clean_html
            st.success("تم التوليد بنجاح!")

# --- عرض النتائج ---
if 'v19_res' in st.session_state:
    tab1, tab2 = st.tabs(["📱 المعاينة البصرية", "💻 الكود المصدري"])
    
    with tab1:
        # العرض المباشر الذي أثبت استقراره
        components.html(st.session_state.v19_res, height=1000, scrolling=True)
        
    with tab2:
        st.code(st.session_state.v19_res, language="html")
