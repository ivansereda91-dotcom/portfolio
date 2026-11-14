#!/usr/bin/env python3
"""Собирает статический сайт-портфолио в папку site/. Тексты — здесь, фото — по images.txt."""
import html
import os
import shutil

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

CONTACT = {
    "phone": "+33 7 45 03 31 38", "tel": "+33745033138",
    "email": "ivansereda91@yahoo.com",
    "instagram": "sereda_foto",
    "telegram": "ivansereda",
}

ABOUT = {
    "en": "Ivan Sereda is a Russian photographer who lives and works in Nice, France. He specializes in "
          "architectural, landscape and travel photography, shooting on film in different formats. One of his "
          "favourite subjects is the interaction between the city and nature.",
    "fr": "Ivan Sereda est un photographe russe qui vit et travaille à Nice. Il se consacre à la photographie "
          "d’architecture, de paysage et de voyage, sur film et dans différents formats. L’un de ses sujets "
          "de prédilection est la rencontre entre la ville et la nature.",
}

SERIES = [
    {
        "slug": "groynes", "count": 21, "cover": "groynes/01.jpg",
        "title": {"en": "Groynes", "fr": "Épis"},
        "short": {"en": "Coastal defences on the Black Sea", "fr": "Ouvrages côtiers de la mer Noire"},
        "text": {
            "en": ["A photo series about the engineering structures built to protect the coast of the Krasnodar "
                   "region (Russia) from storms.",
                   "Many of these standard constructions are now in very different condition — technically and "
                   "visually — and local residents and tourists use them in their own ways.",
                   "The pictures show how people reshape the environment to fit their goals and circumstances, "
                   "and how each of these identical structures becomes a unique protector against the forces "
                   "of nature."],
            "fr": ["Une série consacrée aux ouvrages construits pour protéger le littoral de la région de "
                   "Krasnodar (Russie) des tempêtes.",
                   "Ces constructions standardisées se trouvent aujourd’hui dans des états très divers, techniquement "
                   "comme visuellement, et les habitants comme les touristes se les approprient chacun à leur façon.",
                   "Les images montrent comment l’homme transforme son environnement selon ses besoins, et comment "
                   "chacun de ces ouvrages identiques devient un protecteur unique face aux forces de la nature."],
        },
    },
    {
        "slug": "the-sea", "count": 10, "cover": "the-sea/01.jpg",
        "title": {"en": "The Sea", "fr": "La mer"},
        "short": {"en": "A place of quiet happiness", "fr": "Un lieu de bonheur simple"},
        "text": {
            "en": ["People live with a lot of stress: wars and violence, financial instability and unemployment, "
                   "poverty and hunger. The sea gives peace and tranquillity — a chance to be alone or to spend "
                   "time with family, to read a book or play ball with friends, to watch the sunset or the sunrise.",
                   "The sea is one of the few places where one can still feel pure happiness."],
            "fr": ["Nous vivons avec beaucoup de stress : guerres et violences, instabilité financière et chômage, "
                   "pauvreté et faim. La mer apporte calme et sérénité — l’occasion d’être seul ou en famille, "
                   "de lire un livre ou de jouer au ballon entre amis, de regarder le coucher ou le lever du soleil.",
                   "La mer est l’un des rares endroits où l’on peut encore ressentir un bonheur pur."],
        },
    },
    {
        "slug": "no-name", "count": 18, "cover": "no-name/cover.jpg",
        "title": {"en": "No Name", "fr": "Sans titre"},
        "short": {"en": "Instant film, one moment at a time", "fr": "Film instantané, un instant à la fois"},
        "text": {
            "en": ["A limited series of photographs taken with an Instax instant camera. The project emphasizes the "
                   "significance of a single moment — the tangible experience of holding a printed photo just "
                   "seconds after taking it.",
                   "Modern cameras and smartphones produce high-quality images and store vast amounts of them, so it "
                   "is easy to overlook the emotional weight of the moment a photo is taken. Thousands of nearly "
                   "identical images end up in the cloud, never viewed again, and the memory of a place that felt "
                   "so meaningful stays buried in the phone."],
            "fr": ["Une série limitée de photographies prises avec un appareil instantané Instax. Le projet met en "
                   "valeur la force d’un seul instant — le plaisir de tenir une photo imprimée quelques secondes "
                   "après l’avoir prise.",
                   "Les appareils et smartphones actuels produisent des images de grande qualité et en stockent des "
                   "milliers ; on en oublie facilement l’émotion du moment de la prise de vue. Des images presque "
                   "identiques s’accumulent dans le cloud sans jamais être regardées, et le souvenir d’un lieu "
                   "important reste enfoui dans le téléphone."],
        },
    },
]

UI = {
    "work": ("Work", "Travaux"), "about": ("About", "À propos"), "contact": ("Contact", "Contact"),
    "role": ("Photographer · Nice", "Photographe · Nice"), "back": ("All series", "Toutes les séries"),
    "photos": ("photographs", "photographies"), "next": ("Next series", "Série suivante"),
}

e = html.escape


def t(en: str, fr: str, tag: str = "span") -> str:
    return f'<{tag} lang="en">{e(en)}</{tag}><{tag} lang="fr">{e(fr)}</{tag}>'


