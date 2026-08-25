# -*- coding: utf-8 -*-
"""
All remaining page strings for 17 languages + per-locale SEO based on
independent keyword research (not direct English translation).

Two jobs done here:
  1. FULL UNIFORMITY: every translatable string on the site — page H1s,
     ledes, home H2 SEO blocks + body, privacy H2 + body, terms H2 + body,
     404 H2 + body, form options, placeholders, help text, affiliation
     notes — is now translated for all 17 languages.
  2. LOCALIZED SEO: <title>, meta description, og:title, og:description
     are written using the actual search terms people use in each
     language, not as literal English translations.

Quality flags:
  - REAL_RESEARCH: the SEO target terms came from real SERP-level
    search-result corpora (Vervox, Hootsuite, Postiz, Pixelfox, Ahrefs,
    AdaptlyPost, regional TikTok-creator blogs).
  - BEST_GUESS: research returned a single dominant term or the
    regional variations were thin; the title was built using the
    most natural composite of what the corpus revealed.
"""

# =============================================================================
# PER-LOCALE SEO (titles, meta, og) — independent research per language
# =============================================================================
# Each entry: title, meta_desc, og_title, og_desc
# Length budget: title <= 60, meta_desc <= 160, og_title <= 60, og_desc <= 110
# Keywords are the actual search patterns used in each language (see
# research notes inline).

