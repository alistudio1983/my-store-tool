import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import base64

# --- 1. إعدادات صارمة للواجهة ---
st.set_page_config(page_title="ALI Engine V28 - Ultimate", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    body { background-color: #0e1117; color: white; font-family: 'Cairo'; }
    .status-card { background: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #3b82f6; }
</style>
""", unsafe_allow_html=True)

# --- 2. محرك الحقن البصري ---
def display_html_safely(html_code):
    """تحويل الكود إلى صيغة Base64 لضمان العرض في المتصفحات الصعبة"""
    b64 = base64.b64encode(html_code.encode('utf-8')).decode('utf-8')
    src = f"data:text/html;base64,{b64}"
    components.iframe(src, height=1000, scrolling=True)

# --- 3. لوحة التحكم ---
with st.sidebar:
    st.title("🏗️ مركز التحكم V28")
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج (URL)")
    
    st.divider()
    st.header("📉 الحساب المالي المباشر")
    price = st.number_input("سعر البيع", value=250)
    costs = st.number_input("إجمالي التكاليف (COGS+CPL+Ship)", value=120)
    conf = st.slider("نسبة التأكيد %", 10, 100, 80) / 100
    
    # حساب البريك ايفنت الفوري
    be_rate = round(((costs / (price * conf)) * 100), 2) if (price * conf) > 0 else 0

# --- 4. معالجة البيانات ---
st.header("🚀 ALI Growth Engine - Tactical Output")

if st.button("🔥 تفعيل التوليد الشامل"):
    if not api_key or not product_url:
        st.error("❌ خطأ: يرجى إدخال الرابط والمفتاح.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            with st.spinner("⏳ جاري استخراج البيانات وبناء الهيكل..."):
                # البرومت الصارم المستوحى من ملفاتك (Copywriting + SOP)
                master_prompt = f"""
                Act as a World-Class Landing Page Designer & Copywriter.
                Product: {product_url}
                Framework: Agora Copywriting (PAS + FAB).
                Instructions: Create a full HTML page with Tailwind CSS.
                Sections (Strictly 13):
                1. Hero with product image 2. Trust Bar 3. Problem 4. Solution 
                5. Unique Mechanism 6. Benefits Grid 7. Comparison Table 8. Features 
                9. Social Proof 10. Authority Quote 11. Steps 12. Guarantee 13. Sticky CTA.
                
                CSS: Rounded-3xl, Shadows, Cairo Font, Vibrant Colors matching the product.
                Output: Return ONLY the raw HTML code. No conversation.
                """
                
                response = model.generate_content(master_prompt)
                
                # تخزين النتيجة في الجلسة مع "معرف فريد" لإجبار التحديث
                st.session_state.html_final = response.text.replace("```html", "").replace("```", "").strip()
                st.session_state.update_id = st.session_state.get('update_id', 0) + 1
                
        except Exception as e:
            st.error(f"⚠️ حدث خطأ تقني: {str(e)}")

# --- 5. العرض المقسم ---
tab1, tab2 = st.tabs(["🖼️ المعاينة البصرية (SOP-1)", "📊 المصفوفة المالية"])

with tab1:
    if 'html_final' in st.session_state:
        st.success(f"✅ تم تحديث التصميم بنجاح (نسخة #{st.session_state.update_id})")
        display_html_safely(st.session_state.html_final)
        with st.expander("💻 الكود المصدري للنسخ"):
            st.code(st.session_state.html_final, language="html")
    else:
        st.info("قم بالضغط على 'تفعيل التوليد' أعلاه لبدء العمل.")

with tab2:
    st.markdown(f"""
    <div class="status-card">
        <h3>نقطة التعادل المطلوبة (Delivery Rate)</h3>
        <h1 style="color:#3b82f6;">{be_rate}%</h1>
        <p>بناءً على سعر {price} وتكاليف {costs}، يجب أن تحقق نسبة تسليم {be_rate}% لتصل للتعادل.</p>
    </div>
    """, unsafe_allow_html=True)
