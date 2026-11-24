#!/usr/bin/env python3
"""I Love Being Catholic v2 — generates the 7 pages. Copy comes from the brochure (sentence case headings)."""
import os
OUT = '/home/claude/v2'
import time
V = str(int(time.time()))

def svg(inner, extra='fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"'):
    return f'<svg viewBox="0 0 24 24" {extra} aria-hidden="true">{inner}</svg>'
BOLD = 'fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"'
ARROW = svg('<path d="M5 12h14M13 6l6 6-6 6"/>', BOLD)
UP = svg('<path d="M12 19V5M6 11l6-6 6 6"/>', BOLD)
I_CAL = svg('<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4M8 14h2M14 14h2M8 17.5h2"/>')
I_HOUSE = svg('<path d="M3 21V10.5L12 3l9 7.5V21zM9.5 21v-6.5h5V21"/>')
I_FLAME = svg('<path d="M12 2.5c.5 3.2 4.8 5.2 4.8 10a4.8 4.8 0 0 1-9.6 0c0-2 .9-3.3 2.2-4.4.1 1.7.9 2.6 1.9 2.8C11.8 8.6 11.2 5.6 12 2.5z"/><path d="M9 21.5h6"/>')
I_BOOK = svg('<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3H19v15H6a2 2 0 0 0-2 2zM4 20v1.5h15M9 7.5h6"/>')
I_COMPASS = svg('<circle cx="12" cy="12" r="9"/><path d="M15.8 8.2l-2 5.6-5.6 2 2-5.6z"/>')
I_PENCIL = svg('<path d="M4 20h4.2L19.5 8.7a2 2 0 0 0 0-2.8l-1.4-1.4a2 2 0 0 0-2.8 0L4 15.8zM13.5 6.3l4.2 4.2"/>')
I_PHONES = svg('<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><path d="M4 15h3.2v5H5.5A1.5 1.5 0 0 1 4 18.5zM20 15h-3.2v5h1.7a1.5 1.5 0 0 0 1.5-1.5z"/>')
I_NET = svg('<circle cx="12" cy="4" r="2"/><circle cx="20" cy="10" r="2"/><circle cx="17" cy="19.5" r="2"/><circle cx="7" cy="19.5" r="2"/><circle cx="4" cy="10" r="2"/><path d="M13.7 5.2l4.6 3.6M19.4 11.9l-1.7 5.7M15 19.5h-6M6.3 17.6L4.6 11.9M5.7 8.8l4.6-3.6M12 6v4.2M12 10.2l6 .1M12 10.2L6 10.2M12 10.2l4 7.6M12 10.2l-4 7.6"/>')
I_PIN = svg('<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>')
I_PHONE = svg('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>')
I_MAIL = svg('<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 7.5l8.5 6 8.5-6"/>')
I_GLOBE = svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>')

NAV = [('index.html', 'Home'), ('invitation.html', 'Welcome'), ('settings.html', 'Formats'),
       ('units.html', 'Lessons'), ('resources.html', 'Library'), ('beginning.html', 'Pathway')]
SITE = 'I love being Catholic'

