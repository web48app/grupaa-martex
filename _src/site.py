# Generator stron Grupy Martex: python3 _src/site.py  (uruchamiać z katalogu strony)
# Zdjęcia: wrzuć plik o nazwie z ZDJECIA.md do img/ — pojawi się sam, bez zmian w kodzie.
import os, re, html, unicodedata
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://martextarnow.pl"

# >>> DANE FIRMY <<<
COMPANY = {
    "name": "F.H.U. Martex",
    "street": "Wola Rzędzińska 446B",
    "nip": "873-000-30-67",
    "wni": "PL1216073p",
    "phone": "14 679 23 49", "tel": "+48146792349",
    "email": "biuro@martextarnow.pl",
    "facebook": "https://www.facebook.com/MartexTarnow",
    "rzetelna": "https://wizytowka.rzetelnafirma.pl/I5J4FQ73",
}
SHOP = {"street": "ul. Szkotnik 2B", "city": "Tarnów",
        "hours": ""}   # np. "Pn–Pt 8:00–16:00 · Sob 8:00–13:00" — puste = „zadzwoń przed przyjazdem”
SERWIS_URL = "https://serwis-martex.vercel.app"   # zmienić na docelową domenę serwisu
DOCS = {"katalog": "", "spedycja": ""}   # np. "docs/katalog-martex.pdf" — puste = przycisk się nie pokazuje

PEOPLE = [
    ("Wacław Kmieć", "Właściciel", "501 308 550", "waclaw@martextarnow.pl"),
    ("Mateusz Kmieć", "Handel i logistyka", "509 654 349", "mateusz@martextarnow.pl"),
    ("Miłosz Kmieć", "Księgowość i logistyka", "605 554 349", "milosz@martextarnow.pl"),
    ("Krzysztof Krawczyk", "Przedstawiciel handlowy", "793 515 053", "krzysztof@martextarnow.pl"),
]

# ---------- katalog (ze starej strony, 2017 — do aktualizacji z klientem) ----------
GOLEBIE = [
    ("Supre Mix", "SUPRE MIX", True, "Mieszanka uzupełniająca na cały rok: zioła, muszle ostryg, suszone warzywa i owoce, glinka palona, wapień, granulat i dobrane nasiona."),
    ("Super Martmix", "MARTMIX", True, "Wszystko, co w Supre Mix, wzbogacone o drożdże i granulat energetyczny."),
    ("Lotowa Turbo Mistrzów", "LTM", False, ""),
    ("Lotowa bez pszenicy", "LBP", False, ""),
    ("Rozpłodowo-lotowa Ekstra", "RLE", False, ""),
    ("Rozpłodowo-lotowa", "RL", False, ""),
    ("Energetyczna Ekstra", "EE", False, ""),
    ("Junior Ekstra", "JE", False, ""),
    ("Junior oszczędnościowy", "JO", False, ""),
    ("Super Wdowce", "SPUS", False, ""),
    ("Wdowce", "W", False, ""),
    ("Uniwersalna", "U", False, ""),
    ("Bez pszenicy", "BP", False, ""),
    ("Bez pszenicy i kukurydzy", "BPK", False, ""),
    ("Bez pszenicy i kukurydzy Ekstra Plus", "BK+", False, ""),
    ("Zimowa", "Z", False, ""),
    ("Pierzenie", "P", False, ""),
    ("Pierzenie bez pszenicy", "PBP", False, ""),
    ("Mieszanka nasion", "MN", False, ""),
    ("Krótkodzioby bez pszenicy i popcornu", "KPP", False, ""),
    ("Krótkodzioby ekonomiczna", "KEKO", False, ""),
]
PTAKI = [
    ("Papuga duża", "PD"), ("Papuga średnia", "PŚ"), ("Kanarek", "K"),
    ("Egzotyka", "E"), ("Gryzoń", "G"), ("Pasza sypka dla kur", ""),
]
SUPLEMENTY = ["Olejek czosnkowy", "Olejek czosnkowy z ziołami", "Sok czosnkowy", "Olejek z oregano", "Oregano mielone",
    "Olejek mix ziół", "Olej mix", "Mix ziół", "Mix Natura", "Natumart do wody", "Natumart na karmę",
    "Elektrolit — energia na loty", "Glukoza z minerałami", "Ocet jabłkowy", "Witamina AD3E", "Witamina E + selen",
    "Bomba witaminowa — multiwitamina", "B-complex", "Drożdże piwne", "Probiotyk", "Lecytyna",
    "Siara lęgi / loty / pierzenie", "Zakwaszacz", "Zakwaszacz podwójnie mocny", "Olej na rozród", "Olej pierzenie",
    "Eukaliptus", "Sok anyżowy", "Katar", "Quicksprint", "Quickmix", "Sól kąpielowa", "Minerały dla gołębi"]
AKCESORIA = ["Siodełka drewniane", "Siodełka plastikowe", "Kosze transportowe", "Pudełka transportowe",
    "Karmniki z pokrywą", "Miska lęgowa gipsowa", "Miska lęgowa plastikowa", "Ruszt do cel plastikowy"]
BAKALIE = ["Żurawina", "Jagody goji", "Morela", "Śliwka suszona", "Daktyle", "Migdały", "Orzech włoski",
    "Orzech laskowy", "Mieszanka studencka", "Nasiona dyni łuskane", "Dynia niełuskana", "Słonecznik łuskany",
    "Czarny kminek", "Kasza gryczana", "Kasza jaglana", "Płatki owsiane"]

