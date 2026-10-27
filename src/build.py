#!/usr/bin/env python3
"""Generate the static site from src/site.json + the page copy below.

Run from the repo root:  python3 src/build.py
Writes *.html, sitemap.xml and style.css to the repo root (Vercel serves the root as-is).
"""
import json, os, shutil, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(ROOT, "src", "site.json")))
P = S["prices"]
E = html.escape
TODAY = datetime.date.today().isoformat()
ORG_ID = S["domain"] + "/#org"
PERSON_ID = S["domain"] + "/#sherri"

NAV = [("Lessons & Pricing", "/lessons/"), ("About", "/about/"), ("FAQ", "/faq/"), ("Free Assessment", "/contact/")]


def page(slug, title, desc, body, schema=None, noindex=False):
    url = S["domain"] + ("/" if slug == "index" else f"/{slug}/")
    nav = "".join(f'<a href="{h}">{E(t)}</a>' for t, h in NAV)
    mail = f' · <a href="mailto:{E(S["email"])}">{E(S["email"])}</a>' if S["email"] else ""
    ld = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    head = '<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{url}">'
    topics = " · ".join(f'<a href="/{t[0]}/">{E(t[1])}</a>' for t in TOPICS)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
{head}<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{S["domain"]}/img/sherri.jpg">
<meta property="og:type" content="website"><meta property="og:site_name" content="{E(S["brand"])}">
<meta name="theme-color" content="#2b4c7e"><link rel="stylesheet" href="/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📖</text></svg>">
{ld}<script defer src="/_vercel/insights/script.js"></script></head><body>
<header class="top"><div class="wrap top__in"><a class="logo" href="/">📖 {E(S["brand"])}</a><nav>{nav}</nav></div></header>
<main>{body}</main>
<footer class="foot"><div class="wrap"><p><strong>{E(S["brand"])}</strong> · Private online reading lessons for ages 5–14 with {E(S["teacher_full"])}.</p>
<p>{E(S["booking_note"])}{mail}</p>
<p class="small">Reading help: {topics}</p>
<p class="small">&copy; 2026 {E(S["brand"])}</p></div></footer></body></html>"""


CTA = '<a class="btn" href="/contact/">Book a free reading assessment</a>'

# Topic pages: one page per thing parents search for. Keep every claim to what's in CLAUDE.md "About Sherri".
def topic(h1, intro, sections, related):
    secs = "".join(f"<h2>{E(h)}</h2>{body}" for h, body in sections)
    rel = "".join(f'<li><a href="/{t[0]}/">{E(t[1])}</a></li>' for t in TOPICS if t[0] in related)
    return f"""
