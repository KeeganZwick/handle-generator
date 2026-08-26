#!/usr/bin/env python3
"""
i18n/build.py — One-off build script for localized pages.

Reads public/index.html and generates public/{lang}/index.html for
each of the 17 supported languages.

Run from /workspace/nametok/:
    python3 i18n/build.py

Scope: For each locale, we localize the SEO-critical strings (html
lang/dir, title, meta description, og:title, og:description, og:locale,
canonical, language switcher, and the home hero + generator lede). For
8 Tier 1 languages (es, de, fr, it, pt, nl, pl, ru) we also localize
the FAQ headings and About intro. For the remaining 9 Tier 2 languages
(zh, vi, id, ms, tl, hi, bn, ar, ur) we localize the SEO-critical
strings only; the body content stays in English so the user can decide
whether to commission a professional translator for those markets.

This is honest: Tier 1 languages are fully localized for the visible
content above the fold; Tier 2 languages have proper meta tags and
language switcher for SEO and navigation, but the body text below
the fold is the English source. Spot-check before launching.
"""

import re
import sys
import json
import re
from pathlib import Path
from body_translations import FAQ_ABOUT_BODIES
from page_strings import SEO, PAGES as PAGE_TEMPLATES, _TRANSLATIONS as PAGES_TRANSLATIONS
from per_page_seo import PER_PAGE_SEO, PAGES, url_for, LANG_ORDER
# TIER1/TIER2 are imported from build's own dicts below (not from page_strings)

ROOT = Path(__file__).resolve().parent.parent
EN_PATH = ROOT / 'public' / 'index.html'
OUT_BASE = ROOT / 'public'

# Locale registry
LOCALES = {
    'es': {'native': 'Español', 'short': 'ES', 'en_name': 'Spanish', 'og_locale': 'es_ES', 'dir': 'ltr', 'tier': 1},
    'de': {'native': 'Deutsch', 'short': 'DE', 'en_name': 'German', 'og_locale': 'de_DE', 'dir': 'ltr', 'tier': 1},
    'fr': {'native': 'Français', 'short': 'FR', 'en_name': 'French', 'og_locale': 'fr_FR', 'dir': 'ltr', 'tier': 1},
    'it': {'native': 'Italiano', 'short': 'IT', 'en_name': 'Italian', 'og_locale': 'it_IT', 'dir': 'ltr', 'tier': 1},
    'pt': {'native': 'Português', 'short': 'PT', 'en_name': 'Portuguese', 'og_locale': 'pt_BR', 'dir': 'ltr', 'tier': 1},
    'nl': {'native': 'Nederlands', 'short': 'NL', 'en_name': 'Dutch', 'og_locale': 'nl_NL', 'dir': 'ltr', 'tier': 1},
    'pl': {'native': 'Polski', 'short': 'PL', 'en_name': 'Polish', 'og_locale': 'pl_PL', 'dir': 'ltr', 'tier': 1},
    'ru': {'native': 'Русский', 'short': 'RU', 'en_name': 'Russian', 'og_locale': 'ru_RU', 'dir': 'ltr', 'tier': 1},
    'zh': {'native': '中文', 'short': 'ZH', 'en_name': 'Chinese', 'og_locale': 'zh_CN', 'dir': 'ltr', 'tier': 2},
    'vi': {'native': 'Tiếng Việt', 'short': 'VI', 'en_name': 'Vietnamese', 'og_locale': 'vi_VN', 'dir': 'ltr', 'tier': 2},
    'id': {'native': 'Bahasa Indonesia', 'short': 'ID', 'en_name': 'Indonesian', 'og_locale': 'id_ID', 'dir': 'ltr', 'tier': 2},
    'ms': {'native': 'Bahasa Melayu', 'short': 'MS', 'en_name': 'Malay', 'og_locale': 'ms_MY', 'dir': 'ltr', 'tier': 2},
    'tl': {'native': 'Filipino', 'short': 'TL', 'en_name': 'Tagalog', 'og_locale': 'tl_PH', 'dir': 'ltr', 'tier': 2},
    'hi': {'native': 'हिन्दी', 'short': 'HI', 'en_name': 'Hindi', 'og_locale': 'hi_IN', 'dir': 'ltr', 'tier': 2},
    'bn': {'native': 'বাংলা', 'short': 'BN', 'en_name': 'Bengali', 'og_locale': 'bn_BD', 'dir': 'ltr', 'tier': 2},
    'ur': {'native': 'اردو', 'short': 'UR', 'en_name': 'Urdu', 'og_locale': 'ur_PK', 'dir': 'rtl', 'tier': 2},
    'ar': {'native': 'العربية', 'short': 'AR', 'en_name': 'Arabic', 'og_locale': 'ar_SA', 'dir': 'rtl', 'tier': 2},
}

# --- Tier 1 (full above-the-fold localization): 8 languages -----------------
# All 17 languages get the SEO-critical strings (title, meta, nav,
# free tag). Tier 1 languages additionally get hero h1, lede, button
# labels, generator lede, and FAQ heading. Body paragraphs stay in
# English for both tiers; the user can extend these later.

TIER1 = {
    'es': {
        'title': 'Generador de Nombres para TikTok — Handle',
        'meta_desc': 'Generador gratuito de nombres para TikTok. Escribe una palabra, elige un nicho y un estilo, obtén 10–20 ideas únicas que siguen las reglas de TikTok y comprueba la disponibilidad en TikTok. Sin registro, sin límites.',
        'og_title': 'Generador de Nombres para TikTok — Handle',
        'og_desc': 'Generador gratuito de nombres para TikTok con verificación de disponibilidad en vivo. 17 estilos, 17 nichos, sin registro.',
        'nav_home': 'Inicio', 'nav_generator': 'Generador', 'nav_faq': 'Preguntas', 'nav_about': 'Acerca de', 'nav_cta': 'Abrir la herramienta',
        'home_h1': 'Generador gratuito de nombres para TikTok con verificación en vivo.',
        'home_lede': 'Escribe una palabra, elige un nicho y un estilo, y obtén 10–20 ideas únicas de nombres para TikTok que siguen las reglas actuales. Cada una se verifica en TikTok para que sepas si probablemente está disponible antes de copiarla. Sin registro, sin límites, sin marcas de agua.',
        'home_cta_primary': 'Generar ideas de nombres →',
        'home_cta_secondary': 'Cómo funciona',
        'gen_h1': 'Generador de nombres para TikTok',
        'gen_lede': 'Ideas de nombres para TikTok gratis en segundos. Escribe una palabra, elige uno de los 17 nichos y uno de los 17 estilos temáticos, y el generador devuelve 10–20 sugerencias únicas que respetan las reglas actuales. Cada sugerencia se verifica en vivo en TikTok, con marca de tiempo, y se etiqueta como "Probablemente disponible", "Probablemente ocupado" o "Desconocido" para que sepas lo que estás copiando antes de reclamarlo.',
        '404_h1': '404 — página no encontrada',
        '404_lede': 'Esa URL no coincide con ninguna de nuestras páginas. Podría ser un error de escritura o un enlace que apunta a una versión anterior del sitio.',
        'titles': {
            'home': 'Generador de Nombres para TikTok — Handle',
            'generator': 'Generador de Nombres para TikTok — Handle',
            'faq': 'Preguntas Frecuentes — Handle',
            'about': 'Sobre Handle',
            'privacy': 'Política de Privacidad — Handle',
            'terms': 'Términos de Servicio — Handle',
        },
        'footer_privacy': 'Política de privacidad',
        'footer_terms': 'Términos de servicio',
    },
    'de': {
        'title': 'TikTok-Namensgenerator — Handle',
        'meta_desc': 'Kostenloser TikTok-Namensgenerator. Gib ein Stichwort ein, wähle eine Nische und einen Vibe, erhalte 10–20 TikTok-Nutzernamen-Ideen, die den Regeln entsprechen, und prüfe die Verfügbarkeit auf TikTok. Keine Anmeldung, keine Grenzen.',
        'og_title': 'TikTok-Namensgenerator — Handle',
        'og_desc': 'Kostenloser TikTok-Namensgenerator mit Live-Verfügbarkeitsprüfung. 17 Vibes, 17 Nischen, keine Anmeldung.',
        'nav_home': 'Start', 'nav_generator': 'Generator', 'nav_faq': 'FAQ', 'nav_about': 'Über', 'nav_cta': 'Tool öffnen',
        'home_h1': 'Kostenloser TikTok-Namensgenerator mit Live-Verfügbarkeitsprüfung.',
        'home_lede': 'Gib ein Stichwort ein, wähle eine Nische und einen Vibe, und erhalte 10–20 einzigartige TikTok-Nutzernamen-Ideen, die den aktuellen Regeln folgen. Jede wird live auf TikTok geprüft, damit du weißt, ob der Name wahrscheinlich verfügbar ist. Keine Anmeldung, keine Nutzungsgrenzen, keine Wasserzeichen.',
        'home_cta_primary': 'TikTok-Namen generieren →',
        'home_cta_secondary': 'So funktioniert es',
        'gen_h1': 'TikTok-Namensgenerator',
        'gen_lede': 'Kostenlose TikTok-Namensideen in Sekunden. Gib ein Stichwort ein, wähle eine von 17 Inhaltsnischen und einen von 17 Vibe-Stilen, und der Generator liefert 10–20 einzigartige Handle-Vorschläge, die die aktuellen TikTok-Regeln einhalten. Jeder Vorschlag wird live auf TikTok geprüft, mit Zeitstempel, und als "Wahrscheinlich verfügbar", "Wahrscheinlich vergeben" oder "Unbekannt" gekennzeichnet.',
        '404_h1': '404 — Seite nicht gefunden',
        '404_lede': 'Diese URL passt zu keiner unserer Seiten. Vielleicht ein Tippfehler oder ein Link auf eine alte Version der Seite.',
        'titles': {
            'home': 'TikTok-Namensgenerator — Handle',
            'generator': 'TikTok-Namensgenerator — Handle',
            'faq': 'Häufige Fragen — Handle',
            'about': 'Über Handle',
            'privacy': 'Datenschutzerklärung — Handle',
            'terms': 'Nutzungsbedingungen — Handle',
        },
        'footer_privacy': 'Datenschutzerklärung',
        'footer_terms': 'Nutzungsbedingungen',
    },
    'fr': {
        'title': 'Générateur de Noms TikTok — Handle',
        'meta_desc': "Générateur gratuit de noms d'utilisateur TikTok. Tapez un mot-clé, choisissez une niche et un style, obtenez 10–20 idées qui respectent les règles de TikTok et vérifiez la disponibilité sur TikTok. Sans inscription, sans limite.",
        'og_title': 'Générateur de Noms TikTok — Handle',
        'og_desc': "Générateur gratuit de noms d'utilisateur TikTok avec vérification en direct. 17 styles, 17 niches, sans inscription.",
        'nav_home': 'Accueil', 'nav_generator': 'Générateur', 'nav_faq': 'FAQ', 'nav_about': 'À propos', 'nav_cta': "Ouvrir l'outil",
        'home_h1': "Générateur gratuit de noms TikTok avec vérification de disponibilité en direct.",
        'home_lede': "Tapez un mot-clé, choisissez une niche et un style, et obtenez 10–20 idées de noms d'utilisateur TikTok qui respectent les règles actuelles. Chacune est vérifiée en direct sur TikTok pour que vous sachiez si elle est probablement disponible avant de la copier. Sans inscription, sans limite d'utilisation, sans filigrane.",
        'home_cta_primary': "Générer des idées de noms →",
        'home_cta_secondary': 'Comment ça marche',
        'gen_h1': 'Générateur de noms TikTok',
        'gen_lede': "Des idées de noms TikTok gratuites en quelques secondes. Tapez un mot-clé, choisissez une des 17 niches et un des 17 styles thématiques, et le générateur renvoie 10–20 suggestions de handles uniques qui respectent les règles actuelles. Chaque suggestion est vérifiée en direct sur TikTok, avec horodatage, et étiquetée « Probablement disponible », « Probablement pris » ou « Inconnu ».",
        '404_h1': '404 — page introuvable',
        '404_lede': "Cette URL ne correspond à aucune de nos pages. C'est peut-être une faute de frappe, ou un lien qui pointe vers une ancienne version du site.",
        'titles': {
            'home': 'Générateur de Noms TikTok — Handle',
            'generator': 'Générateur de Noms TikTok — Handle',
            'faq': 'Questions Fréquentes — Handle',
            'about': 'À Propos de Handle',
            'privacy': 'Politique de Confidentialité — Handle',
            'terms': "Conditions d'Utilisation — Handle",
        },
        'footer_privacy': 'Politique de confidentialité',
        'footer_terms': 'Conditions d\'utilisation',
    },
    'it': {
        'title': 'Generatore di Nomi TikTok — Handle',
        'meta_desc': "Generatore gratuito di nomi utente TikTok. Digita una parola, scegli una nicchia e uno stile, ottieni 10–20 idee uniche che rispettano le regole di TikTok e verifica la disponibilità su TikTok. Senza registrazione, senza limiti.",
        'og_title': 'Generatore di Nomi TikTok — Handle',
        'og_desc': "Generatore gratuito di nomi utente TikTok con controllo di disponibilità in tempo reale. 17 stili, 17 nicchie, senza registrazione.",
        'nav_home': 'Home', 'nav_generator': 'Generatore', 'nav_faq': 'FAQ', 'nav_about': 'Info', 'nav_cta': "Apri lo strumento",
        'home_h1': "Generatore gratuito di nomi TikTok con controllo di disponibilità in diretta.",
        'home_lede': "Digita una parola, scegli una nicchia e uno stile, e ottieni 10–20 idee di nomi utente TikTok che seguono le regole attuali. Ognuna viene verificata in diretta su TikTok così sai se è probabilmente disponibile prima di copiarla. Senza registrazione, senza limiti di utilizzo, senza watermark.",
        'home_cta_primary': 'Genera idee per nomi →',
        'home_cta_secondary': 'Come funziona',
        'gen_h1': 'Generatore di nomi TikTok',
        'gen_lede': "Idee per nomi TikTok gratuite in pochi secondi. Digita una parola chiave (il tuo nome, la tua nicchia o qualsiasi parola che ancori il risultato), scegli una delle 17 nicchie e uno dei 17 stili, e il generatore restituisce 10–20 suggerimenti unici che rispettano le regole attuali di TikTok. Ogni suggerimento viene verificato in diretta su TikTok, con timestamp, ed etichettato come \"Probabilmente disponibile\", \"Probabilmente occupato\" o \"Sconosciuto\".",
        '404_h1': '404 — pagina non trovata',
        '404_lede': "Questo URL non corrisponde a nessuna delle nostre pagine. Potrebbe essere un errore di battitura, o un link che punta a una vecchia versione del sito.",
        'titles': {
            'home': 'Generatore di Nomi TikTok — Handle',
            'generator': 'Generatore di Nomi TikTok — Handle',
            'faq': 'Domande Frequenti — Handle',
            'about': 'Su Handle',
            'privacy': 'Informativa sulla Privacy — Handle',
            'terms': 'Termini di Servizio — Handle',
        },
        'footer_privacy': 'Informativa sulla privacy',
        'footer_terms': 'Termini di servizio',
    },
    'pt': {
        'title': 'Gerador de Nomes TikTok — Handle',
        'meta_desc': 'Gerador gratuito de nomes de usuário TikTok. Digite uma palavra-chave, escolha um nicho e um estilo, obtenha 10–20 ideias únicas que seguem as regras do TikTok e verifique a disponibilidade no TikTok. Sem cadastro, sem limites.',
        'og_title': 'Gerador de Nomes TikTok — Handle',
        'og_desc': 'Gerador gratuito de nomes de usuário TikTok com verificação de disponibilidade ao vivo. 17 estilos, 17 nichos, sem cadastro.',
        'nav_home': 'Início', 'nav_generator': 'Gerador', 'nav_faq': 'Perguntas', 'nav_about': 'Sobre', 'nav_cta': 'Abrir a ferramenta',
        'home_h1': 'Gerador gratuito de nomes TikTok com verificação de disponibilidade ao vivo.',
        'home_lede': 'Digite uma palavra-chave, escolha um nicho e um estilo, e obtenha 10–20 ideias únicas de nomes de usuário TikTok que seguem as regras atuais. Cada uma é verificada ao vivo no TikTok para que você saiba se provavelmente está disponível antes de copiar. Sem cadastro, sem limites de uso, sem marcas d\'água.',
        'home_cta_primary': 'Gerar ideias de nomes →',
        'home_cta_secondary': 'Como funciona',
        'gen_h1': 'Gerador de nomes TikTok',
        'gen_lede': 'Ideias de nomes TikTok gratuitas em segundos. Digite uma palavra-chave (seu nome, seu nicho ou qualquer palavra que ancore o resultado), escolha uma das 17 categorias e um dos 17 estilos temáticos, e o gerador devolve 10–20 sugestões únicas que respeitam as regras atuais do TikTok. Cada sugestão é verificada ao vivo no TikTok, com carimbo de data/hora, e rotulada como "Provavelmente disponível", "Provavelmente em uso" ou "Desconhecido".',
        '404_h1': '404 — página não encontrada',
        '404_lede': 'Esta URL não corresponde a nenhuma das nossas páginas. Pode ser um erro de digitação ou um link que aponta para uma versão antiga do site.',
        'titles': {
            'home': 'Gerador de Nomes TikTok — Handle',
            'generator': 'Gerador de Nomes TikTok — Handle',
            'faq': 'Perguntas Frequentes — Handle',
            'about': 'Sobre o Handle',
            'privacy': 'Política de Privacidade — Handle',
            'terms': 'Termos de Serviço — Handle',
        },
        'footer_privacy': 'Política de privacidade',
        'footer_terms': 'Termos de serviço',
    },
    'nl': {
        'title': 'TikTok Naam Generator — Handle',
        'meta_desc': "Gratis TikTok gebruikersnaam generator. Typ een trefwoord, kies een niche en een vibe, krijg 10–20 unieke TikTok gebruikersnaam ideeën die aan de regels voldoen, en check de beschikbaarheid op TikTok. Geen account, geen limiet.",
        'og_title': 'TikTok Naam Generator — Handle',
        'og_desc': "Gratis TikTok naam generator met live beschikbaarheidscontrole. 17 vibes, 17 niches, geen account nodig.",
        'nav_home': 'Home', 'nav_generator': 'Generator', 'nav_faq': 'FAQ', 'nav_about': 'Over', 'nav_cta': 'Open de tool',
        'home_h1': "Gratis TikTok naam generator met live beschikbaarheidscontrole.",
        'home_lede': "Typ een trefwoord, kies een niche en een vibe, en krijg 10–20 unieke TikTok gebruikersnaam ideeën die aan de huidige regels voldoen. Elke naam wordt live op TikTok gecontroleerd zodat je weet of hij waarschijnlijk beschikbaar is voor je hem kopieert. Geen account, geen gebruikslimieten, geen watermerk.",
        'home_cta_primary': 'Genereer TikTok namen →',
        'home_cta_secondary': 'Hoe het werkt',
        'gen_h1': 'TikTok naam generator',
        'gen_lede': "Gratis TikTok naam ideeën in seconden. Typ een trefwoord (je naam, je niche, of een willekeurig woord dat het resultaat verankert), kies een van de 17 content niches en een van de 17 themastijlen, en de generator geeft 10–20 unieke handle suggesties terug die aan de huidige TikTok regels voldoen. Elke suggestie wordt live op TikTok gecontroleerd, met tijdstempel, en gelabeld als \"Waarschijnlijk beschikbaar\", \"Waarschijnlijk in gebruik\" of \"Onbekend\".",
        '404_h1': '404 — pagina niet gevonden',
        '404_lede': 'Die URL komt niet overeen met een van onze pagina\'s. Het kan een typefout zijn, of een link die naar een oude versie van de site wijst.',
        'titles': {
            'home': 'TikTok Naam Generator — Handle',
            'generator': 'TikTok Naam Generator — Handle',
            'faq': 'Veelgestelde Vragen — Handle',
            'about': 'Over Handle',
            'privacy': 'Privacybeleid — Handle',
            'terms': 'Servicevoorwaarden — Handle',
        },
        'footer_privacy': 'Privacybeleid',
        'footer_terms': 'Servicevoorwaarden',
    },
    'pl': {
        'title': 'Generator Nazw TikTok — Handle',
        'meta_desc': 'Darmowy generator nazw użytkownika TikTok. Wpisz słowo kluczowe, wybierz niszę i styl, otrzymaj 10–20 unikalnych pomysłów zgodnych z zasadami TikToka i sprawdź dostępność na TikToku. Bez rejestracji, bez limitów.',
        'og_title': 'Generator Nazw TikTok — Handle',
        'og_desc': 'Darmowy generator nazw użytkownika TikTok z bieżącym sprawdzaniem dostępności. 17 stylów, 17 nisz, bez rejestracji.',
        'nav_home': 'Start', 'nav_generator': 'Generator', 'nav_faq': 'FAQ', 'nav_about': 'O nas', 'nav_cta': 'Otwórz narzędzie',
        'home_h1': 'Darmowy generator nazw TikTok z bieżącym sprawdzaniem dostępności.',
        'home_lede': 'Wpisz słowo kluczowe, wybierz niszę i styl, a otrzymasz 10–20 unikalnych pomysłów na nazwy użytkownika TikTok, które spełniają aktualne zasady. Każdy pomysł jest sprawdzany na żywo na TikToku, dzięki czemu wiesz, czy nazwa jest prawdopodobnie dostępna, zanim ją skopiujesz. Bez rejestracji, bez limitów użycia, bez znaków wodnych.',
        'home_cta_primary': 'Wygeneruj pomysły na nazwy →',
        'home_cta_secondary': 'Jak to działa',
        'gen_h1': 'Generator nazw TikTok',
        'gen_lede': 'Darmowe pomysły na nazwy TikTok w kilka sekund. Wpisz słowo kluczowe (swoje imię, swoją niszę lub dowolne słowo, które zakotwicza wynik), wybierz jedną z 17 nisz treści i jeden z 17 stylów tematycznych, a generator zwróci 10–20 unikalnych sugestii uchwytów, które spełniają aktualne zasady TikToka. Każda sugestia jest sprawdzana na żywo na TikToku, ze znacznikiem czasu, i oznaczana jako „Prawdopodobnie dostępna”, „Prawdopodobnie zajęta” lub „Nieznana”.',
        '404_h1': '404 — nie znaleziono strony',
        '404_lede': 'Ten adres URL nie pasuje do żadnej z naszych stron. Może to literówka lub link wskazujący na starą wersję witryny.',
        'titles': {
            'home': 'Generator Nazw TikTok — Handle',
            'generator': 'Generator Nazw TikTok — Handle',
            'faq': 'Często Zadawane Pytania — Handle',
            'about': 'O Handle',
            'privacy': 'Polityka Prywatności — Handle',
            'terms': 'Warunki Korzystania — Handle',
        },
        'footer_privacy': 'Polityka prywatności',
        'footer_terms': 'Warunki korzystania',
    },
    'ru': {
        'title': 'Генератор Ников TikTok — Handle',
        'meta_desc': 'Бесплатный генератор никнеймов для TikTok. Введите ключевое слово, выберите нишу и стиль, получите 10–20 уникальных идей, соответствующих правилам TikTok, и проверьте доступность в TikTok. Без регистрации, без ограничений.',
        'og_title': 'Генератор Ников TikTok — Handle',
        'og_desc': 'Бесплатный генератор никнеймов для TikTok с проверкой доступности в реальном времени. 17 стилей, 17 ниш, без регистрации.',
        'nav_home': 'Главная', 'nav_generator': 'Генератор', 'nav_faq': 'FAQ', 'nav_about': 'О нас', 'nav_cta': 'Открыть инструмент',
        'home_h1': 'Бесплатный генератор ников TikTok с проверкой доступности в реальном времени.',
        'home_lede': 'Введите ключевое слово, выберите нишу и стиль, и получите 10–20 уникальных идей никнеймов для TikTok, которые соответствуют актуальным правилам. Каждая идея проверяется в реальном времени в TikTok, так что вы знаете, вероятно ли имя доступно, прежде чем его копировать. Без регистрации, без лимитов использования, без водяных знаков.',
        'home_cta_primary': 'Сгенерировать идеи имён →',
        'home_cta_secondary': 'Как это работает',
        'gen_h1': 'Генератор ников TikTok',
        'gen_lede': 'Бесплатные идеи никнеймов для TikTok за секунды. Введите ключевое слово (ваше имя, вашу нишу или любое слово, которое закрепляет результат), выберите одну из 17 ниш контента и один из 17 тематических стилей, и генератор вернёт 10–20 уникальных предложений, которые соответствуют актуальным правилам TikTok. Каждое предложение проверяется в реальном времени в TikTok, с меткой времени, и маркируется как «Вероятно доступно», «Вероятно занято» или «Неизвестно».',
        '404_h1': '404 — страница не найдена',
        '404_lede': 'Этот URL не соответствует ни одной из наших страниц. Возможно, это опечатка или ссылка на старую версию сайта.',
        'titles': {
            'home': 'Генератор Ников TikTok — Handle',
            'generator': 'Генератор Ников TikTok — Handle',
            'faq': 'Часто Задаваемые Вопросы — Handle',
            'about': 'О Handle',
            'privacy': 'Политика Конфиденциальности — Handle',
            'terms': 'Условия Использования — Handle',
        },
        'footer_privacy': 'Политика конфиденциальности',
        'footer_terms': 'Условия использования',
    },
}

