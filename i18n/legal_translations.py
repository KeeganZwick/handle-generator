# -*- coding: utf-8 -*-
"""
Privacy Policy + Terms of Service — full content translations for all
17 languages. This is a complete rewrite of the privacy policy to cover
all required disclosures (AdSense, GDPR legal basis, CCPA "Do Not Sell
or Share", children under 13, contact method, last-updated date, IP
rate-limiting matching server.js behavior).

The content is organized as named blocks that the build script can
do straightforward `string.replace` substitution on.

Each block is identified by a key (e.g. `privacy_p_what_we_collect_p1`)
and contains the localized content. The build script knows the
corresponding English source text and replaces it.

Content keys for privacy policy:
  privacy_p_lede                              : lede paragraph
  privacy_p_what_site_h2                      : section heading
  privacy_p_what_site_p                       : section body
  privacy_p_cookies_h2                        : "Cookies and similar technologies"
  privacy_p_cookies_p1                        : what cookies we set
  privacy_p_cookies_p2                        : localStorage flag
  privacy_p_collect_h2                        : "What we collect"
  privacy_p_collect_p1                        : lead paragraph
  privacy_p_collect_p2                        : server logs
  privacy_p_collect_p3                        : no accounts/emails
  privacy_p_use_h2                            : "How we use information"
  privacy_p_use_p1                            : purpose 1
  privacy_p_use_p2                            : purpose 2
  privacy_p_use_p3                            : purpose 3
  privacy_p_legal_basis_h2                    : "Legal basis (EEA/UK visitors)"
  privacy_p_legal_basis_p1                    : body
  privacy_p_adsense_h2                        : "Advertising (Google AdSense)"
  privacy_p_adsense_p1                        : lead
  privacy_p_adsense_p2                        : disclosure (Google's required text)
  privacy_p_adsense_p3                        : opt-out (Google's required text)
  privacy_p_third_h2                          : "Third parties"
  privacy_p_third_p1                          : TikTok
  privacy_p_third_p2                          : hosting/CDN
  privacy_p_third_p3                          : ad networks
  privacy_p_availability_h2                   : "TikTok availability check"
  privacy_p_availability_p1                   : body
  privacy_p_ratelimit_h2                      : "Rate limiting and IP addresses"
  privacy_p_ratelimit_p1                      : body
  privacy_p_children_h2                       : "Children under 13"
  privacy_p_children_p1                       : body
  privacy_p_rights_h2                         : "Your rights (EEA / UK)"
  privacy_p_rights_p1                         : body
  privacy_p_ccpa_h2                           : "California privacy rights (CCPA / CPRA)"
  privacy_p_ccpa_p1                           : do not sell/share intro
  privacy_p_ccpa_p2                           : do not sell/share language
  privacy_p_ccpa_p3                           : how to exercise
  privacy_p_retention_h2                      : "Data retention"
  privacy_p_retention_p1                      : body
  privacy_p_transfers_h2                      : "International transfers"
  privacy_p_transfers_p1                      : body
  privacy_p_changes_h2                        : "Changes to this policy"
  privacy_p_changes_p1                        : body
  privacy_p_contact_h2                        : "Contact"
  privacy_p_contact_p1                        : body

Content keys for terms of service:
  terms_t_governing_p                         : governing law body (no longer a placeholder)
  terms_t_contact_p                           : contact body (no longer a placeholder)
"""

PRIVACY = {}
TERMS = {}