<section class="wrap narrow"><h1>{E(h1)}</h1>
<p class="lead">{intro}</p>
<p>{CTA}</p>
{secs}
<h2>Start with a free reading assessment</h2>
<p>In 20 minutes on a video call, {E(S["teacher"])} listens to your child read and tells you where they are, what's getting in the way, and what lessons would focus on. No obligation. See <a href="/lessons/">lessons &amp; pricing</a> or <a href="/about/">meet {E(S["teacher"])}</a>.</p>
<p>{CTA}</p>
<h2>Related</h2><ul>{rel}<li><a href="/faq/">Frequently asked questions</a></li></ul>
</section>
"""

T = S["teacher"]
TOPICS = [
    ("dyslexia-reading-tutor", "Dyslexia & struggling readers",
     f"Online Dyslexia Reading Tutor for Kids | {S['brand']}",
     "One-on-one online reading lessons for children with dyslexia or reading struggles, ages 5–14. Explicit, step-by-step EBLI instruction. Free assessment.",
     "Online reading tutor for children with dyslexia and struggling readers",
     f"If your child guesses at words, reads far below grade level, or melts down at homework, they need direct, patient teaching, not more of the same. {E(T)} teaches one-on-one by video call and has experience with dyslexic learners.",
     [("Signs your child may need reading help",
       "<ul><li>Guesses words from the first letter or the picture</li><li>Reads slowly and loses the meaning</li><li>Spells the same word different ways</li><li>Avoids reading or says it's \"boring\"</li><li>Is behind classmates even with extra practice</li></ul>"),
      ("How lessons help",
       f"<p>{E(T)} is trained in EBLI (Evidence-Based Literacy Instruction), a structured, explicit approach that teaches the sounds of English and how they're written, step by step, so children decode words instead of guessing. Each lesson reviews what your child knows, teaches one new skill directly, practices it together, and ends with real reading at the right level.</p><p>Lessons stay short, encouraging and one-on-one, so your child gets a teacher's full attention every minute.</p>"),
      ("What lessons are not",
       "<p>Lessons are tutoring, not a medical or psychological evaluation, and they don't diagnose dyslexia. If you're unsure, the free assessment is a good first step, and your pediatrician or school can advise on formal testing.</p>")],
     ["phonics-tutor", "ebli-reading-tutor", "reading-comprehension-tutor"]),
    ("phonics-tutor", "Phonics for early readers",
     f"Online Phonics Tutor for Kids Ages 5–8 | {S['brand']}",
     "Private online phonics lessons for early readers: letter sounds, blending, sight words. Taught by a teacher with 5 years teaching ages 4–8 in the classroom. Free assessment.",
     "Online phonics tutor for early readers, ages 5–8",
     f"Learning to read starts with sounds. {E(T)} teaches letter sounds, blending and sight words one step at a time, by video call, so reading finally clicks for your child.",
     [("What your child will learn",
       "<ul><li>Letter sounds and how to blend them into words</li><li>Common spelling patterns, taught directly</li><li>High-frequency words</li><li>Reading short books smoothly, with expression</li></ul>"),
      ("Why one-on-one works for young readers",
       f"<p>Young children do best with short, hands-on lessons and a teacher who knows how they learn. {E(T)} spent five years teaching ages 4–8 in a school classroom and two years tutoring reading online. Lessons use games, shared screens and real books, and a 30-minute lesson suits most 5 to 7 year olds.</p>")],
     ["dyslexia-reading-tutor", "homeschool-reading-lessons", "ebli-reading-tutor"]),
    ("reading-comprehension-tutor", "Comprehension & fluency",
     f"Reading Comprehension Tutor Online, Ages 9–14 | {S['brand']}",
     "One-on-one online lessons for reading comprehension, fluency and vocabulary for children ages 9–14. Keep up with harder school texts. Free assessment.",
     "Online reading comprehension and fluency tutor, ages 9–14",
     f"Some children can read the words but don't understand or remember what they read. Others read so slowly that school texts become a chore. {E(T)} works one-on-one with readers ages 9 to 14 to build fluency, vocabulary and understanding.",
     [("What lessons cover",
       "<ul><li>Reading smoothly and accurately at grade level</li><li>Finding the main idea and key details</li><li>Building vocabulary from what they read</li><li>Handling longer chapter books and school texts</li></ul>"),
      ("Where comprehension problems often start",
       "<p>Weak comprehension sometimes traces back to shaky decoding: when a child spends effort on each word, little is left for meaning. The free assessment checks both, so lessons fix the real gap.</p>")],
     ["dyslexia-reading-tutor", "phonics-tutor", "homeschool-reading-lessons"]),
    ("homeschool-reading-lessons", "Homeschool reading",
     f"Homeschool Reading Lessons Online | {S['brand']}",
     "Online one-on-one reading lessons for homeschool families. Use them as your reading curriculum or alongside the one you have. Taught by a homeschooling teacher.",
     "Homeschool reading lessons, one-on-one and online",
     f"{E(T)} homeschooled and taught her own children, so she knows how reading fits into a homeschool day. Families use her lessons as their reading curriculum, or alongside the one they already use.",
     [("How it fits your homeschool",
       "<ul><li>Daytime slots, Monday to Saturday</li><li>A written plan after the free assessment, so you know what's being taught</li><li>A short practice activity each week you can fold into your day</li><li>Progress check-ins with you along the way</li></ul>"),
      ("Who it's for",
       "<p>Beginning readers learning phonics, older children who are behind, and strong readers who need more challenge, ages 5 to 14.</p>")],
     ["phonics-tutor", "reading-comprehension-tutor", "dyslexia-reading-tutor"]),
    ("ebli-reading-tutor", "EBLI reading tutor",
     f"EBLI Reading Tutor Online | {S['brand']}",
     "Online one-on-one reading lessons from an EBLI-trained teacher (Evidence-Based Literacy Instruction) with 30+ years as an educator. Ages 5–14. Free assessment.",
     "EBLI-trained online reading tutor",
     f"Looking for a tutor who uses EBLI? {E(T)} is trained in EBLI (Evidence-Based Literacy Instruction) and teaches it one-on-one by video call to children ages 5 to 14.",
     [("What EBLI is",
       "<p>EBLI teaches the sounds of English and how they're written in a clear, step-by-step way, so children decode words instead of guessing. It covers reading, spelling and writing together, and works for beginning readers and for older students who are behind.</p>"),
      (f"Why families choose {T}",
       "<ul><li>30+ years as an educator</li><li>Bachelor's in Early Childhood Education, Auburn University</li><li>Experience teaching children with dyslexia</li><li>Same teacher every week, one-on-one</li></ul>")],
     ["dyslexia-reading-tutor", "phonics-tutor", "homeschool-reading-lessons"]),
]


HOME = f"""
<section class="hero"><div class="wrap hero__in">
<picture><source srcset="/img/sherri.webp" type="image/webp"><img class="photo photo--hero" src="/img/sherri.jpg" width="640" height="800" alt="{E(S['teacher_full'])}, reading teacher" fetchpriority="high"></picture>
<div>
<p class="eyebrow">Private online reading lessons · ages 5–14</p>
<h1>Online reading lessons that help your child become a confident, happy reader.</h1>
<p class="lead">One-on-one lessons by video call with {E(S["teacher_full"])}, a teacher with <strong>30+ years of experience</strong>.
Every lesson plan is built around your child, not a script.</p>
<p>{CTA} <a class="btn btn--ghost" href="/lessons/">See lessons &amp; pricing</a></p>
<ul class="ticks"><li><a href="/ebli-reading-tutor/">EBLI-trained</a> reading teacher</li><li>Bachelor's in Early Childhood Education, Auburn</li><li>30+ years as an educator</li><li>Experienced with dyslexic learners</li><li>Homeschool teacher</li></ul>
</div>
</div></section>

