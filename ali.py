import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import re

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine - Fixed V1", layout="wide")

# دالة لتنظيف الكود (هذا ما كان ينقص الكود الأول)
def extract_clean_html(raw_text):
    # إزالة علامات الماركداون إذا وجدت
    clean_code = re.sub(r'```html', '', raw_text, flags=re.IGNORECASE)
    clean_code = re.sub(r'```', '', clean_code)
    return clean_code.strip()

# --- 2. الواجهة الجانبية ---
with st.sidebar:
    st.title("🛠️ الإعدادات")
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج (URL)")
    
    st.divider()
    st.header("📊 مصفوفة البريك ايفنت")
    # المعادلة المستخلصة من ملف الإكسل الخاص بك
    price = st.number_input("سعر البيع", value=250)
    cost = st.number_input("التكلفة (منتج+شحن+CPL)", value=100)
    be_rate = (cost / price) * 100 if price > 0 else 0

# --- 3. العرض الرئيسي ---
st.header("🚀 ALI Growth Engine")

if st.button("توليد صفحة الهبوط والاستراتيجية"):
    if not api_key or not product_url:
        st.error("يرجى إدخال API Key والرابط أولاً")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            with st.spinner("جاري التوليد..."):
                # طلب الاستراتيجية (بناءً على ملف Copywriting Mastery)
                strat_prompt = f"حلل المنتج {product_url} واستخرج استراتيجية Agora وسكريبتات فيديو UGC."
                strat_res = model.generate_content(strat_prompt)
                st.session_state.strategy = strat_res.text
                
                # طلب صفحة الهبوط (بناءً على SOP-1 - 13 قسم)
                html_prompt = f"""
                صمم صفحة هبوط Tailwind CSS لمنتج {product_url}. 
                يجب أن تحتوي على 13 قسم (Hero, Problem, Solution, Mechanism...). 
                الألوان: مستوحاة من المنتج. الخط: Cairo. 
                أعطني كود HTML فقط.
                """
                html_res = model.generate_content(html_prompt)
                # تنظيف الكود فوراً قبل الحفظ
                st.session_state.html = extract_clean_html(html_res.text)
                st.session_state.be = be_rate
                
        except Exception as e:
            st.error(f"خطأ في الاتصال: {e}")

# --- 4. عرض النتائج (الأجزاء التي كانت تختفي) ---
if 'html' in st.session_state:
    tab1, tab2, tab3 = st.tabs(["📱 المعاينة الحية", "🎯 الاستراتيجية", "📊 البريك ايفنت"])
    
    with tab1:
        st.success("تم التوليد! إذا كانت المساحة بيضاء، انتظر ثوانٍ للتحميل.")
        # عرض الكود باستخدام مكون Streamlit الرسمي
        components.html(st.session_state.html, height=1000, scrolling=True)
        with st.expander("نسخ الكود البرمجي"):
            st.code(st.session_state.html, language="html")
            
    with tab2:
        st.markdown(st.session_state.strategy)
        
    with tab3:
        st.metric("نسبة التسليم المطلوبة للتعادل", f"{st.session_state.be:.2f}%")