# ---------- program lotowy (dni: 1 = poniedziałek … 0 = niedziela) ----------
PROGRAM = [
    ("parowanie", "Parowanie", [
        "Rozpłodowo-lotowa Ekstra + mix ziół (olejek) + E + selen Martex",
        "Rozpłodowa bez pszenicy + eukaliptus Martex",
        "Rozpłodowo-lotowa Ekstra + eukaliptus Martex + E + selen Martex",
        "Rozpłodowo-lotowa Ekstra",
        "Rozpłodowa bez pszenicy + drożdże piwne Martex + olejek na lęgi Martex",
        "Rozpłodowo-lotowa Ekstra + drożdże piwne Martex + olejek na lęgi Martex",
        "Rozpłodowa bez pszenicy"],
     "Zależnie od uznania hodowcy można stosować karmy z pszenicą: dodać 10% pszenicy do karmy albo kupić odpowiedniki z pszenicą. Podstawowy suplement na odporność to olejek czosnkowy, a trawienie wspierają grity i minerały Martex."),
    ("mlode", "Chów młodych", [
        "Odchów oszczędnościowy + olejek na lęgi Martex",
        "Odchów oszczędnościowy 70% + Junior Ekstra 30% + siara lęgi Martex + olejek czosnkowy Martex + Multivita (w osobnym pojemniku)",
        "Junior Ekstra + Multivita (w osobnym pojemniku)",
        "Odchów oszczędnościowy 70% + Junior Ekstra 30% + proszek na lęgi Martex",
        "Odchów oszczędnościowy + olejek na lęgi Martex + drożdże piwne Martex + siara odchów Martex + ocet Martex",
        "Junior oszczędnościowy",
        "Odchów oszczędnościowy + olej z oregano Martex"],
     "O sukcesie decydują zdrowie i właściwe żywienie: mieszanki pełnoporcjowe Martex dostarczają witamin, probiotyków, mikro- i makroelementów. W tym okresie polecamy probiotyk, drożdże, siarę i zioła oraz lecytynę z karnityną i witaminę C."),
    ("loty-mlodych", "Loty młodych", [
        "Bez strączkowych Light + ocet jabłkowy Martex + olej z oregano Martex + drożdże z pyłkiem pszczelim, ziołami i cytryną Martex",
        "Bez strączkowych Light 40% + Junior Turbo Mistrzów 60% + ocet + olejek czosnkowy Martex + siara loty Martex",
        "Bez strączkowych Light 50% + Junior Turbo Mistrzów 50% + witamina B-complex Martex",
        "Bez strączkowych Light 50% + Super Dieta 50% + Mix Natura Martex lub eukaliptus Martex",
        "Bez strączkowych Light + Bomba witaminowa Martex",
        "Bez strączkowych Light",
        "Super Dieta + elektrolit Martex + woda z sokiem czosnkowym Martex"],
     "Można też stosować Juniora lotowego z pszenicą albo dodać do Juniora Turbo Mistrzów 15% pszenicy. Po powrocie z lotu przez jeden dzień podawaj elektrolit Martex w proszku — szybciej wraca forma i nawodnienie. Wieczorem warto podać sok czosnkowy Martex."),
    ("loty-seniorow", "Loty seniorów", [
        "Bez strączkowych Light + Bomba witaminowa Martex + ostropest plamisty + oregano mielone Martex + olejek mix Martex",
        "Lotowa Turbo Mistrzów + siara turbo + ocet z miodem + drożdże piwne Martex + olejek mix Martex",
        "Lotowa + Mix Natura Martex",
        "Bez strączkowych Light 60% + Wdowce lub Super Wdowce Ultra Sport 40% + mix ziół Martex",
        "Bez strączkowych Light 50% + Super Wdowce Ultra Sport 50% + lecytyna z karnityną Martex + siara turbo Martex + olejek mix Martex",
        "Super Dieta",
        "Super Dieta lub Bez strączkowych Light + glukoza z minerałami Martex + woda z sokiem czosnkowym Martex"],
     "W trakcie i po lotach niezastąpione są elektrolity i Energia na loty Martex — podawane systematycznie dają dobre wyniki i prawidłową regenerację. W tym okresie zapewnij też dostęp do minerałów Multivita i Supremix."),
]
DAYS = [("Pon", 1), ("Wt", 2), ("Śr", 3), ("Czw", 4), ("Pt", 5), ("Sob", 6), ("Nd", 0)]

# ---------- ikony ----------
I_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
I_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
I_SEARCH = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'

# ---------- narzędzia ----------
def slug(s):
    s = s.replace("ł", "l").replace("Ł", "L")
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def esc(s): return html.escape(s, quote=True)

def fig(src, label, cls="", alt="", eager=False, extra=""):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<div class="fig {cls}" data-label="{esc(label)}"{extra}>'
            f'<img src="{src}" alt="{esc(alt)}" {load} onerror="this.parentNode.classList.add(\'is-empty\');this.remove()"></div>')

def btn_tel(cls="btn btn--red", label=None):
    return f'<a href="tel:{COMPANY["tel"]}" class="{cls}">{I_PHONE} {label or COMPANY["phone"]}</a>'

def pcard(name, code, cat, cat_label, best=False, desc=""):
    tag = '<span class="pcard__tag">BESTSELLER</span>' if best else ""
    d = f"<p>{esc(desc)}</p>" if desc else ""
    return f'''<article class="pcard" data-cat="{cat}" data-name="{esc(name + ' ' + code)}">
  <div style="position:relative">{tag}{fig(f"img/produkty/{slug(name)}.jpg", "", alt=name, extra=f' data-code="{esc(code)}"')}</div>
  <div class="pcard__body"><span class="pcard__cat">{cat_label}</span><h3>{esc(name)}</h3>{d}</div>
</article>'''

