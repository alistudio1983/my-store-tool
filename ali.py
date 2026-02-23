<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>صفحة هبوط احترافية - منتج خليجي</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        /* إعدادات عامة وموبايل فيرست */
        body {
            margin: 0;
            padding: 0;
            font-family: 'Cairo', sans-serif;
            background-color: #f5f5f5;
            color: #333;
        }
        .mobile-container {
            max-width: 480px; /* العرض المثالي لشاشات الجوال */
            margin: 0 auto;
            background-color: #ffffff;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
            padding-bottom: 80px; /* مساحة للزر العائم */
        }

        /* 1. الشريط العلوي (الثقة) */
        .top-trust-bar {
            background-color: #1a1a1a;
            color: #d4af37; /* لون ذهبي */
            display: flex;
            justify-content: space-around;
            padding: 8px 5px;
            font-size: 12px;
            font-weight: bold;
        }

        /* 2. قسم الهيرو (البداية الصادمة) */
        .hero-section {
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            padding: 20px;
            text-align: center;
            position: relative;
        }
        .hero-title {
            color: #1a1a1a;
            font-size: 28px;
            font-weight: 900;
            margin-bottom: 10px;
            line-height: 1.3;
        }
        .hero-title span {
            color: #27ae60; /* لون أخضر أو حسب منتجك */
        }
        .badges-container {
            position: absolute;
            right: 10px;
            top: 20%;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .badge {
            background: #d4af37;
            color: #fff;
            padding: 10px;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            text-align: center;
        }
        .hero-image {
            width: 100%;
            border-radius: 15px;
            margin-top: 15px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }

        /* 3. قسم قبل وبعد (التحول) */
        .transformation-section {
            padding: 20px;
            background-color: #fff;
            text-align: center;
        }
        .section-title {
            font-size: 22px;
            font-weight: 800;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .before-after-container {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            position: relative;
        }
        .ba-box {
            width: 48%;
            position: relative;
        }
        .ba-box img {
            width: 100%;
            border-radius: 10px;
        }
        .ba-label {
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        .arrow-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 50px;
            z-index: 10;
        }

        /* 4. قسم الخبراء والدليل الاجتماعي */
        .authority-section {
            background: #f8f9fa;
            padding: 20px;
        }
        .doctor-card {
            background: white;
            border-radius: 15px;
            padding: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            margin-bottom: 15px;
        }
        .doctor-card img {
            width: 80px;
            border-radius: 50%;
            border: 3px solid #d4af37;
        }
        .guarantee-box {
            background: #1a1a1a;
            color: #d4af37;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            border: 2px dashed #d4af37;
        }

        /* 5. قسم المكونات / الآلية (الدوائر) */
        .ingredients-section {
            padding: 20px;
            background: #27ae60; /* يمكنك تغييره حسب هوية المنتج */
            color: white;
        }
        .ingredients-grid {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 20px;
        }
        .ingredient-item {
            width: 30%;
            text-align: center;
        }
        .ingredient-item img {
            width: 100%;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 5px 10px rgba(0,0,0,0.2);
        }
        .ingredient-item p {
            font-size: 12px;
            font-weight: bold;
            margin-top: 8px;
        }

        /* 6. الزر العائم (Call to Action) */
        .sticky-cta {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 480px;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 20px;
            box-sizing: border-box;
            box-shadow: 0 -5px 15px rgba(0,0,0,0.1);
            z-index: 999;
        }
        .order-btn {
            display: block;
            width: 100%;
            background: linear-gradient(90deg, #d4af37 0%, #ffdf00 100%);
            color: #1a1a1a;
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            font-size: 22px;
            font-weight: 900;
            text-decoration: none;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.03); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>

<div class="mobile-container">

    <div class="top-trust-bar">
        <span>🚚 شحن سريع ومجاني</span>
        <span>🛡️ دفع آمن 100%</span>
        <span>⭐ ضمان استعادة الأموال</span>
    </div>

    <div class="hero-section">
        <h1 class="hero-title">عناية فائقة وتألق <span>طبيعي 100%</span></h1>
        
        <div class="badges-container">
            <div class="badge">نتائج<br>مضمونة</div>
            <div class="badge">100%<br>طبيعي</div>
        </div>

        <img src="https://images.unsplash.com/photo-1556228578-0d85b1a4d571?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="صورة المنتج" class="hero-image">
    </div>

    <div class="transformation-section">
        <h2 class="section-title">شاهد التحول المذهل!</h2>
        <div class="before-after-container">
            <div class="ba-box">
                <img src="https://images.unsplash.com/photo-1596215143922-eedece08b6fd?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80" alt="قبل">
                <span class="ba-label">قبل</span>
            </div>
            
            <img src="https://cdn-icons-png.flaticon.com/512/109/109617.png" class="arrow-overlay" alt="سهم">

            <div class="ba-box">
                <img src="https://images.unsplash.com/photo-1600948836101-f9ff5bb56f11?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80" alt="بعد">
                <span class="ba-label" style="background: #27ae60;">بعد</span>
            </div>
        </div>
    </div>

    <div class="authority-section">
        <div class="doctor-card">
            <img src="https://images.unsplash.com/photo-1594824436951-7f12620ce6f8?ixlib=rb-1.2.1&auto=format&fit=crop&w=200&q=80" alt="طبيبة">
            <div>
                <h3 style="margin: 0; color: #2c3e50;">نصيحة الخبراء</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">"أوصي بهذا المنتج كحل نهائي وفعال، لأنه يعالج المشكلة من الجذور."</p>
            </div>
        </div>

        <div class="guarantee-box">
            <h2 style="margin: 0;">ضمان استعادة الأموال لمدة 30 يوماً</h2>
            <p>اطلب الآن بثقة تامة. المعاملة آمنة 100%.</p>
        </div>
    </div>

    <div class="ingredients-section">
        <h2 style="text-align: center; margin-top: 0;">السر وراء الفعالية (الآلية الفريدة)</h2>
        <div class="ingredients-grid">
            <div class="ingredient-item">
                <img src="https://images.unsplash.com/photo-1611078489935-0cb964de46d6?ixlib=rb-1.2.1&auto=format&fit=crop&w=200&q=80" alt="مكون 1">
                <p>مستخلصات طبيعية</p>
            </div>
            <div class="ingredient-item">
                <img src="https://images.unsplash.com/photo-1556228578-0d85b1a4d571?ixlib=rb-1.2.1&auto=format&fit=crop&w=200&q=80" alt="مكون 2">
                <p>تغذية عميقة</p>
            </div>
            <div class="ingredient-item">
                <img src="https://images.unsplash.com/photo-1598440947619-2ce65f80046e?ixlib=rb-1.2.1&auto=format&fit=crop&w=200&q=80" alt="مكون 3">
                <p>نتائج سريعة</p>
            </div>
        </div>
    </div>

    <div class="sticky-cta">
        <a href="#checkout" class="order-btn">اطلب باقتك الآن! 🛒</a>
    </div>

</div>

</body>
</html>
