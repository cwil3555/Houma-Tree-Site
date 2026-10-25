#!/usr/bin/env python3
"""Generate the static site from src/site.json + the page copy below.

Run from the repo root:  python3 src/build.py
Writes *.html, sitemap.xml and style.css to the repo root (Vercel serves the root as-is).
"""
import json, os, shutil, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(ROOT, "src", "site.json")))
P = S["prices"]
E = html.escape

NAV = [("Lessons & Pricing", "/lessons/"), ("About", "/about/"), ("FAQ", "/faq/"), ("Free Assessment", "/contact/")]


def page(slug, title, desc, body, schema=None):
    url = S["domain"] + ("/" if slug == "index" else f"/{slug}/")
    nav = "".join(f'<a href="{h}">{E(t)}</a>' for t, h in NAV)
    mail = f' · <a href="mailto:{E(S["email"])}">{E(S["email"])}</a>' if S["email"] else ""
    ld = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}"><meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<meta name="theme-color" content="#2b4c7e"><link rel="stylesheet" href="/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📖</text></svg>">
{ld}<script defer src="/_vercel/insights/script.js"></script></head><body>
<header class="top"><div class="wrap top__in"><a class="logo" href="/">📖 {E(S["brand"])}</a><nav>{nav}</nav></div></header>
<main>{body}</main>
<footer class="foot"><div class="wrap"><p><strong>{E(S["brand"])}</strong> · Private online reading lessons for ages 5–14 with {E(S["teacher_full"])}.</p>
<p>{E(S["booking_note"])}{mail}</p>
<p class="small">&copy; 2026 {E(S["brand"])}</p></div></footer></body></html>"""


CTA = '<a class="btn" href="/contact/">Book a free reading assessment</a>'

HOME = f"""
<section class="hero"><div class="wrap">
<p class="eyebrow">Private online reading lessons · ages 5–14</p>
<h1>Help your child become a confident, happy reader.</h1>
<p class="lead">One-on-one lessons by video call with {E(S["teacher_full"])}, a teacher with <strong>30+ years of experience</strong>.
Every lesson plan is built around your child, not a script.</p>
<p>{CTA} <a class="btn btn--ghost" href="/lessons/">See lessons &amp; pricing</a></p>
<ul class="ticks"><li>EBLI-trained reading teacher</li><li>Bachelor's in Early Childhood Education, Auburn</li><li>30+ years as an educator</li><li>Experienced with dyslexic learners</li><li>Homeschool teacher</li></ul>
</div></section>

<section class="wrap grid3">
<div class="card"><h3>Early readers (5–8)</h3><p>Letter sounds, phonics, blending and sight words, taught step by step so reading clicks. Five years teaching ages 4–8 in the classroom.</p></div>
<div class="card"><h3>Struggling readers &amp; dyslexia</h3><p>For the child who's behind, guessing at words, or avoids books, including children with dyslexia. Explicit, step-by-step EBLI instruction finds the gap and fills it, and keeps it encouraging.</p></div>
<div class="card"><h3>Comprehension &amp; fluency (9–14)</h3><p>Reading smoothly, understanding what they read, building vocabulary, and keeping up with harder school texts.</p></div>
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
<p><strong>Homeschool friendly.</strong> Use lessons as your reading curriculum, or alongside the one you already use.</p>
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
<p class="lead">{E(S["teacher"])} has spent more than 30 years helping children become confident readers — in the classroom, online, and at her own kitchen table homeschooling her kids. Every lesson is one-on-one and built around where your child is today.</p>
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

BIZ_LD = {"@context": "https://schema.org", "@type": "EducationalOrganization", "name": S["brand"], "url": S["domain"],
          "description": "Private one-on-one online reading lessons for children ages 5-14.", "founder": {"@type": "Person", "name": S["teacher_full"]}}

PAGES = [
    ("index", f"Online Reading Tutor for Kids Ages 5–14 | {S['brand']}",
     "Private one-on-one online reading lessons with an EBLI-trained teacher of 30+ years. Phonics, dyslexia and struggling readers, comprehension. Free reading assessment.", HOME, BIZ_LD),
    ("lessons", f"Reading Lessons & Pricing | {S['brand']}", "Online reading lesson options and prices. 30, 45 and 60-minute one-on-one lessons. Free assessment.", LESSONS, None),
    ("about", f"About {S['teacher']} | {S['brand']}", "EBLI-trained reading teacher with 30+ years as an educator, a bachelor's in Early Childhood Education from Auburn, and experience with dyslexic learners.", ABOUT, None),
    ("faq", f"FAQ | {S['brand']}", "Answers about online reading lessons for kids: ages, equipment, pricing, homeschool.", FAQ, FAQ_LD),
    ("contact", f"Free Reading Assessment | {S['brand']}", "Book a free 20-minute online reading assessment for your child.", CONTACT, None),
]

for slug, title, desc, body, ld in PAGES:
    open(os.path.join(ROOT, f"{slug}.html"), "w").write(page(slug, title, desc, body, ld))
open(os.path.join(ROOT, "404.html"), "w").write(page("404", f"Page not found | {S['brand']}", "Page not found.",
    f'<section class="wrap narrow"><h1>Page not found</h1><p><a href="/">Go home</a> or {CTA}</p></section>'))
urls = "".join(f"<url><loc>{S['domain']}{'/' if s == 'index' else f'/{s}/'}</loc></url>" for s, *_ in PAGES)
open(os.path.join(ROOT, "sitemap.xml"), "w").write(
    f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {S['domain']}/sitemap.xml\n")
shutil.copy(os.path.join(ROOT, "src", "style.css"), os.path.join(ROOT, "style.css"))
print("built", len(PAGES) + 1, "pages")
