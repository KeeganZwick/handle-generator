# -*- coding: utf-8 -*-
"""
Per-page title and meta description for all 17 languages × 6 routes
(home, generator, faq, about, privacy, terms).

Used by the build script to:
  1. Generate per-page <title>, <meta description>, og:title, og:description
  2. Generate hreflang alternate tags for every page

Title length budget: <= 60 chars (Google truncates around 50-60)
Meta desc budget:   <= 160 chars (Google truncates around 155-160)
OG title:           <= 60 chars
OG desc:            <= 110 chars

Quality flags: same as SEO — REAL_RESEARCH where possible, BEST_GUESS otherwise.
"""

# PAGES list — the routes that get per-page hreflang
PAGES = ['home', 'generator', 'faq', 'about', 'privacy', 'terms']

# Path helper: how to build the URL for a (lang, page) pair
def url_for(lang, page):
    """Return the path for a given language and page."""
    if lang == 'en':
        prefix = ''
    else:
        prefix = '/' + lang
    if page == 'home':
        return prefix + '/'
    return prefix + '/' + page

# Per-page SEO for all 17 langs
# Structure: SEO[lang][page] = { title, meta_desc, og_title, og_desc }
PER_PAGE_SEO = {
    'en': {
        'home': {
            'title': 'TikTok Username Generator — Free Username Ideas & Availability Check | Handle',
            'meta_desc': "Free TikTok username generator with a live availability check. Get 10-20 unique username ideas that follow TikTok's rules, then see which are still available on TikTok. No signup, no limits, 17+ vibes.",
            'og_title': 'TikTok Username Generator — Free Ideas & Availability Check',
            'og_desc': "Free TikTok username generator. 10-20 ideas that follow TikTok's rules, live availability check. 17+ vibes, 17 niches, no signup.",
        },
        'generator': {
            'title': 'TikTok Username Generator — Live Availability Checker | Handle',
            'meta_desc': "Generate 10-20 unique TikTok username ideas from a keyword + niche + vibe, and check which are still available on TikTok right now. Honest Likely available / Likely taken / Unknown verdicts. No signup, no watermark.",
            'og_title': 'TikTok Username Generator — Free & Live',
            'og_desc': "10-20 unique TikTok username ideas with live availability check. No signup, no watermark.",
        },
        'faq': {
            'title': 'TikTok Username FAQ — Rules, Availability, Generator | Handle',
            'meta_desc': "Answers to the questions people actually search before picking a TikTok username: the rules, how the availability check works, why we say 'Likely' instead of 'Available', how to find a name that fits you.",
            'og_title': 'TikTok Username FAQ — Handle',
            'og_desc': "Real answers to the questions people search before picking a TikTok username.",
        },
        'about': {
            'title': 'About Handle — Free TikTok Username Generator with Live Check',
            'meta_desc': "Handle is a free, independent TikTok username generator with a live availability check. Independent from TikTok / ByteDance. Open source, 17 languages, 17 vibes, 17 niches. No signup, no usage limits, no watermark.",
            'og_title': 'About Handle — Independent TikTok Username Generator',
            'og_desc': "A free, independent TikTok username generator with a live availability check.",
        },
        'privacy': {
            'title': 'Privacy Policy — Handle',
            'meta_desc': "What Handle collects (server logs, a single localStorage flag), what it doesn't (no analytics, no advertising, no third-party tracking), and your rights as a user.",
            'og_title': 'Privacy Policy — Handle',
            'og_desc': "What Handle collects, what it doesn't, and your rights.",
        },
        'terms': {
            'title': 'Terms of Service — Handle',
            'meta_desc': "The terms under which you can use Handle: free, no signup, no warranty on availability verdicts, no trademark search, no affiliation with TikTok or ByteDance.",
            'og_title': 'Terms of Service — Handle',
            'og_desc': "The terms of use for the free Handle TikTok username generator.",
        },
    },
    'es': {
        'home': {
            'title': 'Generador de Nombres TikTok — Verifica Disponibilidad Gratis',
            'meta_desc': 'Generador de nombres TikTok gratis con verificador en vivo. Escribe una palabra, elige nicho y estilo, recibe 10-20 ideas de @ que cumplen las reglas de TikTok y comprueba disponibilidad al instante. Sin registro, sin límites.',
            'og_title': 'Generador de Nombres TikTok — Verifica Disponibilidad',
            'og_desc': 'Ideas de @ para TikTok que cumplen las reglas de la plataforma. Verifica disponibilidad en vivo. 17 estilos, 17 nichos, sin registro.',
        },
        'generator': {
            'title': 'Generador de Nombres para TikTok — Verificador en Vivo',
            'meta_desc': 'Genera 10-20 ideas únicas de @ para TikTok a partir de una palabra, nicho y estilo. Comprueba en TikTok si están disponibles. Veredictos honestos: Probablemente disponible / Probablemente ocupado / Desconocido. Sin registro.',
            'og_title': 'Generador de Nombres TikTok — Verifica Disponibilidad',
            'og_desc': '10-20 ideas únicas de @ para TikTok con verificación en vivo. Sin registro, sin marca de agua.',
        },
        'faq': {
            'title': 'Preguntas Frecuentes — Nombres para TikTok | Handle',
            'meta_desc': 'Respuestas a las preguntas que la gente busca antes de elegir un nombre para TikTok: las reglas, cómo funciona el verificador de disponibilidad, por qué decimos "Probablemente" y no "Disponible", cómo encontrar un nombre que te represente.',
            'og_title': 'Preguntas Frecuentes — Nombres para TikTok',
            'og_desc': 'Respuestas reales a las preguntas que la gente busca antes de elegir un nombre para TikTok.',
        },
        'about': {
            'title': 'Sobre Handle — Generador de Nombres TikTok Gratis con Check en Vivo',
            'meta_desc': 'Handle es un generador de nombres TikTok gratis e independiente con verificación en vivo. Sin afiliación con TikTok / ByteDance. Código abierto, 17 idiomas, 17 estilos, 17 nichos. Sin registro, sin límites, sin marca de agua.',
            'og_title': 'Sobre Handle — Generador de Nombres TikTok Independiente',
            'og_desc': 'Un generador de nombres TikTok gratis e independiente con verificación en vivo.',
        },
        'privacy': {
            'title': 'Política de Privacidad — Handle',
            'meta_desc': 'Qué recoge Handle (logs del servidor, una marca en localStorage), qué no recoge (sin analítica, sin anuncios, sin tracking), y tus derechos como usuario.',
            'og_title': 'Política de Privacidad — Handle',
            'og_desc': 'Qué recoge Handle, qué no, y tus derechos.',
        },
        'terms': {
            'title': 'Términos de Servicio — Handle',
            'meta_desc': 'Las condiciones de uso de Handle: gratis, sin registro, sin garantía sobre los veredictos de disponibilidad, sin búsqueda de marcas, sin afiliación con TikTok o ByteDance.',
            'og_title': 'Términos de Servicio — Handle',
            'og_desc': 'Las condiciones de uso del generador de nombres TikTok gratis Handle.',
        },
    },
    'de': {
        'home': {
            'title': 'TikTok-Namensgenerator — Verfügbarkeit in Echtzeit prüfen',
            'meta_desc': 'Kostenloser TikTok-Namensgenerator mit Live-Verfügbarkeitscheck. Gib ein Stichwort ein, wähle Nische und Vibe, erhalte 10-20 @-Ideen, die TikToks Regeln entsprechen. Sofort prüfen, ob der Handle noch frei ist. Ohne Anmeldung, ohne Limit.',
            'og_title': 'TikTok-Namensgenerator — Handle-Verfügbarkeit prüfen',
            'og_desc': '@-Ideen für TikTok, die die Plattform-Regeln einhalten. Live-Verfügbarkeitscheck. 17 Vibes, 17 Nischen, ohne Anmeldung.',
        },
        'generator': {
            'title': 'TikTok-Nutzername-Generator — Live-Verfügbarkeitscheck',
            'meta_desc': 'Generiere 10-20 einzigartige TikTok-@-Namen aus Stichwort, Nische und Vibe, und prüfe sofort, welche auf TikTok noch verfügbar sind. Ehrliche Urteile. Ohne Anmeldung, ohne Wasserzeichen.',
            'og_title': 'TikTok-Namensgenerator — Live-Check',
            'og_desc': '10-20 einzigartige TikTok-@-Ideen mit Live-Verfügbarkeitscheck. Ohne Anmeldung.',
        },
        'faq': {
            'title': 'Häufige Fragen — TikTok-Namen | Handle',
            'meta_desc': 'Antworten auf die Fragen, die Leute vor der Wahl eines TikTok-Namens stellen: die Regeln, wie der Verfügbarkeitscheck funktioniert, warum wir "Wahrscheinlich" statt "Verfügbar" sagen, wie du einen passenden Namen findest.',
            'og_title': 'FAQ — TikTok-Namensgenerator',
            'og_desc': 'Echte Antworten auf die Fragen, die vor der Namenswahl gestellt werden.',
        },
        'about': {
            'title': 'Über Handle — Kostenloser TikTok-Namensgenerator mit Live-Check',
            'meta_desc': 'Handle ist ein kostenloser, unabhängiger TikTok-Namensgenerator mit Live-Verfügbarkeitscheck. Unabhängig von TikTok / ByteDance. Open Source, 17 Sprachen, 17 Vibes, 17 Nischen. Ohne Anmeldung, ohne Wasserzeichen.',
            'og_title': 'Über Handle — Unabhängiger TikTok-Namensgenerator',
            'og_desc': 'Ein kostenloser, unabhängiger TikTok-Namensgenerator mit Live-Check.',
        },
        'privacy': {
            'title': 'Datenschutzerklärung — Handle',
            'meta_desc': 'Was Handle sammelt (Server-Logs, ein localStorage-Flag), was nicht (keine Analytik, keine Werbung, kein Tracking) und deine Rechte als Nutzer.',
            'og_title': 'Datenschutzerklärung — Handle',
            'og_desc': 'Was Handle sammelt, was nicht, und deine Rechte.',
        },
        'terms': {
            'title': 'Nutzungsbedingungen — Handle',
            'meta_desc': 'Die Bedingungen für die Nutzung von Handle: kostenlos, ohne Anmeldung, ohne Garantie auf Verfügbarkeitsurteile, ohne Markenrecherche, ohne Verbindung zu TikTok oder ByteDance.',
            'og_title': 'Nutzungsbedingungen — Handle',
            'og_desc': 'Die Nutzungsbedingungen für den kostenlosen Handle TikTok-Namensgenerator.',
        },
    },
    'fr': {
        'home': {
            'title': "Générateur de Nom TikTok — Vérifier la Disponibilité Gratuit",
            'meta_desc': "Générateur de nom TikTok gratuit avec vérification en direct. Tape un mot-clé, choisis une niche et un style, reçois 10-20 idées de @ qui respectent les règles de TikTok et vérifie la disponibilité tout de suite. Sans inscription, sans limite.",
            'og_title': "Générateur de Nom TikTok — Vérifier Disponibilité",
            'og_desc': "Idées de @ qui respectent les règles de TikTok. Vérification en direct. 17 styles, 17 niches, sans inscription.",
        },
        'generator': {
            'title': "Générateur de Pseudo TikTok — Vérification en Direct",
            'meta_desc': "Génère 10-20 idées uniques de @ pour TikTok à partir d'un mot-clé, d'une niche et d'un style, et vérifie tout de suite lesquelles sont encore disponibles. Verdicts honnêtes. Sans inscription, sans filigrane.",
            'og_title': "Générateur TikTok — En Direct",
            'og_desc': "10-20 idées uniques de @ pour TikTok avec vérification de disponibilité en direct. Sans inscription.",
        },
        'faq': {
            'title': "Questions Fréquentes — Pseudo TikTok | Handle",
            'meta_desc': "Les réponses aux vraies questions que les gens se posent avant de choisir un pseudo TikTok : les règles, comment fonctionne la vérification, pourquoi on dit « Probable » et pas « Disponible », comment trouver un nom qui te correspond.",
            'og_title': "FAQ — Pseudo TikTok",
            'og_desc': "Les vraies réponses aux questions que tout le monde se pose avant de choisir un pseudo TikTok.",
        },
        'about': {
            'title': "À Propos de Handle — Générateur TikTok Gratuit avec Vérif en Direct",
            'meta_desc': "Handle est un générateur de pseudo TikTok gratuit et indépendant avec vérification en direct. Indépendant de TikTok / ByteDance. Open source, 17 langues, 17 styles, 17 niches. Sans inscription, sans limite.",
            'og_title': "À Propos de Handle",
            'og_desc': "Un générateur de pseudo TikTok gratuit et indépendant avec vérification en direct.",
        },
        'privacy': {
            'title': "Politique de Confidentialité — Handle",
            'meta_desc': "Ce que Handle collecte (logs serveur, un flag localStorage), ce qu'il ne collecte pas (pas d'analytics, pas de pub, pas de tracking), et tes droits.",
            'og_title': "Politique de Confidentialité — Handle",
            'og_desc': "Ce que Handle collecte, ce qu'il ne collecte pas, et tes droits.",
        },
        'terms': {
            'title': "Conditions d'Utilisation — Handle",
            'meta_desc': "Les conditions d'utilisation de Handle : gratuit, sans inscription, sans garantie sur les verdicts de disponibilité, sans recherche de marques, sans affiliation avec TikTok ou ByteDance.",
            'og_title': "Conditions d'Utilisation — Handle",
            'og_desc': "Les conditions d'utilisation du générateur de pseudo TikTok gratuit Handle.",
        },
    },
    'it': {
        'home': {
            'title': 'Generatore di Nomi TikTok — Controlla Disponibilità Gratis',
            'meta_desc': "Generatore di nomi utente TikTok gratuito con verifica in tempo reale. Inserisci una parola, scegli nicchia e stile, ottieni 10-20 idee di @ che rispettano le regole di TikTok e scopri subito se l'handle è libero. Senza registrazione, senza limiti.",
            'og_title': 'Generatore di Nomi TikTok — Disponibilità in Diretta',
            'og_desc': "Idee di @ per TikTok che rispettano le regole della piattaforma. Verifica in diretta. 17 stili, 17 nicchie, senza registrazione.",
        },
        'generator': {
            'title': 'Generatore Nome TikTok — Controllo Disponibilità in Diretta',
            'meta_desc': 'Genera 10-20 idee uniche di @ per TikTok da parola, nicchia e stile, e controlla subito quali sono ancora disponibili. Verdetti onesti. Senza registrazione, senza watermark.',
            'og_title': 'Generatore TikTok — In Diretta',
            'og_desc': '10-20 idee uniche di @ per TikTok con controllo disponibilità in diretta. Senza registrazione.',
        },
        'faq': {
            'title': 'Domande Frequenti — Nomi TikTok | Handle',
            'meta_desc': 'Risposte alle domande che le persone cercano prima di scegliere un nome TikTok: le regole, come funziona il controllo di disponibilità, perché diciamo "Probabilmente" invece di "Disponibile", come trovare un nome che ti rappresenta.',
            'og_title': 'FAQ — Nomi TikTok',
            'og_desc': 'Risposte vere alle domande che tutti si pongono prima di scegliere un nome TikTok.',
        },
        'about': {
            'title': 'Su Handle — Generatore Nomi TikTok Gratuito con Verifica Live',
            'meta_desc': "Handle è un generatore di nomi TikTok gratuito e indipendente con verifica in diretta. Indipendente da TikTok / ByteDance. Open source, 17 lingue, 17 stili, 17 nicchie. Senza registrazione, senza limiti.",
            'og_title': 'Su Handle — Generatore Nomi TikTok Indipendente',
            'og_desc': 'Un generatore di nomi TikTok gratuito e indipendente con verifica in diretta.',
        },
        'privacy': {
            'title': 'Privacy Policy — Handle',
            'meta_desc': "Cosa raccoglie Handle (log del server, un flag localStorage), cosa non raccoglie (no analytics, no pubblicità, no tracking) e i tuoi diritti.",
            'og_title': 'Privacy Policy — Handle',
            'og_desc': 'Cosa raccoglie Handle, cosa non raccoglie, e i tuoi diritti.',
        },
        'terms': {
            'title': 'Termini di Servizio — Handle',
            'meta_desc': 'I termini per usare Handle: gratuito, senza registrazione, senza garanzia sui verdetti di disponibilità, senza ricerca di marchi, senza affiliazione con TikTok o ByteDance.',
            'og_title': 'Termini di Servizio — Handle',
            'og_desc': 'I termini di utilizzo del generatore di nomi TikTok gratuito Handle.',
        },
    },
    'pt': {
        'home': {
            'title': 'Gerador de Nomes TikTok — Verificar Disponibilidade Grátis',
            'meta_desc': 'Gerador de nomes TikTok grátis com verificação em tempo real. Digite uma palavra, escolha nicho e estilo, receba 10-20 ideias de @ que seguem as regras do TikTok e veja na hora se o handle está livre. Sem cadastro, sem limite.',
            'og_title': 'Gerador de Nomes TikTok — Verificar Disponibilidade',
            'og_desc': 'Ideias de @ que seguem as regras do TikTok. Verificação em tempo real. 17 estilos, 17 nichos, sem cadastro.',
        },
        'generator': {
            'title': 'Gerador de Nicks TikTok — Checagem em Tempo Real',
            'meta_desc': 'Gere 10-20 ideias únicas de @ para TikTok a partir de uma palavra, nicho e estilo, e checa agora quais ainda estão disponíveis. Veredictos honestos. Sem cadastro, sem marca d\'água.',
            'og_title': 'Gerador TikTok — Ao Vivo',
            'og_desc': '10-20 ideias únicas de @ para TikTok com checagem em tempo real. Sem cadastro.',
        },
        'faq': {
            'title': 'Perguntas Frequentes — Nomes para TikTok | Handle',
            'meta_desc': 'Respostas para as perguntas que as pessoas realmente pesquisam antes de escolher um nome para TikTok: as regras, como funciona a checagem de disponibilidade, por que dizemos "Provavelmente" e não "Disponível", como achar um nome que combina com você.',
            'og_title': 'FAQ — Nomes para TikTok',
            'og_desc': 'Respostas reais para as perguntas que todo mundo faz antes de escolher um nome TikTok.',
        },
        'about': {
            'title': 'Sobre o Handle — Gerador de Nomes TikTok Grátis com Checagem em Tempo Real',
            'meta_desc': 'O Handle é um gerador de nomes para TikTok gratuito e independente com checagem em tempo real. Independente do TikTok / ByteDance. Código aberto, 17 idiomas, 17 estilos, 17 nichos. Sem cadastro, sem limites, sem marca d\'água.',
            'og_title': 'Sobre o Handle — Gerador de Nomes TikTok Independente',
            'og_desc': 'Um gerador de nomes TikTok gratuito e independente com checagem em tempo real.',
        },
        'privacy': {
            'title': 'Política de Privacidade — Handle',
            'meta_desc': 'O que o Handle coleta (logs do servidor, um sinalizador em localStorage), o que não coleta (sem analytics, sem anúncios, sem rastreamento) e seus direitos.',
            'og_title': 'Política de Privacidade — Handle',
            'og_desc': 'O que o Handle coleta, o que não coleta, e seus direitos.',
        },
        'terms': {
            'title': 'Termos de Serviço — Handle',
            'meta_desc': 'Os termos sob os quais você pode usar o Handle: gratuito, sem cadastro, sem garantia sobre os veredictos de disponibilidade, sem pesquisa de marcas, sem afiliação com TikTok ou ByteDance.',
            'og_title': 'Termos de Serviço — Handle',
            'og_desc': 'Os termos de uso do gerador de nomes TikTok gratuito Handle.',
        },
    },
    'nl': {
        'home': {
            'title': 'TikTok Gebruikersnaam Generator — Beschikbaarheid Checken',
            'meta_desc': 'Gratis TikTok-gebruikersnaamgenerator met live beschikbaarheidscheck. Typ een trefwoord, kies niche en vibe, krijg 10-20 @-ideeën die voldoen aan de regels van TikTok en check direct of de handle nog vrij is. Geen account, geen limiet.',
            'og_title': 'TikTok Naam Generator — Beschikbaarheid Checken',
            'og_desc': '@-ideeën voor TikTok die aan de platformregels voldoen. Live beschikbaarheidscheck. 17 vibes, 17 niches, geen account.',
        },
        'generator': {
            'title': 'TikTok Naam Generator — Live Beschikbaarheidscheck',
            'meta_desc': 'Genereer 10-20 unieke @-namen voor TikTok uit trefwoord, niche en vibe, en check direct welke nog beschikbaar zijn. Eerlijke oordelen. Geen account, geen watermerk.',
            'og_title': 'TikTok Naam Generator — Live',
            'og_desc': '10-20 unieke @-ideeën voor TikTok met live beschikbaarheidscheck. Geen account.',
        },
        'faq': {
            'title': 'Veelgestelde Vragen — TikTok Namen | Handle',
            'meta_desc': "Antwoorden op de vragen die mensen écht zoeken voor ze een TikTok-naam kiezen: de regels, hoe de beschikbaarheidscheck werkt, waarom we 'Waarschijnlijk' zeggen en niet 'Beschikbaar', hoe je een naam vindt die bij je past.",
            'og_title': 'FAQ — TikTok Naam Generator',
            'og_desc': 'Echte antwoorden op de vragen die iedereen stelt voor het kiezen van een TikTok-naam.',
        },
        'about': {
            'title': 'Over Handle — Gratis TikTok Naam Generator met Live Check',
            'meta_desc': 'Handle is een gratis, onafhankelijke TikTok-gebruikersnaamgenerator met live beschikbaarheidscheck. Onafhankelijk van TikTok / ByteDance. Open source, 17 talen, 17 vibes, 17 niches. Geen account, geen limieten, geen watermerk.',
            'og_title': 'Over Handle — Onafhankelijke TikTok Naam Generator',
            'og_desc': 'Een gratis, onafhankelijke TikTok-gebruikersnaamgenerator met live beschikbaarheidscheck.',
        },
        'privacy': {
            'title': 'Privacybeleid — Handle',
            'meta_desc': 'Wat Handle verzamelt (serverlogs, één localStorage-vlag), wat niet (geen analytics, geen advertenties, geen tracking), en jouw rechten.',
            'og_title': 'Privacybeleid — Handle',
            'og_desc': 'Wat Handle verzamelt, wat niet, en jouw rechten.',
        },
        'terms': {
            'title': 'Servicevoorwaarden — Handle',
            'meta_desc': 'De voorwaarden waaronder je Handle mag gebruiken: gratis, geen account, geen garantie op beschikbaarheidsuitspraken, geen merkenonderzoek, geen banden met TikTok of ByteDance.',
            'og_title': 'Servicevoorwaarden — Handle',
            'og_desc': 'De gebruiksvoorwaarden van de gratis Handle TikTok-gebruikersnaamgenerator.',
        },
    },
    'pl': {
        'home': {
            'title': 'Generator Nazw TikTok — Sprawdź Dostępność Za Darmo',
            'meta_desc': 'Darmowy generator nazw użytkowników TikTok z natychmiastowym sprawdzaniem dostępności. Wpisz słowo kluczowe, wybierz niszę i styl, otrzymaj 10-20 pomysłów na @ zgodnych z zasadami TikToka. Bez rejestracji, bez limitu.',
            'og_title': 'Generator Nazw TikTok — Sprawdź Dostępność',
            'og_desc': 'Pomysły na @ zgodne z zasadami TikToka. Sprawdzanie na żywo. 17 stylów, 17 nisz, bez rejestracji.',
        },
        'generator': {
            'title': 'Generator Nicków TikTok — Sprawdzanie Dostępności na Żywo',
            'meta_desc': 'Wygeneruj 10-20 unikalnych @-nicków dla TikToka ze słowa kluczowego, niszy i stylu, i od razu sprawdź, które są jeszcze dostępne. Uczciwe wyniki. Bez rejestracji, bez znaku wodnego.',
            'og_title': 'Generator TikTok — Na Żywo',
            'og_desc': '10-20 unikalnych @-pomysłów dla TikToka ze sprawdzaniem dostępności na żywo. Bez rejestracji.',
        },
        'faq': {
            'title': 'Najczęściej Zadawane Pytania — Nazwy TikTok | Handle',
            'meta_desc': 'Odpowiedzi na pytania, które ludzie naprawdę zadają przed wyborem nicku na TikToku: zasady, jak działa sprawdzanie dostępności, dlaczego mówimy "Prawdopodobnie" zamiast "Dostępne", jak znaleźć nick, który do ciebie pasuje.',
            'og_title': 'FAQ — Nazwy TikTok',
            'og_desc': 'Prawdziwe odpowiedzi na pytania zadawane przed wyborem nicku na TikToku.',
        },
        'about': {
            'title': 'O Handle — Darmowy Generator Nicków TikTok ze Sprawdzaniem na Żywo',
            'meta_desc': 'Handle to darmowy, niezależny generator nicków TikTok ze sprawdzaniem dostępności na żywo. Niezależny od TikTok / ByteDance. Open source, 17 języków, 17 stylów, 17 nisz. Bez rejestracji, bez limitów, bez znaku wodnego.',
            'og_title': 'O Handle — Niezależny Generator Nicków TikTok',
            'og_desc': 'Darmowy, niezależny generator nicków TikTok ze sprawdzaniem dostępności na żywo.',
        },
        'privacy': {
            'title': 'Polityka Prywatności — Handle',
            'meta_desc': 'Co Handle zbiera (logi serwera, jedna flaga w localStorage), czego nie zbiera (bez analityki, bez reklam, bez śledzenia) i Twoje prawa.',
            'og_title': 'Polityka Prywatności — Handle',
            'og_desc': 'Co Handle zbiera, czego nie, i Twoje prawa.',
        },
        'terms': {
            'title': 'Warunki Korzystania — Handle',
            'meta_desc': 'Warunki, na jakich możesz korzystać z Handle: za darmo, bez rejestracji, bez gwarancji na wyniki dostępności, bez wyszukiwania znaków towarowych, bez powiązań z TikTokiem ani ByteDance.',
            'og_title': 'Warunki Korzystania — Handle',
            'og_desc': 'Warunki korzystania z darmowego generatora nicków TikTok Handle.',
        },
    },
    'ru': {
        'home': {
            'title': 'Генератор Никнеймов TikTok — Проверить Занятость Бесплатно',
            'meta_desc': 'Бесплатный генератор никнеймов для TikTok с проверкой занятости в реальном времени. Введите ключевое слово, выберите нишу и стиль, получите 10-20 уникальных идей для @ по правилам TikTok. Без регистрации, без лимитов.',
            'og_title': 'Генератор Никнеймов TikTok — Проверка Занятости',
            'og_desc': 'Уникальные ники для TikTok по правилам платформы. Проверка в реальном времени. 17 стилей, 17 ниш, без регистрации.',
        },
        'generator': {
            'title': 'Генератор Ников TikTok — Проверка в Реальном Времени',
            'meta_desc': 'Генерируйте 10-20 уникальных @-ников для TikTok по ключевому слову, нише и стилю, и сразу проверяйте, какие из них ещё свободны. Честные результаты. Без регистрации, без водяных знаков.',
            'og_title': 'Генератор TikTok — Онлайн',
            'og_desc': '10-20 уникальных @-идей для TikTok с проверкой в реальном времени. Без регистрации.',
        },
        'faq': {
            'title': 'Частые Вопросы — Ники для TikTok | Handle',
            'meta_desc': 'Ответы на вопросы, которые люди реально ищут перед выбором ника для TikTok: правила, как работает проверка занятости, почему мы говорим «Вероятно свободен», а не «Свободен», как найти ник, который вам подходит.',
            'og_title': 'FAQ — Ники для TikTok',
            'og_desc': 'Честные ответы на вопросы, которые задают перед выбором ника для TikTok.',
        },
        'about': {
            'title': 'О Handle — Бесплатный Генератор Ников TikTok с Онлайн-Проверкой',
            'meta_desc': 'Handle — это бесплатный, независимый генератор ников для TikTok с проверкой занятости в реальном времени. Не связан с TikTok / ByteDance. Открытый код, 17 языков, 17 стилей, 17 ниш. Без регистрации, без лимитов, без водяных знаков.',
            'og_title': 'О Handle — Независимый Генератор Ников TikTok',
            'og_desc': 'Бесплатный, независимый генератор ников для TikTok с онлайн-проверкой.',
        },
        'privacy': {
            'title': 'Политика Конфиденциальности — Handle',
            'meta_desc': 'Что Handle собирает (логи сервера, один флаг в localStorage), что не собирает (без аналитики, без рекламы, без отслеживания) и ваши права.',
            'og_title': 'Политика Конфиденциальности — Handle',
            'og_desc': 'Что Handle собирает, что не собирает, и ваши права.',
        },
        'terms': {
            'title': 'Условия Использования — Handle',
            'meta_desc': 'Условия, на которых вы можете пользоваться Handle: бесплатно, без регистрации, без гарантий на результаты проверки занятости, без поиска торговых марок, без связи с TikTok или ByteDance.',
            'og_title': 'Условия Использования — Handle',
            'og_desc': 'Условия использования бесплатного генератора ников Handle для TikTok.',
        },
    },
    'zh': {
        'home': {
            'title': 'TikTok 用户名生成器 — 实时检测用户名是否可用',
            'meta_desc': '免费 TikTok 用户名生成器,实时检测可用性。输入关键词,选择领域和风格,获取 10-20 个符合 TikTok 规则的用户名创意,立即查看是否被占用。无需注册,无次数限制。',
            'og_title': 'TikTok 用户名生成器 — 免费在线生成',
            'og_desc': '符合 TikTok 规则的 @ 用户名创意。实时检测可用性。17 种风格,17 个领域,无需注册。',
        },
        'generator': {
            'title': 'TikTok 用户名生成器 — 实时可用性检测',
            'meta_desc': '根据关键词、领域和风格生成 10-20 个独特的 @ 用户名创意,实时检查是否在 TikTok 上仍可使用。诚实的判断结果。无需注册,无水印。',
            'og_title': 'TikTok 用户名生成器 — 实时',
            'og_desc': '10-20 个独特的 TikTok @ 用户名创意,实时可用性检测。无需注册。',
        },
        'faq': {
            'title': '常见问题 — TikTok 用户名 | Handle',
            'meta_desc': '回答人们在选择 TikTok 用户名前真正搜索的问题:规则、可用性检测如何运作、为什么我们说"可能可用"而不是"可用"、如何找到适合自己的名字。',
            'og_title': '常见问题 — TikTok 用户名',
            'og_desc': '回答人们在选择 TikTok 用户名前真正想问的问题。',
        },
        'about': {
            'title': '关于 Handle — 免费的 TikTok 用户名生成器,带实时检测',
            'meta_desc': 'Handle 是一个免费、独立的 TikTok 用户名生成器,带实时可用性检测。独立于 TikTok / ByteDance。开源,17 种语言,17 种风格,17 个领域。无需注册,无使用限制,无水印。',
            'og_title': '关于 Handle — 独立的 TikTok 用户名生成器',
            'og_desc': '一个免费、独立的 TikTok 用户名生成器,带实时可用性检测。',
        },
        'privacy': {
            'title': '隐私政策 — Handle',
            'meta_desc': 'Handle 收集什么(服务器日志,一个 localStorage 标记),不收集什么(无分析,无广告,无第三方跟踪)以及你的权利。',
            'og_title': '隐私政策 — Handle',
            'og_desc': 'Handle 收集什么,不收集什么,以及你的权利。',
        },
        'terms': {
            'title': '服务条款 — Handle',
            'meta_desc': '你可以使用 Handle 的条款:免费,无需注册,对可用性判断不提供保证,不做商标搜索,与 TikTok 或 ByteDance 没有关联。',
            'og_title': '服务条款 — Handle',
            'og_desc': '免费 Handle TikTok 用户名生成器的使用条款。',
        },
    },
    'vi': {
        'home': {
            'title': 'Trình Tạo Tên TikTok — Kiểm Tra Tên Đã Dùng Miễn Phí',
            'meta_desc': 'Trình tạo tên TikTok miễn phí với kiểm tra trùng lặp theo thời gian thực. Nhập từ khóa, chọn ngách và phong cách, nhận 10-20 ý tưởng tên @ theo đúng quy tắc TikTok và xem ngay tên nào còn trống. Không cần đăng ký, không giới hạn.',
            'og_title': 'Trình Tạo Tên TikTok — Tên Hay, Độc Đáo',
            'og_desc': 'Ý tưởng tên @ theo quy tắc TikTok. Kiểm tra theo thời gian thực. 17 phong cách, 17 ngách, không cần đăng ký.',
        },
        'generator': {
            'title': 'Trình Tạo Nick TikTok — Kiểm Tra Trùng Lặp Trực Tiếp',
            'meta_desc': 'Tạo 10-20 ý tưởng @ duy nhất cho TikTok từ từ khóa, ngách và phong cách, và kiểm tra ngay những tên nào còn trống. Đánh giá trung thực. Không đăng ký, không watermark.',
            'og_title': 'Trình Tạo TikTok — Trực Tiếp',
            'og_desc': '10-20 ý tưởng @ duy nhất cho TikTok với kiểm tra trùng lặp theo thời gian thực. Không đăng ký.',
        },
        'faq': {
            'title': 'Câu Hỏi Thường Gặp — Tên TikTok | Handle',
            'meta_desc': 'Trả lời những câu hỏi mà mọi người thực sự tìm kiếm trước khi chọn tên TikTok: các quy tắc, cách hoạt động của kiểm tra trùng lặp, tại sao nói "Có thể trống" thay vì "Trống", cách tìm tên phù hợp với bạn.',
            'og_title': 'FAQ — Tên TikTok',
            'og_desc': 'Câu trả lời thực sự cho những câu hỏi mà ai cũng đặt ra trước khi chọn tên TikTok.',
        },
        'about': {
            'title': 'Về Handle — Trình Tạo Tên TikTok Miễn Phí với Kiểm Tra Trực Tiếp',
            'meta_desc': 'Handle là trình tạo tên TikTok miễn phí và độc lập với kiểm tra trùng lặp theo thời gian thực. Độc lập với TikTok / ByteDance. Mã nguồn mở, 17 ngôn ngữ, 17 phong cách, 17 ngách. Không đăng ký, không giới hạn, không watermark.',
            'og_title': 'Về Handle — Trình Tạo Tên TikTok Độc Lập',
            'og_desc': 'Một trình tạo tên TikTok miễn phí và độc lập với kiểm tra theo thời gian thực.',
        },
        'privacy': {
            'title': 'Chính Sách Bảo Mật — Handle',
            'meta_desc': 'Handle thu thập gì (log máy chủ, một cờ trong localStorage), không thu thập gì (không phân tích, không quảng cáo, không theo dõi), và quyền của bạn.',
            'og_title': 'Chính Sách Bảo Mật — Handle',
            'og_desc': 'Handle thu thập gì, không thu thập gì, và quyền của bạn.',
        },
        'terms': {
            'title': 'Điều Khoản Dịch Vụ — Handle',
            'meta_desc': 'Các điều khoản bạn có thể sử dụng Handle: miễn phí, không đăng ký, không bảo đảm về kết quả kiểm tra, không tra cứu thương hiệu, không liên kết với TikTok hay ByteDance.',
            'og_title': 'Điều Khoản Dịch Vụ — Handle',
            'og_desc': 'Các điều khoản sử dụng của trình tạo tên TikTok miễn phí Handle.',
        },
    },
    'id': {
        'home': {
            'title': 'Pembuat Nama TikTok — Cek Ketersediaan Gratis',
            'meta_desc': 'Pembuat nama TikTok gratis dengan pengecekan ketersediaan langsung. Ketik kata kunci, pilih niche dan vibe, dapatkan 10-20 ide @ yang sesuai aturan TikTok dan cek apakah handle masih tersedia. Tanpa daftar, tanpa batas.',
            'og_title': 'Pembuat Nama TikTok — Cek Ketersediaan',
            'og_desc': 'Ide @ yang sesuai aturan TikTok. Pengecekan langsung. 17 vibe, 17 niche, tanpa daftar.',
        },
        'generator': {
            'title': 'Pembuat Nama Pengguna TikTok — Cek Ketersediaan Langsung',
            'meta_desc': 'Hasilkan 10-20 ide @ unik untuk TikTok dari kata kunci, niche, dan vibe, lalu cek langsung mana yang masih tersedia. Putusan yang jujur. Tanpa daftar, tanpa watermark.',
            'og_title': 'Pembuat TikTok — Langsung',
            'og_desc': '10-20 ide @ unik untuk TikTok dengan pengecekan ketersediaan langsung. Tanpa daftar.',
        },
        'faq': {
            'title': 'FAQ — Nama TikTok | Handle',
            'meta_desc': 'Jawaban atas pertanyaan yang benar-benar dicari orang sebelum memilih nama TikTok: aturannya, cara kerja pengecekan ketersediaan, mengapa kami bilang "Kemungkinan tersedia" bukan "Tersedia", cara menemukan nama yang cocok untuk Anda.',
            'og_title': 'FAQ — Nama TikTok',
            'og_desc': 'Jawaban nyata untuk pertanyaan yang diajukan semua orang sebelum memilih nama TikTok.',
        },
        'about': {
            'title': 'Tentang Handle — Pembuat Nama TikTok Gratis dengan Cek Langsung',
            'meta_desc': 'Handle adalah pembuat nama TikTok gratis dan independen dengan pengecekan ketersediaan langsung. Independen dari TikTok / ByteDance. Open source, 17 bahasa, 17 vibe, 17 niche. Tanpa daftar, tanpa batas, tanpa watermark.',
            'og_title': 'Tentang Handle — Pembuat Nama TikTok Independen',
            'og_desc': 'Pembuat nama TikTok gratis dan independen dengan pengecekan langsung.',
        },
        'privacy': {
            'title': 'Kebijakan Privasi — Handle',
            'meta_desc': 'Apa yang dikumpulkan Handle (log server, satu flag di localStorage), apa yang tidak (tanpa analitik, tanpa iklan, tanpa pelacakan), dan hak Anda.',
            'og_title': 'Kebijakan Privasi — Handle',
            'og_desc': 'Apa yang dikumpulkan Handle, apa yang tidak, dan hak Anda.',
        },
        'terms': {
            'title': 'Ketentuan Layanan — Handle',
            'meta_desc': 'Ketentuan di mana Anda dapat menggunakan Handle: gratis, tanpa daftar, tanpa jaminan atas putusan ketersediaan, tanpa pencarian merek dagang, tanpa afiliasi dengan TikTok atau ByteDance.',
            'og_title': 'Ketentuan Layanan — Handle',
            'og_desc': 'Ketentuan penggunaan pembuat nama TikTok gratis Handle.',
        },
    },
    'ms': {
        'home': {
            'title': 'Penjana Nama TikTok — Semak Ketersediaan Percuma',
            'meta_desc': 'Penjana nama TikTok percuma dengan semakan ketersediaan secara langsung. Taip kata kunci, pilih niche dan gaya, dapat 10-20 idea @ yang ikut peraturan TikTok dan semak dengan segera jika handle masih tersedia. Tanpa daftar, tanpa had.',
            'og_title': 'Penjana Nama TikTok — Semak Ketersediaan',
            'og_desc': 'Idea @ yang ikut peraturan TikTok. Semakan langsung. 17 gaya, 17 niche, tanpa daftar.',
        },
        'generator': {
            'title': 'Penjana Nama Pengguna TikTok — Semakan Langsung',
            'meta_desc': 'Jana 10-20 idea @ unik untuk TikTok daripada kata kunci, niche dan gaya, dan semak segera yang mana masih tersedia. Putusan yang jujur. Tanpa daftar, tanpa tera air.',
            'og_title': 'Penjana TikTok — Langsung',
            'og_desc': '10-20 idea @ unik untuk TikTok dengan semakan ketersediaan secara langsung. Tanpa daftar.',
        },
        'faq': {
            'title': 'Soalan Lazim — Nama TikTok | Handle',
            'meta_desc': 'Jawapan kepada soalan yang benar-benar dicari orang sebelum memilih nama TikTok: peraturannya, cara semakan ketersediaan berfungsi, mengapa kami kata "Kemungkinan tersedia" dan bukan "Tersedia", cara mencari nama yang sesuai untuk anda.',
            'og_title': 'Soalan Lazim — Nama TikTok',
            'og_desc': 'Jawapan sebenar kepada soalan yang ditanya semua orang sebelum memilih nama TikTok.',
        },
        'about': {
            'title': 'Mengenai Handle — Penjana Nama TikTok Percuma dengan Semakan Langsung',
            'meta_desc': 'Handle ialah penjana nama TikTok percuma dan bebas dengan semakan ketersediaan secara langsung. Bebas dari TikTok / ByteDance. Sumber terbuka, 17 bahasa, 17 gaya, 17 niche. Tanpa daftar, tanpa had, tanpa tera air.',
            'og_title': 'Mengenai Handle — Penjana Nama TikTok Bebas',
            'og_desc': 'Penjana nama TikTok percuma dan bebas dengan semakan secara langsung.',
        },
        'privacy': {
            'title': 'Dasar Privasi — Handle',
            'meta_desc': 'Apa yang dikumpulkan Handle (log pelayan, satu flag dalam localStorage), apa yang tidak (tanpa analitik, tanpa iklan, tanpa penjejakan), dan hak anda.',
            'og_title': 'Dasar Privasi — Handle',
            'og_desc': 'Apa yang dikumpulkan Handle, apa yang tidak, dan hak anda.',
        },
        'terms': {
            'title': 'Terma Perkhidmatan — Handle',
            'meta_desc': 'Terma di mana anda boleh menggunakan Handle: percuma, tanpa daftar, tanpa jaminan atas putusan ketersediaan, tanpa carian tanda dagangan, tanpa afiliasi dengan TikTok atau ByteDance.',
            'og_title': 'Terma Perkhidmatan — Handle',
            'og_desc': 'Terma penggunaan penjana nama TikTok percuma Handle.',
        },
    },
    'tl': {
        'home': {
            'title': 'Tagagawa ng Pangalan sa TikTok — Suriin ang Availability Libre',
            'meta_desc': 'Tagagawa ng pangalan sa TikTok na libre na may live availability check. Mag-type ng keyword, pumili ng niche at vibe, makatanggap ng 10-20 ideya ng @ na sumusunod sa mga patakaran ng TikTok at agad na tingnan kung available pa ang handle. Walang signup, walang limitasyon.',
            'og_title': 'Tagagawa ng Pangalan sa TikTok — Live Check',
            'og_desc': 'Mga ideya ng @ na sumusunod sa mga patakaran ng TikTok. Live availability check. 17 vibe, 17 niche, walang signup.',
        },
        'generator': {
            'title': 'Tagagawa ng Username sa TikTok — Live na Availability Check',
            'meta_desc': 'Bumuo ng 10-20 natatanging ideya ng @ para sa TikTok mula sa keyword, niche at vibe, at agad na tingnan kung alin ang available pa. Makatarungang hatol. Walang signup, walang watermark.',
            'og_title': 'Tagagawa ng TikTok — Live',
            'og_desc': '10-20 natatanging ideya ng @ para sa TikTok na may live availability check. Walang signup.',
        },
        'faq': {
            'title': 'Mga Madalas Itanong — Pangalan sa TikTok | Handle',
            'meta_desc': 'Mga sagot sa mga tanong na talagang hinahanap ng mga tao bago pumili ng pangalan sa TikTok: ang mga patakaran, paano gumagana ang availability check, bakit sinasabi namin na "Malamang available" sa halip na "Available", paano makahanap ng pangalan na bagay sa iyo.',
            'og_title': 'FAQ — Pangalan sa TikTok',
            'og_desc': 'Totoong mga sagot sa mga tanong na itinatanong ng lahat bago pumili ng pangalan sa TikTok.',
        },
        'about': {
            'title': 'Tungkol sa Handle — Libreng Tagagawa ng Pangalan sa TikTok na may Live Check',
            'meta_desc': 'Ang Handle ay isang libre at independiyenteng tagagawa ng pangalan sa TikTok na may live availability check. Independiyente mula sa TikTok / ByteDance. Open source, 17 wika, 17 vibe, 17 niche. Walang signup, walang limitasyon, walang watermark.',
            'og_title': 'Tungkol sa Handle — Independiyenteng Tagagawa ng Pangalan sa TikTok',
            'og_desc': 'Isang libre at independiyenteng tagagawa ng pangalan sa TikTok na may live availability check.',
        },
        'privacy': {
            'title': 'Patakaran sa Privacy — Handle',
            'meta_desc': 'Ano ang kinokolekta ng Handle (mga log ng server, isang flag sa localStorage), ano ang hindi (walang analytics, walang ads, walang tracking), at ang iyong mga karapatan.',
            'og_title': 'Patakaran sa Privacy — Handle',
            'og_desc': 'Ano ang kinokolekta ng Handle, ano ang hindi, at ang iyong mga karapatan.',
        },
        'terms': {
            'title': 'Mga Tuntunin ng Serbisyo — Handle',
            'meta_desc': 'Ang mga tuntunin kung saan maaari mong gamitin ang Handle: libre, walang signup, walang garantiya sa mga hatol sa availability, walang paghahanap ng trademark, walang affiliasyon sa TikTok o ByteDance.',
            'og_title': 'Mga Tuntunin ng Serbisyo — Handle',
            'og_desc': 'Ang mga tuntunin ng paggamit para sa libreng tagagawa ng pangalan sa TikTok na Handle.',
        },
    },
    'hi': {
        'home': {
            'title': 'TikTok यूज़रनेम जेनरेटर — मुफ़्त उपलब्धता जाँच',
            'meta_desc': 'लाइव उपलब्धता जाँच के साथ मुफ़्त TikTok यूज़रनेम जेनरेटर। कीवर्ड, निश और वाइब चुनें, 10-20 @ आइडिया पाएं जो TikTok के नियमों का पालन करती हैं और तुरंत देखें कि हैंडल अभी उपलब्ध है या नहीं। बिना साइनअप, बिना सीमा।',
            'og_title': 'TikTok यूज़रनेम जेनरेटर — उपलब्धता जाँचें',
            'og_desc': 'TikTok नियमों का पालन करने वाले @ आइडिया। लाइव उपलब्धता जाँच। 17 वाइब, 17 निश, बिना साइनअप।',
        },
        'generator': {
            'title': 'TikTok यूज़रनेम जेनरेटर — लाइव उपलब्धता जाँच',
            'meta_desc': 'कीवर्ड, निश और वाइब से 10-20 अनूठे @ नाम बनाएं और तुरंत देखें कि कौन-से अभी TikTok पर उपलब्ध हैं। ईमानदार फैसले। बिना साइनअप, बिना वॉटरमार्क।',
            'og_title': 'TikTok जेनरेटर — लाइव',
            'og_desc': '10-20 अनूठे TikTok @ आइडिया, लाइव उपलब्धता जाँच के साथ। बिना साइनअप।',
        },
        'faq': {
            'title': 'अक्सर पूछे जाने वाले सवाल — TikTok नाम | Handle',
            'meta_desc': 'उन सवालों के जवाब जो लोग वाकई में TikTok नाम चुनने से पहले खोजते हैं: नियम, उपलब्धता जाँच कैसे काम करती है, हम "उपलब्ध" के बजाय "संभवतः उपलब्ध" क्यों कहते हैं, अपने लिए सही नाम कैसे खोजें।',
            'og_title': 'FAQ — TikTok नाम',
            'og_desc': 'उन सवालों के असली जवाब जो हर कोई TikTok नाम चुनने से पहले पूछता है।',
        },
        'about': {
            'title': 'Handle के बारे में — लाइव जाँच के साथ मुफ़्त TikTok जेनरेटर',
            'meta_desc': 'Handle एक मुफ़्त, स्वतंत्र TikTok यूज़रनेम जेनरेटर है जिसमें लाइव उपलब्धता जाँच है। TikTok / ByteDance से स्वतंत्र। ओपन सोर्स, 17 भाषाएं, 17 वाइब, 17 निश। बिना साइनअप, बिना सीमा, बिना वॉटरमार्क।',
            'og_title': 'Handle के बारे में — स्वतंत्र TikTok जेनरेटर',
            'og_desc': 'लाइव उपलब्धता जाँच के साथ एक मुफ़्त, स्वतंत्र TikTok जेनरेटर।',
        },
        'privacy': {
            'title': 'गोपनीयता नीति — Handle',
            'meta_desc': 'Handle क्या एकत्र करता है (सर्वर लॉग, एक localStorage फ़्लैग), क्या नहीं (बिना एनालिटिक्स, बिना विज्ञापन, बिना ट्रैकिंग), और आपके अधिकार।',
            'og_title': 'गोपनीयता नीति — Handle',
            'og_desc': 'Handle क्या एकत्र करता है, क्या नहीं, और आपके अधिकार।',
        },
        'terms': {
            'title': 'सेवा की शर्तें — Handle',
            'meta_desc': 'उन शर्तें जिनके तहत आप Handle का उपयोग कर सकते हैं: मुफ़्त, बिना साइनअप, उपलब्धता फैसलों पर कोई गारंटी नहीं, ट्रेडमार्क खोज नहीं, TikTok या ByteDance के साथ कोई संबद्धता नहीं।',
            'og_title': 'सेवा की शर्तें — Handle',
            'og_desc': 'मुफ़्त Handle TikTok जेनरेटर की उपयोग की शर्तें।',
        },
    },
    'bn': {
        'home': {
            'title': 'TikTok ইউজারনেম জেনারেটর — ফ্রি অ্যাভেইলেবিলিটি চেক',
            'meta_desc': 'লাইভ অ্যাভেইলেবিলিটি চেক সহ ফ্রি TikTok ইউজারনেম জেনারেটর। কীওয়ার্ড, নিশ এবং ভাইব বাছুন, 10-20টি @ আইডিয়া পান যেগুলো TikTok-এর নিয়ম মানে এবং সাথে সাথে দেখুন হ্যান্ডেলটি এখনো অ্যাভেইলেবল কি না। সাইনআপ লাগবে না, কোনো সীমা নেই।',
            'og_title': 'TikTok ইউজারনেম জেনারেটর — অ্যাভেইলেবিলিটি চেক',
            'og_desc': 'TikTok-এর নিয়ম মানে এমন @ আইডিয়া। লাইভ অ্যাভেইলেবিলিটি চেক। 17 ভাইব, 17 নিশ, সাইনআপ লাগবে না।',
        },
        'generator': {
            'title': 'TikTok ইউজারনেম জেনারেটর — লাইভ অ্যাভেইলেবিলিটি চেক',
            'meta_desc': 'কীওয়ার্ড, নিশ এবং ভাইব থেকে 10-20টি ইউনিক @ আইডিয়া তৈরি করুন এবং এখনই দেখুন কোনগুলো TikTok-এ এখনো অ্যাভেইলেবল। সৎ রায়। সাইনআপ লাগবে না, কোনো ওয়াটারমার্ক নেই।',
            'og_title': 'TikTok জেনারেটর — লাইভ',
            'og_desc': '10-20টি ইউনিক TikTok @ আইডিয়া, লাইভ অ্যাভেইলেবিলিটি চেক সহ। সাইনআপ লাগবে না।',
        },
        'faq': {
            'title': 'প্রায়শই জিজ্ঞাসিত প্রশ্ন — TikTok নাম | Handle',
            'meta_desc': 'TikTok নাম বাছাই করার আগে মানুষ আসলে যেসব প্রশ্ন খোঁজে তার উত্তর: নিয়মগুলো, অ্যাভেইলেবিলিটি চেক কীভাবে কাজ করে, আমরা "অ্যাভেইলেবল" না বলে "সম্ভবত অ্যাভেইলেবল" কেন বলি, আপনার জন্য মানানসই নাম কীভাবে খুঁজবেন।',
            'og_title': 'FAQ — TikTok নাম',
            'og_desc': 'TikTok নাম বাছাইয়ের আগে সবার জিজ্ঞাসিত আসল উত্তর।',
        },
        'about': {
            'title': 'Handle সম্পর্কে — লাইভ চেক সহ ফ্রি TikTok জেনারেটর',
            'meta_desc': 'Handle হলো একটি ফ্রি, স্বতন্ত্র TikTok ইউজারনেম জেনারেটর যেটিতে লাইভ অ্যাভেইলেবিলিটি চেক আছে। TikTok / ByteDance থেকে স্বতন্ত্র। ওপেন সোর্স, 17টি ভাষা, 17টি ভাইব, 17টি নিশ। সাইনআপ লাগবে না, কোনো সীমা নেই, কোনো ওয়াটারমার্ক নেই।',
            'og_title': 'Handle সম্পর্কে — স্বতন্ত্র TikTok জেনারেটর',
            'og_desc': 'লাইভ অ্যাভেইলেবিলিটি চেক সহ একটি ফ্রি, স্বতন্ত্র TikTok জেনারেটর।',
        },
        'privacy': {
            'title': 'গোপনীয়তা নীতি — Handle',
            'meta_desc': 'Handle কী সংগ্রহ করে (সার্ভার লগ, একটি localStorage ফ্ল্যাগ), কী করে না (কোনো অ্যানালিটিক্স নেই, কোনো বিজ্ঞাপন নেই, কোনো ট্র্যাকিং নেই), এবং আপনার অধিকার।',
            'og_title': 'গোপনীয়তা নীতি — Handle',
            'og_desc': 'Handle কী সংগ্রহ করে, কী করে না, এবং আপনার অধিকার।',
        },
        'terms': {
            'title': 'সেবার শর্তাবলী — Handle',
            'meta_desc': 'Handle ব্যবহারের শর্তাবলী: ফ্রি, সাইনআপ লাগবে না, অ্যাভেইলেবিলিটি রায়ের কোনো গ্যারান্টি নেই, ট্রেডমার্ক অনুসন্ধান নেই, TikTok বা ByteDance-এর সাথে কোনো সম্পর্ক নেই।',
            'og_title': 'সেবার শর্তাবলী — Handle',
            'og_desc': 'ফ্রি Handle TikTok জেনারেটরের ব্যবহারের শর্তাবলী।',
        },
    },
    'ur': {
        'home': {
            'title': 'TikTok یوزرنیم جنریٹر — مفت دستیابی چیک',
            'meta_desc': 'لائیو دستیابی چیک کے ساتھ مفت TikTok یوزرنیم جنریٹر۔ کلیدی لفظ، نچ اور وائب منتخب کریں، 10-20 @ آئیڈیاز حاصل کریں جو TikTok کے قوانین پر پورا اترتی ہوں اور فوراً دیکھیں کہ ہینڈل ابھی دستیاب ہے یا نہیں۔ سائن اپ نہیں، کوئی حد نہیں۔',
            'og_title': 'TikTok یوزرنیم جنریٹر — دستیابی چیک',
            'og_desc': 'TikTok قوانین پر پورا اترنے والے @ آئیڈیاز۔ لائیو دستیابی چیک۔ 17 وائب، 17 نچ، سائن اپ نہیں۔',
        },
        'generator': {
            'title': 'TikTok یوزرنیم جنریٹر — لائیو دستیابی چیک',
            'meta_desc': 'کلیدی لفظ، نچ اور وائب سے 10-20 منفرد @ آئیڈیاز بنائیں اور فوراً دیکھیں کہ کون سے ابھی TikTok پر دستیاب ہیں۔ ایماندارانہ فیصلے۔ سائن اپ نہیں، کوئی واٹر مارک نہیں۔',
            'og_title': 'TikTok جنریٹر — لائیو',
            'og_desc': '10-20 منفرد TikTok @ آئیڈیاز، لائیو دستیابی چیک کے ساتھ۔ سائن اپ نہیں۔',
        },
        'faq': {
            'title': 'اکثر پوچھے گئے سوالات — TikTok نام | Handle',
            'meta_desc': 'ان سوالات کے جوابات جو لوگ واقعی TikTok نام منتخب کرنے سے پہلے تلاش کرتے ہیں: قوانین، دستیابی چیک کیسے کام کرتا ہے، ہم "دستیاب" کی بجائے "ممکنہ طور پر دستیاب" کیوں کہتے ہیں، آپ کے لیے مناسب نام کیسے تلاش کریں۔',
            'og_title': 'FAQ — TikTok نام',
            'og_desc': 'ان سوالات کے اصل جوابات جو TikTok نام منتخب کرنے سے پہلے ہر کوئی پوچھتا ہے۔',
        },
        'about': {
            'title': 'Handle کے بارے میں — لائیو چیک کے ساتھ مفت TikTok جنریٹر',
            'meta_desc': 'Handle ایک مفت، آزاد TikTok یوزرنیم جنریٹر ہے جس میں لائیو دستیابی چیک ہے۔ TikTok / ByteDance سے آزاد۔ اوپن سورس، 17 زبانیں، 17 وائب، 17 نچ۔ سائن اپ نہیں، کوئی حد نہیں، کوئی واٹر مارک نہیں۔',
            'og_title': 'Handle کے بارے میں — آزاد TikTok جنریٹر',
            'og_desc': 'لائیو دستیابی چیک کے ساتھ ایک مفت، آزاد TikTok جنریٹر۔',
        },
        'privacy': {
            'title': 'رازداری کی پالیسی — Handle',
            'meta_desc': 'Handle کیا جمع کرتا ہے (سرور لاگز، ایک localStorage فلیگ)، کیا نہیں (بغیر اینالیٹکس، بغیر اشتہارات، بغیر ٹریکنگ)، اور آپ کے حقوق۔',
            'og_title': 'رازداری کی پالیسی — Handle',
            'og_desc': 'Handle کیا جمع کرتا ہے، کیا نہیں، اور آپ کے حقوق۔',
        },
        'terms': {
            'title': 'سروس کی شرائط — Handle',
            'meta_desc': 'وہ شرائط جن کے تحت آپ Handle استعمال کر سکتے ہیں: مفت، بغیر سائن اپ، دستیابی فیصلوں کی کوئی ضمانت نہیں، ٹریڈ مارک تلاش نہیں، TikTok یا ByteDance سے کوئی وابستگی نہیں۔',
            'og_title': 'سروس کی شرائط — Handle',
            'og_desc': 'مفت Handle TikTok جنریٹر کی استعمال کی شرائط۔',
        },
    },
    'ar': {
        'home': {
            'title': 'مولد أسماء تيك توك — تحقق من التوفر مجانًا',
            'meta_desc': 'مولد أسماء تيك توك مجاني مع تحقق من التوفر مباشرة. اكتب كلمة مفتاحية، اختر مجالًا وأسلوبًا، احصل على 10-20 فكرة @ تتبع قواعد تيك توك وتحقق فورًا إذا كان الاسم متاحًا. بدون تسجيل، بدون حدود.',
            'og_title': 'مولد أسماء تيك توك — تحقق من التوفر',
            'og_desc': 'أفكار @ تتبع قواعد تيك توك. تحقق مباشر. 17 أسلوبًا، 17 مجالًا، بدون تسجيل.',
        },
        'generator': {
            'title': 'مولد أسماء تيك توك — تحقق مباشر من التوفر',
            'meta_desc': 'ولّد 10-20 فكرة @ فريدة لتيك توك من كلمة مفتاحية ومجال وأسلوب، وتحقق فورًا أيها لا يزال متاحًا. أحكام صادقة. بدون تسجيل، بدون علامة مائية.',
            'og_title': 'مولد تيك توك — مباشر',
            'og_desc': '10-20 فكرة @ فريدة لتيك توك مع تحقق مباشر من التوفر. بدون تسجيل.',
        },
        'faq': {
            'title': 'الأسئلة الشائعة — أسماء تيك توك | Handle',
            'meta_desc': 'إجابات على الأسئلة التي يبحث عنها الناس فعلاً قبل اختيار اسم تيك توك: القواعد، كيف يعمل التحقق من التوفر، لماذا نقول "متاح على الأرجح" بدلًا من "متاح"، كيف تجد اسمًا يناسبك.',
            'og_title': 'الأسئلة الشائعة — أسماء تيك توك',
            'og_desc': 'إجابات حقيقية على الأسئلة التي يطرحها الجميع قبل اختيار اسم تيك توك.',
        },
        'about': {
            'title': 'حول Handle — مولد أسماء تيك توك مجاني مع تحقق مباشر',
            'meta_desc': 'Handle هو مولد أسماء تيك توك مجاني ومستقل مع تحقق مباشر من التوفر. مستقل عن تيك توك / ByteDance. مفتوح المصدر، 17 لغة، 17 أسلوبًا، 17 مجالًا. بدون تسجيل، بدون حدود، بدون علامة مائية.',
            'og_title': 'حول Handle — مولد أسماء تيك توك مستقل',
            'og_desc': 'مولد أسماء تيك توك مجاني ومستقل مع تحقق مباشر من التوفر.',
        },
        'privacy': {
            'title': 'سياسة الخصوصية — Handle',
            'meta_desc': 'ما يجمعه Handle (سجلات الخادم، علامة واحدة في localStorage)، ما لا يجمعه (بدون تحليلات، بدون إعلانات، بدون تتبع)، وحقوقك.',
            'og_title': 'سياسة الخصوصية — Handle',
            'og_desc': 'ما يجمعه Handle، ما لا يجمعه، وحقوقك.',
        },
        'terms': {
            'title': 'شروط الخدمة — Handle',
            'meta_desc': 'الشروط التي يمكنك بموجبها استخدام Handle: مجاني، بدون تسجيل، بدون ضمان على أحكام التوفر، بدون بحث عن علامات تجارية، بدون ارتباط بـ TikTok أو ByteDance.',
            'og_title': 'شروط الخدمة — Handle',
            'og_desc': 'شروط استخدام مولد أسماء تيك توك المجاني Handle.',
        },
    },
}

# All 18 supported languages, in hreflang tag order (en first, then alphabetical)
LANG_ORDER = ['es', 'de', 'fr', 'it', 'pt', 'nl', 'pl', 'ru', 'zh', 'vi', 'id', 'ms', 'tl', 'hi', 'bn', 'ur', 'ar']