# --- FAQ + About body translations for Tier 1 (8 languages) ---------------
#
# These are applied as find-replace in the localized index.html. The
# English source has the questions and answers as plain text inside
# <h3> and <p> tags. We translate:
#   - FAQ H2 subheadings (4 per language)
#   - FAQ H3 question titles (18 per language)
#   - About H2 subheadings (6 per language)
#   - The first paragraph of each About section
#   - The first paragraph of each FAQ answer
#
# The translations are correct-to-my-knowledge but not professional
# translations. For a real launch in a specific market, have a native
# reviewer confirm the FAQ and About copy.

FAQ_ABOUT_TRANSLATIONS = {
    'es': {
        # FAQ H2
        'faq_h2_picking': 'Cómo elegir un nombre de TikTok',
        'faq_h2_check': 'Cómo funciona la verificación de disponibilidad',
        'faq_h2_styles': 'Nombres, estilos y tendencias',
        'faq_h2_legal': 'Cuenta, legal y soporte',
        # FAQ H3
        'faq_q1': '¿Cuál debería ser mi nombre de TikTok?',
        'faq_q2': '¿Cómo elijo un nombre de TikTok que me represente?',
        'faq_q3': '¿Por qué mi nombre de TikTok ya está ocupado?',
        'faq_q4': '¿Qué hace que un nombre de TikTok sea bueno?',
        'faq_q5': '¿Cómo cambio mi nombre de TikTok?',
        'faq_q6': '¿Cuál es la diferencia entre nombre de usuario y nombre para mostrar?',
        'faq_q7': '¿Cómo sé si un nombre de TikTok está disponible?',
        'faq_q8': '¿Cómo funciona la verificación de disponibilidad?',
        'faq_q9': '¿Por qué dice "Probablemente disponible" en vez de solo "Disponible"?',
        'faq_q10': '¿Por qué un handle aparece como "Desconocido" en los resultados?',
        'faq_q11': '¿Cuáles son los mejores nombres de TikTok para 2026?',
        'faq_q12': '¿Qué es un nombre corto de TikTok y por qué importa la longitud?',
        'faq_q13': '¿Cuáles son los mejores nombres estéticos, cool, graciosos y edgy?',
        'faq_q14': '¿Puedo usar las fuentes de TikTok en mi @handle?',
        'faq_q15': '¿Funciona el generador para otras plataformas?',
        'faq_q16': '¿Puedo usar los nombres que genera Handle con fines comerciales?',
        'faq_q17': '¿Es gratis Handle?',
        'faq_q18': '¿Está Handle afiliado a TikTok?',
        # About H2
        'about_h2_what': 'Qué es esto',
        'about_h2_isnt': 'Qué no es',
        'about_h2_how': 'Cómo funciona por dentro',
        'about_h2_l10n': 'Localización — 17 idiomas, targeting nativo de palabras clave',
        'about_h2_roadmap': 'Hoja de ruta',
        'about_h2_contact': 'Contacto',
        'footer_privacy': 'Política de privacidad',
        'footer_terms': 'Términos de servicio',
    },
    'de': {
        'faq_h2_picking': 'Einen TikTok-Namen auswählen',
        'faq_h2_check': 'Wie die Verfügbarkeitsprüfung funktioniert',
        'faq_h2_styles': 'Namen, Stile und Trends',
        'faq_h2_legal': 'Konto, Rechtliches und Support',
        'faq_q1': 'Was sollte mein TikTok-Name sein?',
        'faq_q2': 'Wie wähle ich einen TikTok-Namen, der zu mir passt?',
        'faq_q3': 'Warum ist mein TikTok-Name schon vergeben?',
        'faq_q4': 'Was macht einen guten TikTok-Namen aus?',
        'faq_q5': 'Wie ändere ich meinen TikTok-Namen?',
        'faq_q6': 'Was ist der Unterschied zwischen Nutzername und Anzeigename?',
        'faq_q7': 'Woher weiß ich, ob ein TikTok-Name verfügbar ist?',
        'faq_q8': 'Wie funktioniert die Verfügbarkeitsprüfung?',
        'faq_q9': 'Warum steht da "Wahrscheinlich verfügbar" statt nur "Verfügbar"?',
        'faq_q10': 'Warum zeigt ein Handle "Unbekannt" in der Ergebnisliste?',
        'faq_q11': 'Was sind die besten TikTok-Namen für 2026?',
        'faq_q12': 'Was ist ein kurzer TikTok-Name und warum ist die Länge wichtig?',
        'faq_q13': 'Was sind die besten ästhetischen, coolen, lustigen und edgy TikTok-Namen?',
        'faq_q14': 'Kann ich TikTok-Schriftarten in meinem @handle verwenden?',
        'faq_q15': 'Funktioniert der Generator auch für andere Plattformen?',
        'faq_q16': 'Darf ich die mit Handle generierten Namen kommerziell nutzen?',
        'faq_q17': 'Ist Handle kostenlos?',
        'faq_q18': 'Ist Handle mit TikTok verbunden?',
        'about_h2_what': 'Was das ist',
        'about_h2_isnt': 'Was es nicht ist',
        'about_h2_how': 'Wie es unter der Haube funktioniert',
        'about_h2_l10n': 'Lokalisierung — 17 Sprachen, native Keyword-Ausrichtung',
        'about_h2_roadmap': 'Fahrplan',
        'about_h2_contact': 'Kontakt',
        'footer_privacy': 'Datenschutzerklärung',
        'footer_terms': 'Nutzungsbedingungen',
    },
    'fr': {
        'faq_h2_picking': 'Choisir un nom TikTok',
        'faq_h2_check': 'Comment fonctionne la vérification de disponibilité',
        'faq_h2_styles': 'Noms, styles et tendances',
        'faq_h2_legal': 'Compte, mentions légales et support',
        'faq_q1': 'Quel devrait être mon nom TikTok ?',
        'faq_q2': 'Comment choisir un nom TikTok qui me correspond ?',
        'faq_q3': 'Pourquoi mon nom TikTok est-il déjà pris ?',
        'faq_q4': 'Qu\'est-ce qui fait un bon nom TikTok ?',
        'faq_q5': 'Comment changer mon nom TikTok ?',
        'faq_q6': 'Quelle est la différence entre nom d\'utilisateur et nom d\'affichage ?',
        'faq_q7': 'Comment savoir si un nom TikTok est disponible ?',
        'faq_q8': 'Comment fonctionne la vérification de disponibilité ?',
        'faq_q9': 'Pourquoi est-il écrit « Probablement disponible » au lieu de juste « Disponible » ?',
        'faq_q10': 'Pourquoi un handle affiche « Inconnu » dans la liste des résultats ?',
        'faq_q11': 'Quels sont les meilleurs noms TikTok pour 2026 ?',
        'faq_q12': 'Qu\'est-ce qu\'un nom TikTok court et pourquoi la longueur compte-t-elle ?',
        'faq_q13': 'Quels sont les meilleurs noms TikTok esthétiques, cool, drôles et edgy ?',
        'faq_q14': 'Puis-je utiliser les polices TikTok dans mon @handle ?',
        'faq_q15': 'Le générateur fonctionne-t-il pour d\'autres plateformes ?',
        'faq_q16': 'Puis-je utiliser commercialement les noms générés par Handle ?',
        'faq_q17': 'Handle est-il gratuit ?',
        'faq_q18': 'Handle est-il affilié à TikTok ?',
        'about_h2_what': 'Ce que c\'est',
        'about_h2_isnt': 'Ce que ce n\'est pas',
        'about_h2_how': 'Comment ça marche sous le capot',
        'about_h2_l10n': 'Localisation — 17 langues, ciblage natif des mots-clés',
        'about_h2_roadmap': 'Feuille de route',
        'about_h2_contact': 'Contact',
        'footer_privacy': 'Politique de confidentialité',
        'footer_terms': 'Conditions d\'utilisation',
    },
    'it': {
        'faq_h2_picking': 'Scegliere un nome TikTok',
        'faq_h2_check': 'Come funziona il controllo di disponibilità',
        'faq_h2_styles': 'Nomi, stili e tendenze',
        'faq_h2_legal': 'Account, legale e supporto',
        'faq_q1': 'Quale dovrebbe essere il mio nome TikTok?',
        'faq_q2': 'Come scelgo un nome TikTok che mi rappresenta?',
        'faq_q3': 'Perché il mio nome TikTok è già occupato?',
        'faq_q4': 'Cosa rende buono un nome TikTok?',
        'faq_q5': 'Come cambio il mio nome TikTok?',
        'faq_q6': 'Qual è la differenza tra nome utente e nome visualizzato?',
        'faq_q7': 'Come faccio a sapere se un nome TikTok è disponibile?',
        'faq_q8': 'Come funziona il controllo di disponibilità?',
        'faq_q9': 'Perché dice "Probabilmente disponibile" invece di solo "Disponibile"?',
        'faq_q10': 'Perché un handle appare come "Sconosciuto" nei risultati?',
        'faq_q11': 'Quali sono i migliori nomi TikTok per il 2026?',
        'faq_q12': 'Cos\'è un nome TikTok corto e perché la lunghezza è importante?',
        'faq_q13': 'Quali sono i migliori nomi TikTok estetici, cool, divertenti e edgy?',
        'faq_q14': 'Posso usare i font TikTok nel mio @handle?',
        'faq_q15': 'Il generatore funziona per altre piattaforme?',
        'faq_q16': 'Posso usare commercialmente i nomi generati da Handle?',
        'faq_q17': 'Handle è gratuito?',
        'faq_q18': 'Handle è affiliato a TikTok?',
        'about_h2_what': 'Cos\'è',
        'about_h2_isnt': 'Cosa non è',
        'about_h2_how': 'Come funziona sotto il cofano',
        'about_h2_l10n': 'Localizzazione — 17 lingue, targeting nativo delle keyword',
        'about_h2_roadmap': 'Roadmap',
        'about_h2_contact': 'Contatti',
        'footer_privacy': 'Informativa sulla privacy',
        'footer_terms': 'Termini di servizio',
    },
    'pt': {
        'faq_h2_picking': 'Escolhendo um nome para TikTok',
        'faq_h2_check': 'Como funciona a verificação de disponibilidade',
        'faq_h2_styles': 'Nomes, estilos e tendências',
        'faq_h2_legal': 'Conta, jurídico e suporte',
        'faq_q1': 'Qual deveria ser meu nome no TikTok?',
        'faq_q2': 'Como escolho um nome para TikTok que combine comigo?',
        'faq_q3': 'Por que meu nome no TikTok já está em uso?',
        'faq_q4': 'O que faz um bom nome de TikTok?',
        'faq_q5': 'Como mudo meu nome no TikTok?',
        'faq_q6': 'Qual a diferença entre nome de usuário e nome de exibição?',
        'faq_q7': 'Como sei se um nome no TikTok está disponível?',
        'faq_q8': 'Como funciona a verificação de disponibilidade?',
        'faq_q9': 'Por que diz "Provavelmente disponível" em vez de apenas "Disponível"?',
        'faq_q10': 'Por que um handle aparece como "Desconhecido" nos resultados?',
        'faq_q11': 'Quais são os melhores nomes de TikTok para 2026?',
        'faq_q12': 'O que é um nome curto no TikTok e por que o tamanho importa?',
        'faq_q13': 'Quais são os melhores nomes de TikTok estéticos, legais, engraçados e ousados?',
        'faq_q14': 'Posso usar as fontes do TikTok no meu @handle?',
        'faq_q15': 'O gerador funciona para outras plataformas?',
        'faq_q16': 'Posso usar comercialmente os nomes gerados pelo Handle?',
        'faq_q17': 'O Handle é gratuito?',
        'faq_q18': 'O Handle é afiliado ao TikTok?',
        'about_h2_what': 'O que é',
        'about_h2_isnt': 'O que não é',
        'about_h2_how': 'Como funciona por dentro',
        'about_h2_l10n': 'Localização — 17 idiomas, segmentação nativa de palavras-chave',
        'about_h2_roadmap': 'Roteiro',
        'about_h2_contact': 'Contato',
        'footer_privacy': 'Política de privacidade',
        'footer_terms': 'Termos de serviço',
    },
    'nl': {
        'faq_h2_picking': 'Een TikTok-naam kiezen',
        'faq_h2_check': 'Hoe de beschikbaarheidscontrole werkt',
        'faq_h2_styles': 'Namen, stijlen en trends',
        'faq_h2_legal': 'Account, juridisch en ondersteuning',
        'faq_q1': 'Wat moet mijn TikTok-naam zijn?',
        'faq_q2': 'Hoe kies ik een TikTok-naam die bij me past?',
        'faq_q3': 'Waarom is mijn TikTok-naam al in gebruik?',
        'faq_q4': 'Wat maakt een goede TikTok-naam?',
        'faq_q5': 'Hoe verander ik mijn TikTok-naam?',
        'faq_q6': 'Wat is het verschil tussen gebruikersnaam en weergavenaam?',
        'faq_q7': 'Hoe weet ik of een TikTok-naam beschikbaar is?',
        'faq_q8': 'Hoe werkt de beschikbaarheidscontrole?',
        'faq_q9': 'Waarom staat er "Waarschijnlijk beschikbaar" in plaats van alleen "Beschikbaar"?',
        'faq_q10': 'Waarom toont een handle "Onbekend" in de resultaten?',
        'faq_q11': 'Wat zijn de beste TikTok-namen voor 2026?',
        'faq_q12': 'Wat is een korte TikTok-naam en waarom is de lengte belangrijk?',
        'faq_q13': 'Wat zijn de beste esthetische, coole, grappige en edgy TikTok-namen?',
        'faq_q14': 'Kan ik TikTok-lettertypen in mijn @handle gebruiken?',
        'faq_q15': 'Werkt de generator ook voor andere platforms?',
        'faq_q16': 'Mag ik de namen die Handle genereert commercieel gebruiken?',
        'faq_q17': 'Is Handle gratis?',
        'faq_q18': 'Is Handle gelieerd aan TikTok?',
        'about_h2_what': 'Wat dit is',
        'about_h2_isnt': 'Wat dit niet is',
        'about_h2_how': 'Hoe het werkt onder de motorkap',
        'about_h2_l10n': 'Lokalisatie — 17 talen, native zoekwoord-targeting',
        'about_h2_roadmap': 'Routekaart',
        'about_h2_contact': 'Contact',
        'footer_privacy': 'Privacybeleid',
        'footer_terms': 'Servicevoorwaarden',
    },
    'pl': {
        'faq_h2_picking': 'Wybór nazwy TikTok',
        'faq_h2_check': 'Jak działa sprawdzanie dostępności',
        'faq_h2_styles': 'Nazwy, style i trendy',
        'faq_h2_legal': 'Konto, kwestie prawne i wsparcie',
        'faq_q1': 'Jaka powinna być moja nazwa TikTok?',
        'faq_q2': 'Jak wybrać nazwę TikTok, która do mnie pasuje?',
        'faq_q3': 'Dlaczego moja nazwa TikTok jest już zajęta?',
        'faq_q4': 'Co sprawia, że nazwa TikTok jest dobra?',
        'faq_q5': 'Jak zmienić moją nazwę TikTok?',
        'faq_q6': 'Jaka jest różnica między nazwą użytkownika a nazwą wyświetlaną?',
        'faq_q7': 'Skąd wiem, czy nazwa TikTok jest dostępna?',
        'faq_q8': 'Jak działa sprawdzanie dostępności?',
        'faq_q9': 'Dlaczego pisze „Prawdopodobnie dostępna” zamiast po prostu „Dostępna”?',
        'faq_q10': 'Dlaczego uchwyt pokazuje „Nieznany” na liście wyników?',
        'faq_q11': 'Jakie są najlepsze nazwy TikTok na 2026?',
        'faq_q12': 'Co to jest krótka nazwa TikTok i dlaczego długość ma znaczenie?',
        'faq_q13': 'Jakie są najlepsze estetyczne, cool, zabawne i edgy nazwy TikTok?',
        'faq_q14': 'Czy mogę użyć czcionek TikTok w moim @handle?',
        'faq_q15': 'Czy generator działa dla innych platform?',
        'faq_q16': 'Czy mogę komercyjnie wykorzystywać nazwy generowane przez Handle?',
        'faq_q17': 'Czy Handle jest darmowy?',
        'faq_q18': 'Czy Handle jest powiązany z TikTokiem?',
        'about_h2_what': 'Co to jest',
        'about_h2_isnt': 'Czym to nie jest',
        'about_h2_how': 'Jak to działa od środka',
        'about_h2_l10n': 'Lokalizacja — 17 języków, natywne targetowanie słów kluczowych',
        'about_h2_roadmap': 'Plan rozwoju',
        'about_h2_contact': 'Kontakt',
        'footer_privacy': 'Polityka prywatności',
        'footer_terms': 'Warunki korzystania',
    },
    'ru': {
        'faq_h2_picking': 'Выбор имени в TikTok',
        'faq_h2_check': 'Как работает проверка доступности',
        'faq_h2_styles': 'Имена, стили и тренды',
        'faq_h2_legal': 'Аккаунт, юридические вопросы и поддержка',
        'faq_q1': 'Каким должно быть моё имя в TikTok?',
        'faq_q2': 'Как выбрать имя в TikTok, которое мне подходит?',
        'faq_q3': 'Почему моё имя в TikTok уже занято?',
        'faq_q4': 'Что делает имя в TikTok хорошим?',
        'faq_q5': 'Как изменить моё имя в TikTok?',
        'faq_q6': 'В чём разница между именем пользователя и отображаемым именем?',
        'faq_q7': 'Как узнать, доступно ли имя в TikTok?',
        'faq_q8': 'Как работает проверка доступности?',
        'faq_q9': 'Почему написано «Вероятно доступно», а не просто «Доступно»?',
        'faq_q10': 'Почему хэндл показывает «Неизвестно» в результатах?',
        'faq_q11': 'Какие лучшие имена в TikTok на 2026 год?',
        'faq_q12': 'Что такое короткое имя в TikTok и почему важна длина?',
        'faq_q13': 'Какие лучшие эстетичные, крутые, смешные и дерзкие имена в TikTok?',
        'faq_q14': 'Можно ли использовать шрифты TikTok в моём @handle?',
        'faq_q15': 'Работает ли генератор для других платформ?',
        'faq_q16': 'Можно ли использовать имена, сгенерированные Handle, в коммерческих целях?',
        'faq_q17': 'Handle бесплатен?',
        'faq_q18': 'Handle связан с TikTok?',
        'about_h2_what': 'Что это',
        'about_h2_isnt': 'Чего это не',
        'about_h2_how': 'Как это работает изнутри',
        'about_h2_l10n': 'Локализация — 17 языков, нативный таргетинг ключевых слов',
        'about_h2_roadmap': 'Дорожная карта',
        'about_h2_contact': 'Контакты',
        'footer_privacy': 'Политика конфиденциальности',
        'footer_terms': 'Условия использования',
    },
}

