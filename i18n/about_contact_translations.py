# -*- coding: utf-8 -*-
"""
About page Contact paragraph translations (v18).

The English source (now in public/index.html) is:
  "Found a bug, want to suggest a feature, or just want to say hi?
   Write to us at <strong>hello@handle.name</strong> — we read
   everything and aim to respond within a week. For formal legal
   notices, takedown requests, or data-subject rights under GDPR/CCPA,
   write to <strong>legal@handle.name</strong> instead."

The build.py replaces the English source with the per-locale value from
ABOUT_CONTACT[lang]. All 18 langs (en + 17 locales) are included.
"""

ABOUT_CONTACT = {
    'en': "Found a bug, want to suggest a feature, or just want to say hi? Write to us at <strong>hello@handle.name</strong> — we read everything and aim to respond within a week. For formal legal notices, takedown requests, or data-subject rights under GDPR/CCPA, write to <strong>legal@handle.name</strong> instead.",

    'es': '¿Encontraste un error, quieres sugerir una función o solo quieres saludar? Escríbenos a <strong>hello@handle.name</strong>: leemos todo y respondemos en menos de una semana. Para avisos legales formales, solicitudes de retirada o derechos de interesado según GDPR/CCPA, escribe a <strong>legal@handle.name</strong>.',

    'de': 'Einen Fehler gefunden, eine Funktion vorschlagen oder einfach nur Hallo sagen? Schreib uns an <strong>hello@handle.name</strong> — wir lesen alles und antworten innerhalb einer Woche. Für formelle rechtliche Hinweise, Takedown-Anfragen oder Betroffenenrechte nach DSGVO/CCPA schreibe an <strong>legal@handle.name</strong>.',

    'fr': "Vous avez trouvé un bug, vous voulez suggérer une fonctionnalité ou simplement dire bonjour ? Écrivez-nous à <strong>hello@handle.name</strong> — nous lisons tout et nous nous efforçons de répondre sous une semaine. Pour les avis juridiques formels, les demandes de retrait ou les droits des personnes concernées au titre du RGPD/CCPA, écrivez à <strong>legal@handle.name</strong>.",

    'it': 'Hai trovato un bug, vuoi suggerire una funzione o vuoi solo salutarci? Scrivici a <strong>hello@handle.name</strong> — leggiamo tutto e cerchiamo di rispondere entro una settimana. Per avvisi legali formali, richieste di rimozione o diritti dell\'interessato ai sensi di GDPR/CCPA, scrivi a <strong>legal@handle.name</strong>.',

    'pt': 'Encontrou um bug, quer sugerir um recurso ou só quer dizer olá? Escreva para <strong>hello@handle.name</strong> — lemos tudo e respondemos em até uma semana. Para avisos legais formais, solicitações de remoção ou direitos de titular sob GDPR/CCPA, escreva para <strong>legal@handle.name</strong>.',

    'nl': 'Een bug gevonden, wil je een functie voorstellen of wil je gewoon hallo zeggen? Schrijf ons op <strong>hello@handle.name</strong> — we lezen alles en streven ernaar binnen een week te reageren. Voor formele juridische kennisgevingen, verzoeken tot verwijdering of rechten van betrokkenen onder AVG/CCPA, schrijf naar <strong>legal@handle.name</strong>.',

    'pl': 'Znalazłeś błąd, chcesz zaproponować funkcję, albo po prostu przywitać się? Napisz do nas na <strong>hello@handle.name</strong> — czytamy wszystko i staramy się odpowiedzieć w ciągu tygodnia. W sprawie formalnych zawiadomień prawnych, żądań usunięcia lub uprawnień osoby, której dane dotyczą, wynikających z RODO/CCPA, pisz na <strong>legal@handle.name</strong>.',

    'ru': 'Нашли ошибку, хотите предложить функцию или просто поздороваться? Напишите нам на <strong>hello@handle.name</strong> — мы читаем всё и стараемся ответить в течение недели. По вопросам официальных юридических уведомлений, запросов на удаление или прав субъекта данных в рамках GDPR/CCPA пишите на <strong>legal@handle.name</strong>.',

    'zh': '发现 bug、想提功能建议、还是只是想打个招呼?写信到 <strong>hello@handle.name</strong> 即可——我们阅读所有来信,并力争在一周内回复。涉及正式法律通知、删除请求或 GDPR/CCPA 规定的数据主体权利,请写信到 <strong>legal@handle.name</strong>。',

    'vi': 'Tìm thấy lỗi, muốn đề xuất tính năng, hay chỉ muốn chào? Hãy viết cho chúng tôi tại <strong>hello@handle.name</strong> — chúng tôi đọc tất cả và cố gắng phản hồi trong vòng một tuần. Đối với các thông báo pháp lý chính thức, yêu cầu gỡ bỏ hoặc quyền của chủ thể dữ liệu theo GDPR/CCPA, vui lòng viết đến <strong>legal@handle.name</strong>.',

    'id': 'Menemukan bug, ingin menyarankan fitur, atau sekadar ingin menyapa? Tulis ke kami di <strong>hello@handle.name</strong> — kami membaca semuanya dan berusaha membalas dalam waktu seminggu. Untuk pemberitahuan hukum formal, permintaan penghapusan, atau hak subjek data berdasarkan GDPR/CCPA, tulis ke <strong>legal@handle.name</strong>.',

    'ms': 'Jumpakan pepijat, ingin mencadangkan ciri, atau hanya ingin bertegur sapa? Tulis kepada kami di <strong>hello@handle.name</strong> — kami membaca semua dan berusaha membalas dalam masa seminggu. Untuk notis undang-undang formal, permintaan penanggalan, atau hak subjek data di bawah GDPR/CCPA, tulis ke <strong>legal@handle.name</strong>.',

    'tl': 'Nakita mo ang bug, nais mong magmungkahi ng feature, o gusto mo lang magbati? Sumulat sa amin sa <strong>hello@handle.name</strong> — nababasa namin ang lahat at nagsusumikap kaming sumagot sa loob ng isang linggo. Para sa mga pormal na legal na abiso, mga kahilingan sa pagtanggal, o mga karapatan ng data subject sa ilalim ng GDPR/CCPA, sumulat sa <strong>legal@handle.name</strong>.',

    'hi': 'कोई बग मिला, कोई सुविधा सुझानी है, या बस हैलो कहना है? हमें <strong>hello@handle.name</strong> पर लिखें — हम सब पढ़ते हैं और एक हफ्ते के भीतर जवाब देने की कोशिश करते हैं। GDPR/CCPA के तहत औपचारिक कानूनी सूचनाओं, हटाने के अनुरोधों या डेटा विषयक अधिकारों के लिए <strong>legal@handle.name</strong> पर लिखें।',

    'bn': 'কোনো বাগ পেয়েছেন, কোনো ফিচার সাজেস্ট করতে চান, নাকি শুধু হ্যালো বলতে চান? আমাদের <strong>hello@handle.name</strong>-এ লিখুন — আমরা সব পড়ি এবং এক সপ্তাহের মধ্যে উত্তর দেওয়ার চেষ্টা করি। GDPR/CCPA-এর অধীনে ফর্মাল আইনি নোটিশ, অপসারণ অনুরোধ বা ডেটা সাবজেক্ট অধিকারের জন্য <strong>legal@handle.name</strong>-এ লিখুন।',

    'ur': 'کوئی بگ ملا، کوئی فیچر تجویز کرنا ہے، یا بس ہیلو کہنا ہے؟ ہمیں <strong>hello@handle.name</strong> پر لکھیں — ہم سب کچھ پڑھتے ہیں اور ایک ہفتے کے اندر جواب دینے کی کوشش کرتے ہیں۔ GDPR/CCPA کے تحت باضابطہ قانونی نوٹس، ہٹانے کی درخواستوں، یا ڈیٹا سبجیکٹ کے حقوق کے لیے <strong>legal@handle.name</strong> پر لکھیں۔',

    'ar': 'وجدت خطأ، تريد اقتراح ميزة، أو تريد فقط إلقاء التحية؟ اكتب إلينا على <strong>hello@handle.name</strong> — نقرأ كل شيء ونسعى للرد خلال أسبوع. للإشعارات القانونية الرسمية، أو طلبات الإزالة، أو حقوق أصحاب البيانات بموجب اللائحة العامة لحماية البيانات (GDPR) أو قانون خصوصية المستهلك في كاليفورنيا (CCPA)، اكتب إلى <strong>legal@handle.name</strong>.',
}