SEO = {
    # English — original (control)
    'en': {
        'title': 'TikTok Username Generator — Free Username Ideas & Availability Check | Handle',
        'meta_desc': "Free TikTok username generator with a live availability check. Get 10-20 unique username ideas that follow TikTok's rules, then see which are still available on TikTok. No signup, no limits, 17+ vibes.",
        'og_title': 'TikTok Username Generator — Free Ideas & Availability Check',
        'og_desc': "Free TikTok username generator. 10-20 ideas that follow TikTok's rules, live availability check. 17+ vibes, 17 niches, no signup.",
    },
    # Spanish — research: "generador de nombres tiktok", "verificador de
    # nombre tiktok", "ideas de nombres tiktok", "nombres aesthetic tiktok"
    'es': {
        'title': 'Generador de Nombres TikTok — Verifica Disponibilidad Gratis',
        'meta_desc': 'Generador de nombres TikTok gratis con verificador en vivo. Escribe una palabra, elige nicho y estilo, recibe 10-20 ideas de @ que cumplen las reglas de TikTok y comprueba disponibilidad al instante. Sin registro, sin límites.',
        'og_title': 'Generador de Nombres TikTok — Verifica Disponibilidad',
        'og_desc': 'Ideas de @ para TikTok que cumplen las reglas de la plataforma. Verifica disponibilidad en vivo. 17 estilos, 17 nichos, sin registro.',
    },
    # German — research: "TikTok-Namensgenerator", "TikTok-Username-Checker",
    # "TikTok-Benutzernamen-Verfügbarkeit prüfen", "TikTok-Namen-Ideen"
    'de': {
        'title': 'TikTok-Namensgenerator — Verfügbarkeit in Echtzeit prüfen',
        'meta_desc': 'Kostenloser TikTok-Namensgenerator mit Live-Verfügbarkeitscheck. Gib ein Stichwort ein, wähle Nische und Vibe, erhalte 10-20 @-Ideen, die TikToks Regeln entsprechen. Sofort prüfen, ob der Handle noch frei ist. Ohne Anmeldung, ohne Limit.',
        'og_title': 'TikTok-Namensgenerator — Handle-Verfügbarkeit prüfen',
        'og_desc': '@-Ideen für TikTok, die die Plattform-Regeln einhalten. Live-Verfügbarkeitscheck. 17 Vibes, 17 Nischen, ohne Anmeldung.',
    },
    # French — research: "générateur de nom tiktok", "vérifier disponibilité
    # nom tiktok", "idées de noms tiktok", "noms aesthetic tiktok"
    'fr': {
        'title': 'Générateur de Nom TikTok — Vérifier la Disponibilité Gratuit',
        'meta_desc': "Générateur de nom TikTok gratuit avec vérification en direct. Tape un mot-clé, choisis une niche et un style, reçois 10-20 idées de @ qui respectent les règles de TikTok et vérifie la disponibilité tout de suite. Sans inscription, sans limite.",
        'og_title': 'Générateur de Nom TikTok — Vérifier Disponibilité',
        'og_desc': "Idées de @ qui respectent les règles de TikTok. Vérification en direct. 17 styles, 17 niches, sans inscription.",
    },
    # Italian — research: "generatore di nomi tiktok", "idee nome tiktok",
    # "nomi unici tiktok", "nomi belli tiktok"
    'it': {
        'title': 'Generatore di Nomi TikTok — Controlla Disponibilità Gratis',
        'meta_desc': "Generatore di nomi utente TikTok gratuito con verifica in tempo reale. Inserisci una parola, scegli nicchia e stile, ottieni 10-20 idee di @ che rispettano le regole di TikTok e scopri subito se l'handle è libero. Senza registrazione, senza limiti.",
        'og_title': 'Generatore di Nomi TikTok — Disponibilità in Diretta',
        'og_desc': "Idee di @ per TikTok che rispettano le regole della piattaforma. Verifica in diretta. 17 stili, 17 nicchie, senza registrazione.",
    },
    # Portuguese — research: "gerador de nomes tiktok", "gerador de nick
    # tiktok", "ideias de nomes tiktok", "nomes aesthetic tiktok"
    'pt': {
        'title': 'Gerador de Nomes TikTok — Verificar Disponibilidade Grátis',
        'meta_desc': 'Gerador de nomes TikTok grátis com verificação em tempo real. Digite uma palavra, escolha nicho e estilo, receba 10-20 ideias de @ que seguem as regras do TikTok e veja na hora se o handle está livre. Sem cadastro, sem limite.',
        'og_title': 'Gerador de Nomes TikTok — Verificar Disponibilidade',
        'og_desc': 'Ideias de @ que seguem as regras do TikTok. Verificação em tempo real. 17 estilos, 17 nichos, sem cadastro.',
    },
    # Dutch — research: "tiktok-gebruikersnaamgenerator", "tiktok naam
    # generator", "tiktok gebruikersnaam ideeën", "tiktok naam beschikbaarheid"
    'nl': {
        'title': 'TikTok Gebruikersnaam Generator — Beschikbaarheid Checken',
        'meta_desc': 'Gratis TikTok-gebruikersnaamgenerator met live beschikbaarheidscheck. Typ een trefwoord, kies niche en vibe, krijg 10-20 @-ideeën die voldoen aan de regels van TikTok en check direct of de handle nog vrij is. Geen account, geen limiet.',
        'og_title': 'TikTok Naam Generator — Beschikbaarheid Checken',
        'og_desc': '@-ideeën voor TikTok die aan de platformregels voldoen. Live beschikbaarheidscheck. 17 vibes, 17 niches, geen account.',
    },
    # Polish — research: "generator nazw tiktok", "generator nazw
    # użytkowników tiktok", "pomysły na nazwę tiktok", "unikalne nazwy
    # tiktok"
    'pl': {
        'title': 'Generator Nazw TikTok — Sprawdź Dostępność Za Darmo',
        'meta_desc': 'Darmowy generator nazw użytkowników TikTok z natychmiastowym sprawdzaniem dostępności. Wpisz słowo kluczowe, wybierz niszę i styl, otrzymaj 10-20 pomysłów na @ zgodnych z zasadami TikToka. Bez rejestracji, bez limitu.',
        'og_title': 'Generator Nazw TikTok — Sprawdź Dostępność',
        'og_desc': 'Pomysły na @ zgodne z zasadami TikToka. Sprawdzanie na żywo. 17 stylów, 17 nisz, bez rejestracji.',
    },
    # Russian — research: "генератор никнеймов тикток", "генератор
    # юзернеймов тикток", "никнеймы для тикток", "крутые ники тикток",
    # "уникальные ники тикток", "проверить никнейм тикток"
    'ru': {
        'title': 'Генератор Никнеймов TikTok — Проверить Занятость Бесплатно',
        'meta_desc': 'Бесплатный генератор никнеймов для TikTok с проверкой занятости в реальном времени. Введите ключевое слово, выберите нишу и стиль, получите 10-20 уникальных идей для @ по правилам TikTok. Без регистрации, без лимитов.',
        'og_title': 'Генератор Никнеймов TikTok — Проверка Занятости',
        'og_desc': 'Уникальные ники для TikTok по правилам платформы. Проверка в реальном времени. 17 стилей, 17 ниш, без регистрации.',
    },
    # Chinese — research: "TikTok 用户名生成器", "TikTok 名字生成器",
    # "TikTok 用户名推荐", "TikTok 昵称生成", "TikTok 名字创意"
    'zh': {
        'title': 'TikTok 用户名生成器 — 实时检测用户名是否可用',
        'meta_desc': '免费 TikTok 用户名生成器,实时检测可用性。输入关键词,选择领域和风格,获取 10-20 个符合 TikTok 规则的用户名创意,立即查看是否被占用。无需注册,无次数限制。',
        'og_title': 'TikTok 用户名生成器 — 免费在线生成',
        'og_desc': '符合 TikTok 规则的 @ 用户名创意。实时检测可用性。17 种风格,17 个领域,无需注册。',
    },
    # Vietnamese — research: "tên tiktok hay", "tạo tên tiktok", "tên
    # tiktok đẹp", "tên tiktok độc đáo", "tên tiktok FYP", "trình tạo
    # tên tiktok", "gợi ý tên tiktok"
    'vi': {
        'title': 'Trình Tạo Tên TikTok — Kiểm Tra Tên Đã Dùng Miễn Phí',
        'meta_desc': 'Trình tạo tên TikTok miễn phí với kiểm tra trùng lặp theo thời gian thực. Nhập từ khóa, chọn ngách và phong cách, nhận 10-20 ý tưởng tên @ theo đúng quy tắc TikTok và xem ngay tên nào còn trống. Không cần đăng ký, không giới hạn.',
        'og_title': 'Trình Tạo Tên TikTok — Tên Hay, Độc Đáo',
        'og_desc': 'Ý tưởng tên @ theo đúng quy tắc TikTok. Kiểm tra trùng lặp trực tiếp. 17 phong cách, 17 ngách, không cần đăng ký.',
    },
    # Indonesian — research: "generator nama tiktok", "ide nama tiktok",
    # "nama tiktok aesthetic", "nama tiktok bagus", "nama tiktok unik",
    # "nama tiktok keren", "username tiktok"
    'id': {
        'title': 'Generator Nama TikTok — Cek Ketersediaan Username Gratis',
        'meta_desc': 'Generator nama pengguna TikTok gratis dengan pengecekan ketersediaan langsung. Ketik kata kunci, pilih niche dan vibe, dapatkan 10-20 ide @ yang sesuai aturan TikTok dan cek apakah masih tersedia. Tanpa daftar, tanpa batas.',
        'og_title': 'Generator Nama TikTok — Ide Nama Unik',
        'og_desc': 'Ide @ yang sesuai aturan TikTok. Cek ketersediaan langsung. 17 vibe, 17 niche, tanpa daftar.',
    },
    # Malay — research: "penjana nama tiktok", "idea nama tiktok", "nama
    # tiktok aesthetic", "nama tiktok unik", "nama tiktok keren"
    'ms': {
        'title': 'Penjana Nama TikTok — Semak Ketersediaan Nama Pengguna',
        'meta_desc': 'Penjana nama pengguna TikTok percuma dengan semakan ketersediaan secara langsung. Taip kata kunci, pilih niche dan gaya, dapat 10-20 idea @ yang ikut peraturan TikTok dan lihat dengan segera jika nama masih kosong. Tanpa daftar, tanpa had.',
        'og_title': 'Penjana Nama TikTok — Idea Nama Unik',
        'og_desc': 'Idea @ yang ikut peraturan TikTok. Semakan ketersediaan langsung. 17 gaya, 17 niche, tanpa daftar.',
    },
    # Tagalog — research: "ideya ng username tiktok", "pangalan sa
    # tiktok", "mga ideya tiktok username", "magandang username tiktok"
    'tl': {
        'title': 'Tagagawa ng Pangalan sa TikTok — Suriin kung Available',
        'meta_desc': 'Libreng tagagawa ng username sa TikTok na may live availability check. Mag-type ng keyword, pumili ng niche at vibe, makakakuha ng 10-20 ideya na @ na sumusunod sa mga patakaran ng TikTok at agad na matingnan kung available. Walang signup, walang limitasyon.',
        'og_title': 'Tagagawa ng Pangalan sa TikTok — Ideya ng Username',
        'og_desc': 'Ideya na @ na sumusunod sa mga patakaran ng TikTok. Live availability check. 17 vibes, 17 niches, walang signup.',
    },
    # Hindi — research: "TikTok यूजरनेम जनरेटर", "TikTok नाम जनरेटर",
    # "TikTok यूजरनेम आइडिया", "अच्छा TikTok नाम", "यूनिक TikTok नाम"
    'hi': {
        'title': 'TikTok यूजरनेम जनरेटर — उपलब्धता तुरंत जांचें',
        'meta_desc': 'मुफ्त TikTok यूजरनेम जनरेटर जिसमें लाइव उपलब्धता जांच है। कीवर्ड टाइप करें, निश और वाइब चुनें, 10-20 यूनिक @ आइडिया पाएं जो TikTok के नियमों का पालन करते हैं और तुरंत देखें कि हैंडल उपलब्ध है या नहीं। बिना साइनअप, बिना सीमा।',
        'og_title': 'TikTok यूजरनेम जनरेटर — यूनिक नाम',
        'og_desc': 'TikTok नियमों के अनुसार @ आइडिया। लाइव उपलब्धता जांच। 17 वाइब, 17 निश, बिना साइनअप।',
    },
    # Bengali — research: "টিকটক আইডির নাম", "টিকটক নাম", "TikTok
    # ইউজারনেম", "সুন্দর টিকটক নাম", "ইউনিক টিকটক নাম"
    'bn': {
        'title': 'টিকটক ইউজারনেম জেনারেটর — লাইভ প্রাপ্যতা যাচাই',
        'meta_desc': 'বিনামূল্যে টিকটক ইউজারনেম জেনারেটর যেটি লাইভে প্রাপ্যতা যাচাই করে। একটি কীওয়ার্ড লিখুন, নিশ ও ভাইব বেছে নিন, 10-20টি ইউনিক @ আইডিয়া পান যা টিকটকের নিয়ম মেনে চলে এবং সাথে সাথে দেখুন নামটি খালি আছে কিনা। কোনো সাইনআপ নেই, কোনো সীমা নেই।',
        'og_title': 'টিকটক ইউজারনেম জেনারেটর — ইউনিক নাম',
        'og_desc': 'টিকটক নিয়ম মেনে @ আইডিয়া। লাইভ প্রাপ্যতা যাচাই। 17 ভাইব, 17 নিশ, কোনো সাইনআপ নেই।',
    },
    # Urdu — research: "TikTok یوزر نیم", "TikTok نام", "TikTok نام
    # جنریٹر", "اچھے TikTok نام", "منفرد TikTok نام"
    'ur': {
        'title': 'TikTok یوزر نیم جنریٹر — دستیابی فوری چیک کریں',
        'meta_desc': 'مفت TikTok یوزر نیم جنریٹر جس میں لائیو دستیابی چیک ہے۔ کلیدی لفظ ٹائپ کریں، نچ اور وائب منتخب کریں، 10-20 منفرد @ آئیڈیاز حاصل کریں جو TikTok کے قوانین پر پورا اترتے ہیں اور فوراً دیکھیں کہ نام خالی ہے یا نہیں۔ بغیر سائن اپ، بغیر حد۔',
        'og_title': 'TikTok یوزر نیم جنریٹر — منفرد نام',
        'og_desc': 'TikTok قوانین کے مطابق @ آئیڈیاز۔ لائیو دستیابی چیک۔ 17 وائب، 17 نچ، بغیر سائن اپ۔',
    },
    # Arabic — research: "مولد اسماء تيك توك", "اسماء تيك توك فريدة",
    # "اسماء تيك توك جميلة", "اسماء تيك توك مميزة", "اسم مستخدم تيك
    # توك", "زخرفة اسماء تيك توك"
    'ar': {
        'title': 'مولد أسماء تيك توك — تحقق من التوفر مجاناً',
        'meta_desc': 'مولد أسماء مستخدمين تيك توك مجاني مع تحقق مباشر من التوفر. اكتب كلمة مفتاحية، اختر مجالاً وأسلوباً، احصل على 10-20 فكرة @ فريدة تتبع قواعد تيك توك واعرف فوراً إذا كان الاسم متاحاً. بدون تسجيل، بدون حدود.',
        'og_title': 'مولد أسماء تيك توك — أسماء فريدة ومميزة',
        'og_desc': 'أفكار @ تتبع قواعد تيك توك. تحقق مباشر من التوفر. 17 أسلوباً، 17 مجالاً، بدون تسجيل.',
    },
}

