import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re
import pandas as pd
import requests
import random
import urllib.parse

st.set_page_config(page_title="ALI Engine Pro - AI Landing Pages", layout="wide", page_icon="\U0001f680")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; background-color: #f8fafc;
    }
    .main-header { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; padding: 40px 20px; border-radius: 20px; text-align: center; margin-bottom: 35px; box-shadow: 0 20px 40px -10px rgba(15,23,42,0.3); border-bottom: 5px solid #3b82f6; }
    .main-header h1 { font-weight: 900; font-size: 3rem; margin-bottom: 5px; background: linear-gradient(to right, #93c5fd, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .main-header p { color: #94a3b8; font-size: 1.2rem; font-weight: 600; }
    .stButton > button { background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important; color: white !important; font-weight: 800 !important; font-size: 1.1rem !important; border: none !important; border-radius: 12px !important; padding: 15px 30px !important; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>ALI Growth Engine Pro \U0001f680</h1><p>\u0645\u0646\u0635\u0629 \u0627\u0644\u0639\u0645\u0644\u064a\u0627\u062a \u0627\u0644\u062a\u0633\u0648\u064a\u0642\u064a\u0629 \u0627\u0644\u0645\u062a\u0643\u0627\u0645\u0644\u0629 | \u0635\u0648\u0631 AI \u0639\u0627\u0644\u064a\u0629 \u0627\u0644\u062c\u0648\u062f\u0629</p></div>', unsafe_allow_html=True)

def get_ai_image(keyword, width=800, height=600, style="professional"):
    safe_keyword = str(keyword).strip()
    if not safe_keyword or safe_keyword.lower() == "none":
        safe_keyword = "product"
    if style == "product":
        prompt = f"professional studio product photography of {safe_keyword}, white background, high resolution, commercial quality, 8k, sharp focus, soft lighting"
    elif style == "person":
        prompt = f"professional portrait photo of {safe_keyword}, natural lighting, high quality, realistic, candid, authentic"
    elif style == "before_after":
        prompt = f"realistic before and after comparison photo of {safe_keyword}, high quality, clear difference, professional photography"
    elif style == "lifestyle":
        prompt = f"lifestyle photography of person using {safe_keyword}, natural setting, warm lighting, authentic, high quality, 8k"
    elif style == "ingredient":
        prompt = f"close up macro photography of {safe_keyword}, natural organic ingredient, studio lighting, white background, 8k, detailed texture"
    elif style == "dimensions":
        prompt = f"product dimensions diagram of {safe_keyword}, measurement overlay, clean white background, professional product photo with size reference, 8k"
    elif style == "gif_step":
        prompt = f"step by step tutorial photo showing how to use {safe_keyword}, clean hands demonstration, bright lighting, instructional photography, 8k"
    else:
        prompt = f"professional high quality photo of {safe_keyword}, 8k, sharp, realistic, commercial photography"
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 999999)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={seed}&model=flux"

AUTO_COLORS = {
    "cosmetics": {"primary": "#0f766e", "secondary": "#f0fdfa", "accent": "#eab308", "gradient1": "#0f766e", "gradient2": "#14b8a6"},
    "skincare": {"primary": "#be185d", "secondary": "#fdf2f8", "accent": "#f59e0b", "gradient1": "#be185d", "gradient2": "#ec4899"},
    "health": {"primary": "#15803d", "secondary": "#f0fdf4", "accent": "#f97316", "gradient1": "#15803d", "gradient2": "#22c55e"},
    "gadgets": {"primary": "#1e3a5f", "secondary": "#f0f4f8", "accent": "#ef4444", "gradient1": "#1e3a5f", "gradient2": "#3b82f6"},
    "fashion": {"primary": "#7c2d12", "secondary": "#fef3c7", "accent": "#d97706", "gradient1": "#7c2d12", "gradient2": "#ea580c"},
    "default": {"primary": "#1e40af", "secondary": "#eff6ff", "accent": "#f59e0b", "gradient1": "#1e40af", "gradient2": "#3b82f6"}
}

def detect_colors(product_name, category):
    text = (product_name + " " + category).lower()
    if any(w in text for w in ["cream", "\u0643\u0631\u064a\u0645", "collagen", "\u0643\u0648\u0644\u0627\u062c\u064a\u0646", "serum", "\u0633\u064a\u0631\u0648\u0645", "cosmetic", "\u062a\u062c\u0645\u064a\u0644"]):
        return AUTO_COLORS["skincare"]
    elif any(w in text for w in ["skin", "\u0628\u0634\u0631\u0629", "face", "\u0648\u062c\u0647", "beauty", "\u062c\u0645\u0627\u0644"]):
        return AUTO_COLORS["cosmetics"]
    elif any(w in text for w in ["health", "\u0635\u062d\u0629", "vitamin", "\u0641\u064a\u062a\u0627\u0645\u064a\u0646", "supplement", "\u0645\u0643\u0645\u0644"]):
        return AUTO_COLORS["health"]
    elif any(w in text for w in ["gadget", "\u062c\u0647\u0627\u0632", "device", "\u0623\u062f\u0627\u0629", "smart", "\u0630\u0643\u064a"]):
        return AUTO_COLORS["gadgets"]
    elif any(w in text for w in ["fashion", "\u0645\u0648\u0636\u0629", "clothes", "\u0645\u0644\u0627\u0628\u0633"]):
        return AUTO_COLORS["fashion"]
    elif "cosmetics" in text.lower() or "Cosmetics" in category:
        return AUTO_COLORS["cosmetics"]
    else:
        return AUTO_COLORS["default"]

def get_fast_working_model(api_key):
    if 'valid_model_name' in st.session_state:
        return st.session_state.valid_model_name
    genai.configure(api_key=api_key, transport="rest")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name.lower():
                st.session_state.valid_model_name = m.name
                return m.name
    except:
        pass
    st.session_state.valid_model_name = "gemini-pro"
    return "gemini-pro"

def generate_landing_page_json(api_key, product, category):
    genai.configure(api_key=api_key, transport="rest")
    model_name = get_fast_working_model(api_key)
    model = genai.GenerativeModel(model_name)
    prompt = f"""
\u0623\u0646\u062a \u062e\u0628\u064a\u0631 Copywriter \u0644\u0635\u0641\u062d\u0627\u062a \u0627\u0644\u0647\u0628\u0648\u0637. \u0627\u0644\u0645\u0646\u062a\u062c: "{product}". \u0627\u0644\u0641\u0626\u0629: "{category}".
\u0627\u0644\u0646\u0635\u0648\u0635 \u0628\u0627\u0644\u0639\u0631\u0628\u064a\u0629 \u0627\u0644\u0641\u0635\u062d\u0649. \u0627\u0644\u062d\u0642\u0648\u0644 \u0627\u0644\u0645\u0646\u062a\u0647\u064a\u0629 \u0628\u0640 _search \u0647\u064a \u0643\u0644\u0645\u0627\u062a \u0628\u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a\u0629 \u0644\u062a\u0648\u0644\u064a\u062f \u0635\u0648\u0631 AI.
\u0631\u062f \u0628\u0635\u064a\u063a\u0629 JSON \u0635\u0627\u0644\u062d\u0629:
{{
    "hero_headline": "\u0639\u0646\u0648\u0627\u0646 \u0631\u0626\u064a\u0633\u064a \u064a\u062e\u0637\u0641 \u0627\u0644\u0627\u0646\u062a\u0628\u0627\u0647",
    "hero_subheadline": "\u0639\u0646\u0648\u0627\u0646 \u0641\u0631\u0639\u064a",
    "image_hero_search": "english keyword for product photo",
    "image_hero_lifestyle_search": "english keyword lifestyle photo of person using product",
    "image_hero_closeup_search": "english keyword close up detail of product",
    "trust_badges": ["\u0634\u062d\u0646 \u0645\u062c\u0627\u0646\u064a", "\u0627\u0644\u062f\u0641\u0639 \u0639\u0646\u062f \u0627\u0644\u0627\u0633\u062a\u0644\u0627\u0645", "\u0636\u0645\u0627\u0646 30 \u064a\u0648\u0645"],
    "social_proof_number": "+12,000",
    "social_proof_text": "\u0639\u0645\u064a\u0644 \u0633\u0639\u064a\u062f",
    "problem_title": "\u0639\u0646\u0648\u0627\u0646 \u0642\u0633\u0645 \u0627\u0644\u0623\u0644\u0645",
    "problem_description": "\u0641\u0642\u0631\u0629 \u062a\u0635\u0641 \u0627\u0644\u0625\u062d\u0628\u0627\u0637",
    "problem_points": ["\u0645\u0634\u0643\u0644\u0629 1", "\u0645\u0634\u0643\u0644\u0629 2", "\u0645\u0634\u0643\u0644\u0629 3"],
    "image_problem_search": "english keyword for problem",
    "image_problem_2_search": "english keyword second problem visual",
    "solution_title": "\u0639\u0646\u0648\u0627\u0646 \u0627\u0644\u062d\u0644",
    "solution_description": "\u0641\u0642\u0631\u0629 \u0627\u0644\u062d\u0644",
    "image_solution_search": "english keyword for solution",
    "image_solution_2_search": "english keyword second solution visual",
    "image_before_search": "english keyword before",
    "image_after_search": "english keyword after",
    "features": [
        {{"title": "\u0645\u064a\u0632\u0629 1", "desc": "\u0627\u0644\u0641\u0627\u0626\u062f\u0629", "icon": "sparkles", "image_search": "keyword1"}},
        {{"title": "\u0645\u064a\u0632\u0629 2", "desc": "\u0627\u0644\u0641\u0627\u0626\u062f\u0629", "icon": "shield", "image_search": "keyword2"}},
        {{"title": "\u0645\u064a\u0632\u0629 3", "desc": "\u0627\u0644\u0641\u0627\u0626\u062f\u0629", "icon": "heart", "image_search": "keyword3"}},
        {{"title": "\u0645\u064a\u0632\u0629 4", "desc": "\u0627\u0644\u0641\u0627\u0626\u062f\u0629", "icon": "check", "image_search": "keyword4"}}
    ],
    "ingredients": [
        {{"name": "\u0645\u0643\u0648\u0646 1", "benefit": "\u0641\u0627\u0626\u062f\u062a\u0647", "image_search": "ingredient keyword"}},
        {{"name": "\u0645\u0643\u0648\u0646 2", "benefit": "\u0641\u0627\u0626\u062f\u062a\u0647", "image_search": "ingredient keyword"}},
        {{"name": "\u0645\u0643\u0648\u0646 3", "benefit": "\u0641\u0627\u0626\u062f\u062a\u0647", "image_search": "ingredient keyword"}}
    ],
    "how_to_use": ["\u062e\u0637\u0648\u0629 1", "\u062e\u0637\u0648\u0629 2", "\u062e\u0637\u0648\u0629 3"],
    "how_to_use_images": ["step 1 keyword", "step 2 keyword", "step 3 keyword"],
    "dimensions": {{"height": "15 cm", "width": "8 cm", "weight": "200g", "volume": "50ml", "image_search": "product with ruler measurement"}},
    "stats": [{{"number": "98%", "label": "\u0625\u062d\u0635\u0627\u0626\u064a\u0629 1"}}, {{"number": "+5000", "label": "\u0625\u062d\u0635\u0627\u0626\u064a\u0629 2"}}, {{"number": "4.9/5", "label": "\u0625\u062d\u0635\u0627\u0626\u064a\u0629 3"}}],
    "reviews": [
        {{"name": "\u0633\u0627\u0631\u0629 \u0645.", "rating": 5, "comment": "\u062a\u0639\u0644\u064a\u0642 \u0648\u0627\u0642\u0639\u064a", "image_search": "happy arab woman selfie"}},
        {{"name": "\u0623\u062d\u0645\u062f \u0639.", "rating": 5, "comment": "\u062a\u0639\u0644\u064a\u0642 \u0648\u0627\u0642\u0639\u064a", "image_search": "satisfied arab man"}},
        {{"name": "\u0646\u0648\u0631\u0629 \u0643.", "rating": 4, "comment": "\u062a\u0639\u0644\u064a\u0642 \u0648\u0627\u0642\u0639\u064a", "image_search": "happy woman portrait"}}
    ],
    "pricing": {{"original": "399", "discounted": "199", "currency": "SAR", "discount_percent": "50%"}},
    "urgency_text": "\u0627\u0644\u0639\u0631\u0636 \u064a\u0646\u062a\u0647\u064a \u062e\u0644\u0627\u0644 24 \u0633\u0627\u0639\u0629!",
    "faq": [
        {{"q": "\u0645\u062a\u0649 \u0633\u0623\u0644\u0627\u062d\u0638 \u0627\u0644\u0646\u062a\u0627\u0626\u062c\u061f", "a": "\u0625\u062c\u0627\u0628\u0629"}},
        {{"q": "\u0647\u0644 \u0627\u0644\u0645\u0646\u062a\u062c \u0622\u0645\u0646\u061f", "a": "\u0625\u062c\u0627\u0628\u0629"}},
        {{"q": "\u0643\u064a\u0641 \u0623\u0637\u0644\u0628\u061f", "a": "\u0625\u062c\u0627\u0628\u0629"}},
        {{"q": "\u0645\u0627 \u0633\u064a\u0627\u0633\u0629 \u0627\u0644\u0625\u0631\u062c\u0627\u0639\u061f", "a": "\u0625\u062c\u0627\u0628\u0629"}}
    ],
    "guarantee_title": "\u0636\u0645\u0627\u0646 \u0627\u0633\u062a\u0631\u062c\u0627\u0639 \u0627\u0644\u0645\u0627\u0644",
    "guarantee_text": "\u0646\u0635 \u0627\u0644\u0636\u0645\u0627\u0646",
    "call_to_action": "\u0627\u0637\u0644\u0628 \u0627\u0644\u0622\u0646",
    "footer_text": "\u062c\u0645\u064a\u0639 \u0627\u0644\u062d\u0642\u0648\u0642 \u0645\u062d\u0641\u0648\u0638\u0629"
}}
"""
    response = model.generate_content(prompt, request_options={"timeout": 60.0})
    tb = chr(96) * 3
    clean_text = re.sub(f'{tb}(?:json|JSON)?', '', response.text, flags=re.IGNORECASE)
    clean_text = clean_text.replace(tb, '').strip()
    match = re.search(r'\{.*\}', clean_text, re.DOTALL)
    if match:
        return match.group(0)
    return clean_text

def generate_deep_research(api_key, product_name, category):
    genai.configure(api_key=api_key, transport="rest")
    model_name = get_fast_working_model(api_key)
    model = genai.GenerativeModel(model_name)
    prompt = f"""
\u0623\u0646\u062a \u0623\u062f\u0627\u0629 Deep Research. \u0627\u0644\u0645\u0646\u062a\u062c: "{product_name}". \u0627\u0644\u0641\u0626\u0629: "{category}".
\u0623\u062e\u0631\u062c \u062a\u0642\u0631\u064a\u0631\u0627\u064b \u0634\u0627\u0645\u0644\u0627\u064b \u0628\u0627\u0644\u0639\u0631\u0628\u064a\u0629 \u0628\u062a\u0646\u0633\u064a\u0642 Markdown:
1. \u0648\u062b\u064a\u0642\u0629 \u0634\u062e\u0635\u064a\u0629 \u0627\u0644\u0639\u0645\u064a\u0644 (Avatar Sheet)
2. \u0648\u062b\u064a\u0642\u0629 \u0628\u062d\u062b \u0627\u0644\u0633\u0648\u0642 \u0648\u0627\u0644\u0645\u0646\u0627\u0641\u0633\u064a\u0646
3. \u0648\u062b\u064a\u0642\u0629 \u0645\u0644\u062e\u0635 \u0627\u0644\u0639\u0631\u0636 (Offer Brief)
4. \u0648\u062b\u064a\u0642\u0629 \u0627\u0644\u0645\u0639\u062a\u0642\u062f\u0627\u062a \u0627\u0644\u0636\u0631\u0648\u0631\u064a\u0629
5. \u0632\u0648\u0627\u064a\u0627 \u0627\u0644\u0628\u064a\u0639 \u0627\u0644\u062c\u0627\u0647\u0632\u0629 (PAS + FAB)
"""
    response = model.generate_content(prompt, request_options={"timeout": 60.0})
    return response.text

def build_landing_page_html(data, colors):
    p = colors["primary"]
    s = colors["secondary"]
    a = colors["accent"]
    g1 = colors["gradient1"]
    g2 = colors["gradient2"]

    # Generate ALL images
    hero_img = get_ai_image(data.get('image_hero_search', 'product'), 900, 1100, 'product')
    hero_lifestyle = get_ai_image(data.get('image_hero_lifestyle_search', 'person using product'), 800, 600, 'lifestyle')
    hero_closeup = get_ai_image(data.get('image_hero_closeup_search', 'product detail'), 600, 600, 'product')
    prob_img = get_ai_image(data.get('image_problem_search', 'worried person'), 700, 500, 'person')
    prob_img2 = get_ai_image(data.get('image_problem_2_search', 'skin problem'), 600, 400, 'person')
    sol_img = get_ai_image(data.get('image_solution_search', 'happy person'), 800, 600, 'person')
    sol_img2 = get_ai_image(data.get('image_solution_2_search', 'product result'), 600, 600, 'lifestyle')
    before_img = get_ai_image(data.get('image_before_search', 'before treatment'), 500, 600, 'before_after')
    after_img = get_ai_image(data.get('image_after_search', 'after treatment'), 500, 600, 'before_after')
    dims = data.get('dimensions', {})
    dim_img = get_ai_image(dims.get('image_search', 'product dimensions'), 600, 600, 'dimensions')

    badges_html = ""
    for badge in data.get('trust_badges', []):
        badges_html += f'<span style="background:white;color:{p};padding:8px 18px;border-radius:30px;font-weight:700;font-size:0.85rem;display:inline-block;margin:4px;">\u2705 {badge}</span> '

    problems_html = ""
    for pt in data.get('problem_points', []):
        problems_html += f'<li style="padding:8px 0;font-size:1.05rem;">\u274c {pt}</li>\n'

    features_html = ""
    for feat in data.get('features', [])[:4]:
        feat_img = get_ai_image(feat.get('image_search', 'feature'), 400, 400, 'product')
        features_html += f'''<div style="display:flex;align-items:center;gap:20px;background:white;border-radius:16px;padding:20px;margin-bottom:15px;box-shadow:0 4px 15px rgba(0,0,0,0.08);">
            <img src="{feat_img}" style="width:140px;height:140px;object-fit:cover;border-radius:12px;flex-shrink:0;" />
            <div><h4 style="color:{p};margin:0 0 5px 0;font-size:1.1rem;">\u2728 {feat.get('title','')}</h4><p style="margin:0;color:#64748b;font-size:0.95rem;">{feat.get('desc','')}</p></div>
        </div>'''

    ingredients_html = ""
    for ing in data.get('ingredients', [])[:3]:
        ing_img = get_ai_image(ing.get('image_search', 'natural ingredient'), 300, 300, 'ingredient')
        ingredients_html += f'''<div style="text-align:center;flex:1;min-width:200px;">
            <img src="{ing_img}" style="width:180px;height:180px;object-fit:cover;border-radius:50%;margin-bottom:10px;border:4px solid {p}20;" />
            <h4 style="color:{p};margin:5px 0;">{ing.get('name','')}</h4>
            <p style="color:#64748b;font-size:0.9rem;">{ing.get('benefit','')}</p>
        </div>'''

    # GIF-style steps (how to use with images)
    steps_html = ""
    step_images = data.get('how_to_use_images', [])
    for i, step in enumerate(data.get('how_to_use', [])[:3], 1):
        step_kw = step_images[i-1] if i-1 < len(step_images) else f'step {i} tutorial'
        step_img = get_ai_image(step_kw, 500, 400, 'gif_step')
        direction = 'row' if i % 2 != 0 else 'row-reverse'
        steps_html += f'''<div style="display:flex;flex-direction:{direction};align-items:center;gap:25px;margin-bottom:25px;flex-wrap:wrap;">
            <img src="{step_img}" style="width:55%;min-width:280px;border-radius:16px;box-shadow:0 8px 25px rgba(0,0,0,0.1);" />
            <div style="flex:1;min-width:200px;">
                <div style="background:linear-gradient(135deg,{g1},{g2});color:white;width:50px;height:50px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1.4rem;margin-bottom:10px;">{i}</div>
                <p style="font-size:1.1rem;font-weight:600;color:#1e293b;">{step}</p>
            </div>
        </div>'''

    stats_html = ""
    for stat in data.get('stats', [])[:3]:
        stats_html += f'<div style="text-align:center;padding:20px;"><div style="font-size:2.2rem;font-weight:900;color:{p};">{stat.get("number","")}</div><div style="color:#64748b;font-weight:600;">{stat.get("label","")}</div></div>'

    reviews_html = ""
    for rev in data.get('reviews', [])[:3]:
        stars = '\u2b50' * int(rev.get('rating', 5))
        rev_img = get_ai_image(rev.get('image_search', 'person portrait'), 150, 150, 'person')
        reviews_html += f'''<div style="background:white;border-radius:16px;padding:20px;box-shadow:0 4px 15px rgba(0,0,0,0.08);flex:1;min-width:250px;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <img src="{rev_img}" style="width:55px;height:55px;border-radius:50%;object-fit:cover;border:3px solid {p}30;" />
                <div><strong style="color:#1e293b;">{rev.get('name','')}</strong><br/><span style="font-size:0.9rem;">{stars}</span></div>
            </div>
            <p style="color:#475569;font-style:italic;margin:0 0 8px 0;">\"{rev.get('comment','')}\"</p>
            <span style="color:{p};font-size:0.8rem;font-weight:600;">\u2705 \u0645\u0634\u062a\u0631\u064a \u0645\u0648\u062b\u0642</span>
        </div>'''

    faq_html = ""
    for faq in data.get('faq', [])[:4]:
        faq_html += f'''<details style="background:white;border-radius:12px;padding:15px 20px;margin-bottom:10px;box-shadow:0 2px 8px rgba(0,0,0,0.06);cursor:pointer;">
            <summary style="font-weight:700;color:{p};font-size:1.05rem;">{faq.get('q','')}</summary>
            <p style="color:#64748b;margin-top:10px;padding-top:10px;border-top:1px solid #e2e8f0;">{faq.get('a','')}</p>
        </details>'''

    pricing = data.get('pricing', {})
    cta = data.get('call_to_action', '\u0627\u0637\u0644\u0628 \u0627\u0644\u0622\u0646')

    html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Cairo',sans-serif; background:{s}; color:#1e293b; direction:rtl; scroll-behavior:smooth; }}
img {{ max-width:100%; height:auto; display:block; }}
.container {{ max-width:860px; margin:0 auto; padding:0 20px; }}
.btn {{ display:block; background:linear-gradient(135deg,{a},{a}cc); color:white; padding:18px 30px; border-radius:14px; font-weight:900; font-size:1.25rem; text-decoration:none; text-align:center; box-shadow:0 8px 25px {a}55; transition:all 0.3s; border:none; cursor:pointer; width:100%; max-width:420px; margin:0 auto; }}
.btn:hover {{ transform:translateY(-3px); box-shadow:0 14px 35px {a}77; }}
.section {{ padding:55px 20px; }}
.section-title {{ font-size:1.9rem; font-weight:900; color:{p}; text-align:center; margin-bottom:30px; line-height:1.3; }}
.section-sub {{ text-align:center; color:#64748b; font-size:1.05rem; margin-bottom:30px; }}
.badge-bar {{ text-align:center; padding:15px; }}
.img-text-row {{ display:flex; align-items:center; gap:30px; flex-wrap:wrap; margin-bottom:30px; }}
.img-text-row img {{ flex:1; min-width:260px; border-radius:18px; box-shadow:0 10px 30px rgba(0,0,0,0.12); }}
.img-text-row .text-side {{ flex:1; min-width:240px; }}
.grid-2 {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; }}
@media(max-width:600px) {{ .grid-2 {{ grid-template-columns:1fr; }} .img-text-row {{ flex-direction:column; }} }}
</style>
</head>
<body>

<!-- 1. HERO SECTION -->
<section style="background:linear-gradient(160deg,{g1} 0%,{g2} 100%);padding:50px 20px 40px;">
    <div class="container">
        <div class="badge-bar">{badges_html}</div>
        <h1 style="font-size:2.3rem;font-weight:900;color:white;text-align:center;line-height:1.35;margin:20px 0 12px;">{data.get('hero_headline','')}</h1>
        <p style="color:rgba(255,255,255,0.88);font-size:1.15rem;text-align:center;margin-bottom:25px;">{data.get('hero_subheadline','')}</p>
        <div style="display:flex;gap:15px;justify-content:center;flex-wrap:wrap;margin-bottom:30px;">
            <img src="{hero_img}" style="width:48%;min-width:240px;max-width:340px;border-radius:20px;box-shadow:0 15px 40px rgba(0,0,0,0.25);" />
            <div style="display:flex;flex-direction:column;gap:15px;flex:1;min-width:200px;">
                <img src="{hero_lifestyle}" style="width:100%;border-radius:16px;box-shadow:0 8px 25px rgba(0,0,0,0.2);" />
                <img src="{hero_closeup}" style="width:100%;border-radius:16px;box-shadow:0 8px 25px rgba(0,0,0,0.2);" />
            </div>
        </div>
        <div style="text-align:center;margin-bottom:15px;">
            <span style="background:rgba(255,255,255,0.2);color:white;padding:10px 25px;border-radius:30px;font-size:1rem;font-weight:700;">
                \u2665 {data.get('social_proof_number','')}{data.get('social_proof_text','')}
            </span>
        </div>
        <div style="text-align:center;"><a href="#order" class="btn" style="max-width:380px;display:inline-block;">{cta} \u2794</a></div>
    </div>
</section>'''

    html += f'''
<!-- 2. STATS SOCIAL PROOF -->
<section style="background:{p};padding:30px 20px;">
    <div class="container" style="display:flex;justify-content:space-around;flex-wrap:wrap;">
        {stats_html}
    </div>
</section>

<!-- 3. PROBLEM SECTION -->
<section class="section" style="background:white;">
    <div class="container">
        <h2 class="section-title" style="color:#dc2626;">\u26a0\ufe0f {data.get('problem_title','')}</h2>
        <div class="img-text-row">
            <img src="{prob_img}" />
            <div class="text-side">
                <p style="color:#475569;font-size:1.05rem;margin-bottom:15px;">{data.get('problem_description','')}</p>
                <ul style="list-style:none;">{problems_html}</ul>
            </div>
        </div>
        <img src="{prob_img2}" style="width:100%;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,0.1);margin-top:15px;" />
    </div>
</section>

<!-- 4. SOLUTION + BEFORE/AFTER -->
<section class="section" style="background:{s};">
    <div class="container">
        <h2 class="section-title">\u2728 {data.get('solution_title','')}</h2>
        <div class="img-text-row" style="flex-direction:row-reverse;">
            <img src="{sol_img}" />
            <div class="text-side">
                <p style="color:#475569;font-size:1.1rem;line-height:1.7;">{data.get('solution_description','')}</p>
            </div>
        </div>
        <img src="{sol_img2}" style="width:100%;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,0.1);margin:20px 0;" />
        <h3 style="text-align:center;font-size:1.5rem;font-weight:900;color:{p};margin:30px 0 20px;">\u2728 \u062a\u062d\u0648\u0644 \u0645\u0630\u0647\u0644 \u062a\u0644\u0627\u062d\u0638\u0647 \u0641\u0648\u0631\u0627\u064b!</h3>
        <div style="display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:15px;">
            <div style="text-align:center;">
                <img src="{before_img}" style="width:100%;border-radius:16px;box-shadow:0 8px 20px rgba(0,0,0,0.12);" />
                <p style="margin-top:10px;font-weight:700;color:#dc2626;font-size:1.1rem;">\u0642\u0628\u0644</p>
            </div>
            <div style="font-size:2.5rem;color:{p};">\u27a1</div>
            <div style="text-align:center;">
                <img src="{after_img}" style="width:100%;border-radius:16px;box-shadow:0 8px 20px rgba(0,0,0,0.12);" />
                <p style="margin-top:10px;font-weight:700;color:#16a34a;font-size:1.1rem;">\u0628\u0639\u062f</p>
            </div>
        </div>
    </div>
</section>

<!-- 5. FEATURES WITH IMAGES -->
<section class="section" style="background:white;">
    <div class="container">
        <h2 class="section-title">\u0644\u0645\u0627\u0630\u0627 \u0647\u0630\u0627 \u0627\u0644\u0645\u0646\u062a\u062c \u0645\u062e\u062a\u0644\u0641\u061f</h2>
        {features_html}
    </div>
</section>

<!-- 6. INGREDIENTS WITH CIRCULAR IMAGES -->
<section class="section" style="background:linear-gradient(160deg,{g1}15,{g2}15);">
    <div class="container">
        <h2 class="section-title">\u0627\u0644\u0633\u0631 \u0641\u064a \u0645\u0643\u0648\u0646\u0627\u062a\u0646\u0627</h2>
        <div style="display:flex;flex-wrap:wrap;gap:20px;justify-content:center;">{ingredients_html}</div>
    </div>
</section>'''

    html += f'''
<!-- 7. GIF HOW TO USE STEPS -->
<section class="section" style="background:white;">
    <div class="container">
        <h2 class="section-title">\U0001f3ac \u0643\u064a\u0641 \u062a\u0633\u062a\u062e\u062f\u0645\u0647\u061f</h2>
        <p class="section-sub">\u062a\u0639\u0644\u064a\u0645\u0627\u062a \u0627\u0644\u0627\u0633\u062a\u062e\u062f\u0627\u0645 \u062e\u0637\u0648\u0629 \u0628\u062e\u0637\u0648\u0629</p>
        {steps_html}
    </div>
</section>

<!-- 8. DIMENSIONS -->
<section class="section" style="background:{s};">
    <div class="container">
        <h2 class="section-title">\U0001f4cf \u0623\u0628\u0639\u0627\u062f \u0648\u062d\u062c\u0645 \u0627\u0644\u0645\u0646\u062a\u062c</h2>
        <div style="display:flex;align-items:center;gap:30px;flex-wrap:wrap;">
            <img src="{dim_img}" style="flex:1;min-width:260px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,0.12);" />
            <div style="flex:1;min-width:220px;">
                <div style="background:white;border-radius:16px;padding:25px;box-shadow:0 4px 15px rgba(0,0,0,0.08);">
                    <h4 style="color:{p};margin-bottom:15px;font-size:1.2rem;">\u0627\u0644\u0645\u0648\u0627\u0635\u0641\u0627\u062a \u0627\u0644\u062a\u0642\u0646\u064a\u0629</h4>
                    <table style="width:100%;border-collapse:collapse;">
                        <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 5px;color:#64748b;">\u0627\u0644\u0627\u0631\u062a\u0641\u0627\u0639</td><td style="padding:10px 5px;font-weight:700;color:{p};">{dims.get('height','')}</td></tr>
                        <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 5px;color:#64748b;">\u0627\u0644\u0639\u0631\u0636</td><td style="padding:10px 5px;font-weight:700;color:{p};">{dims.get('width','')}</td></tr>
                        <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 5px;color:#64748b;">\u0627\u0644\u0648\u0632\u0646</td><td style="padding:10px 5px;font-weight:700;color:{p};">{dims.get('weight','')}</td></tr>
                        <tr><td style="padding:10px 5px;color:#64748b;">\u0627\u0644\u062d\u062c\u0645</td><td style="padding:10px 5px;font-weight:700;color:{p};">{dims.get('volume','')}</td></tr>
                    </table>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- 9. REVIEWS -->
<section class="section" style="background:white;">
    <div class="container">
        <h2 class="section-title">\u2b50 \u0622\u0631\u0627\u0621 \u0627\u0644\u0639\u0645\u0644\u0627\u0621</h2>
        <div style="display:flex;gap:20px;flex-wrap:wrap;">{reviews_html}</div>
    </div>
</section>

<!-- 10. PRICING + CTA -->
<section class="section" id="order" style="background:linear-gradient(160deg,{g1},{g2});">
    <div class="container" style="text-align:center;">
        <h2 style="color:white;font-size:2rem;font-weight:900;margin-bottom:20px;">\U0001f525 \u0627\u062d\u0635\u0644 \u0639\u0644\u064a\u0647 \u0627\u0644\u0622\u0646!</h2>
        <div style="background:white;border-radius:20px;padding:35px;max-width:450px;margin:0 auto;box-shadow:0 20px 50px rgba(0,0,0,0.2);">
            <p style="color:#94a3b8;font-size:1rem;text-decoration:line-through;">{pricing.get('original','')} {pricing.get('currency','')}</p>
            <p style="font-size:3rem;font-weight:900;color:{p};margin:5px 0;">{pricing.get('discounted','')} <span style="font-size:1.5rem;">{pricing.get('currency','')}</span></p>
            <span style="background:{a};color:white;padding:5px 18px;border-radius:20px;font-weight:700;font-size:0.9rem;">\u062e\u0635\u0645 {pricing.get('discount_percent','')}</span>
            <p style="color:#ef4444;font-weight:700;margin:15px 0;font-size:1rem;">\u23f0 {data.get('urgency_text','')}</p>
            <a href="#" class="btn">{cta} \u2794</a>
        </div>
    </div>
</section>'''

    html += f'''
<!-- 11. FAQ -->
<section class="section" style="background:{s};">
    <div class="container">
        <h2 class="section-title">\u2753 \u0627\u0644\u0623\u0633\u0626\u0644\u0629 \u0627\u0644\u0634\u0627\u0626\u0639\u0629</h2>
        {faq_html}
    </div>
</section>

<!-- 12. GUARANTEE -->
<section class="section" style="background:white;">
    <div class="container" style="text-align:center;">
        <div style="max-width:550px;margin:0 auto;padding:35px;background:linear-gradient(135deg,{g1}10,{g2}10);border-radius:24px;border:2px solid {p}30;">
            <div style="font-size:4rem;margin-bottom:15px;">\U0001f6e1</div>
            <h3 style="color:{p};font-size:1.6rem;font-weight:900;margin-bottom:12px;">{data.get('guarantee_title','')}</h3>
            <p style="color:#64748b;font-size:1rem;line-height:1.7;">{data.get('guarantee_text','')}</p>
        </div>
    </div>
</section>

<!-- 13. FINAL CTA -->
<section style="background:linear-gradient(160deg,{g1},{g2});padding:50px 20px;text-align:center;">
    <div class="container">
        <h2 style="color:white;font-size:1.9rem;font-weight:900;margin-bottom:20px;">\u2764\ufe0f \u0644\u0627 \u062a\u0641\u0648\u062a \u0647\u0630\u0627 \u0627\u0644\u0639\u0631\u0636!</h2>
        <a href="#order" class="btn" style="font-size:1.3rem;padding:20px 40px;display:inline-block;">{cta} \u2794</a>
        <p style="color:rgba(255,255,255,0.75);margin-top:20px;font-size:0.9rem;">{data.get('footer_text','')}</p>
    </div>
</section>

</body>
</html>'''
    return html

# UI - Sidebar and Main
with st.sidebar:
    st.header("\u2699\ufe0f \u0627\u0644\u0625\u0639\u062f\u0627\u062f\u0627\u062a \u0627\u0644\u0639\u0627\u0645\u0629")
    global_api_key = st.text_input("\U0001f511 Gemini API Key", type="password")
    global_product_name = st.text_area("\U0001f4e6 \u062a\u0641\u0627\u0635\u064a\u0644 \u0648\u0627\u0633\u0645 \u0627\u0644\u0645\u0646\u062a\u062c", placeholder="\u0645\u062b\u0627\u0644: \u0643\u0631\u064a\u0645 \u0643\u0648\u0644\u0627\u062c\u064a\u0646 \u0643\u0648\u0631\u064a \u0644\u0644\u0628\u0634\u0631\u0629")
    global_category = st.selectbox("\U0001f4e6 \u0641\u0626\u0629 \u0627\u0644\u0645\u0646\u062a\u062c", ["\U0001f484 \u0645\u0633\u062a\u062d\u0636\u0631\u0627\u062a \u062a\u062c\u0645\u064a\u0644 \u0648\u0639\u0646\u0627\u064a\u0629 (Cosmetics)", "\u2699\ufe0f \u0623\u062f\u0648\u0627\u062a \u0648\u0623\u062c\u0647\u0632\u0629 \u0630\u0643\u064a\u0629 (Gadgets)"])
    st.markdown("---")
    st.header("\U0001f6e0\ufe0f \u0627\u062e\u062a\u0631 \u0627\u0644\u0623\u062f\u0627\u0629")
    app_mode = st.radio("\u0642\u0627\u0626\u0645\u0629 \u0627\u0644\u062a\u062d\u0643\u0645:", ["\U0001f3d7\ufe0f \u0645\u0646\u0634\u0626 \u0635\u0641\u062d\u0627\u062a \u0627\u0644\u0647\u0628\u0648\u0637", "\U0001f50d \u0628\u062d\u062b \u0627\u0644\u0633\u0648\u0642 \u0627\u0644\u0645\u0639\u0645\u0642 (SOP-1)", "\U0001f4b0 \u062d\u0627\u0633\u0628\u0629 \u0627\u0644\u062a\u0639\u0627\u062f\u0644 \u0627\u0644\u0645\u0627\u0644\u064a (Matrix)"])
    st.markdown("---")

if app_mode == "\U0001f3d7\ufe0f \u0645\u0646\u0634\u0626 \u0635\u0641\u062d\u0627\u062a \u0627\u0644\u0647\u0628\u0648\u0637":
    start_btn = st.button("\U0001f680 \u062a\u0648\u0644\u064a\u062f \u0635\u0641\u062d\u0629 \u0627\u0644\u0647\u0628\u0648\u0637 (15 \u0642\u0633\u0645 + \u0635\u0648\u0631 AI)")
    if start_btn:
        if not global_api_key or not global_product_name:
            st.error("\u0627\u0644\u0631\u062c\u0627\u0621 \u0625\u062f\u062e\u0627\u0644 \u0627\u0644\u0645\u0641\u062a\u0627\u062d \u0648\u0627\u0633\u0645 \u0627\u0644\u0645\u0646\u062a\u062c.")
        else:
            with st.spinner("\U0001f916 \u062c\u0627\u0631\u064a \u0628\u0646\u0627\u0621 \u0635\u0641\u062d\u0629 \u0627\u0644\u0647\u0628\u0648\u0637 \u0628\u0640 15 \u0642\u0633\u0645 + \u0635\u0648\u0631 AI \u0639\u0627\u0644\u064a\u0629 \u0627\u0644\u062c\u0648\u062f\u0629..."):
                try:
                    raw_json = generate_landing_page_json(global_api_key, global_product_name, global_category)
                    try:
                        parsed_data = json.loads(raw_json)
                    except json.JSONDecodeError:
                        fixed = re.sub(r',\s*}', '}', raw_json)
                        fixed = re.sub(r',\s*]', ']', fixed)
                        fixed = re.sub(r'(["\d])\s*\n\s*"', r'\1,\n"', fixed)
                        parsed_data = json.loads(fixed)
                    st.session_state.parsed_json = parsed_data
                    auto_colors = detect_colors(global_product_name, global_category)
                    st.session_state.final_page = build_landing_page_html(parsed_data, auto_colors)
                    st.success("\U0001f389 \u0627\u0643\u062a\u0645\u0644 \u0627\u0644\u0628\u0646\u0627\u0621! 15 \u0642\u0633\u0645 + \u0635\u0648\u0631 AI + \u0623\u0644\u0648\u0627\u0646 \u062a\u0644\u0642\u0627\u0626\u064a\u0629")
                except Exception as e:
                    st.error(f"\U0001f6d1 \u062e\u0637\u0623: {str(e)}")

    if 'final_page' in st.session_state:
        tab1, tab2, tab3 = st.tabs(["\U0001f4f1 \u0627\u0644\u0645\u0639\u0627\u064a\u0646\u0629 \u0627\u0644\u0628\u0635\u0631\u064a\u0629", "\U0001f4bb \u0643\u0648\u062f HTML", "\U0001f4e5 \u062a\u062d\u0645\u064a\u0644 JSON"])
        with tab1:
            components.html(st.session_state.final_page, height=4000, scrolling=True)
        with tab2:
            st.code(st.session_state.final_page, language="html")
        with tab3:
            if 'parsed_json' in st.session_state:
                json_str = json.dumps(st.session_state.parsed_json, ensure_ascii=False, indent=2)
                st.download_button(
                    label="\U0001f4e5 \u062a\u062d\u0645\u064a\u0644 \u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0635\u0641\u062d\u0629 (JSON)",
                    data=json_str,
                    file_name="landing_page_data.json",
                    mime="application/json"
                )
                st.json(st.session_state.parsed_json)

elif app_mode == "\U0001f50d \u0628\u062d\u062b \u0627\u0644\u0633\u0648\u0642 \u0627\u0644\u0645\u0639\u0645\u0642 (SOP-1)":
    st.markdown("### \U0001f50d \u0627\u0644\u0628\u062d\u062b \u0627\u0644\u0645\u0639\u0645\u0642 \u0641\u064a \u0627\u0644\u0633\u0648\u0642")
    if st.button("\U0001f9e0 \u0627\u0633\u062a\u062e\u0631\u0627\u062c \u0648\u062b\u0627\u0626\u0642 \u0627\u0644\u0628\u064a\u0639"):
        if not global_api_key or not global_product_name:
            st.error("\u0627\u0644\u0631\u062c\u0627\u0621 \u0625\u062f\u062e\u0627\u0644 \u0627\u0644\u0645\u0641\u062a\u0627\u062d \u0648\u0627\u0633\u0645 \u0627\u0644\u0645\u0646\u062a\u062c.")
        else:
            with st.spinner("\U0001f575\ufe0f\u200d\u2642\ufe0f \u062c\u0627\u0631\u064a \u0627\u0644\u0628\u062d\u062b..."):
                try:
                    result = generate_deep_research(global_api_key, global_product_name, global_category)
                    st.session_state.research_output = result
                    st.success("\u2705 \u0627\u0643\u062a\u0645\u0644 \u0627\u0644\u0628\u062d\u062b!")
                except Exception as e:
                    st.error(f"\U0001f6d1 {str(e)}")
    if 'research_output' in st.session_state:
        st.markdown(st.session_state.research_output)

elif app_mode == "\U0001f4b0 \u062d\u0627\u0633\u0628\u0629 \u0627\u0644\u062a\u0639\u0627\u062f\u0644 \u0627\u0644\u0645\u0627\u0644\u064a (Matrix)":
    st.markdown("### \U0001f4b0 \u062d\u0627\u0633\u0628\u0629 \u0646\u0642\u0637\u0629 \u0627\u0644\u062a\u0639\u0627\u062f\u0644")
    COUNTRIES = {
        "\u0627\u0644\u0633\u0639\u0648\u062f\u064a\u0629": {"currency": "SAR", "P": 199.0, "C": 85.0, "CPL": 25.0},
        "\u0627\u0644\u0625\u0645\u0627\u0631\u0627\u062a": {"currency": "AED", "P": 149.0, "C": 60.0, "CPL": 30.0},
        "\u0627\u0644\u0643\u0648\u064a\u062a": {"currency": "KWD", "P": 19.0, "C": 8.0, "CPL": 2.5},
        "\u0627\u0644\u0645\u063a\u0631\u0628": {"currency": "MAD", "P": 299.0, "C": 120.0, "CPL": 40.0},
        "\u0645\u0635\u0631": {"currency": "EGP", "P": 500.0, "C": 200.0, "CPL": 50.0},
        "\u0623\u062e\u0631\u0649": {"currency": "USD", "P": 50.0, "C": 20.0, "CPL": 5.0},
    }
    sel = st.selectbox("\U0001f30d \u0627\u0644\u062f\u0648\u0644\u0629:", list(COUNTRIES.keys()))
    d = COUNTRIES[sel]
    c1, c2, c3 = st.columns(3)
    P = c1.number_input(f"\u0633\u0639\u0631 \u0627\u0644\u0628\u064a\u0639 [{d['currency']}]", value=d["P"])
    C = c2.number_input(f"\u0627\u0644\u062a\u0643\u0644\u0641\u0629 [{d['currency']}]", value=d["C"])
    CPL = c3.number_input(f"CPL [{d['currency']}]", value=d["CPL"])
    c4, c5 = st.columns(2)
    CR = c4.slider("CR %", 10, 100, 60) / 100
    DR = c5.slider("DR %", 10, 100, 55) / 100
    margin = P - C
    max_cpl = margin * CR * DR
    profit = max_cpl - CPL
    m1, m2, m3 = st.columns(3)
    m1.metric("\u0647\u0627\u0645\u0634 \u0627\u0644\u0631\u0628\u062d", f"{margin:.2f} {d['currency']}")
    m2.metric("\u0623\u0642\u0635\u0649 CPL", f"{max_cpl:.2f} {d['currency']}")
    if profit >= 0:
        m3.metric("\u0627\u0644\u062d\u0627\u0644\u0629", "\u2705 \u0631\u0627\u0628\u062d", f"+{profit:.2f}")
    else:
        m3.metric("\u0627\u0644\u062d\u0627\u0644\u0629", "\U0001f6a8 \u062e\u0627\u0633\u0631", f"{profit:.2f}")