def all_products():
    out = [pcard(n, c, "golebie", "Karma dla gołębi", b, d) for n, c, b, d in GOLEBIE]
    out += [pcard(n, "", "suplementy", "Suplement dla gołębi") for n in SUPLEMENTY]
    out += [pcard(n, c, "ptaki", "Papugi i ptaki") for n, c in PTAKI]
    out += [pcard(n, "", "akcesoria", "Akcesoria") for n in AKCESORIA]
    return "\n".join(out)

# ---------- szkielet ----------
NAV = [("index.html", "Start", "home"), ("karmy.html", "Karmy", "karmy"), ("program-lotowy.html", "Program lotowy", "program"),
       ("transport.html", "Transport", "transport"), ("bakalie.html", "Bakalie", "bakalie"),
       ("o-firmie.html", "O firmie", "o-firmie"), ("kontakt.html", "Kontakt", "kontakt")]

def head(title, desc, path):
    c = COMPANY
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#faf7f2">
<link rel="canonical" href="{DOMAIN}/{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}/{path}">
<meta property="og:image" content="{DOMAIN}/img/og.jpg">
<meta property="og:locale" content="pl_PL">
<link rel="icon" type="image/png" href="logo_small.png">
<script>try{{if(localStorage.getItem('martex-grupa-theme')==='dark')document.documentElement.setAttribute('data-theme','dark')}}catch(e){{}}</script>
<link rel="preload" href="fonts/big-shoulders-display-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/barlow-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/fonts.css">
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Organization","name":"Grupa Martex — {c['name']}","url":"{DOMAIN}/","logo":"{DOMAIN}/logo-martex.png",
"telephone":"{c['tel']}","email":"{c['email']}","vatID":"PL{c['nip'].replace('-', '')}","foundingDate":"1990",
"address":{{"@type":"PostalAddress","streetAddress":"{c['street']}","addressLocality":"Wola Rzędzińska","addressCountry":"PL"}},
"sameAs":["{c['facebook']}"]}}
</script>
</head>
'''

def header(active):
    cur = ' class="active" aria-current="page"'
    links = "\n      ".join(f'<a href="{h}"{cur if k == active else ""}>{t}</a>' for h, t, k in NAV)
    return f'''<body data-page="{active}">
<a href="#top" class="skip" style="position:absolute;left:-9999px">Przejdź do treści</a>
<div class="topbar">
  <div class="wrap">
    <div class="topbar__group"><b>Grupa Martex</b><span>Karmy</span><span>Transport</span><span>Bakalie</span><a href="{SERWIS_URL}">Serwis samochodowy →</a></div>
    <div class="topbar__right"><a href="kontakt.html">{COMPANY['street']}</a><a href="tel:{COMPANY['tel']}">{COMPANY['phone']}</a></div>
  </div>
</div>
<header class="nav">
  <div class="wrap">
    <a href="index.html" class="nav__logo" aria-label="Grupa Martex — strona główna"><img src="logo-martex.png" alt="Martex" width="263" height="155"></a>
    <nav class="nav__links" aria-label="Menu główne">
      {links}
    </nav>
    <div class="nav__right">
      <button class="theme" type="button" aria-label="Przełącz jasny lub ciemny motyw" title="Jasny / ciemny motyw">
        <svg class="i-moon" viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
        <svg class="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
      </button>
      {btn_tel("btn btn--red nav__cta")}
      <button class="burger" type="button" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
'''

def footer():
    c = COMPANY
    return f'''
<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div>
        <img src="logo-martex.png" alt="Grupa Martex" width="263" height="155" class="foot__logo" loading="lazy">
        <p>Rodzinna firma z Woli Rzędzińskiej koło Tarnowa. Od 1990 roku produkujemy karmy i suplementy dla gołębi, prowadzimy transport i sprzedajemy bakalie.</p>
      </div>
      <div>
        <h4>Strona</h4>
        <ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t, _ in NAV)}</ul>
      </div>
      <div>
        <h4>Grupa Martex</h4>
        <ul><li><a href="karmy.html">Karmy i suplementy</a></li><li><a href="transport.html">Transport i spedycja</a></li><li><a href="bakalie.html">Bakalie i kasze</a></li><li><a href="{SERWIS_URL}">Serwis Samochodowy Martex</a></li></ul>
      </div>
      <div>
        <h4>Kontakt</h4>
        <ul><li>{c['name']}</li><li>{c['street']}</li><li><a href="tel:{c['tel']}">{c['phone']}</a></li><li><a href="mailto:{c['email']}">{c['email']}</a></li><li><a href="{c['facebook']}" target="_blank" rel="noopener">Facebook</a></li></ul>
      </div>
    </div>
    <div class="foot__bottom">
      <span>© <span data-year>2026</span> {c['name']} · NIP {c['nip']} · WNI {c['wni']}</span>
      <span class="foot__legal"><a href="polityka-prywatnosci.html">Polityka prywatności i cookies</a><button type="button" data-cookie-settings>Ustawienia cookies</button><a href="{c['rzetelna']}" target="_blank" rel="noopener">Rzetelna Firma</a></span>
      <span>Projekt i wykonanie: <a href="https://web48.app" target="_blank" rel="noopener">web48.app</a></span>
    </div>
  </div>
</footer>
<div class="mbar">
  <a href="tel:{c['tel']}">{I_PHONE}Zadzwoń</a>
  <a href="mailto:{c['email']}">{I_MAIL}Napisz</a>