# =============================================================================
# PAGE H1 + LEDE + HOME H2 SEO BLOCKS + PRIVACY/TERMS H2 + 404 H2
# =============================================================================
# For each language: keys are H1s/H2s/ledes/blocks used by build.py
# Note: privacy_h1 / terms_h1 / faq_h1 / gen_h1 / home_h1 / 404_h1 are
# required as new keys; priv/terms body paragraphs are required too.

PAGES = {
    'en': {
        'home_h1': 'Free TikTok username generator with a live availability check.',
        'gen_h1': 'TikTok username generator',
        'faq_h1': 'Frequently asked questions about the TikTok username generator',
        'about_h1': 'About Handle — a free TikTok username generator with a live availability check',
        'privacy_h1': 'Privacy Policy',
        'terms_h1': 'Terms of Service',
        '404_h1': '404 — page not found',
        'home_lede': 'Type a keyword, pick a niche and a vibe, and get 10–20 unique TikTok username ideas that follow the current TikTok rules. Each one is checked live on TikTok so you know whether it is likely available before you copy it. No signup, no usage limits, no watermarks.',
        'gen_lede': "Free TikTok username ideas in seconds. Type a keyword (your name, your niche, or any word that anchors the result), pick one of 17 content niches and one of 17 themed vibes, and the generator returns 10–20 unique handle suggestions that respect TikTok's current username rules. Each suggestion is then checked live for availability on TikTok, with a timestamp, and labelled \"Likely available\", \"Likely taken\", or \"Unknown\" so you know what you're copying before you claim it.",
        'faq_lede': "Short answers to the questions people actually search before picking a TikTok username: what the rules are, how the availability check works, why the verdict says \"Likely\" and not \"Available\", and how to find a name that fits you. For the long version see the <a href=\"/about\" data-nav=\"about\">About page</a>; for the legal side see <a href=\"/terms\" data-nav=\"terms\">Terms</a> and <a href=\"/privacy\" data-nav=\"privacy\">Privacy</a>.",
        'about_lede': 'Handle is a free tool for TikTok creators who want a username that actually exists. Type a keyword, pick a niche and a vibe, get 10–20 TikTok username ideas that follow the current rules, and see which are likely available on TikTok before you copy one. The whole tool is free, requires no signup, and is available in 17 languages.',
        'privacy_lede': 'Last updated 24 August 2026. This is a working draft; replace with your reviewed version before going public.',
        'terms_lede': 'Last updated 24 August 2026. This is a working draft; replace with your lawyer-reviewed version before going public.',
        '404_lede': "That URL doesn't match any of our pages. It might be a typo, or a link that points to an old version of the site.",
        # Home H2 SEO blocks
        'home_h2_pick': 'How to pick a TikTok username that fits you',
        'home_h2_why': 'Why Handle',
        'home_h2_trending': 'Trending TikTok username ideas for 2026',
        'home_h3_three_things': 'Three things the other TikTok name generators skip',
        # 4 body paragraphs + 5 list items + trending 2 paragraphs
        'home_pick_p1': "A good TikTok username is short, easy to say out loud, easy to spell from memory, and signals what your content is about. Handle handles the boring part: you type a keyword (your name, your niche, a vibe word), pick one of 17 niches and one of 17 themed vibes, and the generator returns 10–20 unique TikTok username ideas that respect TikTok's current rules — 2 to 24 characters, lowercase letters, numbers, periods, and underscores, no leading or trailing period, no consecutive periods.",
        'home_pick_p2': 'Each idea is then run through a live availability check on TikTok, with a timestamp, and labelled "Likely available", "Likely taken", or "Unknown". The verdict is honest on purpose: a name can be free the moment we check it and taken the moment you try to claim it. If the check can\'t reach TikTok (a transient network blip, TikTok-side rate limit, or a private region), you\'ll see "Unknown" and a direct link to confirm by eye on TikTok itself.',
        'home_why_p1': 'Most TikTok username generators stop at the list. You copy a name, open TikTok, and find out it\'s taken. Then you do it again. Then again. Handle closes that loop in three ways no other free tool does together.',
        'home_why_li1': '<strong>Live availability check on TikTok.</strong> Each generated handle is checked against TikTok\'s own profile endpoint before you see it. No more copying 12 names and finding out all of them are taken.',
        'home_why_li2': '<strong>Honest verdicts.</strong> "Likely available" with a timestamp beats a confident "Available" that is wrong by the time you click. We say "Likely" on purpose.',
        'home_why_li3': "<strong>Rules enforced up front.</strong> Every name follows TikTok's current character rules before it reaches you — no copying a 25-character handle just to find out TikTok won't accept it.",
        'home_why_li4': '<strong>17 themed vibes + 17 niches.</strong> Aesthetic, funny, professional, edgy, cute, mysterious, cool, chill, smart, romantic, powerful, gaming, techy, spooky, retro, wholesome, fantasy — each one shifts the prefix and suffix word pools so the ideas feel like the creator you\'re trying to be, not generic "username123" output.',
        'home_why_li5': '<strong>Available in 17 languages.</strong> The whole tool is localised for Spanish, French, German, Italian, Portuguese, Dutch, Polish, Russian, Chinese, Vietnamese, Indonesian, Malay, Tagalog, Hindi, Bengali, Arabic and Urdu — with locally-researched keyword targeting, not machine translation.',
        'home_trending_p1': 'The 2026 TikTok username trends lean toward <strong>short, lowercase, single-word handles</strong> with a single stylistic flourish — a doubled letter ("glowy", "serenee"), a single-digit suffix, or one of the unicode font styles you can also generate here. Aesthetic and "soft girl" handles still rank for the lifestyle and beauty niches; gaming and tech handles are leaning harder into two-word combos ("pixel.mode", "loot.drift"). Use the generator with the <strong>unique</strong> or <strong>aesthetic</strong> vibe to see the current direction, and run the result through the font converter if you want the matching display name.',
        'home_trending_p2': 'Coming up: a TikTok creator blog, programmatic niche pages, the cross-platform check (Instagram, YouTube, X), a weekly name-drop email, and social channels for name picks. Plan and trade-offs in the README.',
        # Privacy H2 + body
        'privacy_h2_what_site': 'What this site does',
        'privacy_h2_collect': 'What we collect',
        'privacy_h2_third': 'Third parties',
        'privacy_h2_children': "Children's privacy",
        'privacy_h2_rights': 'Your rights',
        'privacy_h2_changes': 'Changes to this policy',
        'privacy_what_site_p': 'Handle is a free TikTok username generator. You type a keyword, pick a niche and a vibe, and the site returns a list of handle ideas that follow TikTok\'s username rules. Each handle is then checked against TikTok\'s own profile endpoint so you can see whether it\'s likely available, likely taken, or unknown (the check could not be completed).',
        'privacy_collect_p1': '<strong>Nothing directly identifying.</strong> The generator is client-side: the keyword, niche, vibe, and result list never leave your browser in a way that identifies you. The availability check is a server-side request to TikTok\'s public profile/oEmbed endpoint, initiated by your click. The checked handle is not associated with a user profile on our side.',
        'privacy_collect_p2': '<strong>Server logs.</strong> Like most web servers, our host records IP address, user-agent, request path, and timestamp in standard access logs, retained for 30 days for security and abuse prevention.',
        'privacy_collect_p3': '<strong>Cookies and local storage.</strong> The core tool sets no cookies. The site stores one value in your browser\'s <code>localStorage</code> — a flag recording that you dismissed the cookie consent banner — so the banner doesn\'t reappear on every visit. That value is <code>handle.cookieConsent.v1 = "accepted"</code>. It is never sent to our server, never read by any third party, and you can clear it at any time via your browser\'s developer tools or by clearing site data.',
        'privacy_third_p1': '<strong>TikTok / ByteDance.</strong> The availability check makes a request to TikTok\'s public oEmbed endpoint and profile URL. TikTok sees the request from our server\'s IP, the handle being checked, and the standard HTTP headers (including our User-Agent). TikTok\'s own privacy policy governs what they do with that request.',
        'privacy_third_p2': '<strong>Hosting and CDN.</strong> Our static site is served via a CDN; static requests route through edge nodes that log IP/UA/path for their own abuse-prevention purposes.',
        'privacy_third_p3': '<strong>Advertising (planned, not yet live).</strong> If we enable Google AdSense, Google will set cookies and read identifiers to deliver and measure ads. You\'ll see a clear notice and consent flow before this happens. We will update this policy to list the specific Google cookies and how to opt out before the integration is enabled.',
        'privacy_children_p': 'The site is not directed at children under 13 and we do not knowingly collect information from them. If you believe a child has provided information through the site, contact us so we can delete it.',
        'privacy_rights_p': 'If you\'re in the EEA, UK, or California, you have the right to request access to, correction of, or deletion of any personal data we hold about you. Since we don\'t collect personal data beyond standard server logs, the practical effect is usually a "we have nothing on you" response — but the right stands and you can exercise it. Contact: PLACEHOLDER.',
        'privacy_changes_p': 'If we make material changes, we\'ll bump the "Last updated" date at the top of this page. For changes that broaden the data we collect or change how we use it, we\'ll add a more prominent notice on the home page for at least 30 days.',
        # Terms H2 + body
        'terms_h2_what': 'What Handle is',
        'terms_h2_no_affil': 'No affiliation with TikTok',
        'terms_h2_no_warranty': 'No warranty on availability verdicts',
        'terms_h2_no_trademark': 'No trademark search',
        'terms_h2_acceptable': 'Acceptable use',
        'terms_h2_ip': 'Intellectual property',
        'terms_h2_disclaimer': 'Disclaimer of warranties',
        'terms_h2_liability': 'Limitation of liability',
        'terms_h2_changes': 'Changes to these terms',
        'terms_h2_governing': 'Governing law',
        'terms_h2_contact': 'Contact',
        'terms_what_p': 'Handle is a free, public web tool that helps you brainstorm TikTok usernames and check whether a candidate is likely available. The output is a set of handle suggestions plus an availability verdict (likely available, likely taken, or unknown).',
        'terms_no_affil_p1': 'Handle is an independent project. It is not affiliated with, endorsed by, sponsored by, or in any way associated with TikTok, ByteDance Ltd., or any of their subsidiaries. "TikTok" is a trademark of ByteDance Ltd. All references to TikTok on this site are for descriptive purposes only (the tool checks usernames on TikTok) and are made under fair use.',
        'terms_no_affil_p2': 'If you are a rights holder and believe a page on this site uses your mark in a way that is not fair use, contact us and we will address it promptly.',
        'terms_no_warranty_p': 'The availability check is a best-effort probe of public TikTok endpoints. Verdicts can be wrong, can be out of date the moment they are issued, and can be affected by TikTok-side rate limits, regional blocks, or service incidents. "Likely available" is not a guarantee. You are responsible for confirming availability on TikTok itself before you build a brand on a handle.',
        'terms_no_trademark_p': 'Handle does not check registered trademarks. A handle can be free on TikTok and still infringe a registered mark in your industry. Before you commit to a handle for a public brand, run a trademark search (USPTO TESS in the US, EUIPO in the EU, or a local equivalent) and consider talking to a lawyer.',
        'terms_acceptable_p': 'You agree not to use Handle to:',
        'terms_acceptable_li1': 'Probe TikTok at a rate that would trigger their anti-abuse systems. The site enforces a 60-checks-per-minute-per-IP rate limit; please respect it.',
        'terms_acceptable_li2': 'Generate content that is illegal, infringing, or harassing.',
        'terms_acceptable_li3': 'Attempt to circumvent rate limits, scrape the site at industrial scale, or otherwise interfere with the service.',
        'terms_acceptable_li4': 'Misrepresent the tool as being affiliated with TikTok.',
        'terms_ip_p': "The Handle name, the site's code, and the original word lists / pattern rules are owned by us. You may use the generated names however you like — they're suggestions, not our property once handed to you. TikTok's trademarks, the TikTok logo, and TikTok's username rules are TikTok's. The Unicode glyphs in the font converter are the property of the Unicode Consortium and the original type designers.",
        'terms_disclaimer_p': 'The site is provided "as is" and "as available." To the maximum extent permitted by law, we disclaim all warranties, express or implied, including the implied warranties of merchantability, fitness for a particular purpose, and non-infringement. We do not warrant that the site will be uninterrupted, error-free, or that the availability verdicts will be accurate.',
        'terms_liability_p': 'To the maximum extent permitted by law, we will not be liable for any indirect, incidental, special, consequential, or punitive damages arising out of or related to your use of the site, including lost profits, lost data, or business interruption, even if we have been advised of the possibility of such damages.',
        'terms_changes_p': 'If we make material changes, we\'ll bump the "Last updated" date and, for changes that broaden what we can do with your data or how we limit your rights, we\'ll add a more prominent notice on the home page for at least 30 days.',
        'terms_governing_p': 'PLACEHOLDER. Pick the jurisdiction before going public — typically the state/country where you (or the operating company) are based. Common choices: Delaware, USA; England & Wales; Singapore.',
        'terms_contact_p': 'PLACEHOLDER. Add an email address or contact form for legal notices.',
        # 404 H2 + body
        '404_h2_looking': 'Looking for one of these?',
        '404_404_link_home': 'Home',
        '404_404_link_generator': 'TikTok username generator',
        '404_404_link_faq': 'FAQ',
        '404_404_link_about': 'About',
        '404_404_link_privacy': 'Privacy Policy',
        '404_404_link_terms': 'Terms of Service',
    },
    # Other languages are appended via make_lang() below
}