def header(cur):
    AC = ' aria-current="page"'
    items = ''.join(f'<li><a href="{h}"{AC if h == cur else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"></div>
<header class="header"><div class="bar">
<a class="brand" href="index.html" aria-label="{SITE} — home"><img src="assets/img/seal-512.png" alt="" width="46" height="46"><b>{SITE}</b></a>
<button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
<nav class="nav" id="nav" aria-label="Main"><ul>{items}<li><a class="cta" href="get-started.html"{AC if cur == 'get-started.html' else ''}>Get started</a></li></ul></nav>
</div></header>'''

I_MAIL = svg('<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 7 8.5 6.5L20.5 7"/>')
I_PHONE = svg('<path d="M5 3.5h3.5l1.8 4.5-2.2 1.4a11 11 0 0 0 5.5 5.5l1.4-2.2 4.5 1.8V18a2 2 0 0 1-2 2A15 15 0 0 1 3 5.5a2 2 0 0 1 2-2z"/>')
I_GLOBE = svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9S14.6 18.4 12 21c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z"/>')
I_PIN = svg('<path d="M12 21s7-6.2 7-11.5a7 7 0 0 0-14 0C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>')
I_HEART = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 21s-8-5.2-8-11a4.6 4.6 0 0 1 8-3 4.6 4.6 0 0 1 8 3c0 5.800-8 11-8 11z"/></svg>'

def footer():
    links = ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV + [('get-started.html', 'Get started')])
    return f'''<footer class="foot"><div class="foot-glow" aria-hidden="true"></div>
<div class="wrap foot-grid">
<div class="foot-brand"><div class="fb"><img src="assets/img/seal-512.png" alt="" width="72" height="72"><b>{SITE}</b></div>
<p>Five connected units. One welcoming invitation.</p>
<div class="foot-ico"><a href="mailto:liguori@liguori.org" aria-label="Email Liguori Publications">{I_MAIL}</a><a href="tel:+18003259521" aria-label="Call Liguori Publications">{I_PHONE}</a><a href="https://www.liguori.org" target="_blank" rel="noopener" aria-label="Visit liguori.org">{I_GLOBE}</a></div></div>
<div><h4>Explore</h4><ul class="foot-list">{links}</ul></div>
<div><h4>Publisher</h4><img class="lg" src="assets/img/liguori-logo.png" alt="Liguori Publications, A Redemptorist Ministry" width="200" height="94"></div>
<div><h4>Contact</h4><ul class="foot-contact">
<li>{I_PIN}<span>200 Liguori Drive<br>Liguori, MO 63057</span></li>
<li>{I_PHONE}<a href="tel:+18003259521">800-325-9521</a></li>
<li>{I_MAIL}<a href="mailto:liguori@liguori.org">liguori@liguori.org</a></li>
<li>{I_GLOBE}<a href="https://www.liguori.org" target="_blank" rel="noopener">liguori.org</a></li></ul></div>
</div>
<div class="foot-bar"><div class="wrap">
<div class="fb-left"><span class="copy">&copy; I Love Being Catholic</span><button type="button" class="cookie-manage">Manage cookies</button><button type="button" class="ed-lock" aria-label="Site editor sign in" title="Site editor"><svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg></button></div>
<div class="credit"><span>Developed by</span><img src="assets/img/sixjars-color.png" alt="Six Jars Global" width="837" height="267"></div>
</div></div></footer>
<div class="cookie" id="cookie" role="dialog" aria-labelledby="ck-t" aria-live="polite" hidden>
<div><b id="ck-t">Cookies and storage</b><p>This site uses only essential browser storage to remember your progress, checklists and cookie choice. It does not use advertising or tracking cookies.</p></div>
<div class="ck-btns"><button type="button" class="btn small" data-ck="all">Accept</button><button type="button" class="btn light small" data-ck="essential">Essential only</button></div></div>
<a class="to-next" href="invitation.html" aria-label="Next page"><span class="nx-t">Next</span><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
<button class="to-top" aria-label="Back to top">{UP}</button>'''

def cta(title='An invitation to begin', text='Bring together adults who want to understand their faith more fully, including those who are unsure where to begin. Choose a format that suits your community, invite people warmly, and make room for their questions.',
        b1=('get-started.html', 'Plan your next step'), b2=('units.html', 'Explore the five units')):
    return f'''<section class="cta on-ink"><div class="wrap"><img class="s" src="assets/img/seal-512.png" alt="" width="110" height="110" data-reveal="zoom">
<h2 data-reveal>{title}</h2><p data-reveal style="--d:.1s">{text}</p>
<div class="btns" data-reveal style="--d:.2s"><a class="btn gold" href="{b1[0]}">{b1[1]}{ARROW}</a><a class="btn light" href="{b2[0]}">{b2[1]}</a></div></div></section>'''

def page(fname, title, desc, body, cta_html=None):
    import re as _re
    _n = [0]
    def _band(m):
        _n[0] += 1
        return '<section class="section ' + ('band-w' if _n[0] % 2 else 'band-m') + ' acc' + str(_n[0] % 3 + 1) + (' on-ink' if 'on-ink' in m.group(0) else '')
    body = _re.sub(r'<section class="section(?: s[1-5])?(?: on-ink)?', _band, body)
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="color-scheme" content="light"><meta name="format-detection" content="telephone=no"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="ILBC">
<title>{title}</title><meta name="description" content="{desc}"><meta name="theme-color" content="#a20e2b">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<link rel="icon" type="image/png" href="assets/img/favicon.png"><link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/crimson-pro-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css?v={V}"></head><body>
{header(fname)}
<main id="main">
{body}
{cta_html if cta_html is not None else cta()}
</main>
{footer()}
<script src="assets/js/main.js?v={V}"></script>
<script src="assets/js/admin.js?v={V}" defer></script></body></html>'''
    open(os.path.join(OUT, fname), 'w', encoding='utf-8').write(html)

def phero(crumb, h1, sub, bg):
    return f'''<section class="page-hero"><div class="bg" data-parallax style="background-image:url(assets/img/{bg})"></div>
<div class="wrap"><div class="panel"><div class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; {crumb}</div><h1>{h1}</h1><p>{sub}</p></div></div></section>'''

def head(eyebrow, h2, p='', center=False):
    pp = f'<p class="lead" data-reveal style="--d:.1s">{p}</p>' if p else ''
    return f'<div class="sec-head{" center" if center else ""}"><span class="eyebrow" data-reveal>{eyebrow}</span><h2 data-reveal style="--d:.05s">{h2}</h2>{pp}</div>'

UNITS = [
 ('The Magisterium and the Deposit of Faith', 'How does the Church receive and hand on the faith?',
  'This unit introduces the deposit of faith entrusted to the Church and the Magisterium, her teaching office. Participants explore how Scripture and Sacred Tradition transmit the one apostolic faith, and how the Magisterium serves the Word of God.',
  'The relationship among Scripture, Tradition, and the Church’s teaching, and why it matters when reading the Bible, celebrating the sacraments, or considering a Catholic practice.'),
 ('The Catechism as a Guide to the Faith', 'The Catechism of the Catholic Church offers a coherent account of what Catholics believe, celebrate, live, and pray.',
  'This unit helps participants become comfortable using it as a guide, following a question from its biblical foundations to the Church’s teaching and its place in daily life.',
  'How to find a teaching, read it in context, and recognize its connections with worship, moral life, and prayer.'),
 ('Sacred Scripture Whole and Entire', 'The Bible is received and read within the Church’s living Tradition.',
  'This unit introduces ways of reading inspired Scripture that attend to literary form, historical setting, the unity of the Bible, and the coherence of faith. A passage heard at Mass becomes an invitation to discover its wider meaning.',
  'How to read a passage in context, recognize the limits of an isolated quotation, and connect the Word proclaimed in the liturgy with doctrine and sacramental life.'),
 ('The Sacraments as Encounters with Christ', 'The seven sacraments are encounters with Jesus Christ, who acts through these effective signs of grace.',
  'This unit explores their signs and words and the place of each sacrament in Catholic life. Speaking of Christ as “the Sacrament” points to him as their source, not to an eighth sacrament.',
  'The seven sacraments, their relationship to Christ’s action, and the connections among Scripture, the Church’s teaching, sacramental celebration, and daily discipleship.'),
 ('The Smells and the Bells', 'Catholic life engages the senses through prayer, ritual, disciplines, and customs.',
  'This unit explores liturgy, sacramentals, devotions, the Church year, and local practices. Participants consider how these expressions of faith nourish prayer and lead toward charity and everyday discipleship.',
  'The distinction among a sacrament, a sacramental, and a devotion, and the difference between the Church’s shared faith and customs that can vary across times and places.'),
]
SHORT = ['Magisterium', 'Catechism', 'Scripture', 'Sacraments', 'Smells & bells']

# ================= HOME =================
orbit = ''.join(f'<div class="slot" style="--a:{i*72}deg"><span class="sticker{" gold" if i%2==0 else ""}">{n}</span></div>' for i, n in enumerate(SHORT))
ucards = ''.join(f'''<a class="card ucard" href="units.html#u{i+1}"><span class="num">{i+1}</span><h3>{t}</h3><p>{d}</p><span class="more">Explore {ARROW}</span></a>''' for i, (t, d, *_ ) in enumerate(UNITS))
ticker = ''.join(f'<span><b>I love being Catholic because of</b> {x}</span>' for x in ['the Magisterium and the Deposit of Faith', 'the Catechism', 'Sacred Scripture', 'the Sacraments', 'the Smells and Bells'] * 2)
home = f'''
<section class="hero"><div class="blob a"></div><div class="blob b"></div><div class="wrap">
<div><span class="eyebrow hero-line">Parish adult formation</span>
<h1 class="hero-line" style="--i:1">I love being <span class="hl">Catholic</span></h1>
<p class="sub hero-line" style="--i:2">An invitation to parish adult formation</p>
<p class="hero-line" style="--i:3">We invite your parish to consider I Love Being Catholic as an essential part of its adult formation. The program helps people see how the Church’s teaching, Sacred Scripture, the sacraments, and everyday Catholic life belong together in Jesus Christ. Through five connected units, adults find a welcoming approach to learning, asking questions, and deepening their understanding of the faith they share.</p>
<strong class="tagline hero-line" style="--i:4">Five connected units. One welcoming invitation.</strong>
<div class="btns hero-line" style="--i:5"><a class="btn" href="units.html">Explore the five units{ARROW}</a><a class="btn light" href="settings.html">Choose a setting</a></div></div>
<div class="stage hero-line" style="--i:3"><div class="orbit"></div><div class="orbit-wrap">{orbit}</div>
<div class="seal"><img src="assets/img/seal-512.png" alt="I Love Being Catholic seal: a golden cross with rays on a green field" width="300" height="300"></div>
</div>
</div></section>

<div class="marquee" aria-label="I love being Catholic because of the Magisterium, the Catechism, Sacred Scripture, the Sacraments, the Smells and Bells"><div class="track">{ticker}</div></div>

<section class="section s5"><div class="wrap"><div class="stats rounds" data-reveal>
<div class="stat"><b data-count="5">0</b><small>connected units</small></div>
<div class="stat"><b data-count="3">0</b><small>parish formats to choose from</small></div>
<div class="stat"><b><span data-count="60">0</span>–<span data-count="75">0</span></b><small>minutes to plan for a gathering</small></div>
<div class="stat"><b data-count="5">0</b><small>twelve-week studies to continue</small></div></div></div></section>

<section class="section s3"><div class="wrap split">
<div>{head('The invitation', 'A familiar gesture can open the door to a fuller faith')}
<p data-reveal>A familiar gesture, a passage heard at Mass, or a question about Church teaching can open the door to a fuller understanding of Catholic faith. I Love Being Catholic begins with those recognizable experiences and helps participants follow the connections among belief, worship, prayer, and daily choices.</p>
<p data-reveal>No prior course of study is assumed. Longtime parishioners and adults seeking a fresh understanding are invited to bring their questions, with room for honest reflection.</p>
<a class="link-arrow" data-reveal href="invitation.html">Read the invitation {ARROW}</a></div>
<div class="photo" style="--rot:2deg" data-reveal="right"><img src="assets/img/discussion.jpg" alt="Parishioners of different ages talking together around a table with Bibles and notebooks" loading="lazy"></div>
</div></section>

<section class="section s1"><div class="wrap">
{head('Explore the faith', 'Five connected units', 'Each unit begins with the invitation “I love being Catholic because of” and explores one part of the faith in relationship to the whole.')}
<div class="scroller" data-reveal tabindex="0" aria-label="The five units">{ucards}</div></div></section>

<section class="section s5"><div class="wrap">
{head('Choose a setting', 'A place within parish life', 'Consider I Love Being Catholic as a continuing resource for your parish’s adult formation. At least three formats offer ways to shape the experience around your community.', center=True)}
<div class="arches">
<article class="card res-card" data-reveal><div class="ic">{I_CAL}</div><span class="sticker">Five Sundays</span><h3>A parish preaching event</h3><p>Introduce one unit each week through the bulletin and the homily, then gather in small groups after Mass.</p><a class="link-arrow" href="settings.html#sundays">Learn more {ARROW}</a></article>
<article class="card res-card" data-reveal style="--d:.1s"><div class="ic">{I_HOUSE}</div><span class="sticker">One weekend</span><h3>A parish retreat weekend</h3><p>Five presentations with discussion, from Friday evening to Sunday, in your own parish.</p><a class="link-arrow" href="settings.html#retreat">Learn more {ARROW}</a></article>
<article class="card res-card" data-reveal style="--d:.2s"><div class="ic">{I_FLAME}</div><span class="sticker">Five nights</span><h3>A parish mission</h3><p>A missionary presents one subject each night within a service of hymns, music, and prayers.</p><a class="link-arrow" href="settings.html#mission">Learn more {ARROW}</a></article>
</div></div></section>

<section class="section s4"><div class="wrap split">
<div>{head('Prepared and available', 'Resources for leaders and participants', 'The materials work together while allowing your parish to choose the format and pace that best fit its community.')}
<p data-reveal>Four resources share one structure, so readers at home, facilitators, and listeners all meet the same clear account of the faith.</p>
<a class="btn light" data-reveal href="resources.html">See all resources{ARROW}</a></div>
<div class="honey" data-reveal="right"><div class="row a">
<a class="hexwrap" href="resources.html"><div class="hex"><span class="ic">{I_BOOK}</span><h3>Narrative guide</h3><p>The main account of the faith</p></div></a>
<a class="hexwrap" href="resources.html"><div class="hex"><span class="ic">{I_COMPASS}</span><h3>Leader guide</h3><p>Equips each gathering’s leader</p></div></a></div>
<div class="row b">
<a class="hexwrap" href="resources.html"><div class="hex"><span class="ic">{I_PENCIL}</span><h3>Participant guide</h3><p>Key ideas, notes, reflection</p></div></a>
<a class="hexwrap" href="resources.html"><div class="hex"><span class="ic">{I_PHONES}</span><h3>Podcast companion</h3><p>Short episodes with transcripts</p></div></a></div></div>
</div></section>

<section class="section on-ink"><div class="wrap split">
<div>{head('A beginning, not an ending', 'More than a five-week experience')}
<p data-reveal>I Love Being Catholic is an invitation to begin an ongoing journey of discovery, conversation, and growth in faith. The introductory program is supported by five additional, twelve-week programs that explore its subjects more deeply.</p>
<p data-reveal>Two are complete and ready for use. Three others are under development and scheduled to be ready by October 1, 2027.</p>
<p class="count" data-reveal><span data-countdown="2027-10-01">0</span> <small style="font:600 1rem var(--sans);">days until all five are ready</small></p>
<a class="btn gold" data-reveal href="beginning.html">See the pathway{ARROW}</a></div>
<div class="photo" style="--rot:-2deg" data-reveal="right"><img src="assets/img/wedding.jpg" alt="A couple exchanging vows before a priest in a bright church" loading="lazy"></div></div></section>
'''
page('index.html', 'I love being Catholic — An invitation to parish adult formation', 'Five connected units. One welcoming invitation. A parish adult formation program from Liguori Publications.', home,
     cta('Bring I Love Being Catholic to your parish', 'The five narratives, coordinated leader and participant guides, podcasts, and supporting materials are prepared and available for use.'))

# ================= INVITATION =================
kit = [('Five connected units', I_NET), ('A narrative guide', I_BOOK), ('A leader guide', I_COMPASS), ('A participant guide', I_PENCIL), ('Companion podcasts with transcripts', I_PHONES)]
aims = ['Connect belief with worship and daily life', 'Find reliable sources for further learning', 'Understand more clearly the meaning of Catholic practices']
inv = f'''{phero('The invitation', 'The invitation', 'Why bring this experience to your parish, and who it is for.', 'discussion.jpg')}
<section class="section s5"><div class="wrap split">
<div>{head('Why bring it', 'Why bring this experience to your parish')}
<p class="lead" data-reveal>A familiar gesture, a passage heard at Mass, or a question about Church teaching can open the door to a fuller understanding of Catholic faith.</p>
<p data-reveal>I Love Being Catholic begins with those recognizable experiences and helps participants follow the connections among belief, worship, prayer, and daily choices.</p>
<p data-reveal>Adult formation is an essential part of parish life, not simply an occasional course. I Love Being Catholic offers a shared framework for that continuing work. Its units return to central questions rather than treating doctrine, Scripture, and Catholic practices as unrelated subjects. The companion materials give local leaders a common foundation for teaching and conversation.</p></div>
<div class="photo" style="--rot:2deg" data-reveal="right"><img src="assets/img/congregation.jpg" alt="A diverse congregation standing in the pews of a church at Mass" loading="lazy"></div></div></section>

<section class="section s3"><div class="wrap split rev">
<div class="photo" style="--rot:-2deg" data-reveal="left"><img src="assets/img/priest.jpg" alt="A priest in conversation with parishioners in a garden outside the church" loading="lazy"></div>
<div>{head('A welcome', 'A welcome for adults with questions')}
<p data-reveal>The program welcomes adults with varied levels of familiarity with Catholic faith. No prior course of study is assumed. Longtime parishioners and adults seeking a fresh understanding are invited to bring their questions, including questions shaped by difficult experiences of Church life.</p>
<div class="callout" data-reveal><b>What “love” means here</b>“Love” expresses an invitation to informed belonging, with room for honest reflection.</div></div></div></section>

<section class="section s1"><div class="wrap">
{head('Learning aims', 'The learning aims are practical', 'Prayer and guided conversation help participants consider how what they learn takes shape beyond the gathering.', center=True)}
<div class="grid g3 aims-flow">{''.join(f'<article class="card" data-reveal style="--d:{i*.1:.1f}s"><span class="step-no">Step {i+1}</span><h3 style="margin-top:18px">{t}</h3></article>' for i,t in enumerate(aims))}</div></div></section>

<section class="section on-ink"><div class="wrap">
{head('Ready for your parish', 'Ready for your parish to use', 'The complete program brings together everything below. Your parish can choose the setting that best serves its people and begin with materials prepared for that purpose.')}
<div class="kitrow">{''.join(f'<a class="kit" data-reveal style="--d:{i*.08:.2f}s" href="{h}"><span class="kit-ic">{ic}</span><span class="kit-t">{t}</span></a>' for i,((t,ic),h) in enumerate(zip(kit,['units.html','resources.html','resources.html','resources.html','resources.html'])))}</div>
<div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:36px" data-reveal><a class="btn gold" href="settings.html">Choose a setting{ARROW}</a><a class="btn light" href="resources.html">See the resources</a></div></div></section>
'''
page('invitation.html', 'The invitation — I love being Catholic', 'Why bring I Love Being Catholic to your parish: a welcome for adults with questions, and a program ready for your parish to use.', inv)

# ================= SETTINGS =================
def dots(labels): return '<div class="sched">' + ''.join(f'<div class="dot" style="--k:{i}"><i>{i+1}</i>{l}</div>' for i, l in enumerate(labels)) + '</div>'
def fmt(fid, kicker, title, text, extra, img, alt, rot):
    return f'''<div class="fmt-panel" data-f="{fid}" id="{fid}" role="tabpanel"><div class="split"><div><span class="sticker gold" style="--rot:-2deg">{kicker}</span><h3 style="font-size:clamp(1.6rem,3vw,2.3rem);margin-top:16px">{title}</h3><p>{text}</p>{extra}</div>
<div class="photo" style="--rot:{rot}deg"><img src="assets/img/{img}" alt="{alt}" loading="lazy"></div></div></div>'''
settings = f'''{phero('Choose a setting', 'Choose a setting', 'Shape the experience around your community: five Sundays, one weekend, or five nights.', 'priest.jpg')}
<section class="section s5" style="padding-bottom:30px"><div class="wrap"><div class="sec-head">{head('A place within parish life', 'A place within parish life')}</div>
<p class="lead" data-reveal style="max-width:70ch">Consider I Love Being Catholic as a continuing resource for your parish’s adult formation. It can complement existing opportunities for learning and prayer, while leaving the Order of Christian Initiation of Adults and sacramental preparation in their proper roles. At least three formats offer ways to shape the experience around your community.</p></div></section>

<section class="section s3"><div class="wrap split">
<div>{head('Not sure yet?', 'Find a starting point in three questions')}<p data-reveal>A quick way to think it through with your parish team. It is a prompt for conversation, not a rule. Every format covers the same five units.</p></div>
<div class="quiz" data-reveal="right"><div class="quiz-body"></div></div></div></section>

<section class="section s5"><div class="wrap">
<div class="fmt-tabs" role="tablist" aria-label="Formats"><button class="fmt-tab" role="tab" data-f="sundays">1 · Five Sundays</button><button class="fmt-tab" role="tab" data-f="retreat">2 · Retreat weekend</button><button class="fmt-tab" role="tab" data-f="mission">3 · Five-night mission</button></div>
{fmt('sundays', 'Over five consecutive Sundays', 'A parish preaching event over five Sundays', 'Over five consecutive Sundays, introduce one unit each week through written material inserted in the parish bulletin. The priest speaks about the topic at Masses, connecting it with the lectionary readings of the day. After Mass, parishioners gather in small groups for discussion, using packets prepared for that purpose.', dots(['Sunday 1','Sunday 2','Sunday 3','Sunday 4','Sunday 5']) + '<div style="display:flex;gap:8px;flex-wrap:wrap"><span class="sticker">Bulletin insert</span><span class="sticker">Homily tied to the lectionary</span><span class="sticker">After-Mass small groups</span></div>', 'congregation.jpg', 'A congregation at Mass', 2)}
{fmt('retreat', 'One weekend, in your own parish', 'A parish retreat weekend', 'Present the five units over one parish retreat weekend: one presentation and discussion on Friday evening, three presentations with discussion on Saturday, and the concluding presentation and discussion on Sunday. Parishioners come together in their own parish for a weekend of learning and conversation with fellow parishioners.', '<div class="wk"><div><b>1</b><small>Friday evening</small></div><div class="hi"><b>3</b><small>Saturday</small></div><div><b>1</b><small>Sunday (concluding)</small></div></div>', 'discussion.jpg', 'Parishioners in discussion around a table', -2)}
{fmt('mission', 'Five nights with a missionary', 'A parish mission over five nights', 'Invite a missionary to offer the main subject for consideration on each of five nights. The mission includes written material, discussion material, and participant material. Each presentation takes place within a liturgical or paraliturgical service consisting of hymns, music, and prayers.', dots(['Night 1','Night 2','Night 3','Night 4','Night 5']) + '<div style="display:flex;gap:8px;flex-wrap:wrap"><span class="sticker">Written material</span><span class="sticker">Discussion material</span><span class="sticker">Participant material</span></div>', 'prayer.jpg', 'Parishioners seated in the pews in prayer, with a statue of Mary behind them', 2)}
</div></section>

<section class="section s1"><div class="wrap"><div class="ocia" data-reveal><div class="txt"><span class="eyebrow" >Other settings</span><h3 style="font-size:clamp(1.5rem,2.6vw,2.1rem)">Parish groups and families accompanying OCIA</h3>
<p>Existing parish groups, such as the Knights of Columbus, offer another setting for the program.</p>
<p>It can also accompany the Order of Christian Initiation of Adults by serving the Catholic spouses, family members, and extended families of OCIA catechumens. As the catechumens study the introduction to the faith, their families can follow a complementary track of learning and reflection.</p>
<div style="display:flex;gap:10px;flex-wrap:wrap"><span class="sticker gold">Knights of Columbus</span><span class="sticker">OCIA families</span></div></div><div class="img" role="img" aria-label="A family gathered around a baptism"></div></div></div></section>
'''
page('settings.html', 'Choose a setting — I love being Catholic', 'Three ways to bring I Love Being Catholic to your parish: a five-Sunday preaching event, a retreat weekend, or a five-night mission.', settings,
     cta('Not sure which format fits?', 'Begin by considering which format best serves your parish. Each brings the five connected units into a setting with opportunities for discussion and participation.', ('get-started.html', 'Plan your next step'), ('resources.html', 'See the resources')))

# ================= UNITS =================
btns = ''
for i, (t, *_ ) in enumerate(UNITS):
    if i == 0: btns += '<span class="step-group">Five connected units</span>'
    if i == 3: btns += '<span class="step-group">Faith celebrated and lived</span>'
    btns += f'<button class="step-btn" role="tab" data-u="{i+1}" aria-selected="false"><span class="n">{i+1}</span><span>{t}</span></button>'
panels = ''
for i, (t, q, body, ex) in enumerate(UNITS):
    nxt = f'<button class="btn small" type="button" data-next-unit="{i+2}">Next unit{ARROW}</button>' if i < 4 else f'<a class="btn small" href="#glimpse">See a glimpse of the experience{ARROW}</a>'
    panels += f'''<article class="unit-panel" data-u="{i+1}" role="tabpanel" id="u{i+1}"{'' if i == 0 else ' hidden'}><span class="sticker" style="--rot:-2deg">Unit {i+1} of 5</span><h2 style="font-size:clamp(1.6rem,3vw,2.4rem);margin-top:14px">{t}</h2>
<p class="q">{q}</p><p>{body}</p><div class="callout"><b>What participants explore</b>{ex}</div><div style="margin-top:24px">{nxt}</div></article>'''
badges = ''.join(f'<span class="badge" data-u="{i+1}" title="Unit {i+1}">{i+1}</span>' for i in range(5))
units = f'''{phero('The five units', 'Five connected units', 'Explore the faith: how the Church receives it, teaches it, celebrates it, and lives it.', 'scripture.jpg')}
<section class="section s5" style="padding-bottom:30px"><div class="wrap" style="max-width:900px"><div class="callout" data-reveal style="text-align:center;margin:0"><b>How every unit begins</b><span style="font:italic 600 clamp(1.2rem,2.4vw,1.6rem)/1.4 var(--serif)">“I love being Catholic because of…”</span><p style="margin:12px auto 0">…and explores one part of the faith in relationship to the whole.</p></div>
<p class="lead" data-reveal style="text-align:center;margin:28px auto 0">Together, the units help participants understand how the Church <b>receives</b> the faith, <b>teaches</b> it, <b>celebrates</b> it, and <b>lives</b> it.</p></div></section>
<section class="section s4"><div class="wrap">
<div class="meter-row" data-units-meter><div class="badges" aria-hidden="true">{badges}</div><div class="bar-meter"><i></i></div><span class="mtxt">0 of 5 units explored</span></div>
<div class="units-board"><div class="step-list" role="tablist" aria-label="Units">{btns}</div><div>{panels}</div></div></div></section>

<section class="section on-ink" id="glimpse"><div class="wrap glimpse">
<div class="cross-box" aria-hidden="true"><svg viewBox="0 0 100 130"><path d="M50 6 L50 124"/><path d="M16 42 L84 42"/></svg><span class="lbl">The sign of the cross</span></div>
<div><span class="eyebrow">A glimpse of the experience</span><h2>Begin with a familiar gesture</h2>
<p>Consider the sign of the cross. A gathering could begin with this familiar gesture and explore its scriptural and baptismal setting. Participants could connect it with the Church’s profession of faith, then reflect on what it means to pray with the body during an ordinary day. One simple practice would open a conversation that reaches across the program’s themes.</p>
<p>A gathering can include:</p>
<ol class="flow"><li>Prayer and Scripture</li><li>A short teaching</li><li>Guided conversation</li><li>Practical application</li><li>A closing reflection</li></ol>
<div class="time-pill"><b>60–75</b> minutes — a useful starting point for planning, rather than a fixed requirement.</div>
<p style="margin-top:20px">The pace should leave room for understanding and participation and can be adjusted to the setting.</p></div></div></section>
'''
page('units.html', 'The five connected units — I love being Catholic', 'Five connected units: the Magisterium, the Catechism, Sacred Scripture, the Sacraments, and the Smells and Bells of Catholic life.', units,
     cta('See how the units fit your parish', 'Choose a format that suits your community and make room for their questions.', ('settings.html', 'Choose a setting'), ('resources.html', 'See the resources')))

# ================= RESOURCES =================
R = [
 (I_BOOK, 'The narrative guide', 'The program’s main account of Catholic faith in a welcoming, readable voice. The five narratives develop their subjects through Scripture and authoritative sources, with concrete examples from Catholic life.',
  ['Five narratives, one for each unit', 'Scripture and authoritative sources', 'Concrete examples from Catholic life', 'References for continued learning', 'Connections among the units keep the whole program in view']),
 (I_COMPASS, 'The leader guide', 'Equips a priest, formation director, spiritual director, or prepared lay facilitator to lead each gathering.',
  ['The unit’s purpose', 'Essential readings', 'A suggested sequence', 'Discussion questions', 'Optional activities', 'Help with common misunderstandings', 'Identifies questions that call for further research or the care of a priest or trained pastoral professional']),
 (I_PENCIL, 'The participant guide', 'Key ideas, Scripture and Catechism references, room for notes, reflection questions, and invitations to practice between gatherings.',
  ['Key ideas', 'Scripture and Catechism references', 'Room for notes', 'Reflection questions', 'Invitations to practice between gatherings', 'Printable materials and readable digital versions — no smartphone or social media account needed']),
 (I_PHONES, 'The podcast companion', 'Short audio episodes introduce or revisit each unit through explanation and conversation. They supplement the written materials, whether participants are preparing for a gathering or reflecting afterward.',
  ['Short audio episodes for each unit', 'Explanation and conversation', 'Transcripts accompany the audio', 'Source notes accompany the audio']),
]
rc = ''.join(f'''<article class="card res-card" data-reveal style="--d:{i%2*.1:.1f}s"><div class="ic">{ic}</div><h3>{t}</h3><p>{p}</p><button class="tog" type="button" aria-expanded="false">Learn more</button><div class="more"><div><ul>{''.join(f"<li>{x}</li>" for x in items)}</ul></div></div></article>''' for i, (ic, t, p, items) in enumerate(R))
resources = f'''{phero('Resources', 'Resources for leaders and participants', 'A narrative guide, a leader guide, a participant guide, and podcasts with transcripts.', 'prayer.jpg')}
<section class="section s5"><div class="wrap">{head('Prepared and available', 'Four resources, one structure', 'The companion resources follow the same unit structure and learning aims. Participants reading at home, facilitators preparing a gathering, and listeners revisiting a topic encounter a consistent explanation of the faith.')}
<div class="grid g2">{rc}</div>
<p style="margin-top:36px" data-reveal>The materials work together while allowing your parish to choose the format and pace that best fit its community.</p></div></section>'''
page('resources.html', 'Resources for leaders and participants — I love being Catholic', 'The narrative guide, leader guide, participant guide and podcast companion for I Love Being Catholic.', resources,
     cta('A complete resource for your parish', 'The five narratives, coordinated leader and participant guides, podcasts, and supporting materials are prepared and available for use.', ('get-started.html', 'Plan your next step'), ('beginning.html', 'See the pathway')))

# ================= BEGINNING =================
steps = [('1', '', 'The five-week introduction', 'Five connected units that welcome adults with questions into a fuller understanding of the faith.'),
         ('2', 'ready', 'Two twelve-week studies ready for use', 'A study of the Catechism of the Catholic Church and a study of the Second Vatican Council.'),
         ('3', 'dev', 'Three more studies on the way', 'Sacred Scripture, the Sacraments, and the Smells and Bells of Catholicism. All three are scheduled to be completed and ready for use by October 1, 2027.'),
         ('∞', 'ready', 'A continuing pathway', 'A parish can begin with the five-week introduction and then choose the twelve-week studies that best serve its people.')]
path = '<div class="path"><div class="path-line" aria-hidden="true"><i></i></div>' + ''.join(f'<div class="pstep" data-reveal><div class="pin {c}">{n}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for n, c, t, d in steps) + '</div>'
studies = [('The Catechism of the Catholic Church', ''), ('The Second Vatican Council', ''), ('Sacred Scripture', 'dev'), ('The Sacraments', 'dev'), ('The Smells and Bells of Catholicism', 'dev')]
sh = ''.join(f'<div class="study {d}" data-reveal style="--d:{i*.08:.2f}s"><div class="w">12<small>weeks</small></div><h4>{t}</h4><span class="sticker {"gold" if not d else ""}">{"Ready for use" if not d else "Available from Oct 1, 2027"}</span></div>' for i, (t, d) in enumerate(studies))
beginning = f'''{phero('A beginning, not an ending', 'A beginning, not an ending', 'An ongoing journey of discovery, conversation, and growth in faith.', 'wedding.jpg')}
<section class="section s5" style="padding-bottom:30px"><div class="wrap" style="max-width:900px"><div class="callout" data-reveal style="text-align:center;margin:0"><span style="font:italic 600 clamp(1.25rem,2.6vw,1.75rem)/1.45 var(--serif)">I Love Being Catholic is more than a five-week experience. It is <b>an invitation to begin an ongoing journey</b> of discovery, conversation, and growth in faith.</span></div></div></section>
<section class="section s4"><div class="wrap split" style="align-items:start">
<div>{head('The pathway', 'Begin with five weeks, then go deeper', 'The introductory program is supported by five additional, twelve-week programs that explore its subjects more deeply. Each includes narratives, participant guides, and leader guides, providing parishes with the materials needed to continue adult formation beyond the initial five sessions.')}
<div class="callout" data-reveal><b>Not just a single program</b>I Love Being Catholic offers a continuing pathway for parish adult formation.</div>
<p class="count" style="margin-top:28px;color:var(--ink)" data-reveal><span data-countdown="2027-10-01">0</span> <small style="font:600 1rem var(--sans)">days until all five studies are ready</small></p></div>
<div>{path}</div></div></section>
<section class="section s1"><div class="wrap">{head('The twelve-week studies', 'Five studies to continue', center=True)}<div class="studies">{sh}</div></div></section>
<section class="section s5"><div class="wrap split rev">
<div class="photo" style="--rot:-2deg" data-reveal="left"><img src="assets/img/scripture.jpg" alt="Three parishioners reading the Bible in a garden near a chapel" loading="lazy"></div>
<div>{head('Additional support', 'Faithful teaching and thoughtful conversation')}
<p data-reveal>The curriculum draws on:</p>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px" data-reveal><span class="sticker gold">Sacred Scripture</span><span class="sticker gold">The Church’s living Tradition</span><span class="sticker gold">The Catechism of the Catholic Church</span></div>
<p data-reveal>The witness of saints and the experience of ordinary believers help illuminate how faith is lived. Those experiences are understood as the lived reception of the faith, rather than an independent source of new revelation.</p>
<p data-reveal>Faithful teaching and thoughtful conversation belong together. Leaders are encouraged to welcome questions, use the sources provided, and recognize when a question needs individual pastoral care rather than a group answer. The purpose is to help adults grow in understanding and discipleship, not to turn every gathering into a debate or a test of religious knowledge.</p></div></div></section>'''
page('beginning.html', 'A beginning, not an ending — I love being Catholic', 'Beyond the five-week introduction: five twelve-week studies, two ready now and three scheduled by October 1, 2027.', beginning,
     cta('Begin the journey', 'Start with the five-week introduction, then choose the twelve-week studies that best serve your people.', ('get-started.html', 'Plan your next step'), ('units.html', 'Explore the five units')))

# ================= GET STARTED =================
def chk(items): return '<ul class="checks">' + ''.join(f'<li><label><input type="checkbox" data-k="{k}"><span>{x}</span></label></li>' for k, x in items) + '</ul>'
gs = f'''{phero('Get started', 'Your next step', 'Bringing the program to your parish, from choosing a format to arranging materials.', 'congregation.jpg')}
<section class="section s5"><div class="wrap">{head('Your next step', 'Bring the program to your parish', 'Work through these four steps with your parish team. Your ticks are saved on this device.', center=True)}
<div class="meter-row" data-checks-meter style="justify-content:center"><div class="bar-meter" style="max-width:420px"><i></i></div><span class="mtxt">0 of 8 ready</span></div>
<div class="steps4">
<article class="card" data-n="1" data-reveal><h3>Choosing a parish format</h3><p>Begin by considering which format best serves your parish: a five-Sunday preaching event, a parish retreat weekend, or a five-night parish mission. Each brings the five connected units into a setting with opportunities for discussion and participation.</p><p>Your parish can also use the materials for a deeper series with several gatherings on a particular unit, or for personal reading supported by reflection questions and audio.</p><a class="link-arrow" href="settings.html">Compare the formats {ARROW}</a></article>
<article class="card" data-n="2" data-reveal style="--d:.1s"><h3>Preparing your parish to participate</h3><p>Invite a leader or formation team to review the materials and choose a workable schedule and setting.</p>
{chk([('a1','Review the materials with a leader or formation team'),('a2','Identify the adults you hope to reach'),('a3','Choose a workable schedule and setting'),('a4','Discuss teaching approach, reading level, and accessibility needs'),('a5','Plan the preparation a facilitator will need')])}
<p>Leader preparation depends on the format, the group, and the facilitator’s experience. Allow enough time to read the narrative, review the leader guide, and choose the questions and activities that will serve the group.</p></article>
<article class="card" data-n="3" data-reveal><h3>A complete resource for your parish</h3><p>The five narratives, coordinated leader and participant guides, podcasts, and supporting materials are prepared and available for use. Your parish can concentrate on bringing people together, preparing its leaders, and choosing how to make this experience part of its ongoing adult formation.</p><p>Before distributing resources, confirm:</p>
{chk([('b1','The applicable ordering details'),('b2','Copying permissions'),('b3','Digital access arrangements')])}<a class="link-arrow" href="resources.html">See the resources {ARROW}</a></article>
<article class="card" data-n="4" data-reveal style="--d:.1s"><h3>An invitation to begin</h3><p>We invite your parish to make I Love Being Catholic an essential part of its adult formation. Bring together adults who want to understand their faith more fully, including those who are unsure where to begin.</p><p>Choose a format that suits your community, invite people warmly, and make room for their questions. The resources are ready to help your parish keep learning, praying, and living the faith together.</p></article>
</div></div></section>
<section class="section s3" id="contact"><div class="wrap">{head('Get in touch', 'Talk with Liguori Publications', 'Reach out to review the program, choose a format, and arrange the materials and access your group needs.')}
<div class="contact"><div class="contact-card" data-reveal="left"><img class="logo" src="assets/img/liguori-logo.png" alt="Liguori Publications — A Redemptorist Ministry" width="230" height="108">
<ul><li>{I_PIN}<span>200 Liguori Drive<br>Liguori, MO 63057</span></li><li>{I_PHONE}<span><a href="tel:+18003259521">800-325-9521</a></span></li><li>{I_MAIL}<span><a href="mailto:liguori@liguori.org">liguori@liguori.org</a></span></li><li>{I_GLOBE}<span><a href="https://www.liguori.org" target="_blank" rel="noopener">liguori.org</a><br>ilovebeingcatholic.com</span></li></ul></div>
<form class="compose card" data-reveal="right" data-to="liguori@liguori.org" aria-label="Enquiry form">
<div class="row"><label>Your name<input name="name" required autocomplete="name"></label><label>Your parish<input name="parish" required></label></div>
<label>Email address<input type="email" name="email" required autocomplete="email"></label>
<label>Format of interest<select name="format"><option>Five-Sunday preaching event</option><option>Parish retreat weekend</option><option>Five-night parish mission</option><option>A deeper series on one unit</option><option>Personal reading and audio</option><option>Not sure yet</option></select></label>
<label>Your message<textarea name="message" placeholder="Tell us about your parish and the adults you hope to reach."></textarea></label>
<button class="btn" type="submit">Send enquiry{ARROW}</button><p class="form-note">This opens your email app with the message ready to send to Liguori Publications.</p></form></div></div></section>'''
page('get-started.html', 'Get started — Bring I love being Catholic to your parish', 'Choose a parish format, prepare your team, and contact Liguori Publications to bring I Love Being Catholic to your parish.', gs,
     cta('An invitation to begin', 'We invite your parish to make I Love Being Catholic an essential part of its adult formation.', ('#contact', 'Contact Liguori'), ('index.html', 'Back to home')))
print('built', sorted(f for f in os.listdir(OUT) if f.endswith('.html')))