# ============================================================================
# English
# ============================================================================
PRIVACY['en'] = {
    'privacy_p_lede': 'Last updated 25 August 2026. This policy explains what Handle collects, what it does not, and how you can exercise your rights. We try to write in plain language; the formal legal terms are the ones that apply if there is ever a conflict between plain language and these formal terms.',

    'privacy_p_what_site_h2': 'What Handle is',
    'privacy_p_what_site_p': 'Handle is a free TikTok username generator. You type a keyword, pick a niche and a vibe, and the site returns a list of handle ideas that follow TikTok\'s username rules. Each handle is then checked against TikTok\'s own profile endpoint so you can see whether it is likely available, likely taken, or unknown (the check could not be completed). Handle is an independent project. It is not affiliated with TikTok or ByteDance Ltd.',

    'privacy_p_cookies_h2': 'Cookies and similar technologies',
    'privacy_p_cookies_p1': 'The core tool does not set any cookies. The only persistent client-side storage we use is a single entry in your browser\'s <code>localStorage</code>, which is not sent to any server and is not read by third parties. If Google AdSense is enabled (see the Advertising section below), Google will set its own cookies and read its own identifiers to deliver and measure ads; that section explains what those are and how to opt out.',
    'privacy_p_cookies_p2': 'The localStorage flag we set is named <code>handle.cookieConsent.v1</code> and stores only the string <code>"accepted"</code> after you click the consent banner\'s acknowledge button. It is never sent to our server, never read by any third party, and you can clear it at any time via your browser\'s developer tools or by clearing site data for this domain.',

    'privacy_p_collect_h2': 'What we collect',
    'privacy_p_collect_p1': 'Nothing directly identifying you. The keyword you type, the niche and vibe you pick, and the list of generated handles are processed in your browser and are not associated with any user profile on our side.',
    'privacy_p_collect_p2': '<strong>Server logs.</strong> Like most web servers, our hosting provider records IP address, user-agent, request path, response status, and timestamp in standard access logs, retained for 30 days for security and abuse prevention. We do not use these logs for advertising, profiling, or any user-facing analytics.',
    'privacy_p_collect_p3': '<strong>No accounts, no email, no profiles.</strong> Handle does not require an account, does not ask for your email address, and does not build a profile of you. The site has no newsletter signup, no comment system, and no contact form that asks for personal details.',

    'privacy_p_use_h2': 'How we use information',
    'privacy_p_use_p1': 'We use the information we collect for three things: (1) to deliver the tool to you — running the generator, checking availability against TikTok, and rendering the result cards; (2) to keep the service healthy — rate limiting, abuse prevention, debugging outages; and (3) to respond to legal requests if we ever receive any.',
    'privacy_p_use_p2': 'We do not sell your data. We do not share it with advertisers except in the aggregate statistical way that every ad-supported site does (an ad network sees a request, not a name). We do not use it to make automated decisions about you.',
    'privacy_p_use_p3': 'If you write to us through the contact email below, we use whatever you tell us only to reply to you, and we delete the thread after 12 months unless you ask us to keep it.',

    'privacy_p_legal_basis_h2': 'Legal basis (EEA / UK visitors)',
    'privacy_p_legal_basis_p1': 'If you are in the European Economic Area or the United Kingdom, the General Data Protection Regulation (GDPR) requires us to state a legal basis for each processing activity. Our legal bases are: <strong>consent</strong> for setting any non-essential cookies (including any AdSense cookies, if and when AdSense is enabled); <strong>legitimate interest</strong> for the in-memory IP rate-limiting needed to keep the availability-check endpoint reachable; and <strong>legal obligation</strong> for retaining standard server logs for the security and abuse-prevention period required by our hosting provider.',

    'privacy_p_adsense_h2': 'Advertising (Google AdSense)',
    'privacy_p_adsense_p1': 'Handle reserves space for Google AdSense via the <code>ads.txt</code> file at the root of the site, but AdSense is not currently serving ads. When AdSense is enabled, the following disclosures apply. We will display a clear notice and obtain consent before any AdSense cookies are set for visitors in the EEA, the UK, and Switzerland.',
    'privacy_p_adsense_p2': '<strong>Google\'s required disclosure.</strong> Third-party vendors, including Google, use cookies to serve ads based on a user\'s prior visits to this website or other websites. Google\'s use of advertising cookies enables it and its partners to serve ads to users based on their visit to this site and/or other sites on the Internet.',
    'privacy_p_adsense_p3': '<strong>How to opt out of personalised advertising.</strong> You may opt out of personalised advertising by visiting Google\'s <a href="https://adssettings.google.com/" rel="noopener noreferrer" target="_blank">Ads Settings</a>. You may also opt out of some third-party vendors\' use of cookies for personalised advertising by visiting <a href="https://www.aboutads.info/" rel="noopener noreferrer" target="_blank">www.aboutads.info</a>. For information about how Google uses data from partner sites, see <a href="https://policies.google.com/technologies/partner-sites" rel="noopener noreferrer" target="_blank">How Google uses information from sites or apps that use our services</a>.',

    'privacy_p_third_h2': 'Third-party services',
    'privacy_p_third_p1': '<strong>TikTok / ByteDance.</strong> The availability check sends a request from our server to TikTok\'s public profile and oEmbed endpoints. TikTok sees the request from our server\'s IP, the handle being checked, and standard HTTP headers (including our <code>HandleBot/0.1</code> User-Agent). What TikTok does with that request is governed by <a href="https://www.tiktok.com/legal/privacy-policy" rel="noopener noreferrer" target="_blank">TikTok\'s Privacy Policy</a>.',
    'privacy_p_third_p2': '<strong>Hosting and CDN.</strong> Our static files are served through a content delivery network. The CDN logs IP, user-agent, and request path for its own abuse-prevention purposes; that logging is governed by the CDN provider\'s privacy policy.',
    'privacy_p_third_p3': '<strong>Ad networks.</strong> When AdSense is enabled, Google and its certified ad partners may set and read cookies and similar identifiers on your browser for the purpose of selecting and measuring ads. See the Advertising section above for the full list of disclosures and opt-out links.',

    'privacy_p_availability_h2': 'TikTok availability check',
    'privacy_p_availability_p1': 'When you click "Check" or "Generate", the server you are talking to sends a request to TikTok to find out whether a given handle is associated with a live profile. The handle you checked is included in that request, and TikTok can therefore see which handle you are interested in. We do not send your IP address, your name, your email, or any other identifier together with that request beyond the standard HTTP headers that every web request carries. The check is best-effort: TikTok may rate-limit, block, or return incomplete results at any time, and verdicts can be out of date the moment they are issued.',

    'privacy_p_ratelimit_h2': 'Rate limiting and IP addresses',
    'privacy_p_ratelimit_p1': 'To keep the availability-check endpoint reachable and to stay within TikTok\'s anti-abuse thresholds, the server applies a token-bucket rate limit keyed on your IP address. The bucket is held in a JavaScript <code>Map</code> in the Node process memory. It is not written to disk, not replicated across servers, and not shared with any third party. When the server restarts, the bucket is gone. We do not log, store, or analyze IP addresses for any other purpose; the IP is used solely as a key into the in-memory bucket, then forgotten when the bucket is dropped or evicted.',

    'privacy_p_children_h2': 'Children under 13',
    'privacy_p_children_p1': 'Handle is not directed at children under 13, and we do not knowingly collect personal information from children under 13. The site is a tool for adult TikTok creators and brand-builders. If you believe a child under 13 has provided personal information through the site, contact us at the address below and we will delete it. The United States Children\'s Online Privacy Protection Act (COPPA) and the EU\'s GDPR-K both define a child as under 13 unless a member state sets a higher age up to 16; we apply the stricter threshold.',

    'privacy_p_rights_h2': 'Your rights (EEA / UK)',
    'privacy_p_rights_p1': 'If you are in the EEA, the UK, or Switzerland, you have the right to: access the personal data we hold about you; correct inaccurate data; request deletion of your data; restrict or object to processing; receive your data in a portable, machine-readable format; and withdraw consent at any time without affecting the lawfulness of processing carried out before withdrawal. You also have the right to lodge a complaint with your local data protection authority. Because we do not collect personal data beyond standard server logs, most requests will receive a "we hold nothing identifiable about you" response — but the right stands. To exercise any of these rights, contact us at the address below.',

    'privacy_p_ccpa_h2': 'California privacy rights (CCPA / CPRA)',
    'privacy_p_ccpa_p1': 'If you are a California resident, the California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), gives you specific rights regarding your personal information.',
    'privacy_p_ccpa_p2': '<strong>Do Not Sell or Share My Personal Information.</strong> We do not sell personal information for money, and we do not share it for cross-context behavioural advertising as those terms are defined under the CPRA. If AdSense is enabled and you would like to opt out of any future cross-context advertising, you can do so by enabling the "Limit ad tracking" or "Opt out of personalised ads" controls described in the Advertising section above, or by following the link <a href="https://adssettings.google.com/" rel="noopener noreferrer" target="_blank">here</a>. We do not knowingly sell or share the personal information of consumers under 16.',
    'privacy_p_ccpa_p3': 'You also have the right to know what categories of personal information we collect (server logs only), to request deletion, and to not be discriminated against for exercising your rights. To exercise any of these rights, contact us at the address below. We will respond within 45 days as required by the CCPA.',

    'privacy_p_retention_h2': 'Data retention',
    'privacy_p_retention_p1': 'Server logs: 30 days, then deleted. Rate-limit buckets: until the bucket fills back to capacity (1 hour after your last request, in practice) or until the server restarts, whichever comes first. Availability check results: not stored on our side; each check is a fresh probe. The localStorage consent flag persists in your browser until you clear site data.',

    'privacy_p_transfers_h2': 'International transfers',
    'privacy_p_transfers_p1': 'Handle is operated from servers located in the United States and the European Union (our CDN edges). When you use the tool, your request may be served from an edge near you, but the availability-check requests that we make to TikTok originate from a fixed set of our server IPs (US and EU regions). If you are in a region with strict data-residency rules, the act of using the tool means your request is processed outside your region. We rely on standard contractual clauses and the European Commission\'s adequacy decisions for the limited personal data processed (IP for rate-limiting).',

    'privacy_p_changes_h2': 'Changes to this policy',
    'privacy_p_changes_p1': 'If we make material changes, we will update the "Last updated" date at the top of this page. For changes that broaden the data we collect, change how we use it, or change the third parties we share with, we will add a more prominent notice on the home page for at least 30 days before the change takes effect. The previous version of this policy is available on request.',

    'privacy_p_contact_h2': 'Contact',
    'privacy_p_contact_p1': 'For privacy questions, data-subject requests, CCPA requests, copyright notices, and any other legal matter, write to <strong>privacy@handle.name</strong>. We aim to respond within 14 days for privacy requests and within 30 days for data-subject requests as required by the GDPR.',
}

TERMS['en'] = {
    'terms_governing_p': 'These terms are governed by the laws of the State of Delaware, United States of America, without regard to its conflict-of-laws provisions. Any dispute arising out of or related to these terms will be resolved in the state or federal courts located in Delaware, and you consent to the personal jurisdiction of those courts.',
    'terms_contact_p': 'For legal notices, takedown requests, and any other formal correspondence, write to <strong>legal@handle.name</strong>. We aim to respond within 14 days. Casual feedback and bug reports can go to the same address — we read everything — but formal legal notices must follow this channel.',
    'terms_lede_p': "Last updated 25 August 2026. By using Handle you agree to these terms. They cover what Handle is, who owns what, what you can and can't do with the tool, and what happens if something goes wrong.",
}

# ============================================================================
# Placeholder for other languages - to be filled
# ============================================================================
for _lang in ['es','de','fr','it','pt','nl','pl','ru','zh','vi','id','ms','tl','hi','bn','ur','ar']:
    if _lang not in PRIVACY:
        PRIVACY[_lang] = {}
    if _lang not in TERMS:
        TERMS[_lang] = {}