<section class="wrap grid3">
<div class="card"><h3><a href="/phonics-tutor/">Early readers &amp; phonics (5–8)</a></h3><p>Letter sounds, phonics, blending and sight words, taught step by step so reading clicks. Five years teaching ages 4–8 in the classroom.</p></div>
<div class="card"><h3><a href="/dyslexia-reading-tutor/">Struggling readers &amp; dyslexia</a></h3><p>For the child who's behind, guessing at words, or avoids books, including children with dyslexia. Explicit, step-by-step EBLI instruction finds the gap and fills it, and keeps it encouraging.</p></div>
<div class="card"><h3><a href="/reading-comprehension-tutor/">Comprehension &amp; fluency (9–14)</a></h3><p>Reading smoothly, understanding what they read, building vocabulary, and keeping up with harder school texts.</p></div>
</section>

<section class="band"><div class="wrap">
<h2>How it works</h2>
<ol class="steps">
<li><strong>Free assessment (20 min).</strong> A relaxed video call where {E(S["teacher"])} listens to your child read and finds where they are.</li>
<li><strong>A custom plan.</strong> You get a short written summary of strengths, gaps, and goals.</li>
<li><strong>Weekly lessons.</strong> Live, one-on-one, and fun. Progress check-ins with you along the way.</li>
</ol><p>{CTA}</p></div></section>

