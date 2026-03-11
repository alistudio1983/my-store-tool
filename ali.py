import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import re

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine V32 - API Fix", layout="wide")

def clean_html_tags(raw_text):
    """تنظيف الكود لضمان عرضه في المتصفح"""
    clean = re.sub(r'```html', '', raw_text, flags=re.IGNORECASE)
    clean = re.sub(r'```', '', clean)
    return clean.strip()

# --- 2. القائمة الجانبية ---
with st.sidebar:
    st.title("🏗️ مركز الإعدادات")
    st.info("💡 إذا ظهر خطأ 400، تأكد من مفتاح الـ API الخاص بك.")
    api_key = st.text_input("🔑 Gemini API Key", type="password", help="احصل عليه من Google AI Studio")
    product_url = st.text_input("🔗 رابط المنتج")
    
    st.divider()
    st.markdown("[احصل على API Key مجاني من هنا](https://aistudio.google.com/app/apikey)")

# --- 3. المحرك ---
st.title("🚀 ALI Growth Engine - المصلح")

if st.button("🔥 تفعيل التوليد"):
    if not api_key or not product_url:
        st.warning("أرجوك أدخل المفتاح والرابط.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            with st.spinner("⏳ جاري محاولة الاتصال بـ Google Cloud..."):
                # طلب توليد الصفحة بناءً على المنهجية
                prompt = f"Write a full professional landing page in HTML using Tailwind CSS for: {product_url}. Include 13 sections as per SOP-1. Return ONLY HTML code."
                response = model.generate_content(prompt)
                
                # فحص هل الاستجابة تحتوي على كود
                if response.text:
                    st.session_state.final_v32 = clean_html_tags(response.text)
                    st.success("✅ تم الاتصال والتوليد بنجاح!")
                else:
                    st.error("❌ استجاب الذكاء الاصطناعي بنص فارغ.")
        
        except Exception as e:
            # هذا الجزء سيمسك خطأ 400 الذي ظهر في صورتك ويشرحه لك
            if "400" in str(e):
                st.error("❌ خطأ 400: مفتاح الـ API غير صالح. تأكد من نسخه بشكل صحيح أو قم بتوليد مفتاح جديد.")
            else:
                st.error(f"⚠️ خطأ فني: {str(e)}")

# --- 4. العرض ---
if 'final_v32' in st.session_state:
    t1, t2 = st.tabs(["📱 المعاينة الحية", "💻 الكود المصدري"])
    with t1:
        components.html(st.session_state.final_v32, height=900, scrolling=True)
    with t2:
        st.code(st.session_state.final_v32, language="html")
