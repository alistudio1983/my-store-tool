import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="API Tester", layout="centered")

st.title("🛡️ فاحص صلاحية المفتاح")

with st.sidebar:
    api_key = st.text_input("ضع المفتاح هنا للفحص", type="password")

if st.button("تحقق من الصلاحية"):
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            # محاولة توليد كلمة واحدة فقط للتأكد
            response = model.generate_content("Say Hello")
            if response.text:
                st.success("✅ المفتاح صالح وشغال 100%! يمكنك الآن استخدامه في الكود الكبير.")
        except Exception as e:
            if "400" in str(e):
                st.error("❌ المفتاح غير صالح (Error 400). يرجى توليد مفتاح جديد من AI Studio.")
            elif "429" in str(e):
                st.warning("⚠️ المفتاح صالح ولكنك وصلت للحد الأقصى للاستخدام المجاني.")
            else:
                st.error(f"⚠️ خطأ آخر: {e}")
    else:
        st.warning("يرجى إدخال مفتاح أولاً.")