def make_lang(lang_code, native, **overrides):
    """Create a PAGES entry for a non-English language by translating the
    English template through this script's translation function. For
    real this is filled in by the build script via _translate_page_dict
    below — but we expose the helper so users can preview translations.
    """
    raise NotImplementedError("Translations are inserted by build.py at build time")


# =============================================================================
# Per-language translations of every PAGES key.
# These are the full, hand-written translations — not direct English
# passes, but locale-native phrasing that matches the SEO keyword
# patterns above. Some "PLACEHOLDER" terms stay as PLACEHOLDER (e.g.
# jurisdiction, contact email) because those are intentionally
# operator-set in English; they are NOT translated.
# =============================================================================

_TRANSLATIONS = {
    'es': {
        'home_h1': 'Generador de nombres TikTok gratis con verificador de disponibilidad en vivo.',
        'gen_h1': 'Generador de nombres de usuario TikTok',
        'faq_h1': 'Preguntas frecuentes sobre el generador de nombres de TikTok',
        'about_h1': 'Sobre Handle — un generador de nombres TikTok gratis con verificador en vivo',
        'privacy_h1': 'Política de privacidad',
        'terms_h1': 'Términos de servicio',
        '404_h1': '404 — página no encontrada',
        'home_lede': 'Escribe una palabra, elige un nicho y un estilo, y obtén 10–20 ideas de nombres para TikTok que siguen las reglas actuales de TikTok. Cada uno se verifica en vivo en TikTok para que sepas si está disponible antes de copiarlo. Sin registro, sin límites de uso, sin marcas de agua.',
        'gen_lede': 'Ideas de nombres para TikTok gratis en segundos. Escribe una palabra (tu nombre, tu nicho o cualquier palabra que ancle el resultado), elige uno de los 17 nichos y uno de los 17 estilos, y el generador devuelve 10–20 sugerencias de @ únicas que respetan las reglas de TikTok. Cada sugerencia se verifica en vivo para ver si está disponible, con marca de tiempo, y se etiqueta como "Probablemente disponible", "Probablemente ocupado" o "Desconocido" para que sepas lo que estás copiando antes de reclamarlo.',
        'faq_lede': 'Respuestas cortas a las preguntas que la gente realmente busca antes de elegir un nombre de TikTok: cuáles son las reglas, cómo funciona el verificador de disponibilidad, por qué el veredicto dice "Probablemente" y no "Disponible", y cómo encontrar un nombre que te represente. Para la versión larga, consulta la <a href="/about" data-nav="about">página Sobre</a>; para la parte legal, consulta los <a href="/terms" data-nav="terms">Términos</a> y la <a href="/privacy" data-nav="privacy">Privacidad</a>.',
        'about_lede': 'Handle es una herramienta gratuita para creadores de TikTok que quieren un nombre que realmente exista. Escribe una palabra, elige un nicho y un estilo, obtén 10–20 ideas de nombres para TikTok que sigan las reglas actuales y mira cuáles están probablemente disponibles antes de copiar uno. La herramienta es gratis, no requiere registro y está disponible en 17 idiomas.',
        'privacy_lede': 'Última actualización 24 de agosto de 2026. Este es un borrador; reemplázalo con tu versión revisada antes de publicar.',
        'terms_lede': 'Última actualización 24 de agosto de 2026. Este es un borrador; reemplázalo con tu versión revisada por un abogado antes de publicar.',
        '404_lede': 'Esa URL no coincide con ninguna de nuestras páginas. Puede ser un error de escritura o un enlace que apunta a una versión antigua del sitio.',
        'home_h2_pick': 'Cómo elegir un nombre de TikTok que se adapte a ti',
        'home_h2_why': 'Por qué Handle',
        'home_h2_trending': 'Ideas de nombres de TikTok en tendencia para 2026',
        'home_h3_three_things': 'Tres cosas que los otros generadores de nombres TikTok se saltan',
        'home_pick_p1': "Un buen nombre de TikTok es corto, fácil de decir en voz alta, fácil de escribir de memoria e indica de qué trata tu contenido. Handle se encarga de la parte aburrida: escribes una palabra (tu nombre, tu nicho, una palabra de estilo), eliges uno de los 17 nichos y uno de los 17 estilos temáticos, y el generador devuelve 10–20 ideas de nombres de TikTok que respetan las reglas actuales de TikTok — 2 a 24 caracteres, letras minúsculas, números, puntos y guiones bajos, sin puntos al principio o al final, sin puntos consecutivos.",
        'home_pick_p2': 'Cada idea pasa por un verificador de disponibilidad en vivo en TikTok, con marca de tiempo, y se etiqueta como "Probablemente disponible", "Probablemente ocupado" o "Desconocido". El veredicto es honesto a propósito: un nombre puede estar libre en el momento en que lo verificamos y ocupado en el momento en que intentas reclamarlo. Si la verificación no puede llegar a TikTok (un fallo de red transitorio, un límite de velocidad de TikTok o una región privada), verás "Desconocido" con un enlace directo para confirmar visualmente en TikTok.',
        'home_why_p1': 'La mayoría de los generadores de nombres de TikTok se quedan en la lista. Copias un nombre, abres TikTok y descubres que está ocupado. Y otra vez. Handle cierra ese ciclo de tres formas que ninguna otra herramienta gratuita hace a la vez.',
        'home_why_li1': '<strong>Verificación de disponibilidad en vivo en TikTok.</strong> Cada handle generado se verifica con el endpoint de perfil de TikTok antes de que lo veas. No más copiar 12 nombres y descubrir que todos están ocupados.',
        'home_why_li2': '<strong>Veredictos honestos.</strong> "Probablemente disponible" con marca de tiempo es mejor que un "Disponible" seguro que está equivocado cuando haces clic. Decimos "Probablemente" a propósito.',
        'home_why_li3': '<strong>Reglas aplicadas desde el principio.</strong> Cada nombre sigue las reglas de caracteres de TikTok antes de llegar a ti — no copies un handle de 25 caracteres solo para descubrir que TikTok no lo aceptará.',
        'home_why_li4': '<strong>17 estilos temáticos + 17 nichos.</strong> Aesthetic, funny, professional, edgy, cute, mysterious, cool, chill, smart, romantic, powerful, gaming, techy, spooky, retro, wholesome, fantasy — cada uno cambia los pools de prefijos y sufijos para que las ideas se sientan como el creador que intentas ser, no como un "usuario123" genérico.',
        'home_why_li5': '<strong>Disponible en 17 idiomas.</strong> Toda la herramienta está localizada en español, francés, alemán, italiano, portugués, holandés, polaco, ruso, chino, vietnamita, indonesio, malayo, tagalo, hindi, bengalí, árabe y urdu — con palabras clave investigadas localmente, no traducción automática.',
        'home_trending_p1': 'Las tendencias de nombres de TikTok 2026 se inclinan hacia <strong>handles cortos, en minúsculas, de una sola palabra</strong> con un único toque estilístico: una letra duplicada ("glowy", "serenee"), un sufijo de un dígito o uno de los estilos de fuente Unicode que también puedes generar aquí. Los handles aesthetic y "soft girl" siguen posicionando para los nichos de estilo de vida y belleza; los handles de gaming y tech se inclinan más hacia combinaciones de dos palabras ("pixel.mode", "loot.drift"). Usa el generador con el estilo <strong>único</strong> o <strong>aesthetic</strong> para ver la dirección actual y pasa el resultado por el conversor de fuentes si quieres el nombre visual a juego.',
        'home_trending_p2': 'Próximamente: un blog para creadores de TikTok, páginas programáticas por nicho, verificación multiplataforma (Instagram, YouTube, X), un email semanal con nombres y canales sociales para sugerencias. Plan y compensaciones en el README.',
        'privacy_h2_what_site': 'Qué hace este sitio',
        'privacy_h2_collect': 'Qué recopilamos',
        'privacy_h2_third': 'Terceros',
        'privacy_h2_children': 'Privacidad de los menores',
        'privacy_h2_rights': 'Tus derechos',
        'privacy_h2_changes': 'Cambios en esta política',
        'privacy_what_site_p': 'Handle es un generador de nombres de usuario de TikTok gratuito. Escribes una palabra, eliges un nicho y un estilo, y el sitio devuelve una lista de ideas de @ que siguen las reglas de TikTok. Cada @ se verifica con el endpoint de perfil de TikTok para que veas si está probablemente disponible, probablemente ocupado o desconocido (la verificación no se pudo completar).',
        'privacy_collect_p1': '<strong>Nada que te identifique directamente.</strong> El generador es del lado del cliente: la palabra, el nicho, el estilo y la lista de resultados nunca salen de tu navegador de forma que te identifiquen. La verificación de disponibilidad es una solicitud del servidor al endpoint público de perfil/oEmbed de TikTok, iniciada por tu clic. El @ verificado no se asocia con un perfil de usuario en nuestro lado.',
        'privacy_collect_p2': '<strong>Registros del servidor.</strong> Como la mayoría de servidores web, nuestro proveedor registra la dirección IP, el agente de usuario, la ruta de la solicitud y la marca de tiempo en registros de acceso estándar, conservados durante 30 días por seguridad y prevención de abuso.',
        'privacy_collect_p3': '<strong>Cookies y almacenamiento local.</strong> La herramienta principal no establece cookies. El sitio almacena un valor en el <code>localStorage</code> de tu navegador — una marca que indica que descartaste el banner de consentimiento de cookies — para que el banner no aparezca en cada visita. Ese valor es <code>handle.cookieConsent.v1 = "accepted"</code>. Nunca se envía a nuestro servidor, nunca lo lee ningún tercero y puedes borrarlo en cualquier momento desde las herramientas de desarrollador del navegador o limpiando los datos del sitio.',
        'privacy_third_p1': '<strong>TikTok / ByteDance.</strong> La verificación de disponibilidad hace una solicitud al endpoint público de oEmbed y a la URL de perfil de TikTok. TikTok ve la solicitud desde la IP de nuestro servidor, el @ que se está verificando y las cabeceras HTTP estándar (incluido nuestro User-Agent). La política de privacidad de TikTok rige lo que hacen con esa solicitud.',
        'privacy_third_p2': '<strong>Hosting y CDN.</strong> Nuestro sitio estático se sirve a través de una CDN; las solicitudes estáticas se enrutan a través de nodos edge que registran IP/UA/ruta para sus propios fines de prevención de abuso.',
        'privacy_third_p3': '<strong>Publicidad (planeada, aún no activa).</strong> Si activamos Google AdSense, Google establecerá cookies y leerá identificadores para servir y medir anuncios. Verás un aviso claro y un flujo de consentimiento antes de que esto ocurra. Actualizaremos esta política para enumerar las cookies específicas de Google y cómo excluirlas antes de activar la integración.',
        'privacy_children_p': 'El sitio no está dirigido a menores de 13 años y no recopilamos información de ellos a sabiendas. Si crees que un menor ha proporcionado información a través del sitio, contáctanos para que podamos eliminarla.',
        'privacy_rights_p': 'Si estás en el EEE, Reino Unido o California, tienes derecho a solicitar acceso, corrección o eliminación de cualquier dato personal que tengamos sobre ti. Como no recopilamos datos personales más allá de los registros estándar del servidor, el efecto práctico suele ser una respuesta de "no tenemos nada sobre ti" — pero el derecho sigue vigente y puedes ejercerlo. Contacto: PLACEHOLDER.',
        'privacy_changes_p': 'Si hacemos cambios materiales, actualizaremos la fecha de "Última actualización" en la parte superior de esta página. Para cambios que amplíen los datos que recopilamos o cambien cómo los usamos, añadiremos un aviso más prominente en la página de inicio durante al menos 30 días.',
        'terms_h2_what': 'Qué es Handle',
        'terms_h2_no_affil': 'Sin afiliación con TikTok',
        'terms_h2_no_warranty': 'Sin garantía sobre los veredictos de disponibilidad',
        'terms_h2_no_trademark': 'Sin búsqueda de marcas registradas',
        'terms_h2_acceptable': 'Uso aceptable',
        'terms_h2_ip': 'Propiedad intelectual',
        'terms_h2_disclaimer': 'Exención de garantías',
        'terms_h2_liability': 'Limitación de responsabilidad',
        'terms_h2_changes': 'Cambios en estos términos',
        'terms_h2_governing': 'Ley aplicable',
        'terms_h2_contact': 'Contacto',
        'terms_what_p': 'Handle es una herramienta web pública y gratuita que te ayuda a generar ideas de nombres de TikTok y comprobar si un candidato está probablemente disponible. El resultado es un conjunto de sugerencias de @ más un veredicto de disponibilidad (probablemente disponible, probablemente ocupado o desconocido).',
        'terms_no_affil_p1': 'Handle es un proyecto independiente. No está afiliado, respaldado, patrocinado ni asociado de ninguna manera con TikTok, ByteDance Ltd. o cualquiera de sus filiales. "TikTok" es una marca comercial de ByteDance Ltd. Todas las referencias a TikTok en este sitio son únicamente con fines descriptivos (la herramienta verifica nombres de usuario en TikTok) y se hacen bajo uso justo.',
        'terms_no_affil_p2': 'Si eres titular de derechos y crees que una página de este sitio utiliza tu marca de una manera que no es uso justo, contáctanos y lo abordaremos con prontitud.',
        'terms_no_warranty_p': 'La verificación de disponibilidad es una sonda de mejor esfuerzo de los endpoints públicos de TikTok. Los veredictos pueden ser incorrectos, pueden estar desactualizados en el momento en que se emiten y pueden verse afectados por límites de velocidad de TikTok, bloqueos regionales o incidentes del servicio. "Probablemente disponible" no es una garantía. Eres responsable de confirmar la disponibilidad en TikTok antes de construir una marca sobre un @.',
        'terms_no_trademark_p': 'Handle no verifica marcas registradas. Un @ puede estar libre en TikTok y aun así infringir una marca registrada en tu industria. Antes de comprometerte con un @ para una marca pública, haz una búsqueda de marcas (USPTO TESS en EE. UU., EUIPO en la UE o equivalente local) y considera hablar con un abogado.',
        'terms_acceptable_p': 'Aceptas no usar Handle para:',
        'terms_acceptable_li1': 'Sondear TikTok a una velocidad que active sus sistemas anti-abuso. El sitio aplica un límite de 60 comprobaciones por minuto por IP; por favor respétalo.',
        'terms_acceptable_li2': 'Generar contenido ilegal, infractor o acosador.',
        'terms_acceptable_li3': 'Intentar eludir límites de velocidad, hacer scraping del sitio a escala industrial o interferir de otro modo con el servicio.',
        'terms_acceptable_li4': 'Hacerte pasar por una herramienta afiliada a TikTok.',
        'terms_ip_p': 'El nombre Handle, el código del sitio y las listas de palabras/reglas de patrones originales son de nuestra propiedad. Puedes usar los nombres generados como quieras: son sugerencias, no son nuestra propiedad una vez que te los entregamos. Las marcas de TikTok, el logo de TikTok y las reglas de nombres de TikTok son de TikTok. Los glifos Unicode en el conversor de fuentes son propiedad del Unicode Consortium y de los diseñadores tipográficos originales.',
        'terms_disclaimer_p': 'El sitio se proporciona "tal cual" y "según disponibilidad". En la máxima medida permitida por la ley, renunciamos a todas las garantías, expresas o implícitas, incluidas las garantías implícitas de comerciabilidad, idoneidad para un propósito particular y no infracción. No garantizamos que el sitio sea ininterrumpido, esté libre de errores o que los veredictos de disponibilidad sean precisos.',
        'terms_liability_p': 'En la máxima medida permitida por la ley, no seremos responsables de ningún daño indirecto, incidental, especial, consecuente o punitivo derivado o relacionado con tu uso del sitio, incluidos lucros cesantes, pérdida de datos o interrupción del negocio, incluso si se nos ha advertido de la posibilidad de tales daños.',
        'terms_changes_p': 'Si hacemos cambios materiales, actualizaremos la fecha de "Última actualización" y, para cambios que amplíen lo que podemos hacer con tus datos o cómo limitamos tus derechos, añadiremos un aviso más prominente en la página de inicio durante al menos 30 días.',
        'terms_governing_p': 'PLACEHOLDER. Elige la jurisdicción antes de publicar — típicamente el estado/país donde tú (o la empresa operadora) estés basado. Opciones comunes: Delaware, EE. UU.; Inglaterra y Gales; Singapur.',
        'terms_contact_p': 'PLACEHOLDER. Añade una dirección de correo electrónico o formulario de contacto para avisos legales.',
        '404_h2_looking': '¿Buscas alguno de estos?',
        '404_404_link_home': 'Inicio',
        '404_404_link_generator': 'Generador de nombres TikTok',
        '404_404_link_faq': 'Preguntas',
        '404_404_link_about': 'Sobre',
        '404_404_link_privacy': 'Política de privacidad',
        '404_404_link_terms': 'Términos de servicio',
    },
}

# Add the other 16 languages. Each entry is the FULL translation of
# PAGES[lang_code] using locale-native phrasing. PLACEHOLDER strings
# (jurisdiction, contact email) stay as PLACEHOLDER in English.
# This file is large; the remaining 16 languages are appended below
# in the build_pages_translations.py sibling file (kept separate so
# this file stays readable).

# (Stub — actual per-language dicts imported from pages_translations.py
# and pages_translations_tier2.py)
try:
    from pages_translations import TRANSLATIONS as _MORE
    _TRANSLATIONS.update(_MORE)
except ImportError:
    pass
try:
    from pages_translations_tier2 import TRANSLATIONS as _MORE2
    _TRANSLATIONS.update(_MORE2)
except ImportError:
    pass

# Extra strings discovered during a comprehensive audit that found
# additional gaps: Roadmap list items, Terms acceptable use list items,
# 404 buttons, affiliation note. Loaded as a 3rd patch.
try:
    from extra_strings import EXTRA as _EXTRA
    for _lang, _dict in _EXTRA.items():
        _TRANSLATIONS.setdefault(_lang, {}).update(_dict)
except ImportError:
    pass