</div>
<button class="totop" type="button" aria-label="Przewiń do góry"><svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>
<div class="cookies" role="dialog" aria-live="polite" aria-label="Pliki cookies">
  <b>Ciasteczka</b>
  <p>Strona zapamiętuje Twoje wybory (np. jasny lub ciemny motyw) w przeglądarce. Za Twoją zgodą wczytamy też mapę Google, która zapisuje własne pliki cookies. Więcej w <a href="polityka-prywatnosci.html">polityce prywatności</a>.</p>
  <div class="cookies__btns">
    <button type="button" class="btn btn--red" data-consent="all">Akceptuję</button>
    <button type="button" class="btn btn--line" data-consent="necessary">Tylko niezbędne</button>
  </div>
</div>
<script src="js/main.js"></script>
</body>
</html>
'''

def phero(crumb, title_html, lead):
    return f'''
<section class="phero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Okruszki"><a href="index.html">Start</a><span>/</span><span>{crumb}</span></nav>
    <h1>{title_html}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
'''

def page(fname, active, title, desc, body):
    path = "" if fname == "index.html" else fname.replace(".html", "")
    out = head(title, desc, path) + header(active) + '\n<main id="top">\n' + body + "\n</main>\n" + footer()
    assert "{{" not in out, fname
    open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(out)
    print("ok", fname, len(out))

def doc_btn(key, label, cls="btn btn--line"):
    return f'<a href="{DOCS[key]}" class="{cls}" download>{label}</a>' if DOCS[key] else ""

# ---------- wspólne bloki ----------
def hurt_serwis():
    k = PEOPLE[3]
    return f'''
<section class="sec">
  <div class="wrap duo">
    <div class="box box--red rv">
      <h2>Hurtownie i sklepy zoologiczne</h2>
      <p>Zaopatrujemy hurtownie i sklepy w Polsce i za granicą, własnym transportem. Zapytaj o warunki współpracy i aktualny cennik.</p>
      <p class="person"><b>{k[0]}, {k[1].lower()}</b><a href="tel:+48{k[2].replace(' ', '')}">{k[2]}</a> · <a href="mailto:{k[3]}">{k[3]}</a></p>
    </div>
    <a href="{SERWIS_URL}" class="box box--black rv">
      <span class="label">Grupa Martex</span>
      <h2>Serwis Samochodowy Martex</h2>
      <p>Mechanika, wulkanizacja i klimatyzacja dla aut osobowych i dostawczych. Tarnów, ul. Bielatowicza 5, tel. 605 554 349.</p>
      <span class="more">Przejdź do serwisu →</span>
    </a>
  </div>
</section>'''

# ---------- strony ----------
best = "\n".join(pcard(n, c, "golebie", "Karma dla gołębi", b, d) for n, c, b, d in GOLEBIE[:4])
snacks6 = "\n".join(f'<div class="scard">{fig(f"img/bakalie/{slug(n)}.jpg", "Zdjęcie: " + n, "fig--dark", n)}<b>{n}</b></div>' for n in BAKALIE[:8])

HOME = f'''
<section class="hero">
  <div class="wrap">
    <div class="hero__txt">
      <span class="label">Producent z Tarnowa · od 1990 roku</span>
      <h1>Karmy dla gołębi <span class="red">na każdy sezon.</span></h1>
      <p class="hero__sub">Mieszanki, preparaty i akcesoria dla gołębi, papug i małej egzotyki. Tworzymy je z doświadczonymi hodowcami i lekarzem weterynarii, z ziarna kupowanego bezpośrednio od rolników, bez GMO.</p>
      <div class="hero__ctas"><a href="karmy.html" class="btn btn--red">Zobacz katalog</a><a href="program-lotowy.html" class="btn btn--line">Program lotowy</a></div>
    </div>
    <div class="hero__visual">
      {fig("img/hero.jpg", "Zdjęcie: wiadro Supre Mix i ziarno z bliska", alt="Karma Martex dla gołębi", eager=True)}
      <div class="hero__badge"><b>Od 1990</b><span>rodzinna firma</span></div>
    </div>
  </div>
</section>

<section class="stats" aria-label="Martex w liczbach">
  <div class="wrap">
    <div class="stat"><b>1990</b><span>rok założenia, rodzina Kmieciów</span></div>
    <div class="stat"><b>200+</b><span>karm, preparatów i akcesoriów</span></div>
    <div class="stat"><b>14 palet</b><span>lub 7 ton na jedno auto</span></div>
    <div class="stat"><b>24/7</b><span>transport w Polsce i UE</span></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec__head rv"><div><span class="label">Grupa Martex</span><h2>Czym się zajmujemy</h2></div><p class="lead">Trzy działy pod jednym szyldem, a obok nich nasz serwis samochodowy w Tarnowie.</p></div>
    <div class="divs">
      <a href="karmy.html" class="div rv">{fig("img/karmy.jpg", "Zdjęcie: gołębie lub karma", alt="Karmy Martex")}<div class="div__body"><h3>Karmy i suplementy</h3><p>Mieszanki lotowe, rozpłodowe i dla młodych, olejki, elektrolity, witaminy i akcesoria. Także dla papug, kanarków, gryzoni i kur.</p><span class="more">Katalog produktów →</span></div></a>
      <a href="transport.html" class="div rv">{fig("img/flota-1.jpg", "Zdjęcie: bus Iveco Daily w barwach Martex", alt="Flota Martex")}<div class="div__body"><h3>Transport i spedycja</h3><p>Własna flota, przewozy krajowe i międzynarodowe przez całą dobę. Zabudowy sztywne, plandeki i chłodnie.</p><span class="more">Zapytaj o wycenę →</span></div></a>
      <a href="bakalie.html" class="div rv">{fig("img/bakalie.jpg", "Zdjęcie: bakalie na czarnym tle", "fig--dark", "Bakalie Martex")}<div class="div__body"><h3>Bakalie i kasze</h3><p>Suszone owoce, orzechy, pestki, kasze i płatki dla osób, które jedzą świadomie.</p><span class="more">Zobacz produkty →</span></div></a>
    </div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    <div class="sec__head rv"><div><span class="label">Najczęściej wybierane</span><h2>Karmy dla gołębi</h2></div><p class="lead">Ponad 20 mieszanek na każdy okres sezonu, do tego ponad 30 preparatów i akcesoria do gołębnika.</p></div>
    <div class="pgrid">{best}</div>
    <p style="margin-top:30px"><a href="karmy.html" class="more">Cały katalog →</a></p>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="rv">
      <span class="label">Dla hodowców</span>
      <h2 style="margin:14px 0 20px">Program lotowy Martex</h2>
      <p class="lead">Tydzień żywienia rozpisany dzień po dniu na cztery okresy: parowanie, chów młodych, loty młodych i loty seniorów. Do wydruku i powieszenia w gołębniku.</p>
      <div class="btns" style="margin-top:28px"><a href="program-lotowy.html" class="btn btn--red">Otwórz program</a></div>
    </div>
    <div class="plan on rv" aria-label="Loty seniorów — fragment programu">
      <table><tbody>{"".join(f'<tr data-d="{d}"><th scope="row">{lbl}</th><td>{t}</td></tr>' for (lbl, d), t in list(zip(DAYS, PROGRAM[3][2]))[:4])}</tbody></table>
      <div class="plan__note">Loty seniorów · pełny tydzień i pozostałe okresy w programie</div>
    </div>
  </div>
