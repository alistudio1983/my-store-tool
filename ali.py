import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import re

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V31", layout="wide")

# دالة تنظيف صارمة جداً
def clean_the_code(text):
    if not text: return ""
    # إزالة أي نصوص توضيحية قبل أو بعد الكود
    text = re.sub(r'```html', '', text, flags=re.IGNORECASE)
    text = re.sub(r'```', '', text)
    return text.strip()

# --- 2. القائمة الجانبية ---
with st.sidebar:
    st.header("🔑 إعدادات الوصول")
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج")
    
    st.divider()
    st.header("📊 مصفوفة البريك ايفنت")
    p_price = st.number_input("سعر البيع", value=250)
    p_costs = st.number_input("التكاليف (منتج+شحن+CPL)", value=120)
    be_rate = (p_costs / p_price) * 100 if p_price > 0 else 0

# --- 3. المنطق البرمجي ---
if st.button("🚀 تشغيل المحرك وتوليد الصفحة"):
    if not api_key or not product_url:
        st.error("❌ أرجوك أدخل الـ API Key ورابط المنتج!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            with st.spinner("⏳ جاري التواصل مع الذكاء الاصطناعي..."):
                # برومت الاستراتيجية (Agora + Copywriting Mastery)
                strat_prompt = f"حلل {product_url} واستخرج استراتيجية Agora وسكريبتات فيديو UGC بناءً على قواعد Copywriting Mastery."
                res_strat = model.generate_content(strat_prompt)
                st.session_state.v31_strat = res_strat.text
                
                # برومت صفحة الهبوط (SOP-1 - 13 قسم)
                html_prompt = f"""
                Create a high-converting landing page for {product_url}.
                Framework: 13 sections strictly (Hero, Problem, Solution, Mechanism, etc.) from SOP-1.
                Style: Tailwind CSS, Cairo Font, Mobile-First.
                Return ONLY the HTML code. No talk.
                """
                res_html = model.generate_content(html_prompt)
                st.session_state.v31_html = clean_the_code(res_html.text)
                
                st.session_state.v31_be = be_rate
                st.success("✅ اكتمل التوليد!")
        except Exception as e:
            st.error(f"⚠️ خطأ فني: {str(e)}")

# --- 4. عرض النتائج (الحل النهائي للفراغ) ---
if 'v31_html' in st.session_state:
    tab1, tab2, tab3 = st.tabs(["📱 المعاينة الحية", "🎯 الاستراتيجية", "📊 البريك ايفنت"])
    
    with tab1:
        # إذا كانت المعاينة فارغة، سنعرض الكود ليتمكن المستخدم من نسخه
        if st.session_state.v31_html:
            st.write("💡 إذا لم تظهر المعاينة بالأسفل، استخدم 'كود النسخ' في المربع أدناه.")
            # عرض المعاينة
            components.html(st.session_state.v31_html, height=800, scrolling=True)
            
            with st.expander("📄 كود صفحة الهبوط (جاهز للنسخ)"):
                st.text_area("انسخ الكود بالكامل وضعه في ملف HTML", st.session_state.v31_html, height=300)
        else:
            st.warning("⚠️ يبدو أن الـ API لم يرجع كود HTML. تأكد من الرابط.")

    with tab2:
        st.markdown(st.session_state.v31_strat)

    with tab3:
        st.metric("نسبة التسليم للتعادل (BEP)", f"{st.session_state.v31_be:.2f}%")
