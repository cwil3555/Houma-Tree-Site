# Online Reading Lessons site (formerly Houma Tree Pros)

Lead-gen site for private one-on-one online reading lessons (ages 5–14). Replaced the tree-service site on 2026-10-25.

## Edit / build
1. Fill in `src/site.json` (brand, teacher name, email, domain, prices). Anything in `[brackets]` is a placeholder.
2. Page copy lives in `src/build.py`; styles in `src/style.css`.
3. Run `python3 src/build.py` — regenerates the `.html` pages, `sitemap.xml`, `robots.txt`, `style.css` at the repo root.
4. Commit both `src/` and the generated files. Vercel serves the repo root as static files (no build step).

## Before going live — checklist
- [ ] Brand name + new domain (don't keep houmatreepros.com — Google associates it with trees). Old tree URLs 301 to the new pages via `vercel.json`.
- [ ] Teacher name, photo, bio, extra certifications, 2–3 student results (About page)
- [ ] Payment method (FAQ)
- [ ] Her own Web3Forms access key (current key emails whoever registered it for the tree site) — free at web3forms.com
- [ ] Enable Vercel Web Analytics on the project (script tag is already in every page)
- [ ] Google Business Profile + Google Search Console (submit sitemap.xml)

## Growth plan (the site is the landing page, not the lead source)
1. Warm network: past Hoot / homeschool families + referral offer
2. Marketplaces: Outschool group class → private, Wyzant/Varsity profiles (check off-platform rules)
3. Community: homeschool Facebook groups/co-ops, Nextdoor, PTO pages
4. Offer everywhere: free 20-min reading assessment
5. Track: "How did you hear about us?" field on the form + Vercel analytics