</section>

<section class="sec dark">
  <div class="wrap split">
    {fig("img/flota-2.jpg", "Zdjęcie: flota Martex", alt="Busy Martex")}
    <div class="rv">
      <span class="label">Transport i spedycja</span>
      <h2 style="margin-top:14px">Szybko i bezpiecznie, w Polsce i całej Unii</h2>
      <ul class="facts">
        <li><b>Do 7 t lub 14 palet</b><span>na jedno auto, aut może być więcej</span></li>
        <li><b>24 godziny, 7 dni</b><span>just in time i door-to-door</span></li>
        <li><b>Plandeki i chłodnie</b><span>także zabudowy sztywne</span></li>
        <li><b>Euro 5 i Euro 6</b><span>Iveco, Fiat, Peugeot</span></li>
      </ul>
      <div class="btns"><a href="transport.html" class="btn btn--red">Zapytaj o wycenę</a></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec__head rv"><div><span class="label">Zdrowa przekąska</span><h2>Bakalie i kasze</h2></div><p class="lead">Suszone owoce, orzechy i kasze z surowców najwyższej jakości.</p></div>
    <div class="sgrid">{snacks6}</div>
    <p style="margin-top:30px"><a href="bakalie.html" class="more">Wszystkie produkty →</a></p>
  </div>
</section>
''' + hurt_serwis()

KARMY = phero("Karmy i suplementy", 'Karmy, suplementy<br><span class="red">i akcesoria.</span>',
              "Mieszanki dla gołębi na każdy okres sezonu, preparaty robione z hodowcami i lekarzem weterynarii, karmy dla papug i ptaków oraz akcesoria do gołębnika.") + f'''
<section class="sec">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Kategoria">
      <button class="chip on" type="button" data-filter="all" aria-pressed="true">Wszystkie</button>
      <button class="chip" type="button" data-filter="golebie" aria-pressed="false">Karmy dla gołębi <small>{len(GOLEBIE)}</small></button>
      <button class="chip" type="button" data-filter="suplementy" aria-pressed="false">Suplementy <small>{len(SUPLEMENTY)}</small></button>
      <button class="chip" type="button" data-filter="ptaki" aria-pressed="false">Papugi i ptaki <small>{len(PTAKI)}</small></button>
      <button class="chip" type="button" data-filter="akcesoria" aria-pressed="false">Akcesoria <small>{len(AKCESORIA)}</small></button>
      <label class="search">{I_SEARCH}<span style="position:absolute;left:-9999px">Szukaj produktu</span><input type="search" placeholder="Szukaj, np. olejek, LTM" data-search></label>
    </div>
    <div class="pgrid" data-products>
{all_products()}
    </div>
    <p class="empty-msg">Nie mamy takiego produktu w katalogu. Zadzwoń, sprawdzimy: <a href="tel:{COMPANY['tel']}">{COMPANY['phone']}</a>.</p>
    <div class="btns" style="margin-top:40px">{doc_btn("katalog", "Pobierz katalog PDF")}{btn_tel("btn btn--red", "Zapytaj o cenę")}</div>
  </div>
</section>
''' + hurt_serwis()

def plan_html(i, key, name, rows, note):
    trs = "".join(f'<tr data-d="{d}"><th scope="row">{lbl}</th><td>{t}</td></tr>' for (lbl, d), t in zip(DAYS, rows))
    return f'<div class="plan{" on" if i == 0 else ""}" id="plan-{key}" role="tabpanel" data-title="{name}"><table><tbody>{trs}</tbody></table><div class="plan__note">{note}</div></div>'

PROG = phero("Program lotowy", 'Program lotowy<br><span class="red">Martex.</span>',
             "Tydzień żywienia dzień po dniu, na każdy okres sezonu. Dzisiejszy dzień jest podświetlony. Proporcje i dodatki dobieraj do kondycji swoich ptaków.") + f'''
