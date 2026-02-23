import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V13", layout="wide", page_icon="https://i.postimg.cc/xCt20gWj/image.png")

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

# --- 3. تهيئة الذاكرة ---
if 'html_code' not in st.session_state: st.session_state.html_code = ""
if 'image_prompts' not in st.session_state: st.session_state.image_prompts = []
if 'video_scripts' not in st.session_state: st.session_state.video_scripts = ""
if 'marketing_strategy' not in st.session_state: st.session_state.marketing_strategy = ""
if 'active_model' not in st.session_state: st.session_state.active_model = None

# --- 4. دوال الذكاء الاصطناعي (محدثة بقواعد Copywriting Mastery & Agora) ---
def get_working_model(api_key):
    if st.session_state.active_model: return st.session_state.active_model
    try:
        genai.configure(api_key=api_key)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name.lower():
                st.session_state.active_model = m.name
                return m.name
        st.session_state.active_model = "gemini-pro"
        return "gemini-pro"
    except: return "gemini-pro"

def generate_html_page(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        # برومت مدمج بقواعد PAS و FAB والمحفزات النفسية
        prompt = f"""أنت أعظم كاتب إعلانات (Copywriter) مبرمج ومصمم واجهات في العالم.
        المطلوب: برمجة صفحة هبوط كاملة (HTML & CSS مدمج) لمنتج: {product_name}.
        
        ⚠️ القواعد التسويقية الصارمة للتصميم والنص:
        1. الهيكل الأعلى (Hero): استخدم إطار PAS (Problem, Agitate, Solution). ابدأ بنقطة الألم، ضخمها، ثم قدم المنتج كحل نهائي.
        2. الفوائد (Benefits): استخدم إطار FAB (Feature, Advantage, Benefit). لا تذكر ميزة إلا وتربطها بنتيجة عاطفية للعميل (كيف سيشعر).
        3. المحفزات النفسية: يجب أن يتضمن التصميم أقساماً واضحة لـ (الدليل الاجتماعي - 3 تقييمات قوية) و (عكس المخاطر - ضمان استرجاع أو تجربة بدون مخاطر).
        4. الوضوح التام: لا تستخدم مصطلحات تقنية معقدة. فكرة واحدة لكل جملة. جمل قصيرة جداً ومقنعة.
        5. النداء للعمل (CTA): اجعله واضحاً، يخلق إلحاحاً (Urgency)، مثل "اطلب الآن ووفر، الكمية محدودة!".
        
        ⚠️ القواعد البرمجية:
        لغة الصفحة العربية (RTL) بخط 'Cairo'. تصميم حديث وسريع التجاوب (Responsive). زر عائم للطلب في الأسفل.
        أعطني فقط كود الـ HTML والـ CSS الكامل داخل علامتي ```html و ```."""
        
        response = model.generate_content(prompt)
        code = response.text
        if "```html" in code: code = code.split("```html")[1].split("```")[0]
        elif "```" in code: code = code.split("```")[1]
        return code.strip()
    except Exception as e: return f"<h3>خطأ في التوليد: {str(e)}</h3>"

def generate_video_scripts(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        # برومت مدمج بقواعد AIDA
        prompt = f"""أنت خبير محتوى تسويقي و Copywriter محترف. 
        اكتب 5 سكريبتات مفصلة لفيديوهات (UGC) قصيرة لمنتج: {product_name}.
        خصصها للمنصات: 1. تيك توك، 2. انستجرام ريلز، 3. يوتيوب شورتس، 4. سناب شات، 5. فيسبوك.
        
        ⚠️ قواعد الكتابة لكل سكريبت:
        1. الإطار العام: استخدم نموذج AIDA (انتباه، اهتمام، رغبة، إجراء).
        2. الثواني الأولى (Hook): يجب أن تخطف الانتباه فوراً بالتركيز على مشكلة العميل (Pain Point) وليس المنتج.
        3. العاطفة قبل المنطق: اجعل التعليق الصوتي يركز على (النتيجة العاطفية) التي سيحصل عليها العميل.
        4. المحفزات: ادمج محفز (الندرة) أو (الإلحاح) في الثواني الأخيرة لدفعهم نحو زر الشراء.
        
        أعطني السكريبتات منسقة بشكل احترافي."""
        return model.generate_content(prompt).text
    except Exception as e: return f"خطأ: {str(e)}"

def generate_strategy(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        # برومت مدمج بقواعد Agora (الحجة والآلية الفريدة)
        prompt = f"""أنت خبير أبحاث تسويقية من مدرسة Agora العملاقة لكتابة الإعلانات.
        المطلوب: دراسة سوق واستراتيجية اختراق لمنتج: {product_name}.
        
        ⚠️ يجب أن تغطي دراستك بدقة ما يلي:
        1. الآلية الفريدة (Unique Mechanism): لا تروج للمنتج كسلعة عادية. ما هو الشيء الفريد، المختلف، والأفضل في هذا المنتج الذي يجعله الحل الوحيد الفعال مقارنة بالمنافسين؟
        2. الحجة التي لا تقهر (The Magnificent Argument): ما هي الحجة المنطقية والعاطفية المتسلسلة التي يجب أن نبنيها في عقل العميل ليقتنع بالشراء؟ (ركز على الحجة وليس مجرد الكلمات الرنانة).
        3. المعتقدات الأساسية (Necessary Beliefs): اكتب 4 معتقدات حتمية يجب أن نزرعها في عقل العميل المستهدف قبل أن نعرض عليه المنتج، بصيغة "يجب أن يعتقد أن...".
        4. فجوات السوق (Market Gaps): ما هي نقاط الضعف في إعلانات المنافسين التي يمكننا استغلالها؟"""
        return model.generate_content(prompt).text
    except Exception as e: return f"خطأ: {str(e)}"

def generate_image_prompts(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""اكتب 3 برومتات (Prompts) احترافية باللغة الإنجليزية لتوليد صور لمنتج: "{product_name}".
        1. Hero Shot
        2. Lifestyle Shot
        3. Macro Shot
        افصل بينها بـ: "---PROMPT_SEPARATOR---" """
        response = model.generate_content(prompt)
        prompts = response.text.split("---PROMPT_SEPARATOR---")
        return [p.strip() for p in prompts if p.strip()]
    except: return []

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.title("🏗️ محرك علي V13.0")
    api_key = st.text_input("🔑 API Key", type="password")
    product_name = st.text_input("📦 اسم المنتج")
    st.markdown("---")
    st.markdown("### 💰 إعدادات المالية (نقطة التعادل)")
    P = st.number_input("سعر البيع (P)", value=250.0)
    C = st.number_input("التكلفة (C)", value=50.0)
    CPL = st.number_input("تكلفة الليد (CPL)", value=15.0)
    uploaded_file = st.file_uploader("📊 ارفع ملف الإكسل (المالية)", type=['xlsx', 'csv'])

# --- 6. الواجهة الرئيسية ---
st.markdown('<div class="main-header"><h1>ALI Growth Engine - Master Copywriter</h1></div>', unsafe_allow_html=True)

if not api_key:
    st.warning("الرجاء إدخال API Key في القائمة الجانبية للبدء.")
else:
    tabs = st.tabs(["🎯 الاستراتيجية (Agora)", "📄 صفحة الهبوط (PAS/FAB)", "🎬 سكريبتات الفيديو (AIDA)", "🖼️ استوديو الصور", "💰 التحليل المالي"])
    
    # --- التبويب 1: الاستراتيجية ---
    with tabs[0]:
        st.subheader("دراسة السوق وبناء الحجة (طريقة Agora)")
        if st.button("🧠 استخراج الاستراتيجية والآلية الفريدة"):
            if product_name:
                with st.spinner("جاري تحليل السوق وبناء الحجة..."):
                    st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
            else: st.error("أدخل اسم المنتج أولاً!")
        if st.session_state.marketing_strategy:
            st.markdown(st.session_state.marketing_strategy)

    # --- التبويب 2: صفحة الهبوط ---
    with tabs[1]:
        st.subheader("بناء صفحة الهبوط (هياكل PAS و FAB)")
        if st.button("🚀 توليد صفحة الهبوط الاحترافية"):
            if product_name:
                with st.spinner("جاري برمجة وتصميم الصفحة..."):
                    st.session_state.html_code = generate_html_page(api_key, product_name)
            else: st.error("أدخل اسم المنتج أولاً!")
        if st.session_state.html_code:
            st.success("✅ الصفحة جاهزة ومبنية على أصول علم النفس الشرائي!")
            components.html(st.session_state.html_code, height=500, scrolling=True)
            with st.expander("💻 عرض كود الـ HTML للنسخ"):
                st.code(st.session_state.html_code, language='html')

    # --- التبويب 3: سكريبتات الفيديو ---
    with tabs[2]:
        st.subheader("توليد 5 سكريبتات فيديو (نموذج AIDA)")
        if st.button("🎬 توليد السكريبتات البيعية"):
            if product_name:
                with st.spinner("جاري كتابة السكريبتات..."):
                    st.session_state.video_scripts = generate_video_scripts(api_key, product_name)
            else: st.error("أدخل اسم المنتج أولاً!")
        if st.session_state.video_scripts:
            st.markdown(st.session_state.video_scripts)

    # --- التبويب 4: استوديو الصور ---
    with tabs[3]:
        st.subheader("أوامر توليد الصور")
        if st.button("🖼️ توليد البرومتات"):
            if product_name:
                with st.spinner("المخرج الفني يعمل..."):
                    st.session_state.image_prompts = generate_image_prompts(api_key, product_name)
            else: st.error("أدخل اسم المنتج أولاً!")
        if st.session_state.image_prompts and len(st.session_state.image_prompts) >= 3:
            for i, p in enumerate(st.session_state.image_prompts):
                st.markdown(f'<div class="image-prompt-box"><strong>البرومت {i+1}:</strong><br>{p}</div>', unsafe_allow_html=True)
                st.code(p, language="text")

    # --- التبويب 5: التحليل المالي ---
    with tabs[4]:
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
                        results.append({"المنطقة": row[country_col], "التسليم (DR)": f"{round(val_dr*100, 1)}%", "التعادل المطلوب": f"{round(break_even_dr*100, 1)}%", "الحالة": status})
                    except: continue
                if results: st.table(pd.DataFrame(results))
            except Exception as e: st.error(f"خطأ: {str(e)}")
        else:
            st.info("ارفع ملف البيانات المالي لعرض التحليل.")