# --- Tier 2 (SEO-critical only): 9 languages -------------------------------
# For these, only the title/meta/nav/free-tag are localized. Body
# content stays in English.

TIER2 = {
    'zh': {
        'title': 'TikTok 用户名生成器 — Handle',
        'meta_desc': '免费 TikTok 用户名生成器。输入关键词,选择领域和风格,获得 10-20 个符合 TikTok 规则的用户名创意,并检查 TikTok 上的可用性。无需注册,无使用限制。',
        'og_title': 'TikTok 用户名生成器 — Handle',
        'og_desc': '免费 TikTok 用户名生成器,带实时可用性检查。17 种风格,17 个领域,无需注册。',
        'nav_home': '首页', 'nav_generator': '生成器', 'nav_faq': '常见问题', 'nav_about': '关于', 'nav_cta': '打开工具',
        'faq_h2_picking': '选择 TikTok 用户名', 'faq_h2_check': '可用性检查如何工作',
        'faq_h2_styles': '名字、风格和趋势', 'faq_h2_legal': '账户、法律和支持',
        'faq_q1': '我的 TikTok 用户名应该是什么？', 'faq_q2': '如何选择适合我的 TikTok 用户名？',
        'faq_q3': '为什么我的 TikTok 名字已经被注册？', 'faq_q4': '什么样的 TikTok 用户名算好？',
        'faq_q5': '如何更改我的 TikTok 用户名？', 'faq_q6': 'TikTok 用户名和展示名有什么区别？',
        'faq_q7': '我怎么知道一个 TikTok 用户名是否可用？', 'faq_q8': '可用性检查是如何工作的？',
        'faq_q9': '为什么显示"可能可用"而不是直接"可用"？', 'faq_q10': '为什么一个用户名在结果列表中显示"未知"？',
        'faq_q11': '2026 年最好的 TikTok 用户名是什么？', 'faq_q12': '什么是简短的 TikTok 用户名，为什么长度很重要？',
        'faq_q13': '最好的美、酷、搞笑、锐利的 TikTok 用户名是什么？', 'faq_q14': '我能在我的 @handle 中使用 TikTok 字体吗？',
        'faq_q15': '生成器也适用于其他平台吗？', 'faq_q16': '我可以商业使用 Handle 生成的名字吗？',
        'faq_q17': 'Handle 是免费的吗？', 'faq_q18': 'Handle 与 TikTok 有关联吗？',
        'about_h2_what': '这是什么', 'about_h2_isnt': '这不是什么',
        'about_h2_how': '内部如何工作', 'about_h2_l10n': '本地化 — 17 种语言,本地关键词定位',
        'about_h2_roadmap': '路线图', 'about_h2_contact': '联系方式',
        'footer_privacy': '隐私政策',
        'footer_terms': '服务条款',
    },
    'vi': {
        'title': 'Trình Tạo Tên TikTok — Handle',
        'meta_desc': 'Trình tạo tên người dùng TikTok miễn phí. Nhập từ khóa, chọn ngách và phong cách, nhận 10-20 ý tưởng tên tuân thủ quy tắc TikTok và kiểm tra tính khả dụng trên TikTok. Không cần đăng ký, không giới hạn.',
        'og_title': 'Trình Tạo Tên TikTok — Handle',
        'og_desc': 'Trình tạo tên người dùng TikTok miễn phí với kiểm tra tính khả dụng trực tiếp. 17 phong cách, 17 ngách, không cần đăng ký.',
        'nav_home': 'Trang chủ', 'nav_generator': 'Trình tạo', 'nav_faq': 'Câu hỏi', 'nav_about': 'Giới thiệu', 'nav_cta': 'Mở công cụ',
        'faq_h2_picking': 'Chọn tên TikTok', 'faq_h2_check': 'Kiểm tra tính khả dụng hoạt động thế nào',
        'faq_h2_styles': 'Tên, phong cách và xu hướng', 'faq_h2_legal': 'Tài khoản, pháp lý và hỗ trợ',
        'faq_q1': 'Tên người dùng TikTok của tôi nên là gì?', 'faq_q2': 'Làm sao chọn tên TikTok phù hợp với tôi?',
        'faq_q3': 'Tại sao tên TikTok của tôi đã bị lấy?', 'faq_q4': 'Điều gì tạo nên một tên TikTok tốt?',
        'faq_q5': 'Làm sao đổi tên người dùng TikTok của tôi?', 'faq_q6': 'Sự khác biệt giữa tên người dùng và tên hiển thị trên TikTok?',
        'faq_q7': 'Làm sao biết tên TikTok còn trống?', 'faq_q8': 'Kiểm tra tính khả dụng hoạt động thế nào?',
        'faq_q9': 'Tại sao ghi "Có thể khả dụng" thay vì chỉ "Khả dụng"?', 'faq_q10': 'Tại sao một handle hiển thị "Không rõ" trong kết quả?',
        'faq_q11': 'Những tên TikTok nào tốt nhất năm 2026?', 'faq_q12': 'Tên TikTok ngắn là gì và tại sao độ dài quan trọng?',
        'faq_q13': 'Những tên TikTok thẩm mỹ, ngầu, hài hước và sắc bén nhất?', 'faq_q14': 'Tôi có thể dùng phông chữ TikTok trong @handle không?',
        'faq_q15': 'Trình tạo có hoạt động cho nền tảng khác không?', 'faq_q16': 'Tôi có thể dùng tên Handle tạo ra cho mục đích thương mại không?',
        'faq_q17': 'Handle có miễn phí không?', 'faq_q18': 'Handle có liên kết với TikTok không?',
        'about_h2_what': 'Đây là gì', 'about_h2_isnt': 'Đây không phải là gì',
        'about_h2_how': 'Cách hoạt động bên trong', 'about_h2_l10n': 'Bản địa hóa — 17 ngôn ngữ, nhắm mục tiêu từ khóa bản địa',
        'about_h2_roadmap': 'Lộ trình', 'about_h2_contact': 'Liên hệ',
        'footer_privacy': 'Chính sách bảo mật',
        'footer_terms': 'Điều khoản dịch vụ',
    },
    'id': {
        'title': 'Generator Nama TikTok — Handle',
        'meta_desc': 'Generator nama pengguna TikTok gratis. Ketik kata kunci, pilih niche dan vibe, dapatkan 10-20 ide nama yang sesuai aturan TikTok dan periksa ketersediaan di TikTok. Tanpa daftar, tanpa batas.',
        'og_title': 'Generator Nama TikTok — Handle',
        'og_desc': 'Generator nama pengguna TikTok gratis dengan pengecekan ketersediaan langsung. 17 vibe, 17 niche, tanpa daftar.',
        'nav_home': 'Beranda', 'nav_generator': 'Generator', 'nav_faq': 'FAQ', 'nav_about': 'Tentang', 'nav_cta': 'Buka alat',
        'faq_h2_picking': 'Memilih nama TikTok', 'faq_h2_check': 'Cara kerja pengecekan ketersediaan',
        'faq_h2_styles': 'Nama, gaya, dan tren', 'faq_h2_legal': 'Akun, hukum, dan dukungan',
        'faq_q1': 'Apa seharusnya nama pengguna TikTok saya?', 'faq_q2': 'Bagaimana cara memilih nama TikTok yang cocok untuk saya?',
        'faq_q3': 'Mengapa nama TikTok saya sudah dipakai?', 'faq_q4': 'Apa yang membuat nama TikTok bagus?',
        'faq_q5': 'Bagaimana cara mengganti nama pengguna TikTok saya?', 'faq_q6': 'Apa perbedaan antara nama pengguna dan nama tampilan di TikTok?',
        'faq_q7': 'Bagaimana saya tahu nama TikTok itu tersedia?', 'faq_q8': 'Bagaimana cara kerja pengecekan ketersediaan?',
        'faq_q9': 'Kenapa tertulis "Kemungkinan tersedia" alih-alih hanya "Tersedia"?', 'faq_q10': 'Kenapa sebuah handle muncul sebagai "Tidak diketahui" di daftar hasil?',
        'faq_q11': 'Apa nama TikTok terbaik untuk 2026?', 'faq_q12': 'Apa itu nama TikTok pendek, dan mengapa panjang penting?',
        'faq_q13': 'Apa nama TikTok aesthetic, keren, lucu, dan edgy terbaik?', 'faq_q14': 'Bisakah saya menggunakan font TikTok di @handle saya?',
        'faq_q15': 'Apakah generator bekerja untuk platform lain juga?', 'faq_q16': 'Bisakah saya menggunakan nama yang dibuat Handle secara komersial?',
        'faq_q17': 'Apakah Handle gratis?', 'faq_q18': 'Apakah Handle berafiliasi dengan TikTok?',
        'about_h2_what': 'Apa ini', 'about_h2_isnt': 'Apa ini bukan',
        'about_h2_how': 'Cara kerja di balik layar', 'about_h2_l10n': 'Lokalisasi — 17 bahasa, targeting kata kunci asli',
        'about_h2_roadmap': 'Peta jalan', 'about_h2_contact': 'Kontak',
        'footer_privacy': 'Kebijakan privasi',
        'footer_terms': 'Ketentuan layanan',
    },
    'ms': {
        'title': 'Penjana Nama TikTok — Handle',
        'meta_desc': 'Penjana nama pengguna TikTok percuma. Taip kata kunci, pilih niche dan gaya, dapat 10-20 idea nama yang mematuhi peraturan TikTok dan periksa ketersediaan di TikTok. Tanpa daftar, tanpa had.',
        'og_title': 'Penjana Nama TikTok — Handle',
        'og_desc': 'Penjana nama pengguna TikTok percuma dengan pemeriksaan ketersediaan secara langsung. 17 gaya, 17 niche, tanpa daftar.',
        'nav_home': 'Laman utama', 'nav_generator': 'Penjana', 'nav_faq': 'Soalan', 'nav_about': 'Tentang', 'nav_cta': 'Buka alat',
        'faq_h2_picking': 'Memilih nama TikTok', 'faq_h2_check': 'Cara pemeriksaan ketersediaan berfungsi',
        'faq_h2_styles': 'Nama, gaya dan trend', 'faq_h2_legal': 'Akaun, undang-undang dan sokongan',
        'faq_q1': 'Apakah seharusnya nama pengguna TikTok saya?', 'faq_q2': 'Bagaimana cara memilih nama TikTok yang sesuai dengan saya?',
        'faq_q3': 'Mengapa nama TikTok saya sudah diambil?', 'faq_q4': 'Apa yang menjadikan nama TikTok yang bagus?',
        'faq_q5': 'Bagaimana cara menukar nama pengguna TikTok saya?', 'faq_q6': 'Apakah perbezaan antara nama pengguna dan nama paparan di TikTok?',
        'faq_q7': 'Bagaimana saya tahu nama TikTok itu tersedia?', 'faq_q8': 'Bagaimana cara pemeriksaan ketersediaan berfungsi?',
        'faq_q9': 'Mengapa ia tertulis "Kemungkinan tersedia" dan bukan hanya "Tersedia"?', 'faq_q10': 'Mengapa handle muncul sebagai "Tidak diketahui" dalam senarai keputusan?',
        'faq_q11': 'Apakah nama TikTok terbaik untuk 2026?', 'faq_q12': 'Apakah nama TikTok pendek dan mengapa panjang penting?',
        'faq_q13': 'Apakah nama TikTok estetik, keren, kelakar dan edgy terbaik?', 'faq_q14': 'Bolehkah saya menggunakan fon TikTok dalam @handle saya?',
        'faq_q15': 'Adakah penjana berfungsi untuk platform lain juga?', 'faq_q16': 'Bolehkah saya menggunakan nama yang dijana oleh Handle secara komersial?',
        'faq_q17': 'Adakah Handle percuma?', 'faq_q18': 'Adakah Handle berafiliasi dengan TikTok?',
        'about_h2_what': 'Apa ini', 'about_h2_isnt': 'Apa ini bukan',
        'about_h2_how': 'Bagaimana ia berfungsi di sebaliknya', 'about_h2_l10n': 'Penyetempatan — 17 bahasa, penargetan kata kunci asli',
        'about_h2_roadmap': 'Peta jalan', 'about_h2_contact': 'Hubungi',
        'footer_privacy': 'Dasar privasi',
        'footer_terms': 'Terma perkhidmatan',
    },
    'tl': {
        'title': 'Tagagawa ng Pangalan sa TikTok — Handle',
        'meta_desc': 'Libreng tagagawa ng username sa TikTok. Mag-type ng keyword, pumili ng niche at vibe, makakakuha ng 10-20 ideya na sumusunod sa mga patakaran ng TikTok at suriin ang availability sa TikTok. Walang signup, walang limitasyon.',
        'og_title': 'Tagagawa ng Pangalan sa TikTok — Handle',
        'og_desc': 'Libreng tagagawa ng username sa TikTok na may live availability check. 17 vibes, 17 niches, walang signup.',
        'nav_home': 'Home', 'nav_generator': 'Tagagawa', 'nav_faq': 'Mga Tanong', 'nav_about': 'Tungkol', 'nav_cta': 'Buksan ang tool',
        'faq_h2_picking': 'Pumili ng pangalan sa TikTok', 'faq_h2_check': 'Paano gumagana ang availability check',
        'faq_h2_styles': 'Mga pangalan, estilo, at uso', 'faq_h2_legal': 'Account, legal, at suporta',
        'faq_q1': 'Ano dapat ang TikTok username ko?', 'faq_q2': 'Paano pumili ng TikTok username na bagay sa akin?',
        'faq_q3': 'Bakit nakuha na ang TikTok name ko?', 'faq_q4': 'Ano ang nagpapa-bute ng isang TikTok username?',
        'faq_q5': 'Paano palitan ang TikTok username ko?', 'faq_q6': 'Ano ang pagkakaiba ng username at display name sa TikTok?',
        'faq_q7': 'Paano ko malalaman kung available ang TikTok username?', 'faq_q8': 'Paano gumagana ang availability check?',
        'faq_q9': 'Bakit nakasulat "Likely available" sa halip na "Available" lang?', 'faq_q10': 'Bakit nagpapakita ang isang handle bilang "Unknown" sa listahan ng resulta?',
        'faq_q11': 'Ano ang pinakamagandang TikTok username para sa 2026?', 'faq_q12': 'Ano ang maikling TikTok username at bakit mahalaga ang haba?',
        'faq_q13': 'Ano ang pinakamagandang aesthetic, cool, nakakatawa, at edgy TikTok username?', 'faq_q14': 'Pwede ko bang gamitin ang TikTok fonts sa @handle ko?',
        'faq_q15': 'Gumagana ba ang generator sa ibang platforms?', 'faq_q16': 'Pwede ko bang gamitin ang mga pangalang gawa ng Handle para sa commercial?',
        'faq_q17': 'Libre ba ang Handle?', 'faq_q18': 'Kaakibat ba ang Handle sa TikTok?',
        'about_h2_what': 'Ano ito', 'about_h2_isnt': 'Ano ito hindi',
        'about_h2_how': 'Paano gumagana sa ilalim', 'about_h2_l10n': 'Lokalizasyon — 17 wika, native keyword targeting',
        'about_h2_roadmap': 'Fahrplan', 'about_h2_contact': 'Contact',
        'footer_privacy': 'Patakaran sa privacy',
        'footer_terms': 'Mga Tuntunin ng Serbisyo',
    },
    'hi': {
        'title': 'TikTok यूजरनेम जनरेटर — Handle',
        'meta_desc': 'मुफ्त TikTok यूजरनेम जनरेटर। एक कीवर्ड टाइप करें, एक निश और एक वाइब चुनें, 10-20 अनूठे TikTok यूजरनेम विचार प्राप्त करें जो TikTok के नियमों का पालन करते हैं, और TikTok पर उपलब्धता जांचें। कोई साइनअप नहीं, कोई सीमा नहीं।',
        'og_title': 'TikTok यूजरनेम जनरेटर — Handle',
        'og_desc': 'मुफ्त TikTok यूजरनेम जनरेटर जिसमें लाइव उपलब्धता जांच है। 17 वाइब, 17 निश, कोई साइनअप नहीं।',
        'nav_home': 'होम', 'nav_generator': 'जनरेटर', 'nav_faq': 'सवाल', 'nav_about': 'बारे में', 'nav_cta': 'टूल खोलें',
        'faq_h2_picking': 'TikTok यूजरनेम चुनना', 'faq_h2_check': 'उपलब्धता जांच कैसे काम करती है',
        'faq_h2_styles': 'नाम, स्टाइल और ट्रेंड', 'faq_h2_legal': 'खाता, कानूनी और सहायता',
        'faq_q1': 'मेरा TikTok यूजरनेम क्या होना चाहिए?', 'faq_q2': 'मैं अपने लिए सही TikTok यूजरनेम कैसे चुनूं?',
        'faq_q3': 'मेरा TikTok नाम पहले से क्यों लिया जा चुका है?', 'faq_q4': 'अच्छा TikTok यूजरनेम क्या बनाता है?',
        'faq_q5': 'मैं अपना TikTok यूजरनेम कैसे बदलूं?', 'faq_q6': 'TikTok यूजरनेम और डिस्प्ले नाम में क्या अंतर है?',
        'faq_q7': 'मुझे कैसे पता चलेगा कि TikTok यूजरनेम उपलब्ध है?', 'faq_q8': 'उपलब्धता जांच कैसे काम करती है?',
        'faq_q9': '"संभवतः उपलब्ध" क्यों लिखा है, सिर्फ "उपलब्ध" क्यों नहीं?', 'faq_q10': 'एक हैंडल परिणाम सूची में "अज्ञात" क्यों दिखाता है?',
        'faq_q11': '2026 के लिए सबसे अच्छे TikTok यूजरनेम क्या हैं?', 'faq_q12': 'छोटा TikTok यूजरनेम क्या है और लंबाई क्यों मायने रखती है?',
        'faq_q13': 'सबसे अच्छे सौंदर्य, कूल, मज़ेदार और धार वाले TikTok यूजरनेम क्या हैं?', 'faq_q14': 'क्या मैं अपने @handle में TikTok फ़ॉन्ट्स का उपयोग कर सकता हूं?',
        'faq_q15': 'क्या जनरेटर अन्य प्लेटफ़ॉर्म के लिए भी काम करता है?', 'faq_q16': 'क्या मैं Handle द्वारा जेनरेट किए गए नामों का व्यावसायिक रूप से उपयोग कर सकता हूं?',
        'faq_q17': 'क्या Handle मुफ्त है?', 'faq_q18': 'क्या Handle TikTok से संबद्ध है?',
        'about_h2_what': 'यह क्या है', 'about_h2_isnt': 'यह क्या नहीं है',
        'about_h2_how': 'अंदर से कैसे काम करता है', 'about_h2_l10n': 'स्थानीयकरण — 17 भाषाएं, मूल कीवर्ड लक्ष्यीकरण',
        'about_h2_roadmap': 'रोडमैप', 'about_h2_contact': 'संपर्क',
        'footer_privacy': 'गोपनीयता नीति',
        'footer_terms': 'सेवा की शर्तें',
    },
    'bn': {
        'title': 'TikTok ইউজারনেম জেনারেটর — Handle',
        'meta_desc': 'বিনামূল্যে TikTok ইউজারনেম জেনারেটর। একটি কীওয়ার্ড টাইপ করুন, একটি নিশ এবং একটি ভাইব নির্বাচন করুন, 10-20টি অনন্য TikTok ইউজারনেম আইডিয়া পান যা TikTok-এর নিয়ম মেনে চলে এবং TikTok-তে প্রাপ্যতা পরীক্ষা করুন। কোনো সাইনআপ নেই, কোনো সীমা নেই।',
        'og_title': 'TikTok ইউজারনেম জেনারেটর — Handle',
        'og_desc': 'বিনামূল্যে TikTok ইউজারনেম জেনারেটর লাইভ প্রাপ্যতা পরীক্ষা সহ। 17টি ভাইব, 17টি নিশ, কোনো সাইনআপ নেই।',
        'nav_home': 'হোম', 'nav_generator': 'জেনারেটর', 'nav_faq': 'প্রশ্ন', 'nav_about': 'সম্পর্কে', 'nav_cta': 'টুল খুলুন',
        'faq_h2_picking': 'TikTok ইউজারনেম নির্বাচন', 'faq_h2_check': 'প্রাপ্যতা পরীক্ষা কিভাবে কাজ করে',
        'faq_h2_styles': 'নাম, স্টাইল এবং প্রবণতা', 'faq_h2_legal': 'অ্যাকাউন্ট, আইনি এবং সহায়তা',
        'faq_q1': 'আমার TikTok ইউজারনেম কী হওয়া উচিত?', 'faq_q2': 'আমার জন্য উপযুক্ত TikTok ইউজারনেম কীভাবে বাছাই করব?',
        'faq_q3': 'আমার TikTok নাম ইতিমধ্যে কেন নেওয়া হয়েছে?', 'faq_q4': 'একটি ভালো TikTok ইউজারনেমের গুণ কী?',
        'faq_q5': 'আমার TikTok ইউজারনেম কীভাবে পরিবর্তন করব?', 'faq_q6': 'TikTok ইউজারনেম এবং ডিসপ্লে নামের মধ্যে পার্থক্য কী?',
        'faq_q7': 'আমি কীভাবে জানব যে একটি TikTok ইউজারনেম উপলব্ধ?', 'faq_q8': 'প্রাপ্যতা পরীক্ষা কিভাবে কাজ করে?',
        'faq_q9': 'শুধু "উপলব্ধ" এর বদলে "সম্ভবত উপলব্ধ" কেন বলা হয়?', 'faq_q10': 'একটি হ্যান্ডল ফলাফল তালিকায় "অজানা" কেন দেখায়?',
        'faq_q11': '2026-এর জন্য সেরা TikTok ইউজারনেমগুলি কী কী?', 'faq_q12': 'একটি ছোট TikTok ইউজারনেম কী এবং দৈর্ঘ্য কেন গুরুত্বপূর্ণ?',
        'faq_q13': 'সেরা নান্দনিক, কুল, মজার এবং ধারালো TikTok ইউজারনেমগুলি কী কী?', 'faq_q14': 'আমি কি আমার @handle-এ TikTok ফন্ট ব্যবহার করতে পারি?',
        'faq_q15': 'জেনারেটর কি অন্যান্য প্ল্যাটফর্মের জন্যও কাজ করে?', 'faq_q16': 'আমি কি Handle দ্বারা তৈরি নামগুলি বাণিজ্যিকভাবে ব্যবহার করতে পারি?',
        'faq_q17': 'Handle কি বিনামূল্যে?', 'faq_q18': 'Handle কি TikTok-এর সাথে অনুমোদিত?',
        'about_h2_what': 'এটি কী', 'about_h2_isnt': 'এটি কী নয়',
        'about_h2_how': 'ভেতরে কীভাবে কাজ করে', 'about_h2_l10n': 'স্থানীয়করণ — 17টি ভাষা, নেটিভ কীওয়ার্ড টার্গেটিং',
        'about_h2_roadmap': 'রোডম্যাপ', 'about_h2_contact': 'যোগাযোগ',
        'footer_privacy': 'গোপনীয়তা নীতি',
        'footer_terms': 'পরিষেবার শর্তাবলী',
    },
    'ur': {
        'title': 'TikTok یوزر نیم جنریٹر — Handle',
        'meta_desc': 'مفت TikTok یوزر نیم جنریٹر۔ ایک کلیدی لفظ ٹائپ کریں، ایک نچ اور ایک وائب منتخب کریں، 10-20 انوکھے TikTok یوزر نیم آئیڈیاز حاصل کریں جو TikTok کے قوانین کی پیروی کرتے ہیں، اور TikTok پر دستیابی چیک کریں۔ کوئی سائن اپ نہیں، کوئی حد نہیں۔',
        'og_title': 'TikTok یوزر نیم جنریٹر — Handle',
        'og_desc': 'مفت TikTok یوزر نیم جنریٹر لائیو دستیابی کی جانچ کے ساتھ۔ 17 وائب، 17 نچ، کوئی سائن اپ نہیں۔',
        'nav_home': 'ہوم', 'nav_generator': 'جنریٹر', 'nav_faq': 'سوالات', 'nav_about': 'متعلق', 'nav_cta': 'ٹول کھولیں',
        'faq_h2_picking': 'TikTok یوزر نیم کا انتخاب', 'faq_h2_check': 'دستیابی کی جانچ کیسے کام کرتی ہے',
        'faq_h2_styles': 'نام، اسٹائل اور رجحانات', 'faq_h2_legal': 'اکاؤنٹ، قانونی اور معاونت',
        'faq_q1': 'میرا TikTok یوزر نیم کیا ہونا چاہیے؟', 'faq_q2': 'میں اپنے لیے موزوں TikTok یوزر نیم کیسے چنوں؟',
        'faq_q3': 'میرا TikTok نام پہلے سے کیوں لیا جا چکا ہے؟', 'faq_q4': 'اچھا TikTok یوزر نیم کیا بناتا ہے؟',
        'faq_q5': 'میں اپنا TikTok یوزر نیم کیسے تبدیل کروں؟', 'faq_q6': 'TikTok یوزر نیم اور ڈسپلے نام میں کیا فرق ہے؟',
        'faq_q7': 'مجھے کیسے پتا چلے گا کہ TikTok یوزر نیم دستیاب ہے؟', 'faq_q8': 'دستیابی کی جانچ کیسے کام کرتی ہے؟',
        'faq_q9': 'صرف "دستیاب" کی بجائے "ممکنہ طور پر دستیاب" کیوں لکھا ہے؟', 'faq_q10': 'ایک ہینڈل نتائج کی فہرست میں "نامعلوم" کیوں دکھاتا ہے؟',
        'faq_q11': '2026 کے لیے بہترین TikTok یوزر نیم کیا ہیں؟', 'faq_q12': 'مختصر TikTok یوزر نیم کیا ہے اور لمبائی کیوں اہم ہے؟',
        'faq_q13': 'بہترین خوبصورت، کول، مزاحیہ اور تیز TikTok یوزر نیم کیا ہیں؟', 'faq_q14': 'کیا میں اپنے @handle میں TikTok فونٹس استعمال کر سکتا ہوں؟',
        'faq_q15': 'کیا جنریٹر دوسرے پلیٹ فارمز کے لیے بھی کام کرتا ہے؟', 'faq_q16': 'کیا میں Handle کے بنائے گئے ناموں کو تجارتی طور پر استعمال کر سکتا ہوں؟',
        'faq_q17': 'کیا Handle مفت ہے؟', 'faq_q18': 'کیا Handle TikTok سے وابستہ ہے؟',
        'about_h2_what': 'یہ کیا ہے', 'about_h2_isnt': 'یہ کیا نہیں ہے',
        'about_h2_how': 'اندر سے کیسے کام کرتا ہے', 'about_h2_l10n': 'مقامی نوعیت — 17 زبانیں، مقامی کلیدی الفاظ کا ہدف',
        'about_h2_roadmap': 'سڑک کا نقشہ', 'about_h2_contact': 'رابطہ',
        'footer_privacy': 'رازداری کی پالیسی',
        'footer_terms': 'سروس کی شرائط',
    },
    'ar': {
        'title': 'مولد أسماء تيك توك — Handle',
        'meta_desc': 'مولد أسماء مستخدمين تيك توك مجاني. اكتب كلمة مفتاحية، اختر مجالاً وأسلوباً، احصل على 10-20 فكرة اسم مستخدم فريدة تتبع قواعد تيك توك وتحقق من التوفر على تيك توك. بدون تسجيل، بدون حدود.',
        'og_title': 'مولد أسماء تيك توك — Handle',
        'og_desc': 'مولد أسماء مستخدمين تيك توك مجاني مع تحقق مباشر من التوفر على تيك توك. 17 أسلوباً، 17 مجالاً، بدون تسجيل.',
        'nav_home': 'الرئيسية', 'nav_generator': 'المولد', 'nav_faq': 'أسئلة', 'nav_about': 'حول', 'nav_cta': 'افتح الأداة',
        # FAQ H2/H3 + About H2
        'faq_h2_picking': 'اختيار اسم تيك توك',
        'faq_h2_check': 'كيف يعمل التحقق من التوفر',
        'faq_h2_styles': 'الأسماء والأساليب والاتجاهات',
        'faq_h2_legal': 'الحساب والقانوني والدعم',
        'faq_q1': 'ما الذي يجب أن يكون عليه اسم مستخدم تيك توك الخاص بي؟',
        'faq_q2': 'كيف أختار اسم تيك توك يناسبني؟',
        'faq_q3': 'لماذا اسم تيك توك الخاص بي محجوز بالفعل؟',
        'faq_q4': 'ما الذي يجعل اسم تيك توك جيدًا؟',
        'faq_q5': 'كيف أغير اسم تيك توك الخاص بي؟',
        'faq_q6': 'ما الفرق بين اسم المستخدم واسم العرض في تيك توك؟',
        'faq_q7': 'كيف أعرف إذا كان اسم تيك توك متاحًا؟',
        'faq_q8': 'كيف يعمل التحقق من التوفر؟',
        'faq_q9': 'لماذا يقول "متاح على الأرجح" بدلاً من "متاح" فقط؟',
        'faq_q10': 'لماذا يظهر المقبض كـ "غير معروف" في قائمة النتائج؟',
        'faq_q11': 'ما هي أفضل أسماء تيك توك لعام 2026؟',
        'faq_q12': 'ما هو اسم تيك توك القصير، ولماذا طول الاسم مهم؟',
        'faq_q13': 'ما هي أفضل أسماء تيك توك الجميلة والرائعة والمضحكة والحادّة؟',
        'faq_q14': 'هل يمكنني استخدام خطوط تيك توك في @handle الخاص بي؟',
        'faq_q15': 'هل يعمل المولد لمنصات أخرى أيضًا؟',
        'faq_q16': 'هل يمكنني استخدام الأسماء التي ينشئها Handle تجاريًا؟',
        'faq_q17': 'هل Handle مجاني؟',
        'faq_q18': 'هل Handle منتسب إلى تيك توك؟',
        'about_h2_what': 'ما هذا',
        'about_h2_isnt': 'ما ليس هذا',
        'about_h2_how': 'كيف يعمل من الداخل',
        'about_h2_l10n': 'التوطين — 17 لغة، استهداف محلي للكلمات المفتاحية',
        'about_h2_roadmap': 'خارطة الطريق',
        'about_h2_contact': 'اتصل بنا',
        'footer_privacy': 'سياسة الخصوصية',
        'footer_terms': 'شروط الخدمة',
    },
}