<section class="sec">
  <div class="wrap">
    <div class="tabs" role="tablist" aria-label="Okres">
      {"".join(f'<button class="tab" type="button" role="tab" data-key="{k}" aria-controls="plan-{k}" aria-selected="{"true" if i == 0 else "false"}">{n}</button>' for i, (k, n, _, _) in enumerate(PROGRAM))}
    </div>
    {"".join(plan_html(i, *p) for i, p in enumerate(PROGRAM))}
    <div class="plan-actions"><button type="button" class="btn btn--line" data-print>Drukuj wszystkie okresy</button><a href="karmy.html" class="btn btn--red">Produkty z programu</a></div>
  </div>
</section>
'''

TRANS = phero("Transport", 'Transport<br><span class="red">i spedycja.</span>',
              "Przewozy krajowe i międzynarodowe własną flotą, 24 godziny na dobę, 7 dni w tygodniu. Pracujemy z dużymi firmami i z małymi przedsiębiorstwami.") + f'''
<section class="sec dark">
  <div class="wrap split">
    {fig("img/flota-1.jpg", "Zdjęcie: Iveco Daily w barwach Martex", alt="Bus Martex")}
    <div class="rv">
      <span class="label">Flota</span>
      <h2 style="margin-top:14px">Do 7 ton lub 14 palet na auto</h2>
      <ul class="facts">
        <li><b>Polska i cała UE</b><span>także Europa Wschodnia i Południowa</span></li>
        <li><b>24/7</b><span>dostawy just in time</span></li>
        <li><b>Door-to-door</b><span>także dla mniejszych przesyłek</span></li>
        <li><b>Euro 5 i Euro 6</b><span>Iveco, Fiat, Peugeot</span></li>
        <li><b>Zabudowy</b><span>sztywne, plandeki, chłodnie</span></li>
        <li><b>Więcej aut</b><span>przy dużych zleceniach</span></li>
      </ul>
      <div class="btns">{btn_tel("btn btn--red", "Zapytaj o wycenę")}{doc_btn("spedycja", "Broszura PDF", "btn btn--light")}</div>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec__head rv"><div><span class="label">Jak pracujemy</span><h2>Usługa pod Twój ładunek</h2></div><p class="lead">Systemy zarządzania transportem i relacjami z klientem pozwalają nam dopasować usługę do wymagań zlecenia.</p></div>
    <div class="vals">
      <div class="val rv"><h3>Zapytanie</h3><p>Dzwonisz lub piszesz: skąd, dokąd, co, ile palet lub ton i na kiedy.</p></div>
      <div class="val rv"><h3>Wycena</h3><p>Dobieramy auto i zabudowę, podajemy cenę i termin.</p></div>
      <div class="val rv"><h3>Załadunek</h3><p>Przyjeżdżamy na czas, także nocą i w weekend.</p></div>
      <div class="val rv"><h3>Dostawa</h3><p>Pod wskazany adres, just in time lub door-to-door.</p></div>
    </div>
    <div class="cgrid" style="margin-top:40px">
      {"".join(f'<div class="person rv"><b>{n}</b><span>{r}</span><a href="tel:+48{t.replace(" ", "")}">{t}</a><a href="mailto:{m}">{m}</a></div>' for n, r, t, m in PEOPLE[1:3])}
      <div class="person rv"><b>Biuro</b><span>{COMPANY['street']}</span><a href="tel:{COMPANY['tel']}">{COMPANY['phone']}</a><a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></div>
    </div>
  </div>
</section>
'''

BAK = phero("Bakalie", 'Bakalie<br><span class="red">i kasze.</span>',
            "Suszone owoce, orzechy, pestki, kasze i płatki z surowców najwyższej jakości. Dla osób, które jedzą świadomie i szukają zdrowej przekąski.") + f'''
<section class="sec">
  <div class="wrap">
    <div class="sgrid">{"".join(f'<div class="scard rv">{fig(f"img/bakalie/{slug(n)}.jpg", "Zdjęcie: " + n, "fig--dark", n)}<b>{n}</b></div>' for n in BAKALIE)}</div>
    <div class="box box--red rv" style="margin-top:50px">
      <h2>Kupisz w sklepie firmowym i w hurcie</h2>
      <p>Sklep: {SHOP['city']}, {SHOP['street']}. Dla sklepów i hurtowni: zadzwoń po cennik.</p>
      <div class="btns">{btn_tel("btn btn--light")}</div>
    </div>
  </div>
</section>
'''

ABOUT = phero("O firmie", 'Rodzinna firma<br><span class="red">od 1990 roku.</span>',
              "Martex to firma rodziny Kmieciów z Woli Rzędzińskiej koło Tarnowa. Zaczynaliśmy od karm dla gołębi, dziś mamy też transport, bakalie i serwis samochodowy.") + f'''
<section class="sec">
  <div class="wrap split">
    <div class="prose rv">
      <p>Produkujemy karmy, suplementy i akcesoria dla gołębi, papug, egzotyki i zwierząt domowych. Każdą mieszankę i każdy preparat układamy razem z utytułowanymi hodowcami i lekarzem weterynarii.</p>
      <p>Ziarno kupujemy bezpośrednio od rolników. Dzięki temu znamy jego pochodzenie, a nasze pasze są świeże i wolne od GMO.</p>
      <p>Nasze produkty trafiają do hurtowni i sklepów w Polsce i za granicą, do sklepów firmowych i prosto do hodowców. Wozimy je własną flotą, a tę samą flotę udostępniamy innym firmom jako usługę transportową.</p>
      <p>Od początku inwestujemy w sprzęt i nowe technologie, rozbudowujemy i modernizujemy zakład. Najlepszą reklamą jest dla nas zadowolony klient.</p>
      <p style="color:var(--mute)">Zarząd F.H.U. Martex</p>
    </div>
    {fig("img/zaklad.jpg", "Zdjęcie: zakład lub rodzina Kmieciów", alt="Zakład Martex")}
  </div>
