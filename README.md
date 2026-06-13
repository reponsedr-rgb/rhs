# Rusumo High School — Website (rhs)

Comprehensive A→Z guide for the Rusumo High School static website repository.

---

## Project Summary

- **Name:** Rusumo High School (RHS) website
- **Repo:** rhs
- **Purpose:** Public school website with pages, assets, and helpful scripts for SEO, analytics, and site maintenance.
- **Stack:** Static HTML, CSS, JS, assets, and small Python scripts in `scripts/`.

---

## Table of Contents

1. Project overview
2. Quick start (local)
3. Editing content
4. Phone-number policy (important)
5. Scripts and automation
6. SEO & Analytics
7. Structured data & sitemap
8. Accessibility, performance & security
9. Testing & troubleshooting
10. Deployment and CI
11. Contribution guide
12. Credits & license

---

## 1) Project overview

This repository contains the static HTML website for Rusumo High School. Key folders:

- `assets/` — CSS, JS, images, libs
- `about-us/`, `academic/`, `programs/`, etc. — per-page HTML files
- `scripts/` — utility Python scripts used to audit and update the site
- `Contact/Contact.html` — contact form + WhatsApp integration

Use this README as a single source of truth for editing, deploying, and maintaining the site.

---

## 2) Quick start — run locally

Prerequisites:
- Git
- Python 3 (for quick static server or running scripts)

Clone:

```bash
git clone https://github.com/reponsedr-rgb/rhs.git
cd rhs
```

Serve locally (simple, for preview):

```bash
# From repository root
python3 -m http.server 8000
# then open http://localhost:8000 in your browser
```

For a slightly more robust live reload dev experience, use a static site server of your choice (live-server, http-server, etc.).

---

## 3) Editing content

- Edit HTML files under the relevant folders. Keep backups (many `.bak` files exist already).
- CSS lives in `assets/css/` and `assets/lib/` for external libs.
- JS lives in `assets/js/` and `assets/lib/`.

When updating layout or repeated content (footer, header), prefer editing the included fragments under `assets/` if present; otherwise edit each page consistently.

When changing images, place optimized images in `assets/img/` and update `src`/`srcset`.

---

## 4) Phone-number policy (CRITICAL)

This repository intentionally uses two distinct phone numbers for different purposes. Do NOT conflate them.

- **School contact (primary outward-facing contact for parents/students):** 0788871560
  - Used in contact sections, `tel:` links, and the floating WhatsApp chat button intended to reach Rusumo High School staff.
  - Files where this appears: contact lists and `tel:` anchors across pages (for example in Contact/Contact.html, our-school.html, index.html, and many pages under `academic/`, `programs/`, etc.).

- **Developer contact (web developer / credit link):** 0796315374 (RD Solutions)
  - Used exclusively in the footer credit anchor linking to RD Solutions via WhatsApp. This should remain as the developer contact only.

Rules to follow when editing:

1. When updating school contacts, change only the `tel:` href values and any `gtag('event','phone_click',...)` values that are meant to track the school's phone clicks to `0788871560`.
2. When updating the floating WhatsApp chat button intended to contact the school, ensure the `href` uses `https://wa.me/0788871560` and the tracking event uses `'phone':'0788871560'`.
3. Preserve the RD Solutions footer anchor pointing to `https://wa.me/0796315374` and its tracking value `'phone':'0796315374'`.

Example (school contact):

```html
<a class="nlca-footer-contact-text" href="tel:0788871560" onclick="gtag('event','phone_click',{'phone':'0788871560'})">0788871560</a>
```

Example (developer credit — keep as-is):

```html
<span class="nlca-footer-credit">Designed By <a class="border-bottom" href="https://wa.me/0796315374" onclick="gtag('event','whatsapp_click',{'phone':'0796315374'})">RD Solutions</a></span>
```

If you need to update both types, be explicit and search the repo first to avoid accidental global replaces.

Repo grep examples:

```bash
# find occurrences of the school number
git grep -n "0788871560" -- '*.html' '*.md'

# find dev credit occurrences
git grep -n "0796315374" -- '*.html' '*.md'
```

---

## 5) Scripts and automation

The repository contains helpful Python scripts under `scripts/` to audit and update content, run Lighthouse, check assets, and more.

Common patterns:

```bash
python3 scripts/check_assets.py     # list missing files or broken asset links
python3 scripts/fix_paths.py        # fix known path inconsistencies
python3 scripts/update_sitemap_canon_redirects.py  # update sitemap/canonical/redirect helpers
python3 scripts/sync_nav.py         # keep navigation consistent across pages
python3 scripts/run_lighthouse.py   # run automated Lighthouse audits
```

Read each script header for usage details and exercise caution before running scripts that modify files; prefer running them with a test branch first.

---

## 6) SEO & Analytics

- The repo includes GA4 instrumentation and `gtag` event calls to track phone clicks and WhatsApp clicks. See `SEO-GA4-SETUP.md` for GA4 guidance.
- Keep structured data (`ld+json`) for each page updated — it appears at the top of pages (EducationalOrganization data, telephone numbers, etc.). When changing phone numbers, update structured data `telephone` fields too.

GA4 event examples:

```js
gtag('event','phone_click',{'phone':'0788871560'});
gtag('event','whatsapp_click',{'phone':'0788871560'});
```

Ensure that the event `phone` field matches the actual phone used in the `tel:` link.

---

## 7) Structured data & sitemap

- Each page contains JSON-LD near the top describing the organization and contact points. Keep the `telephone` and `url` fields accurate.
- `sitemap.xml` and `image-sitemap.xml` exist at repo root — update them when you add or remove pages.

Recommended tools:

- Google Rich Results Test for structured data validation
- XML sitemap validation in Google Search Console

---

## 8) Accessibility, performance & security

Accessibility:
- Use semantic HTML where possible.
- Ensure color contrasts, alt attributes, and keyboard navigation are supported.

Performance:
- Optimize images (WebP where supported), use responsive `srcset`.
- Use minified CSS/JS for production deployment.

Security:
- Keep emails obfuscated if scraping is a concern, or serve contact forms through a server-side endpoint.
- Do NOT commit secrets or API keys to the repository.

---

## 9) Testing & troubleshooting

Common checks:

- Visual check: serve locally and inspect pages
- Link check: `python3 scripts/check_assets.py` or use `linkchecker`
- Lighthouse audit: `python3 scripts/run_lighthouse.py` or Chrome devtools

If a change broke site layout, revert quickly using Git and work in a branch:

```bash
git checkout -b fix/some-descriptive-name
# make edits
git add -A && git commit -m "Fix: ..."
git push --set-upstream origin fix/some-descriptive-name
```

---

## 10) Deployment & CI

Common hosting options:

- GitHub Pages — works for static sites. Configure `index.html` and publish the `main` branch or `gh-pages` branch.
- Netlify / Vercel — automated deploys via Git push. Set build command to `echo 'static'` (no build) and publish directory to repository root.

Suggested CI checks:

- Link check
- Lighthouse performance audit
- Linting (HTML/CSS/JS)

---

## 11) Contributing

Please follow these guidelines:

1. Open an issue describing the change or bug first.
2. Create a feature branch: `git checkout -b feat/your-change`.
3. Make small commits with clear messages.
4. Run the relevant scripts and preview locally.
5. Open a pull request with a description and request reviews.

Include a `CODE_OF_CONDUCT.md` and `CONTRIBUTING.md` in the future for public contributions.

---

## 12) Changelog & Releases

Maintain a `CHANGELOG.md` or use GitHub Releases. Each release should include:

- Version
- Date
- Summary of changes
- Migration notes (if any)

---

## 13) Credits & Contact

- Site maintained by Rusumo High School
- Developer credit: RD Solutions (footer link)

If you need help with repository operations, contact the maintainer listed in the repo settings or reach RD Solutions via the footer credit.

---

## 14) License

This repository does not include a license file by default. Add a `LICENSE` (e.g., MIT) for clarity. Example:

```
MIT License
Copyright (c) 2026 Rusumo High School
```

---

## Appendix: Useful commands & patterns

- Search for phone references:

```bash
git grep -n "0788871560" -- '*.html' '*.md'
git grep -n "0796315374" -- '*.html' '*.md'
```

- Replace (careful — test in branch):

```bash
perl -pi -e 's#https://wa.me/0788871560#https://wa.me/0796315374#g' $(git grep -l "0788871560" -- '*.html' '*.md')
```

---