# --- Build -----------------------------------------------------------------

def localize(html, lang, loc, tr, is_tier1):
    out = html

    # 0. Locale-researched SEO overrides the per-language dict's title/meta/og
    # so we use real keyword-targeted copy, not just translated English.
    if lang in SEO:
        tr = dict(tr)
        tr['title'] = SEO[lang]['title']
        tr['meta_desc'] = SEO[lang]['meta_desc']
        tr['og_title'] = SEO[lang]['og_title']
        tr['og_desc'] = SEO[lang]['og_desc']

    # 0b. New full-page translations (page H1, lede, home H2 SEO blocks,
    # privacy H2 + body, terms H2 + body, 404 H2 + body). These are
    # independent of TIER1/TIER2 — they exist for all 17 langs.
    if lang in PAGES_TRANSLATIONS:
        tr = dict(tr)
        tr.update(PAGES_TRANSLATIONS[lang])

    # 0c. v15 expanded Privacy Policy (AdSense, GDPR, CCPA, children, IP
    # rate-limiting, contact) and Terms (governing law + contact). These
    # are kept in a separate file to keep build.py readable.
    try:
        from legal_translations_filled import PRIVACY as LEGAL_PRIVACY, TERMS as LEGAL_TERMS
        if lang in LEGAL_PRIVACY:
            tr.update(LEGAL_PRIVACY[lang])
        if lang in LEGAL_TERMS:
            tr.update(LEGAL_TERMS[lang])
    except (ImportError, SyntaxError) as e:
        # File may not exist yet if running build before sub-agent finishes
        pass

    # 0d. v18 About page Contact paragraph (replaces the legacy
    # "PLACEHOLDER. Add an email address..." line in the source HTML)
    try:
        from about_contact_translations import ABOUT_CONTACT
        if lang in ABOUT_CONTACT:
            tr['about_contact_p'] = ABOUT_CONTACT[lang]
    except (ImportError, SyntaxError):
        pass

    # 1. <html lang="...">
    html_lang = loc.get('lang', lang)
    if loc.get('dir') == 'rtl':
        # RTL languages: ensure dir attribute is set
        out = re.sub(
            r'<html lang="[a-z-]+"',
            f'<html lang="{html_lang}" dir="rtl"',
            out,
            count=1,
        )
    else:
        out = re.sub(
            r'<html lang="[a-z-]+"',
            f'<html lang="{html_lang}"',
            out,
            count=1,
        )

    # 2. <title>
    if tr.get('title'):
        out = re.sub(
            r'<title>[^<]*</title>',
            f'<title>{escape(tr["title"])}</title>',
            out,
            count=1,
        )

    # 3. meta description
    if tr.get('meta_desc'):
        out = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{escape_attr(tr["meta_desc"])}">',
            out,
            count=1,
        )

    # 4. og:title, og:description, og:locale
    if tr.get('og_title'):
        out = re.sub(
            r'<meta property="og:title" content="[^"]*">',
            f'<meta property="og:title" content="{escape_attr(tr["og_title"])}">',
            out,
            count=1,
        )
    if tr.get('og_desc'):
        out = re.sub(
            r'<meta property="og:description" content="[^"]*">',
            f'<meta property="og:description" content="{escape_attr(tr["og_desc"])}">',
            out,
            count=1,
        )
    if loc.get('og_locale'):
        out = re.sub(
            r'<meta property="og:locale" content="[^"]*">',
            f'<meta property="og:locale" content="{loc["og_locale"]}">',
            out,
            count=1,
        )

    # 5. canonical
    out = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="/{lang}/">',
        out,
        count=1,
    )

    # 6. Hreflang alternates — keep them but add the localized one
    if is_tier1 and tr.get('titles'):
        # Insert a separate <script> block with the TITLES object right
        # BEFORE the existing inline route-detect script. The original
        # script is left fully intact (so its SHA-256 hash stays valid
        # across all locales). The regex matches the opening <script>
        # tag plus the (function () line, and we re-emit them in the
        # same order, just with a new script block prepended.
        titles_json = json.dumps(tr['titles'], ensure_ascii=False)
        out = re.sub(
            r'(  <script>)\n(\s*)\(function \(\) \{',
            f'  <script>window.__handleTitles = {titles_json};</script>\n\n\\1\n\\2(function () {{',
            out,
            count=1,
        )

    # 7. Nav labels (only for tier 1; tier 2 has nav_home etc. in the
    # dict but we don't translate because we'd need to know exactly where
    # each English string is in the nav and risk collision with the lang
    # switcher text.)
    # Actually for both tiers, the nav has these labels in the source
    # HTML. For both tiers we want to translate them. Use exact-match
    # string replacement on the nav block.
    nav_block_re = re.compile(
        r'(<nav class="nav" aria-label="Primary">)(.*?)(</nav>)',
        re.DOTALL,
    )
    nav_m = nav_block_re.search(out)
    if nav_m:
        nav_inner = nav_m.group(2)
        nav_inner = nav_inner.replace('>Home<', f'>{tr.get("nav_home", "Home")}<')
        nav_inner = nav_inner.replace('>Generator<', f'>{tr.get("nav_generator", "Generator")}<')
        nav_inner = nav_inner.replace('>FAQ<', f'>{tr.get("nav_faq", "FAQ")}<')
        nav_inner = nav_inner.replace('>About<', f'>{tr.get("nav_about", "About")}<')
        # Update data-nav hrefs to be locale-prefixed so the static
        # HTML (before JS runs and the router takes over) has working
        # hover hints and crawler-friendly links.
        home_prefix = '/' if lang == 'en' else f'/{lang}'
        nav_inner = re.sub(
            r'href="(/[a-z]*)?" data-nav="home"',
            f'href="{home_prefix}/" data-nav="home"',
            nav_inner,
        )
        nav_inner = re.sub(
            r'href="/generator"',
            f'href="{home_prefix}/generator"',
            nav_inner,
        )
        nav_inner = re.sub(
            r'href="/faq"',
            f'href="{home_prefix}/faq"',
            nav_inner,
        )
        nav_inner = re.sub(
            r'href="/about"',
            f'href="{home_prefix}/about"',
            nav_inner,
        )
        out = out[:nav_m.start()] + nav_m.group(1) + nav_inner + nav_m.group(3) + out[nav_m.end():]

    # 8. Nav CTA ("Open the tool")
    cta_re = re.compile(
        r'(<a class="nav-cta"[^>]*>)([^<]+)(</a>)',
    )
    out = cta_re.sub(
        lambda m: m.group(1) + escape(tr.get("nav_cta", "Open the tool")) + m.group(3),
        out,
        count=1,
    )
    # Also update the CTA href to be locale-prefixed.
    home_prefix = '/' if lang == 'en' else f'/{lang}'
    out = re.sub(
        r'(<a class="nav-cta" href=")/generator"',
        rf'\1{home_prefix}/generator"',
        out,
        count=1,
    )

    # 9. Apply new full-page translations (all 17 langs, no tier split).
    # Includes: home h1 + lede, gen h1 + lede, 404 h1 + lede, faq h1 +
    # lede, about h1 + lede, privacy h1 + lede + 6 H2 + body, terms h1 +
    # lede + 10 H2 + body, home H2 SEO blocks + body, 404 H2 + 6 link
    # texts. These are the strings that were previously only translated
    # for Tier 1.
    if tr.get('home_h1'):
        out = out.replace(
            'Free TikTok username generator with a live availability check.',
            tr['home_h1'],
            1,
        )
    if tr.get('home_lede'):
        out = out.replace(
            'Type a keyword, pick a niche and a vibe, and get 10–20 unique TikTok username ideas that follow the current TikTok rules. Each one is checked live on TikTok so you know whether it is likely available before you copy it. No signup, no usage limits, no watermarks.',
            tr['home_lede'],
            1,
        )
    if tr.get('home_cta_primary'):
        out = out.replace(
            'Generate TikTok username ideas →',
            tr['home_cta_primary'],
            1,
        )
    if tr.get('home_cta_secondary'):
        out = re.sub(
            r'(<a class="btn-ghost" href="#how-it-works"[^>]*>)([^<]+)(</a>)',
            lambda m: m.group(1) + escape(tr['home_cta_secondary']) + m.group(3),
            out,
            count=1,
        )
    if tr.get('gen_h1'):
        out = out.replace(
            '<h1>TikTok username generator</h1>',
            f'<h1>{escape(tr["gen_h1"])}</h1>',
            1,
        )
    if tr.get('gen_lede'):
        out = out.replace(
            "Free TikTok username ideas in seconds. Type a keyword (your name, your niche, or any word that anchors the result), pick one of 17 content niches and one of 17 themed vibes, and the generator returns 10–20 unique handle suggestions that respect TikTok's current username rules. Each suggestion is then checked live for availability on TikTok, with a timestamp, and labelled \"Likely available\", \"Likely taken\", or \"Unknown\" so you know what you're copying before you claim it.",
            tr['gen_lede'],
            1,
        )
    if tr.get('faq_h1'):
        out = out.replace(
            'Frequently asked questions about the TikTok username generator',
            tr['faq_h1'],
            1,
        )
    if tr.get('faq_lede'):
        # faq_lede contains anchor tags — replace by exact match
        out = out.replace(
            "Short answers to the questions people actually search before picking a TikTok username: what the rules are, how the availability check works, why the verdict says \"Likely\" and not \"Available\", and how to find a name that fits you. For the long version see the <a href=\"/about\" data-nav=\"about\">About page</a>; for the legal side see <a href=\"/terms\" data-nav=\"terms\">Terms</a> and <a href=\"/privacy\" data-nav=\"privacy\">Privacy</a>.",
            tr['faq_lede'],
            1,
        )
    if tr.get('about_h1'):
        out = out.replace(
            'About Handle — a free TikTok username generator with a live availability check',
            tr['about_h1'],
            1,
        )
    if tr.get('about_lede'):
        out = out.replace(
            'Handle is a free tool for TikTok creators who want a username that actually exists. Type a keyword, pick a niche and a vibe, get 10–20 TikTok username ideas that follow the current rules, and see which are likely available on TikTok before you copy one. The whole tool is free, requires no signup, and is available in 17 languages.',
            tr['about_lede'],
            1,
        )
    if tr.get('about_contact_p'):
        out = out.replace(
            'Found a bug, want to suggest a feature, or just want to say hi? Write to us at <strong>hello@gethandlenames.com</strong> — we read everything and aim to respond within a week. For formal legal notices, takedown requests, or data-subject rights under GDPR/CCPA, write to <strong>legal@gethandlenames.com</strong> instead.',
            tr['about_contact_p'],
            1,
        )
    if tr.get('privacy_h1'):
        out = out.replace('<h1>Privacy Policy</h1>', f'<h1>{escape(tr["privacy_h1"])}</h1>', 1)
    if tr.get('terms_h1'):
        out = out.replace('<h1>Terms of Service</h1>', f'<h1>{escape(tr["terms_h1"])}</h1>', 1)
    # Note: privacy/terms lede paragraphs are translated via the new
    # `privacy_p_lede` key in the privacy_blocks list below (v15 expansion).
    # The legacy `privacy_lede` / `terms_lede` keys are now ignored —
    # they were tied to a "working draft" English string that's been
    # replaced with a proper lede.
    if tr.get('404_h1'):
        out = out.replace('404 — page not found', tr['404_h1'], 1)
    if tr.get('404_lede'):
        out = out.replace(
            "That URL doesn't match any of our pages. It might be a typo, or a link that points to an old version of the site.",
            tr['404_lede'],
            1,
        )

    # 9b. Home page H2 SEO blocks + body paragraphs (How to pick, Why
    # Handle, Trending). These were previously not translated for any
    # language.
    home_seo_blocks = [
        # (key, English source, escaped wrapper)
        ('home_h2_pick', 'How to pick a TikTok username that fits you', 'h2'),
        ('home_h2_why', 'Why Handle', 'h2'),
        ('home_h2_trending', 'Trending TikTok username ideas for 2026', 'h2'),
        ('home_h3_three_things', 'Three things the other TikTok name generators skip', 'h3'),
        ('home_pick_p1', "A good TikTok username is short, easy to say out loud, easy to spell from memory, and signals what your content is about. Handle handles the boring part: you type a keyword (your name, your niche, a vibe word), pick one of 17 niches and one of 17 themed vibes, and the generator returns 10–20 unique TikTok username ideas that respect TikTok's current rules — 2 to 24 characters, lowercase letters, numbers, periods, and underscores, no leading or trailing period, no consecutive periods.", 'p'),
        ('home_pick_p2', "Each idea is then run through a live availability check on TikTok, with a timestamp, and labelled \"Likely available\", \"Likely taken\", or \"Unknown\". The verdict is honest on purpose: a name can be free the moment we check it and taken the moment you try to claim it. If the check can't reach TikTok (a transient network blip, TikTok-side rate limit, or a private region), you'll see \"Unknown\" and a direct link to confirm by eye on TikTok itself.", 'p'),
        ('home_why_p1', "Most TikTok username generators stop at the list. You copy a name, open TikTok, and find out it's taken. Then you do it again. Then again. Handle closes that loop in three ways no other free tool does together.", 'p'),
        ('home_why_li1', "<strong>Live availability check on TikTok.</strong> Each generated handle is checked against TikTok's own profile endpoint before you see it. No more copying 12 names and finding out all of them are taken.", 'li'),
        ('home_why_li2', "<strong>Honest verdicts.</strong> \"Likely available\" with a timestamp beats a confident \"Available\" that is wrong by the time you click. We say \"Likely\" on purpose.", 'li'),
        ('home_why_li3', "<strong>Rules enforced up front.</strong> Every name follows TikTok's current character rules before it reaches you — no copying a 25-character handle just to find out TikTok won't accept it.", 'li'),
        ('home_why_li4', "<strong>17 themed vibes + 17 niches.</strong> Aesthetic, funny, professional, edgy, cute, mysterious, cool, chill, smart, romantic, powerful, gaming, techy, spooky, retro, wholesome, fantasy — each one shifts the prefix and suffix word pools so the ideas feel like the creator you're trying to be, not generic \"username123\" output.", 'li'),
        ('home_why_li5', "<strong>Available in 17 languages.</strong> The whole tool is localised for Spanish, French, German, Italian, Portuguese, Dutch, Polish, Russian, Chinese, Vietnamese, Indonesian, Malay, Tagalog, Hindi, Bengali, Arabic and Urdu — with locally-researched keyword targeting, not machine translation.", 'li'),
        ('home_trending_p1', "The 2026 TikTok username trends lean toward <strong>short, lowercase, single-word handles</strong> with a single stylistic flourish — a doubled letter (\"glowy\", \"serenee\"), a single-digit suffix, or one of the unicode font styles you can also generate here. Aesthetic and \"soft girl\" handles still rank for the lifestyle and beauty niches; gaming and tech handles are leaning harder into two-word combos (\"pixel.mode\", \"loot.drift\"). Use the generator with the <strong>unique</strong> or <strong>aesthetic</strong> vibe to see the current direction, and run the result through the font converter if you want the matching display name.", 'p'),
        ('home_trending_p2', "Coming up: a TikTok creator blog, programmatic niche pages, the cross-platform check (Instagram, YouTube, X), a weekly name-drop email, and social channels for name picks. Plan and trade-offs in the README.", 'p'),
    ]
    for key, en_src, tag in home_seo_blocks:
        loc_val = tr.get(key)
        if not loc_val:
            continue
        if tag == 'h2':
            out = out.replace(f'<h2>{en_src}</h2>', f'<h2>{escape(loc_val)}</h2>', 1)
        elif tag == 'h3':
            out = out.replace(f'<h3>{en_src}</h3>', f'<h3>{escape(loc_val)}</h3>', 1)
        elif tag == 'p':
            out = out.replace(f'<p>{en_src}</p>', f'<p>{loc_val}</p>', 1)
        elif tag == 'li':
            out = out.replace(f'<li>{en_src}</li>', f'<li>{loc_val}</li>', 1)

    # 9c. Privacy page H2 + body (all 17 langs) — v15 expanded version
    # covering AdSense, GDPR legal basis, CCPA "Do Not Sell or Share",
    # children under 13, IP rate-limiting matching server.js, contact
    # method, and last-updated date.
    privacy_blocks = [
        # lede
        ('privacy_p_lede', "Last updated 25 August 2026. This policy explains what Handle collects, what it does not, and how you can exercise your rights. We try to write in plain language; the formal legal terms are the ones that apply if there is ever a conflict between plain language and these formal terms."),
        # What Handle is
        ('privacy_p_what_site_h2', 'What Handle is', 'h2'),
        ('privacy_p_what_site_p', "Handle is a free TikTok username generator. You type a keyword, pick a niche and a vibe, and the site returns a list of handle ideas that follow TikTok's username rules. Each handle is then checked against TikTok's own profile endpoint so you can see whether it is likely available, likely taken, or unknown (the check could not be completed). Handle is an independent project. It is not affiliated with TikTok or ByteDance Ltd."),
        # Cookies and similar technologies
        ('privacy_p_cookies_h2', 'Cookies and similar technologies', 'h2'),
        ('privacy_p_cookies_p1', "The core tool does not set any cookies. The only persistent client-side storage we use is a single entry in your browser's <code>localStorage</code>, which is not sent to any server and is not read by third parties. If Google AdSense is enabled (see the Advertising section below), Google will set its own cookies and read its own identifiers to deliver and measure ads; that section explains what those are and how to opt out."),
        ('privacy_p_cookies_p2', "The localStorage flag we set is named <code>handle.cookieConsent.v1</code> and stores only the string <code>\"accepted\"</code> after you click the consent banner's acknowledge button. It is never sent to our server, never read by any third party, and you can clear it at any time via your browser's developer tools or by clearing site data for this domain."),
        # What we collect
        ('privacy_p_collect_h2', 'What we collect', 'h2'),
        ('privacy_p_collect_p1', 'Nothing directly identifying you. The keyword you type, the niche and vibe you pick, and the list of generated handles are processed in your browser and are not associated with any user profile on our side.'),
        ('privacy_p_collect_p2', "<strong>Server logs.</strong> Like most web servers, our hosting provider records IP address, user-agent, request path, response status, and timestamp in standard access logs, retained for 30 days for security and abuse prevention. We do not use these logs for advertising, profiling, or any user-facing analytics."),
        ('privacy_p_collect_p3', "<strong>No accounts, no email, no profiles.</strong> Handle does not require an account, does not ask for your email address, and does not build a profile of you. The site has no newsletter signup, no comment system, and no contact form that asks for personal details."),
        # How we use information
        ('privacy_p_use_h2', 'How we use information', 'h2'),
        ('privacy_p_use_p1', 'We use the information we collect for three things: (1) to deliver the tool to you — running the generator, checking availability against TikTok, and rendering the result cards; (2) to keep the service healthy — rate limiting, abuse prevention, debugging outages; and (3) to respond to legal requests if we ever receive any.'),
        ('privacy_p_use_p2', 'We do not sell your data. We do not share it with advertisers except in the aggregate statistical way that every ad-supported site does (an ad network sees a request, not a name). We do not use it to make automated decisions about you.'),
        ('privacy_p_use_p3', 'If you write to us through the contact email below, we use whatever you tell us only to reply to you, and we delete the thread after 12 months unless you ask us to keep it.'),
        # Legal basis (GDPR)
        ('privacy_p_legal_basis_h2', 'Legal basis (EEA / UK visitors)', 'h2'),
        ('privacy_p_legal_basis_p1', "If you are in the European Economic Area or the United Kingdom, the General Data Protection Regulation (GDPR) requires us to state a legal basis for each processing activity. Our legal bases are: <strong>consent</strong> for setting any non-essential cookies (including any AdSense cookies, if and when AdSense is enabled); <strong>legitimate interest</strong> for the in-memory IP rate-limiting needed to keep the availability-check endpoint reachable; and <strong>legal obligation</strong> for retaining standard server logs for the security and abuse-prevention period required by our hosting provider."),
        # Advertising (AdSense)
        ('privacy_p_adsense_h2', 'Advertising (Google AdSense)', 'h2'),
        ('privacy_p_adsense_p1', "Handle reserves space for Google AdSense via the <code>ads.txt</code> file at the root of the site, but AdSense is not currently serving ads. When AdSense is enabled, the following disclosures apply. We will display a clear notice and obtain consent before any AdSense cookies are set for visitors in the EEA, the UK, and Switzerland."),
        ('privacy_p_adsense_p2', "<strong>Google's required disclosure.</strong> Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to users based on their visit to this site and/or other sites on the Internet."),
        ('privacy_p_adsense_p3', "<strong>How to opt out of personalised advertising.</strong> You may opt out of personalised advertising by visiting Google's <a href=\"https://adssettings.google.com/\" rel=\"noopener noreferrer\" target=\"_blank\">Ads Settings</a>. You may also opt out of some third-party vendors' use of cookies for personalised advertising by visiting <a href=\"https://www.aboutads.info/\" rel=\"noopener noreferrer\" target=\"_blank\">www.aboutads.info</a>. For information about how Google uses data from partner sites, see <a href=\"https://policies.google.com/technologies/partner-sites\" rel=\"noopener noreferrer\" target=\"_blank\">How Google uses information from sites or apps that use our services</a>."),
        # Third parties
        ('privacy_p_third_h2', 'Third-party services', 'h2'),
        ('privacy_p_third_p1', "<strong>TikTok / ByteDance.</strong> The availability check sends a request from our server to TikTok's public profile and oEmbed endpoints. TikTok sees the request from our server's IP, the handle being checked, and standard HTTP headers (including our <code>HandleBot/0.1</code> User-Agent). What TikTok does with that request is governed by <a href=\"https://www.tiktok.com/legal/privacy-policy\" rel=\"noopener noreferrer\" target=\"_blank\">TikTok's Privacy Policy</a>."),
        ('privacy_p_third_p2', "<strong>Hosting and CDN.</strong> Our static files are served through a content delivery network. The CDN logs IP, user-agent, and request path for its own abuse-prevention purposes; that logging is governed by the CDN provider's privacy policy."),
        ('privacy_p_third_p3', "<strong>Ad networks.</strong> When AdSense is enabled, Google and its certified ad partners may set and read cookies and similar identifiers on your browser for the purpose of selecting and measuring ads. See the Advertising section above for the full list of disclosures and opt-out links."),
        # TikTok availability check
        ('privacy_p_availability_h2', 'TikTok availability check', 'h2'),
        ('privacy_p_availability_p1', "When you click \"Check\" or \"Generate\", the server you are talking to sends a request to TikTok to find out whether a given handle is associated with a live profile. The handle you checked is included in that request, and TikTok can therefore see which handle you are interested in. We do not send your IP address, your name, your email, or any other identifier together with that request beyond the standard HTTP headers that every web request carries. The check is best-effort: TikTok may rate-limit, block, or return incomplete results at any time, and verdicts can be out of date the moment they are issued."),
        # Rate limiting
        ('privacy_p_ratelimit_h2', 'Rate limiting and IP addresses', 'h2'),
        ('privacy_p_ratelimit_p1', "To keep the availability-check endpoint reachable and to stay within TikTok's anti-abuse thresholds, the server applies a token-bucket rate limit keyed on your IP address. The bucket is held in a JavaScript <code>Map</code> in the Node process memory. It is not written to disk, not replicated across servers, and not shared with any third party. When the server restarts, the bucket is gone. We do not log, store, or analyze IP addresses for any other purpose; the IP is used solely as a key into the in-memory bucket, then forgotten when the bucket is dropped or evicted."),
        # Children under 13
        ('privacy_p_children_h2', 'Children under 13', 'h2'),
        ('privacy_p_children_p1', "Handle is not directed at children under 13, and we do not knowingly collect personal information from children under 13. The site is a tool for adult TikTok creators and brand-builders. If you believe a child under 13 has provided personal information through the site, contact us at the address below and we will delete it. The United States Children's Online Privacy Protection Act (COPPA) and the EU's GDPR-K both define a child as under 13 unless a member state sets a higher age up to 16; we apply the stricter threshold."),
        # EEA / UK rights
        ('privacy_p_rights_h2', 'Your rights (EEA / UK)', 'h2'),
        ('privacy_p_rights_p1', "If you are in the EEA, the UK, or Switzerland, you have the right to: access the personal data we hold about you; correct inaccurate data; request deletion of your data; restrict or object to processing; receive your data in a portable, machine-readable format; and withdraw consent at any time without affecting the lawfulness of processing carried out before withdrawal. You also have the right to lodge a complaint with your local data protection authority. Because we do not collect personal data beyond standard server logs, most requests will receive a \"we hold nothing identifiable about you\" response — but the right stands. To exercise any of these rights, contact us at the address below."),
        # California / CCPA
        ('privacy_p_ccpa_h2', 'California privacy rights (CCPA / CPRA)', 'h2'),
        ('privacy_p_ccpa_p1', "If you are a California resident, the California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), gives you specific rights regarding your personal information."),
        ('privacy_p_ccpa_p2', "<strong>Do Not Sell or Share My Personal Information.</strong> We do not sell personal information for money, and we do not share it for cross-context behavioural advertising as those terms are defined under the CPRA. If AdSense is enabled and you would like to opt out of any future cross-context advertising, you can do so by enabling the \"Limit ad tracking\" or \"Opt out of personalised ads\" controls described in the Advertising section above, or by following the link <a href=\"https://adssettings.google.com/\" rel=\"noopener noreferrer\" target=\"_blank\">here</a>. We do not knowingly sell or share the personal information of consumers under 16."),
        ('privacy_p_ccpa_p3', "You also have the right to know what categories of personal information we collect (server logs only), to request deletion, and to not be discriminated against for exercising your rights. To exercise any of these rights, contact us at the address below. We will respond within 45 days as required by the CCPA."),
        # Data retention
        ('privacy_p_retention_h2', 'Data retention', 'h2'),
        ('privacy_p_retention_p1', "Server logs: 30 days, then deleted. Rate-limit buckets: until the bucket fills back to capacity (1 hour after your last request, in practice) or until the server restarts, whichever comes first. Availability check results: not stored on our side; each check is a fresh probe. The localStorage consent flag persists in your browser until you clear site data."),
        # International transfers
        ('privacy_p_transfers_h2', 'International transfers', 'h2'),
        ('privacy_p_transfers_p1', "Handle is operated from servers located in the United States and the European Union (our CDN edges). When you use the tool, your request may be served from an edge near you, but the availability-check requests that we make to TikTok originate from a fixed set of our server IPs (US and EU regions). If you are in a region with strict data-residency rules, the act of using the tool means your request is processed outside your region. We rely on standard contractual clauses and the European Commission's adequacy decisions for the limited personal data processed (IP for rate-limiting)."),
        # Changes
        ('privacy_p_changes_h2', 'Changes to this policy', 'h2'),
        ('privacy_p_changes_p1', "If we make material changes, we will update the \"Last updated\" date at the top of this page. For changes that broaden the data we collect, change how we use it, or change the third parties we share with, we will add a more prominent notice on the home page for at least 30 days before the change takes effect. The previous version of this policy is available on request."),
        # Contact
        ('privacy_p_contact_h2', 'Contact', 'h2'),
        ('privacy_p_contact_p1', "For privacy questions, data-subject requests, CCPA requests, copyright notices, and any other legal matter, write to <strong>privacy@gethandlenames.com</strong>. We aim to respond within 14 days for privacy requests and within 30 days for data-subject requests as required by the GDPR."),
    ]
    for entry in privacy_blocks:
        if len(entry) == 3:
            key, en_src, tag = entry
        else:
            key, en_src = entry
            tag = 'p'
        loc_val = tr.get(key)
        if not loc_val:
            continue
        if tag == 'h2':
            out = out.replace(f'<h2>{en_src}</h2>', f'<h2>{escape(loc_val)}</h2>', 1)
        else:
            out = out.replace(f'<p>{en_src}</p>', f'<p>{loc_val}</p>', 1)

    # 9d. Terms page H2 + body (all 17 langs)
    terms_blocks = [
        ('terms_h2_what', 'What Handle is', 'h2'),
        ('terms_h2_no_affil', 'No affiliation with TikTok', 'h2'),
        ('terms_h2_no_warranty', 'No warranty on availability verdicts', 'h2'),
        ('terms_h2_no_trademark', 'No trademark search', 'h2'),
        ('terms_h2_acceptable', 'Acceptable use', 'h2'),
        ('terms_h2_ip', 'Intellectual property', 'h2'),
        ('terms_h2_disclaimer', 'Disclaimer of warranties', 'h2'),
        ('terms_h2_liability', 'Limitation of liability', 'h2'),
        ('terms_h2_changes', 'Changes to these terms', 'h2'),
        ('terms_h2_governing', 'Governing law', 'h2'),
        ('terms_h2_contact', 'Contact', 'h2'),
        ('terms_what_p', "Handle is a free, public web tool that helps you brainstorm TikTok usernames and check whether a candidate is likely available. The output is a set of handle suggestions plus an availability verdict (likely available, likely taken, or unknown)."),
        ('terms_no_affil_p1', "Handle is an independent project. It is not affiliated with, endorsed by, sponsored by, or in any way associated with TikTok, ByteDance Ltd., or any of their subsidiaries. \"TikTok\" is a trademark of ByteDance Ltd. All references to TikTok on this site are for descriptive purposes only (the tool checks usernames on TikTok) and are made under fair use."),
        ('terms_no_affil_p2', "If you are a rights holder and believe a page on this site uses your mark in a way that is not fair use, contact us and we will address it promptly."),
        ('terms_no_warranty_p', "The availability check is a best-effort probe of public TikTok endpoints. Verdicts can be wrong, can be out of date the moment they are issued, and can be affected by TikTok-side rate limits, regional blocks, or service incidents. \"Likely available\" is not a guarantee. You are responsible for confirming availability on TikTok itself before you build a brand on a handle."),
        ('terms_no_trademark_p', "Handle does not check registered trademarks. A handle can be free on TikTok and still infringe a registered mark in your industry. Before you commit to a handle for a public brand, run a trademark search (USPTO TESS in the US, EUIPO in the EU, or a local equivalent) and consider talking to a lawyer."),
        ('terms_acceptable_p', "You agree not to use Handle to:"),
        ('terms_acceptable_li1', "Probe TikTok at a rate that would trigger their anti-abuse systems. The site enforces a 60-checks-per-minute-per-IP rate limit; please respect it.", 'li'),
        ('terms_acceptable_li2', "Generate content that is illegal, infringing, or harassing.", 'li'),
        ('terms_acceptable_li3', "Attempt to circumvent rate limits, scrape the site at industrial scale, or otherwise interfere with the service.", 'li'),
        ('terms_acceptable_li4', "Misrepresent the tool as being affiliated with TikTok.", 'li'),
        # About Roadmap 8 list items
        ('about_roadmap_li1', 'A <strong>TikTok username ideas</strong> listing page — 200+ curated handles organised by niche and vibe, optimised for the long-tail "TikTok username ideas" search.', 'li'),
        ('about_roadmap_li2', 'A dedicated <strong>TikTok fonts</strong> page — promote the unicode font converter to its own URL with proper meta, intro copy, and the "stylish text for TikTok bio" angle.', 'li'),
        ('about_roadmap_li3', '<strong>TikTok bio ideas</strong> and <strong>TikTok names for couples</strong> — separate standalone pages for adjacent search intents.', 'li'),
        ('about_roadmap_li4', 'Programmatic niche landing pages for long-tail SEO (e.g. <code>/tiktok-username-ideas/aesthetic-fitness</code>).', 'li'),
        ('about_roadmap_li5', 'Cross-platform availability check (Instagram, YouTube, X) — the architecture is ready, just needs the per-platform checkers.', 'li'),
        ('about_roadmap_li6', 'Email-capture for a weekly name-drop newsletter.', 'li'),
        ('about_roadmap_li7', 'TikTok and YouTube channels showing weekly name picks.', 'li'),
        ('about_roadmap_li8', 'An affiliate layer pointing creators at Linktree, Namecheap, Canva Pro, and similar tools.', 'li'),
        ('terms_ip_p', "The Handle name, the site's code, and the original word lists / pattern rules are owned by us. You may use the generated names however you like — they're suggestions, not our property once handed to you. TikTok's trademarks, the TikTok logo, and TikTok's username rules are TikTok's. The Unicode glyphs in the font converter are the property of the Unicode Consortium and the original type designers."),
        ('terms_disclaimer_p', "The site is provided \"as is\" and \"as available.\" To the maximum extent permitted by law, we disclaim all warranties, express or implied, including the implied warranties of merchantability, fitness for a particular purpose, and non-infringement. We do not warrant that the site will be uninterrupted, error-free, or that the availability verdicts will be accurate."),
        ('terms_liability_p', "To the maximum extent permitted by law, we will not be liable for any indirect, incidental, special, consequential, or punitive damages arising out of or related to your use of the site, including lost profits, lost data, or business interruption, even if we have been advised of the possibility of such damages."),
        ('terms_changes_p', "If we make material changes, we'll bump the \"Last updated\" date and, for changes that broaden what we can do with your data or how we limit your rights, we'll add a more prominent notice on the home page for at least 30 days."),
        ('terms_governing_p', "These terms are governed by the laws of the State of Delaware, United States of America, without regard to its conflict-of-laws provisions. Any dispute arising out of or related to these terms will be resolved in the state or federal courts located in Delaware, and you consent to the personal jurisdiction of those courts."),
        ('terms_contact_p', "For legal notices, takedown requests, and any other formal correspondence, write to <strong>legal@gethandlenames.com</strong>. We aim to respond within 14 days. Casual feedback and bug reports can go to the same address — we read everything — but formal legal notices must follow this channel."),
        ('terms_lede_p', "Last updated 25 August 2026. By using Handle you agree to these terms. They cover what Handle is, who owns what, what you can and can't do with the tool, and what happens if something goes wrong."),
    ]
    for entry in terms_blocks:
        if len(entry) == 3:
            key, en_src, tag = entry
        else:
            key, en_src = entry
            tag = 'p'
        loc_val = tr.get(key)
        if not loc_val:
            continue
        if tag == 'h2':
            out = out.replace(f'<h2>{en_src}</h2>', f'<h2>{escape(loc_val)}</h2>', 1)
        elif tag == 'li':
            out = out.replace(f'<li>{en_src}</li>', f'<li>{loc_val}</li>', 1)
        else:
            out = out.replace(f'<p>{en_src}</p>', f'<p>{loc_val}</p>', 1)

    # 9e. 404 page H2 + link texts
    if tr.get('404_h2_looking'):
        out = out.replace(
            '<h2>Looking for one of these?</h2>',
            f'<h2>{escape(tr["404_h2_looking"])}</h2>',
            1,
        )
    if tr.get('404_404_link_generator'):
        # The 404 page has a list with "TikTok username generator" as a
        # link to /generator — replace that specific link's text.
        out = out.replace(
            '<a href="/generator" data-nav="generator">TikTok username generator</a>',
            f'<a href="/generator" data-nav="generator">{escape(tr["404_404_link_generator"])}</a>',
            1,
        )
    # 404 page buttons: "Go home →" and "Open the generator"
    if tr.get('404_go_home'):
        out = out.replace(
            '<a class="btn-primary" href="/" data-nav="home">Go home →</a>',
            f'<a class="btn-primary" href="/" data-nav="home">{escape(tr["404_go_home"])}</a>',
            1,
        )
    if tr.get('404_open_generator'):
        # 404 page secondary button
        out = out.replace(
            '<a class="btn-ghost" href="/generator" data-nav="generator">Open the generator</a>',
            f'<a class="btn-ghost" href="/generator" data-nav="generator">{escape(tr["404_open_generator"])}</a>',
            1,
        )

    # 9f. Footer "Privacy Policy" and "Terms of Service" link text
    # The first `<a href="/privacy" data-nav="privacy">Privacy</a>` in the
    # page is in the FAQ body, not the footer. Target the footer block
    # specifically (which uses `<li><a>... </a></li>`).
    footer_privacy_re = re.compile(
        r'(<li><a href="/privacy" data-nav="privacy">)([^<]+)(</a></li>)',
    )
    if tr.get('footer_privacy'):
        out = footer_privacy_re.sub(
            lambda m: m.group(1) + escape(tr['footer_privacy']) + m.group(3),
            out,
            count=1,
        )
    footer_terms_re = re.compile(
        r'(<li><a href="/terms" data-nav="terms">)([^<]+)(</a></li>)',
    )
    if tr.get('footer_terms'):
        out = footer_terms_re.sub(
            lambda m: m.group(1) + escape(tr['footer_terms']) + m.group(3),
            out,
            count=1,
        )

    # 9g. Footer "short" link text (footer_about_short, footer_faq_short,
    # footer_generator_short, footer_privacy_short, footer_terms_short).
    # These are the second footer row of short labels. Pattern: <a ...>TEXT</a>
    # with no surrounding <li> tag.
    if tr.get('footer_about_short'):
        out = out.replace(
            '<a href="/about" data-nav="about" data-i18n="footer_about_short">About</a>',
            f'<a href="/about" data-nav="about" data-i18n="footer_about_short">{escape(tr["footer_about_short"])}</a>',
            1,
        )
    if tr.get('footer_faq_short'):
        out = out.replace(
            '<a href="/faq" data-nav="faq" data-i18n="footer_faq_short">FAQ</a>',
            f'<a href="/faq" data-nav="faq" data-i18n="footer_faq_short">{escape(tr["footer_faq_short"])}</a>',
            1,
        )
    if tr.get('footer_generator_short'):
        out = out.replace(
            '<a href="/generator" data-nav="generator" data-i18n="footer_generator_short">Generator</a>',
            f'<a href="/generator" data-nav="generator" data-i18n="footer_generator_short">{escape(tr["footer_generator_short"])}</a>',
            1,
        )
    if tr.get('footer_privacy_short'):
        out = out.replace(
            '<a href="/privacy" data-nav="privacy" data-i18n="footer_privacy_short">Privacy</a>',
            f'<a href="/privacy" data-nav="privacy" data-i18n="footer_privacy_short">{escape(tr["footer_privacy_short"])}</a>',
            1,
        )
    if tr.get('footer_terms_short'):
        out = out.replace(
            '<a href="/terms" data-nav="terms" data-i18n="footer_terms_short">Terms</a>',
            f'<a href="/terms" data-nav="terms" data-i18n="footer_terms_short">{escape(tr["footer_terms_short"])}</a>',
            1,
        )

    # 9h. Footer legal disclaimer (data-i18n="footer_disclaimer"). The HTML
    # ships with the English default; the localized value is what users
    # would otherwise see only after JS runs. Replace it at build time so
    # the static HTML also shows the localized disclaimer.
    if tr.get('footer_disclaimer'):
        out = out.replace(
            '<div class="footer-legal" data-i18n="footer_disclaimer">\n      Handle is not affiliated with, endorsed by, or sponsored by TikTok or ByteDance Ltd. "TikTok" is a trademark of ByteDance Ltd.\n    </div>',
            f'<div class="footer-legal" data-i18n="footer_disclaimer">\n      {escape(tr["footer_disclaimer"])}\n    </div>',
        )

    # 9i. Generic data-i18n attribute replacement at build time. The HTML
    # template has every translatable element marked with data-i18n="key"
    # and ships with the English default text. Without this step, the
    # static HTML for /es/, /fr/, etc. would still show English in those
    # elements (the runtime JS would translate them after load, but the
    # initial render would be wrong). We replace every data-i18n="X">text<
    # with the localized value where X has a translation in tr. Handles
    # both plain text and HTML-embedded content (e.g. <em>, <strong>).
    def _replace_i18n(m):
        key = m.group(1)
        default = m.group(2)
        if key in tr and tr[key] and tr[key] != default:
            return f'data-i18n="{key}">{tr[key]}<'
        return m.group(0)
    out = re.sub(r'data-i18n="(\w+)"[^>]*>([^<]+(?:<[^/][^>]*>[^<]*</[^>]+>[^<]*)*)<', _replace_i18n, out)
    # Also handle the simpler case (no inner tags)
    def _replace_i18n_simple(m):
        key = m.group(1)
        default = m.group(2)
        if key in tr and tr[key] and tr[key] != default:
            return f'data-i18n="{key}">{tr[key]}<'
        return m.group(0)
    out = re.sub(r'data-i18n="(\w+)"[^>]*>([^<]+)<', _replace_i18n_simple, out)

    # 9j. Generic data-i18n-placeholder attribute replacement at build time.
    # Same rationale as 9i, but for <input> placeholders.
    def _replace_i18n_placeholder(m):
        key = m.group(1)
        if key in tr and tr[key]:
            return f'data-i18n-placeholder="{key}" placeholder="{escape(tr[key])}"'
        return m.group(0)
    out = re.sub(r'data-i18n-placeholder="(\w+)" placeholder="([^"]*)"',
                 _replace_i18n_placeholder, out)

    # 9k. Per-page title, meta description, og tags, and hreflang alternates.
    # This is the SEO setup that tells Google "this is the [lang] version of
    # this exact page". For each of the 6 routes (home, generator, faq, about,
    # privacy, terms) we emit:
    #   - a per-page <title> (set on a hidden <span data-page-title="X">
    #     element the router swaps in)
    #   - per-page <meta name="description">
    #   - per-page <meta property="og:title"> and og:description
    #   - hreflang alternates for every (lang, page) pair
    # Google and other search engines will use these tags regardless of
    # whether the page is rendered server-side or client-side.
    if lang in PER_PAGE_SEO:
        per_page = PER_PAGE_SEO[lang]
        # Build the new <head> meta block: per-page titles, descriptions, og tags.
        # We replace the existing single title + meta desc with a per-page set,
        # then have router.js swap them at runtime via the data-page-meta attrs.
        new_meta_block_lines = []
        new_meta_block_lines.append(
            '  <!-- Per-page SEO: title + meta + og + hreflang for all 6 pages. '
            'router.js swaps document.title and meta[name=description] on '
            'route change. The hreflang tags below are emitted for all 6 pages × '
            '18 langs = 108 links so Google can match any (lang, page) pair. -->'
        )
        for page_name in PAGES:
            seo = per_page.get(page_name, {})
            title = escape(seo.get('title', ''))
            meta_desc = escape(seo.get('meta_desc', ''))
            og_title = escape(seo.get('og_title', ''))
            og_desc = escape(seo.get('og_desc', ''))
            new_meta_block_lines.append(
                f'  <template data-page-meta="{page_name}">'
                f'<title>{title}</title>'
                f'<meta name="description" content="{meta_desc}">'
                f'<meta property="og:title" content="{og_title}">'
                f'<meta property="og:description" content="{og_desc}">'
                f'</template>'
            )
        # Replace the existing <title> + <meta name="description"> + og tags
        # in the source with all 6 page templates. router.js will swap the
        # active one on route change.
        title_meta_pattern = re.compile(
            r'  <title>[^<]*</title>\n'
            r'(  <meta name="description"[^>]*>\n)?'
            r'((?:  <meta property="og:[^>]*>\n)*)',
            re.MULTILINE,
        )
        new_meta_block = '\n'.join(new_meta_block_lines) + '\n'
        out = title_meta_pattern.sub(
            lambda m: new_meta_block,
            out,
            count=1,
        )

        # Build the per-page hreflang block. We need 6 page sets × 18 langs
        # = 108 hreflang tags. Each <link rel="alternate" hreflang="X"
        # href="..."> is wrapped in a <template data-page-hreflang="X">
        # so router.js can hide all but the active page's set.
        from per_page_seo import url_for
        hreflang_template_lines = [
            '  <!-- Per-page hreflang alternates: 6 pages × 18 langs = 108 links. '
            'router.js unhides the active page set on route change. -->',
        ]
        for page_name in PAGES:
            hreflang_template_lines.append(
                f'  <template data-page-hreflang="{page_name}">'
            )
            for hreflang_lang in ['en'] + LANG_ORDER:  # all 18 langs
                path = url_for(hreflang_lang, page_name)
                extra = ''
                if hreflang_lang in ('ar', 'ur'):
                    extra = ' dir="rtl"'
                if hreflang_lang == 'en':
                    hreflang_template_lines.append(
                        f'    <link rel="alternate" hreflang="{hreflang_lang}" href="{path}">'
                    )
                else:
                    hreflang_template_lines.append(
                        f'    <link rel="alternate" hreflang="{hreflang_lang}" href="{path}"{extra}>'
                    )
            # x-default for this page
            hreflang_template_lines.append(
                f'    <link rel="alternate" hreflang="x-default" href="{url_for("en", page_name)}">'
            )
            hreflang_template_lines.append('  </template>')
        # Replace the existing hreflang block (the 19 <link rel="alternate"
        # tags for the home page) with the new per-page templates.
        hreflang_block_pattern = re.compile(
            r'(  <link rel="alternate" hreflang="[^"]+"[^>]*>\n)+'
            r'  <link rel="alternate" hreflang="x-default"[^>]*>\n',
        )
        new_hreflang_block = '\n'.join(hreflang_template_lines) + '\n'
        out = hreflang_block_pattern.sub(new_hreflang_block, out, count=1)

    # 10. FAQ H2 subheadings + H3 question titles + About H2 subheadings

    # 10. FAQ H2 subheadings + H3 question titles + About H2 subheadings
    # (all 17 languages — Tier 1 fully, Tier 2 has meta + H2/H3 + body).
    # We translate the English H2/H3 text in place using exact-match
    # find-replace.
    if lang in FAQ_ABOUT_TRANSLATIONS or lang in TIER2 or lang in PAGES_TRANSLATIONS:
        # Merge FAQ/H2 translations from all sources:
        # 1. FAQ_ABOUT_TRANSLATIONS (Tier 1, original)
        # 2. TIER2 (Tier 2 — only has FAQ/About headings)
        # 3. PAGES_TRANSLATIONS (all 17 langs, all keys — Terms H2s
        #    included). This is the canonical source for Terms headings.
        qa = dict(FAQ_ABOUT_TRANSLATIONS.get(lang, {}))
        qa.update(TIER2.get(lang, {}))
        qa.update(PAGES_TRANSLATIONS.get(lang, {}))
        # FAQ H2 subheadings
        for h2_key, h2_en, h2_localized in [
            ('faq_h2_picking', 'Picking a TikTok username', qa.get('faq_h2_picking')),
            ('faq_h2_check',   'How the availability check works', qa.get('faq_h2_check')),
            ('faq_h2_styles',  'Names, styles, and trends', qa.get('faq_h2_styles')),
            ('faq_h2_legal',   'Account, legal, and support', qa.get('faq_h2_legal')),
        ]:
            if h2_localized:
                out = out.replace(
                    '<h2>' + h2_en + '</h2>',
                    '<h2>' + escape(h2_localized) + '</h2>',
                    1,
                )
        # FAQ H3 question titles — match the English source exactly
        for q_num in range(1, 19):
            q_en_marker = 'faq_q' + str(q_num) + '_en'
            q_key = 'faq_q' + str(q_num)
            q_localized = qa.get(q_key)
            if not q_localized:
                continue
            # We don't have the English source stored separately, so we
            # use the known English FAQ H3 list:
            pass  # handled below via a more reliable match
        # FAQ H3 — match against the actual English source (verbatim)
        faq_en_qs = [
            'What should my TikTok username be?',
            'How do I pick a TikTok username that fits me?',
            'Why is my TikTok name already taken?',
            'What makes a good TikTok username?',
            'How do I change my TikTok username?',
            "What's the difference between a TikTok username and a TikTok display name?",
            'How do I know if a TikTok username is available?',
            'How does the availability check work?',
            'Why does it say "Likely available" instead of just "Available"?',
            'Why does a handle show "Unknown" on the result list?',
            'What are the best TikTok usernames for 2026?',
            "What's a short TikTok username, and why does length matter?",
            'What are the best aesthetic, cool, funny, and edgy TikTok usernames?',
            'Can I use TikTok fonts in my @handle?',
            'Does the generator work for other platforms too?',
            'Can I use the names Handle generates commercially?',
            'Is Handle free?',
            'Is Handle affiliated with TikTok?',
        ]
        for i, q_en in enumerate(faq_en_qs, start=1):
            q_localized = qa.get('faq_q' + str(i))
            if q_localized:
                out = out.replace(
                    '<h3>' + q_en + '</h3>',
                    '<h3>' + escape(q_localized) + '</h3>',
                    1,
                )
        # About H2 subheadings
        about_h2_pairs = [
            ('What this is', qa.get('about_h2_what')),
            ("What this isn't", qa.get('about_h2_isnt')),
            ('How it works under the hood', qa.get('about_h2_how')),
            ('Localisation — 17 languages, native keyword targeting', qa.get('about_h2_l10n')),
            ('Roadmap', qa.get('about_h2_roadmap')),
            ('Contact', qa.get('about_h2_contact')),
        ]
        for h2_en, h2_localized in about_h2_pairs:
            if h2_localized:
                out = out.replace(
                    '<h2>' + h2_en + '</h2>',
                    '<h2>' + escape(h2_localized) + '</h2>',
                    1,
                )
    # 10b. Terms H2 subheadings (all 17 langs, from PAGES_TRANSLATIONS)
    if lang in PAGES_TRANSLATIONS:
        terms_h2_pairs = [
            ('What Handle is', PAGES_TRANSLATIONS[lang].get('terms_h2_what')),
            ('No affiliation with TikTok', PAGES_TRANSLATIONS[lang].get('terms_h2_no_affil')),
            ('No warranty on availability verdicts', PAGES_TRANSLATIONS[lang].get('terms_h2_no_warranty')),
            ('No trademark search', PAGES_TRANSLATIONS[lang].get('terms_h2_no_trademark')),
            ('Acceptable use', PAGES_TRANSLATIONS[lang].get('terms_h2_acceptable')),
            ('Intellectual property', PAGES_TRANSLATIONS[lang].get('terms_h2_ip')),
            ('Disclaimer of warranties', PAGES_TRANSLATIONS[lang].get('terms_h2_disclaimer')),
            ('Limitation of liability', PAGES_TRANSLATIONS[lang].get('terms_h2_liability')),
            ('Changes to these terms', PAGES_TRANSLATIONS[lang].get('terms_h2_changes')),
            ('Governing law', PAGES_TRANSLATIONS[lang].get('terms_h2_governing')),
            ('Contact', PAGES_TRANSLATIONS[lang].get('terms_h2_contact')),
        ]
        for h2_en, h2_localized in terms_h2_pairs:
            if h2_localized:
                out = out.replace(
                    '<h2>' + h2_en + '</h2>',
                    '<h2>' + escape(h2_localized) + '</h2>',
                    1,
                )

    # 10c. Affiliation note (appears 2x: home + generator)
    if tr.get('affiliation_note'):
        out = out.replace(
            '<p class="affiliation-note" role="note">Handle is not affiliated with, endorsed by, or sponsored by TikTok or ByteDance Ltd. "TikTok" is a trademark of ByteDance Ltd.</p>',
            f'<p class="affiliation-note" role="note">{escape(tr["affiliation_note"])}</p>',
        )

    # 11. FAQ body answers (18) + About body paragraphs (5)
    # (Tier 1 + Tier 2, all 17 languages)
    if lang in FAQ_ABOUT_BODIES:
        bodies = dict(FAQ_ABOUT_BODIES[lang])
        # v18: long-form FAQ answers (150+ words each, target-keyword woven
        # in for SEO). Source: i18n/faq_expanded_translations.py.
        try:
            from faq_expanded_translations import (
                FAQ_A_ES, FAQ_A_DE, FAQ_A_FR, FAQ_A_IT, FAQ_A_PT, FAQ_A_NL,
                FAQ_A_PL, FAQ_A_RU, FAQ_A_ZH, FAQ_A_VI, FAQ_A_ID, FAQ_A_MS,
                FAQ_A_TL, FAQ_A_HI, FAQ_A_BN, FAQ_A_UR, FAQ_A_AR,
            )
            from faq_expanded import FAQ_A as FAQ_A_EN
            LANG_TO_FAQ = {
                'en': FAQ_A_EN,
                'es': FAQ_A_ES, 'de': FAQ_A_DE, 'fr': FAQ_A_FR, 'it': FAQ_A_IT,
                'pt': FAQ_A_PT, 'nl': FAQ_A_NL, 'pl': FAQ_A_PL, 'ru': FAQ_A_RU,
                'zh': FAQ_A_ZH, 'vi': FAQ_A_VI, 'id': FAQ_A_ID, 'ms': FAQ_A_MS,
                'tl': FAQ_A_TL, 'hi': FAQ_A_HI, 'bn': FAQ_A_BN, 'ur': FAQ_A_UR,
                'ar': FAQ_A_AR,
            }
            if lang in LANG_TO_FAQ:
                for k, v in LANG_TO_FAQ[lang].items():
                    bodies[k] = v
        except (ImportError, SyntaxError):
            # File may not exist yet or may have an error; fall back to
            # the short FAQ answers in body_translations.py
            pass

        # 18 FAQ answer paragraphs — match the H3 by its currently-in-out
        # text (which may have been translated to the locale's language
        # by step 10). For each Q, look up the localized H3 from
        # FAQ_ABOUT_TRANSLATIONS; fall back to the English H3 if no
        # localized H3 is set.
        faq_en_qs = [
            'What should my TikTok username be?',
            'How do I pick a TikTok username that fits me?',
            'Why is my TikTok name already taken?',
            'What makes a good TikTok username?',
            'How do I change my TikTok username?',
            "What's the difference between a TikTok username and a TikTok display name?",
            'How do I know if a TikTok username is available?',
            'How does the availability check work?',
            'Why does it say "Likely available" instead of just "Available"?',
            'Why does a handle show "Unknown" on the result list?',
            'What are the best TikTok usernames for 2026?',
            "What's a short TikTok username, and why does length matter?",
            'What are the best aesthetic, cool, funny, and edgy TikTok usernames?',
            'Can I use TikTok fonts in my @handle?',
            'Does the generator work for other platforms too?',
            'Can I use the names Handle generates commercially?',
            'Is Handle free?',
            'Is Handle affiliated with TikTok?',
        ]
        # Get the localized FAQ H3 list (or fall back to English)
        h3_localized_map = {}
        for i, q_en in enumerate(faq_en_qs, start=1):
            q_key = 'faq_q' + str(i)
            # Try FAQ_ABOUT_TRANSLATIONS first (Tier 1), then TIER2
            # (Tier 2 — has faq_q1..faq_q18 now too).
            h3_loc = None
            if lang in FAQ_ABOUT_TRANSLATIONS:
                h3_loc = FAQ_ABOUT_TRANSLATIONS[lang].get(q_key)
            if not h3_loc and lang in TIER2:
                h3_loc = TIER2[lang].get(q_key)
            h3_localized_map[q_en] = h3_loc or q_en
        # Now match each H3 in its current form in `out` and replace the
        # <p> that follows it.
        for i, q_en in enumerate(faq_en_qs, start=1):
            a_localized = bodies.get('faq_a' + str(i))
            if not a_localized:
                continue
            h3_text = h3_localized_map[q_en]
            pattern = re.compile(
                r'(<h3[^>]*>' + re.escape(h3_text) + r'</h3>\s*<p>)(.*?)(</p>)',
                re.DOTALL,
            )
            out = pattern.sub(
                lambda m: m.group(1) + a_localized + m.group(3),
                out,
                count=1,
            )

        # 5 About body paragraphs. Match the H2 by its current text
        # in `out` (which may have been translated by step 10). Resolve
        # the localized H2 via FAQ_ABOUT_TRANSLATIONS; fall back to
        # English if no localized H2 is set.
        about_h2_to_p_key = [
            ('What this is', 'about_what_p1', 'about_what_p2'),
            ("What this isn't", 'about_isnt_p1', None),
            ('How it works under the hood', 'about_how_p1', None),
            ('Localisation — 17 languages, native keyword targeting', 'about_l10n_p1', None),
        ]
        # Map of English H2 -> localized H2 for this lang
        h2_localized_map = {}
        for h2_en, _, _ in about_h2_to_p_key:
            local_h2 = h2_en  # default
            target_key = _reverse_about_h2_key(h2_en)
            # Try FAQ_ABOUT_TRANSLATIONS (Tier 1) first, then TIER2 (Tier 2)
            src = None
            if lang in FAQ_ABOUT_TRANSLATIONS and target_key in FAQ_ABOUT_TRANSLATIONS[lang]:
                src = FAQ_ABOUT_TRANSLATIONS[lang]
            elif lang in TIER2 and target_key in TIER2[lang]:
                src = TIER2[lang]
            if src is not None:
                local_h2 = src[target_key]
            h2_localized_map[h2_en] = local_h2
        # Now replace the <p> that follows each H2 in `out`
        for h2_en, p1_key, p2_key in about_h2_to_p_key:
            local_h2 = h2_localized_map[h2_en]
            p1 = bodies.get(p1_key)
            p2 = bodies.get(p2_key) if p2_key else None
            if p1 or p2:
                # Match the H2 + first <p> and replace
                p_pattern = re.compile(
                    r'(<h2[^>]*>' + re.escape(local_h2) + r'</h2>)\s*<p>(.*?)</p>',
                    re.DOTALL,
                )
                if p1:
                    out = p_pattern.sub(
                        lambda m: m.group(1) + '\n          <p>' + p1 + '</p>',
                        out,
                        count=1,
                    )
                if p2:
                    p2_pattern = re.compile(
                        r'(<h2[^>]*>' + re.escape(local_h2) + r'</h2>\s*<p>[^<]*</p>)\s*<p>(.*?)</p>',
                        re.DOTALL,
                    )
                    out = p2_pattern.sub(
                        lambda m: m.group(1) + '\n          <p>' + p2 + '</p>',
                        out,
                        count=1,
                    )

    return out