</section>
<section class="sec sec--alt">
  <div class="wrap">
    <div class="vals">
      <div class="val rv"><h3>Od 1990</h3><p>Ponad trzydzieści lat na rynku, wciąż jako firma rodzinna.</p></div>
      <div class="val rv"><h3>Z hodowcami</h3><p>Receptury powstają z doświadczonymi hodowcami i lekarzem weterynarii.</p></div>
      <div class="val rv"><h3>Bez GMO</h3><p>Surowiec prosto od rolników, sprawdzony przez naszych pracowników.</p></div>
      <div class="val rv"><h3>Rzetelna Firma</h3><p>Uczestniczymy w programie Rzetelna Firma. <a href="{COMPANY['rzetelna']}" target="_blank" rel="noopener" class="more">Certyfikat →</a></p></div>
    </div>
  </div>
</section>
''' + hurt_serwis()

MAP_SRC = "https://maps.google.com/maps?q=Wola%20Rz%C4%99dzi%C5%84ska%20446B&amp;z=15&amp;output=embed"
shop_hours = esc(SHOP["hours"]) if SHOP["hours"] else "Godziny otwarcia: zadzwoń przed przyjazdem"
CONTACT = phero("Kontakt", 'Kontakt<br><span class="red">i dojazd.</span>',
                "Najszybciej załatwisz sprawę telefonicznie. Do handlu, transportu i księgowości masz bezpośrednie numery poniżej.") + f'''
<section class="sec">
  <div class="wrap">
    <div class="cgrid">
      <div class="cbox rv"><h3>Biuro i siedziba</h3><a href="tel:{COMPANY['tel']}" class="cbig">{COMPANY['phone']}</a><a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a><span>{COMPANY['name']}<br>{COMPANY['street']}</span></div>
      <div class="cbox rv"><h3>Sklep firmowy</h3><span class="cbig">{SHOP['street'].replace('ul. ', '')}</span><span>{SHOP['city']}</span><span class="muted">{shop_hours}</span></div>
      <div class="cbox rv"><h3>Na Facebooku</h3><p class="muted">Nowości, promocje i zdjęcia od hodowców.</p><a href="{COMPANY['facebook']}" target="_blank" rel="noopener" class="more">facebook.com/MartexTarnow →</a></div>
    </div>
  </div>
</section>
<section class="sec sec--alt">
  <div class="wrap">
    <div class="sec__head rv"><div><span class="label">Bezpośrednio</span><h2>Z kim rozmawiać</h2></div></div>
    <div class="people">
      {"".join(f'<div class="person rv"><b>{n}</b><span>{r}</span><a href="tel:+48{t.replace(" ", "")}">{t}</a><a href="mailto:{m}">{m}</a></div>' for n, r, t, m in PEOPLE)}
    </div>
  </div>
</section>
<section class="sec" id="dojazd">
  <div class="wrap">
    <div class="map" data-map="{MAP_SRC}" data-title="Mapa: Martex, Wola Rzędzińska 446B">
      <div class="map__consent"><b style="font-family:var(--display);font-size:28px;text-transform:uppercase">Mapa Google</b><p class="muted">Mapa wczyta się po zgodzie na pliki cookies Google.</p><button type="button" class="btn btn--red" data-map-load>Pokaż mapę</button></div>
    </div>
  </div>
</section>
''' + hurt_serwis()

POLICY = phero("Polityka prywatności", 'Polityka<br><span class="red">prywatności.</span>',
               "Krótko i po ludzku: jakie dane przetwarzamy, po co i jakie masz prawa.") + f'''