<section class="wrap"><h2>Why parents choose a private teacher</h2>
<div class="grid2">
<p><strong>Same teacher every week.</strong> Your child builds a relationship with one experienced teacher, not a rotating roster.</p>
<p><strong>Fully custom.</strong> Lessons, practice, and assessments are made for your child's level and interests.</p>
<p><strong>From home.</strong> No driving. All you need is a laptop or tablet with a camera.</p>
<p><strong>Homeschool friendly.</strong> Use lessons as your <a href="/homeschool-reading-lessons/">homeschool reading curriculum</a>, or alongside the one you already use.</p>
</div></section>
"""

LESSONS = f"""
<section class="wrap narrow"><h1>Lessons &amp; pricing</h1>
<p class="lead">All lessons are live, one-on-one video calls. Lesson prep, custom materials, and progress assessments are included. No extra fees.</p>
<table class="price"><thead><tr><th>Option</th><th>Best for</th><th>Price</th></tr></thead><tbody>
<tr><td>Reading assessment (20 min)</td><td>Every new student</td><td><strong>{P["assessment"]}</strong></td></tr>
<tr><td>30-minute lesson</td><td>Ages 5–7, shorter attention spans</td><td><strong>{P["short"]}</strong></td></tr>
<tr><td>45-minute lesson</td><td>Most students</td><td><strong>{P["standard"]}</strong></td></tr>
<tr><td>60-minute lesson</td><td>Ages 10–14, comprehension work</td><td><strong>{P["long"]}</strong></td></tr>
<tr><td>10 × 45-minute lessons</td><td>Steady weekly progress</td><td><strong>{P["pack_standard"]}</strong> ({P["pack_standard_each"]} each)</td></tr>
</tbody></table>
<p class="small">Most families book 1–2 lessons a week. Please give 24 hours' notice to reschedule.</p>
<h2>What's in a lesson</h2>
<ul><li>Warm-up review of last week's skills</li><li>New skill taught directly, then practiced together</li><li>Reading a book or passage at the right level</li><li>A short, doable practice activity for the week</li></ul>
<p>{CTA}</p></section>
"""

ABOUT = f"""
<section class="wrap narrow"><h1>Meet {E(S["teacher_full"])}</h1>
<div class="intro"><picture><source srcset="/img/sherri.webp" type="image/webp"><img class="photo" src="/img/sherri.jpg" width="640" height="800" alt="{E(S['teacher_full'])}, reading teacher" loading="lazy"></picture>
<p class="lead">{E(S["teacher"])} has spent more than 30 years helping children become confident readers — in the classroom, online, and at her own kitchen table homeschooling her kids. Every lesson is one-on-one and built around where your child is today.</p></div>
<ul class="ticks ticks--col">
<li>30+ years as an educator</li>
<li>Bachelor's degree in Early Childhood Education from Auburn University</li>
<li>Trained in EBLI (Evidence-Based Literacy Instruction)</li>
<li>Experience teaching children with dyslexia</li>
<li>K–12 teaching experience, including 5 years teaching ages 4–8 in a school classroom</li>
<li>2 years as an online reading tutor with Hoot Reading</li>
<li>Homeschooled and taught her own children</li>
</ul>
<p>{CTA}</p></section>
"""

FAQS = [
    ("What ages do you teach?", "Children from about age 5 up to 13 or 14: from first letter sounds through middle-school reading comprehension."),
    ("Do you work with children with dyslexia?", f"Yes. {S['teacher']} has experience teaching children with dyslexia and is trained in EBLI (Evidence-Based Literacy Instruction), a structured, explicit approach to teaching reading, spelling, and writing. Lessons are not a medical or psychological evaluation; if you're unsure whether your child has dyslexia, the free assessment is a good first step, and your pediatrician or school can advise on formal testing."),
    ("What is EBLI?", "EBLI (Evidence-Based Literacy Instruction) is a reading method that teaches the sounds of English and how they're written in a clear, step-by-step way, so children decode words instead of guessing. It works for beginning readers and for older students who are behind."),
    ("How do online lessons work for young kids?", "Lessons are short, interactive, and hands-on: games, shared screens, and real books. Young children usually do great online when the teacher is experienced with them. A parent nearby for the first lesson or two helps."),
    ("What do we need?", "A laptop or tablet with a camera and microphone, a quiet spot, and a reliable internet connection. A phone screen is usually too small."),
    ("Is the assessment really free?", "Yes. It's 20 minutes, there's no obligation, and you'll come away with a clear picture of your child's reading level either way."),
    ("Do you work with homeschool families?", f"Yes. {S['teacher']} has homeschooled and taught her own children and can be your reading curriculum or support the one you use."),
    ("How soon will we see progress?", "Most families notice more confidence within a few weeks. Measurable reading-level gains depend on the starting point and how often lessons happen. You'll get progress check-ins along the way."),
    ("How do I pay?", "After your free assessment, {} will send simple payment details. Payment is due before each lesson or package.".format(S["teacher"])),
]
FAQ = '<section class="wrap narrow"><h1>Frequently asked questions</h1>' + "".join(
    f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQS) + f"<p>{CTA}</p></section>"
FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}

CONTACT = f"""
<section class="wrap narrow"><h1>Book a free reading assessment</h1>
<p class="lead">Tell us a little about your child and {E(S["teacher"])} will reach out within one business day to set up a 20-minute video call.</p>
<form id="f" class="card form">
<input type="hidden" name="access_key" value="{E(S["web3forms_key"])}">
<input type="hidden" name="subject" value="New reading assessment request">
<input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">
<label>Parent name<input name="name" required autocomplete="name"></label>
<label>Email<input name="email" type="email" required autocomplete="email"></label>
<label>Phone (optional)<input name="phone" type="tel" autocomplete="tel"></label>
<label>Child's age<input name="child_age" required></label>
<label>What would you like help with?<textarea name="details" rows="4" placeholder="e.g. struggles with sounding out words, reads slowly, doesn't enjoy reading..."></textarea></label>
<label>How did you hear about us?<select name="source">
<option>Friend or family referral</option><option>Facebook group</option><option>Google search</option>
<option>Nextdoor</option><option>Outschool / tutoring site</option><option>Other</option></select></label>
<button class="btn" type="submit">Request my free assessment</button>
<p id="note" role="status" aria-live="polite"></p></form>
</section>
<script>
document.getElementById('f').addEventListener('submit',async e=>{{e.preventDefault();const f=e.target,n=document.getElementById('note'),b=f.querySelector('button');
b.disabled=true;b.textContent='Sending...';try{{const r=await(await fetch('https://api.web3forms.com/submit',{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify(Object.fromEntries(new FormData(f)))}})).json();
if(!r.success)throw 0;n.textContent="Thank you! We'll be in touch within one business day.";f.reset();}}catch(_){{n.textContent='Something went wrong. Please try again in a minute.';}}finally{{b.disabled=false;b.textContent='Request my free assessment';}}}});
</script>
"""

PERSON = {"@type": "Person", "@id": PERSON_ID, "name": S["teacher_full"], "jobTitle": "Reading teacher", "image": S["domain"] + "/img/sherri.jpg",
          "url": S["domain"] + "/about/", "worksFor": {"@id": ORG_ID},
          "alumniOf": {"@type": "CollegeOrUniversity", "name": "Auburn University"},
          "knowsAbout": ["Reading instruction", "Phonics", "Dyslexia", "Reading comprehension", "EBLI (Evidence-Based Literacy Instruction)", "Homeschooling"]}

def price_num(v):
    return v.replace("$", "").replace(",", "")

OFFERS = [("Free reading assessment (20 min)", "0"), ("30-minute online reading lesson", price_num(P["short"])),
          ("45-minute online reading lesson", price_num(P["standard"])), ("60-minute online reading lesson", price_num(P["long"])),
          ("10 x 45-minute online reading lessons", price_num(P["pack_standard"]))]
ORG = {"@type": "EducationalOrganization", "@id": ORG_ID, "name": S["brand"], "url": S["domain"] + "/",
       "description": "Private one-on-one online reading lessons for children ages 5-14: phonics, dyslexia and struggling readers, comprehension and fluency.",
       "founder": {"@id": PERSON_ID}, "image": S["domain"] + "/img/sherri.jpg", "availableLanguage": "English",
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Online reading lessons", "itemListElement": [
           {"@type": "Offer", "name": n, "price": v, "priceCurrency": "USD"} for n, v in OFFERS]}}
BIZ_LD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "@id": S["domain"] + "/#website", "url": S["domain"] + "/", "name": S["brand"], "publisher": {"@id": ORG_ID}},
    ORG, PERSON]}
ABOUT_LD = {"@context": "https://schema.org", "@type": "ProfilePage", "mainEntity": PERSON}

def service_ld(name, desc):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc,
            "serviceType": "Online reading tutoring", "provider": {"@type": "EducationalOrganization", "@id": ORG_ID, "name": S["brand"], "url": S["domain"] + "/"},
            "audience": {"@type": "EducationalAudience", "educationalRole": "student", "audienceType": "Children ages 5-14"},
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "name": "Free reading assessment"}}

PAGES = [
    ("index", f"Online Reading Tutor for Kids Ages 5–14 | {S['brand']}",
     "Private one-on-one online reading lessons with an EBLI-trained teacher of 30+ years. Phonics, dyslexia and struggling readers, comprehension. Free reading assessment.", HOME, BIZ_LD),
    ("lessons", f"Reading Lessons & Pricing | {S['brand']}", "Online reading lesson prices: a free 20-minute assessment, then one-on-one 30, 45 or 60-minute lessons from $45, plus a 10-lesson package.", LESSONS, None),
    ("about", f"About {S['teacher']} | {S['brand']}", "EBLI-trained reading teacher with 30+ years as an educator, a bachelor's in Early Childhood Education from Auburn, and experience with dyslexic learners.", ABOUT, ABOUT_LD),
    ("faq", f"FAQ | {S['brand']}", "Answers about online reading lessons for kids: ages, dyslexia, EBLI, what you need, pricing, homeschool.", FAQ, FAQ_LD),
    ("contact", f"Free Reading Assessment | {S['brand']}", "Book a free 20-minute online reading assessment for your child.", CONTACT, None),
]

PAGES += [(slug, title, desc, topic(h1, intro, secs, rel), service_ld(h1, desc)) for slug, _, title, desc, h1, intro, secs, rel in TOPICS]

for slug, title, desc, body, ld in PAGES:
    open(os.path.join(ROOT, f"{slug}.html"), "w").write(page(slug, title, desc, body, ld))
open(os.path.join(ROOT, "404.html"), "w").write(page("404", f"Page not found | {S['brand']}", "Page not found.",
    f'<section class="wrap narrow"><h1>Page not found</h1><p><a href="/">Go home</a> or {CTA}</p></section>', noindex=True))
urls = "".join(f"<url><loc>{S['domain']}{'/' if s == 'index' else f'/{s}/'}</loc><lastmod>{TODAY}</lastmod></url>" for s, *_ in PAGES)
open(os.path.join(ROOT, "sitemap.xml"), "w").write(
    f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {S['domain']}/sitemap.xml\n")
shutil.copy(os.path.join(ROOT, "src", "style.css"), os.path.join(ROOT, "style.css"))
print("built", len(PAGES) + 1, "pages")