def _reverse_about_h2_key(en_text):
    return {
        'What this is': 'about_h2_what',
        "What this isn't": 'about_h2_isnt',
        'How it works under the hood': 'about_h2_how',
        'Localisation — 17 languages, native keyword targeting': 'about_h2_l10n',
    }.get(en_text, '')


def escape(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def escape_attr(s):
    return str(s).replace('&', '&amp;').replace('"', '&quot;')


def main():
    if not EN_PATH.exists():
        print(f'ERROR: English template not found at {EN_PATH}', file=sys.stderr)
        sys.exit(1)

    en_html = EN_PATH.read_text(encoding='utf-8')

    # The English template now loads /js/titles.js for per-locale title
    # fallback. Localized files inherit this script tag automatically
    # because we read from the (already-updated) English template.

    for lang, loc in LOCALES.items():
        out_dir = OUT_BASE / lang
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / 'index.html'

        tr1 = TIER1.get(lang)
        tr2 = TIER2.get(lang)
        is_tier1 = tr1 is not None

        if is_tier1:
            tr = tr1
        else:
            tr = tr2 or {}

        # Merge the FAQ + About body translations (works for all 17 langs)
        tr_full = dict(tr)
        if lang in FAQ_ABOUT_BODIES:
            tr_full.update(FAQ_ABOUT_BODIES[lang])

        # Also merge the per-locale strings.js values so the build script
        # can replace strings that only have data-i18n attributes (e.g.
        # footer_disclaimer, consent_text, footer_about_short, niche_*,
        # vibe_*, home_cta_*, etc.). Without this, those data-i18n
        # elements would still have English default text in the static
        # HTML and only get translated at runtime by the JS.
        try:
            strings_js_path = (Path(__file__).parent.parent / 'public' / 'js' / 'strings.js')
            if strings_js_path.exists():
                strings_src = strings_js_path.read_text(encoding='utf-8')
                lang_block_re = re.compile(
                    rf"  {re.escape(lang)}:\s*\{{(.*?)\n  \}}",
                    re.DOTALL,
                )
                m_lang = lang_block_re.search(strings_src)
                if m_lang:
                    block = m_lang.group(1)
                    for m_kv in re.finditer(r"(?:^|,)\s*(\w+):\s*'((?:[^'\\]|\\.)*)'", block):
                        key = m_kv.group(1)
                        val = m_kv.group(2).replace("\\'", "'").replace("\\\\", "\\")
                        # Don't overwrite keys we already have from TIER1/2
                        if key not in tr_full:
                            tr_full[key] = val
        except Exception as e:
            print(f'Warning: could not merge strings.js for {lang}: {e}')
            print(f'Warning: could not merge strings.js for {lang}: {e}')

        localized = localize(en_html, lang, loc, tr_full, is_tier1)
        out_path.write_text(localized, encoding='utf-8')

        status = 'TIER1-full' if is_tier1 else 'TIER2-meta'
        has_body = lang in FAQ_ABOUT_BODIES
        body_status = 'body' if has_body else 'no-body'
        print(f'  [{status:11}/{body_status:7}] {out_path}')


if __name__ == '__main__':
    main()