def ui(k: str) -> str:
    return t(*UI[k])


def img(path: str, alt: str, sizes: str, cls: str = "", lazy: bool = True, idx: int | None = None) -> str:
    base = "/img/" + path[:-4]
    attrs = f' data-i="{idx}"' if idx is not None else ""
    return (f'<img class="{cls}" src="{base}_m.jpg" srcset="{base}_s.jpg 800w, {base}_m.jpg 1600w" '
            f'sizes="{sizes}" alt="{e(alt)}"{" loading=lazy" if lazy else ""} decoding="async"'
            f' data-full="{base}_m.jpg"{attrs}>')


def page(title: str, body: str, desc: str) -> str:
    return f"""<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="https://ivansereda.fr/img/hero_m.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script>try{{var l=localStorage.getItem('lang')||((navigator.language||'').slice(0,2)==='fr'?'fr':'en');document.documentElement.dataset.lang=l;document.documentElement.lang=l}}catch(e){{}}</script>
</head>
<body>
<header class="top">
  <a class="name" href="/">Ivan Sereda</a>
  <nav>
    <a href="/#work">{ui('work')}</a>
    <a href="/#about">{ui('about')}</a>
    <a href="/#contact">{ui('contact')}</a>
    <button class="lang" type="button" aria-label="Language"><span lang="en">FR</span><span lang="fr">EN</span></button>
  </nav>
</header>
{body}
<footer class="foot" id="contact">
  <div class="foot-name">Ivan Sereda</div>
  <ul class="contacts">
    <li><a href="tel:{CONTACT['tel']}">{e(CONTACT['phone'])}</a></li>
    <li><a href="mailto:{CONTACT['email']}">{e(CONTACT['email'])}</a></li>
    <li><a href="https://www.instagram.com/{CONTACT['instagram']}/" target="_blank" rel="noopener">Instagram @{CONTACT['instagram']}</a></li>
    <li><a href="https://t.me/{CONTACT['telegram']}" target="_blank" rel="noopener">Telegram @{CONTACT['telegram']}</a></li>
  </ul>
  <div class="foot-small">Nice, France · © Ivan Sereda</div>
</footer>
<div class="lb" hidden><button class="lb-x" type="button" aria-label="Close">×</button><button class="lb-p" type="button" aria-label="Previous">‹</button><img alt=""><button class="lb-n" type="button" aria-label="Next">›</button><div class="lb-c"></div></div>
<script src="/site.js" defer></script>
</body>
</html>
"""


def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    cards = []
    for s in SERIES:
        cards.append(f"""<a class="card" href="/{s['slug']}/">
      {img(s['cover'], s['title']['en'], '(max-width: 700px) 100vw, 33vw', 'card-img')}
      <span class="card-t">{t(s['title']['en'], s['title']['fr'])}</span>
      <span class="card-s">{t(s['short']['en'], s['short']['fr'])}</span>
    </a>""")
    home = f"""<main>
<section class="hero">
  {img('hero.jpg', 'Ivan Sereda — photograph', '(max-width: 900px) 100vw, 60vw', 'hero-img', lazy=False)}
  <div class="hero-txt"><h1>Ivan Sereda</h1><p>{ui('role')}</p></div>
</section>
<section class="work" id="work">
  <h2 class="label">{ui('work')}</h2>
  <div class="cards">
    {''.join(cards)}
  </div>
</section>
<section class="about" id="about">
  <h2 class="label">{ui('about')}</h2>
  <div class="about-grid">
    {img('about.jpg', 'Ivan Sereda', '(max-width: 700px) 100vw, 40vw', 'about-img')}
    <p class="about-txt">{t(ABOUT['en'], ABOUT['fr'])}</p>
  </div>
</section>
</main>"""
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("Ivan Sereda — Photographer, Nice", home,
                     "Ivan Sereda — film photographer based in Nice: architecture, landscape and travel."))

    for n, s in enumerate(SERIES):
        nxt = SERIES[(n + 1) % len(SERIES)]
        paras = "".join(f"<p>{t(en, fr)}</p>" for en, fr in zip(s["text"]["en"], s["text"]["fr"]))
        photos = "".join(img(f"{s['slug']}/{i:02d}.jpg", f"{s['title']['en']} — {i}",
                             "(max-width: 900px) 100vw, 1100px", "ph", idx=i - 1)
                         for i in range(1, s["count"] + 1))
        body = f"""<main class="series">
<a class="back" href="/#work">← {ui('back')}</a>
<header class="s-head">
  <h1>{t(s['title']['en'], s['title']['fr'])}</h1>
  <div class="s-meta">{s['count']} {ui('photos')}</div>
  <div class="s-text">{paras}</div>
</header>
<div class="photos">{photos}</div>
<a class="next" href="/{nxt['slug']}/">{ui('next')}: {t(nxt['title']['en'], nxt['title']['fr'])} →</a>
</main>"""
        d = os.path.join(OUT, s["slug"])
        os.makedirs(d)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(f"{s['title']['en']} — Ivan Sereda", body, s["text"]["en"][0]))

    for name in ("style.css", "site.js", "favicon.svg", "404.html"):
        shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), name), OUT)


if __name__ == "__main__":
    build()
    print("site/ готов")