<section class="sec">
  <div class="wrap legal">
    <p class="upd">Ostatnia aktualizacja: listopad 2026</p>
    <h2>1. Kto jest administratorem</h2>
    <p>Administratorem danych osobowych jest <b>{COMPANY['name']}</b>, {COMPANY['street']}, NIP {COMPANY['nip']}.</p>
    <p>Kontakt w sprawach danych osobowych: telefon <a href="tel:{COMPANY['tel']}">{COMPANY['phone']}</a>, e-mail <a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a> lub listownie na adres siedziby.</p>
    <h2>2. Jakie dane i po co</h2>
    <p>Strona nie ma formularzy ani kont użytkowników — nie zbieramy przez nią imion, adresów e-mail ani numerów telefonów.</p>
    <table>
      <tr><th>Sytuacja</th><th>Dane</th><th>Cel i podstawa</th></tr>
      <tr><td>Dzwonisz lub piszesz e-mail</td><td>numer telefonu lub adres e-mail, treść wiadomości, dane do zamówienia</td><td>obsługa zapytania i zamówienia (art. 6 ust. 1 lit. b i f RODO)</td></tr>
      <tr><td>Odwiedzasz stronę</td><td>adres IP, typ przeglądarki, data i godzina wizyty (logi serwera)</td><td>bezpieczeństwo i prawidłowe działanie strony (art. 6 ust. 1 lit. f RODO)</td></tr>
      <tr><td>Wczytujesz mapę Google</td><td>adres IP, pliki cookies Google</td><td>pokazanie dojazdu — wyłącznie za Twoją zgodą (art. 6 ust. 1 lit. a RODO)</td></tr>
    </table>
    <h2>3. Komu przekazujemy dane</h2>
    <ul>
      <li><b>Vercel Inc.</b> — firma hostingowa, na której serwerach działa strona (logi serwera).</li>
      <li><b>Google Ireland Ltd.</b> — dostawca map, po Twojej zgodzie.</li>
      <li>Podmiotom uprawnionym na podstawie przepisów prawa, gdy tego zażądają.</li>
    </ul>
    <p>Vercel i Google mogą przetwarzać dane także poza Europejskim Obszarem Gospodarczym (m.in. w USA), na podstawie mechanizmów przewidzianych w RODO, takich jak EU-US Data Privacy Framework lub standardowe klauzule umowne.</p>
    <h2>4. Jak długo</h2>
    <ul>
      <li>Dane z kontaktu — przez czas obsługi zapytania lub zamówienia, a potem przez okres wymagany przepisami (np. podatkowymi) lub do przedawnienia roszczeń.</li>
      <li>Logi serwera — przez okres ustalony przez dostawcę hostingu, zwykle kilka–kilkanaście dni.</li>
      <li>Ustawienia zapisane w przeglądarce — do czasu, aż je usuniesz.</li>
    </ul>
    <h2>5. Pliki cookies i pamięć przeglądarki</h2>
    <table>
      <tr><th>Nazwa</th><th>Rodzaj</th><th>Po co</th></tr>
      <tr><td><code>martex-grupa-consent</code></td><td>niezbędne (pamięć przeglądarki)</td><td>zapamiętuje Twoją decyzję o cookies</td></tr>
      <tr><td><code>martex-grupa-theme</code></td><td>niezbędne (pamięć przeglądarki)</td><td>zapamiętuje wybrany motyw — jasny lub ciemny</td></tr>
      <tr><td>Cookies Google Maps</td><td>zewnętrzne, za zgodą</td><td>działanie osadzonej mapy Google</td></tr>
    </table>
    <p>Nie używamy cookies reklamowych ani narzędzi śledzących. Decyzję możesz zmienić w każdej chwili w <button type="button" data-cookie-settings style="color:var(--red-t);text-decoration:underline">ustawieniach cookies</button> (link jest też w stopce) albo w ustawieniach przeglądarki.</p>
    <h2>6. Twoje prawa</h2>
    <p>Masz prawo do dostępu do swoich danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przenoszenia, sprzeciwu wobec przetwarzania opartego na prawnie uzasadnionym interesie oraz do wycofania zgody w dowolnym momencie (bez wpływu na zgodność z prawem przetwarzania przed jej wycofaniem).</p>
    <p>Możesz złożyć skargę do Prezesa Urzędu Ochrony Danych Osobowych (ul. Stawki 2, 00-193 Warszawa, <a href="https://uodo.gov.pl" target="_blank" rel="noopener">uodo.gov.pl</a>).</p>
    <p>Nie podejmujemy decyzji w sposób zautomatyzowany i nie profilujemy.</p>
    <h2>7. Linki zewnętrzne</h2>
    <p>Na stronie są odnośniki do Facebooka, Google Maps, programu Rzetelna Firma i strony Serwisu Samochodowego Martex. Po ich kliknięciu obowiązują zasady prywatności tych serwisów.</p>
  </div>
</section>
'''

page("index.html", "home", "Grupa Martex — karmy dla gołębi, transport, bakalie | Tarnów",
     "Martex z Woli Rzędzińskiej koło Tarnowa: producent karm i suplementów dla gołębi i papug od 1990 roku, transport i spedycja w Polsce i UE, bakalie i kasze. Tel. 14 679 23 49.", HOME)
page("karmy.html", "karmy", "Karmy i suplementy dla gołębi — katalog | Martex Tarnów",
     "Katalog Martex: mieszanki dla gołębi (lotowe, rozpłodowe, dla młodych, wdowce), suplementy, olejki, elektrolity, karmy dla papug i ptaków oraz akcesoria do gołębnika.", KARMY)
page("program-lotowy.html", "program", "Program lotowy dla gołębi — żywienie dzień po dniu | Martex",
     "Program żywienia gołębi Martex: parowanie, chów młodych, loty młodych i loty seniorów. Plan na każdy dzień tygodnia, do wydruku.", PROG)
page("transport.html", "transport", "Transport i spedycja krajowa i międzynarodowa | Martex Tarnów",
     "Transport Martex: do 7 ton lub 14 palet na auto, 24/7, Polska i cała UE. Zabudowy sztywne, plandeki, chłodnie, Euro 5 i 6. Just in time i door-to-door.", TRANS)
page("bakalie.html", "bakalie", "Bakalie i kasze — suszone owoce i orzechy | Martex Tarnów",
     "Bakalie Martex: żurawina, goji, morele, daktyle, migdały, orzechy, pestki, kasze i płatki owsiane. Sklep firmowy w Tarnowie i sprzedaż hurtowa.", BAK)
page("o-firmie.html", "o-firmie", "O firmie — rodzinna firma od 1990 roku | Grupa Martex",
     "F.H.U. Martex — rodzinna firma Kmieciów z Woli Rzędzińskiej. Od 1990 roku produkujemy karmy dla gołębi, prowadzimy transport i sprzedajemy bakalie.", ABOUT)
page("kontakt.html", "kontakt", "Kontakt — Grupa Martex, Wola Rzędzińska 446B",
     "Kontakt z Martex: biuro 14 679 23 49, biuro@martextarnow.pl, Wola Rzędzińska 446B. Sklep firmowy: Tarnów, ul. Szkotnik 2B. Bezpośrednie numery do handlu i logistyki.", CONTACT)
page("polityka-prywatnosci.html", "", "Polityka prywatności i cookies — Grupa Martex",
     "Polityka prywatności i plików cookies strony Grupy Martex.", POLICY)
