# SEO Monitoring & Reporting Setup

## 1. Google Search Console Dashboard

### Setup (30 minutes)

1. Go to https://search.google.com/search-console
2. Select your property (Domain: rusumohighschool.org)
3. Navigate to **Sitemaps** and submit:
   - https://rusumohighschool.org/sitemap.xml
   - https://rusumohighschool.org/image-sitemap.xml

4. Check **Coverage** to see indexed pages
5. Review **Performance** tab for keyword rankings

### Weekly Reports to Monitor

| Metric | Ideal Target | Check In |
|--------|--------------|----------|
| Total impressions | +10% week-over-week | Performance tab |
| Average CTR | >5% | Performance tab |
| Indexed pages | All main pages | Coverage tab |
| Crawl errors | 0 | Coverage tab |
| Mobile usability | 100% | Mobile Usability tab |
| Search traffic | +20% month-over-month | Performance tab |

---

## 2. Google Analytics 4 (GA4) Dashboard

### Setup (20 minutes)

1. Go to https://analytics.google.com
2. Create a property for rusumohighschool.org (if not already created)
3. Add GA4 ID to all HTML (replace `G-PNQVXH2VSV` with your ID)
4. Wait 24–48 hours for data collection

### Weekly Metrics to Track

| Metric | What It Means | Good Benchmark |
|--------|--------------|-----------------|
| Users | Unique visitors | +5% week-over-week |
| Sessions | Total visits | +10% week-over-week |
| Pages/Session | Engagement depth | 3+ pages |
| Avg. Session Duration | Engagement quality | 2+ minutes |
| Bounce Rate | % of single-page visits | <60% |
| Conversion Rate | % completing tracked actions | 5%+ |

### Key Events to Monitor (after implementing GA4 setup)

- `phone_click` — Admissions phone inquiries
- `contact_form_submit` — Contact form submissions
- `admissions_click` — Apply Now link clicks
- `whatsapp_click` — WhatsApp inquiries
- `scroll_depth` — Content engagement

---

## 3. Automated Reporting Template (Google Sheets)

### Create a Weekly SEO Report

**Sheet: SEO_Weekly_Report**

```
Date Range | Metric | This Week | Last Week | Change | Goal | Status
2026-06-13 | GSC Impressions | 450 | 400 | +12% | +10% | ✓
2026-06-13 | GSC Avg CTR | 6.2% | 5.8% | +0.4% | 5%+ | ✓
2026-06-13 | GA Users | 320 | 280 | +14% | +5% | ✓
2026-06-13 | GA Sessions | 420 | 380 | +10% | +10% | ✓
2026-06-13 | GA Bounce Rate | 58% | 62% | -4% | <60% | ✓
2026-06-13 | Top Keyword | "rusumo high school" | Position 12 | — | Top 10 | ⚠
2026-06-13 | Backlinks | 18 | 16 | +2 | +5/week | — 
2026-06-13 | Mobile Usability | 100% | 100% | — | 100% | ✓
```

### Monthly Goals Tracking

```
Objective | Q2 Target | Q3 Target | Current | On Track?
Organic Traffic | +20% | +50% | +14% | On track
Indexed Pages | 30+ | 40+ | 21 | On track
Backlinks | 30+ | 60+ | 18 | Behind
Keyword Rankings (Top 10) | 8+ | 15+ | 2 | Behind
Conversion Rate | 3%+ | 5%+ | 1.2% | Behind
```

---

## 4. Rank Tracking Tools (Free Alternatives)

### Option A: Google Search Console (Free)

- Tracks top keywords + rankings for your domain
- Limited to your own site
- **How to use:** Performance tab → Filter by "Query" → Sort by position

### Option B: Ahrefs (Paid, $99/mo) or Semrush (Paid, $120/mo)

- Tracks competitor keywords + backlinks
- Free trial available
- **Setup:** Add domain, set 5–10 target keywords, track weekly

### Option C: Monitorank (Free)

- https://monitorank.com/
- Tracks up to 10 keywords for free
- Easy dashboard

### Option D: AccuRanker (Paid, $10+/mo)

- More accurate than free tools
- API-based integrations

---

## 5. Weekly SEO Audit Checklist

**Every Monday, run this audit:**

```bash
# 1. Check if site is still indexed
curl -s "https://www.google.com/search?q=site:rusumohighschool.org" | grep -o "About [0-9]" 

# 2. Check robots.txt
curl https://rusumohighschool.org/robots.txt

# 3. Check for 404 errors in GSC
# Go to: Search Console → Coverage → Errors

# 4. Check mobile usability
# Go to: Search Console → Mobile Usability

# 5. Validate SSL certificate
echo | openssl s_client -servername rusumohighschool.org -connect rusumohighschool.org:443 2>/dev/null | openssl x509 -noout -dates

# 6. Check page speed (Lighthouse)
python3 /workspaces/rhs/scripts/run_lighthouse.py
```

---

## 6. Monthly Business Review Report

**Send this to school leadership on the 1st of each month:**

### Format

```
=== Rusumo High School SEO Monthly Report ===
Month: June 2026

EXECUTIVE SUMMARY
- Organic traffic: 320 users (+14% week-over-week)
- Ranking position for "Rusumo High School": #12 (target: Top 10)
- Backlinks acquired: 2 (goal: 5/week)
- Contact inquiries from site: 12 (+20% vs. May)

KEY METRICS
| KPI | This Month | Last Month | Change |
| Organic Users | 1,200 | 980 | +22% |
| Organic Sessions | 1,850 | 1,500 | +23% |
| Pages Indexed | 21 | 18 | +17% |
| Backlinks | 18 | 15 | +20% |
| Top Keyword Ranking | #12 | #18 | +6 positions |
| Mobile Usability | 100% | 100% | — |
| Avg Page Load | 3.2s | 3.5s | -9% |

GOALS STATUS
✓ = On track
⚠ = At risk
✗ = Off track

✓ +20% organic growth
⚠ Backlink acquisition (18/30 target, need 12 more)
✓ Mobile optimization
✗ Keyword ranking (position 12, target top 10)

RECOMMENDATIONS
1. Priority: Increase backlink outreach (Rwanda Education Board, local NGOs)
2. Optimize title/meta for "RHS Rwanda" keyword
3. Create 2–3 blog posts on "A-Level Science Rwanda" to target long-tail keywords
4. Add student testimonials to homepage (trust signals)

BUDGET & ROI
- SEO Investment: $0 (in-house)
- Lead Value: ~$2,400 (12 inquiries × estimated $200 per admission)
- ROI: Infinite (no paid spend, organic only)

Next Month Goals
- +30% organic traffic
- 25+ backlinks
- Top 5 ranking for "Rusumo High School"
```

---

## 7. Quarterly Strategy Review

**Every 3 months, analyze trends and adjust strategy:**

1. **Keyword Performance:** Which keywords are ranking? Which need more work?
2. **Content Performance:** Which pages drive most traffic? Which have high bounce rate?
3. **Backlink Profile:** Which domains link to you? Are there patterns?
4. **Competitor Analysis:** Check how competitors rank for same keywords
5. **Seasonal Trends:** Are admissions searches increasing? Adjust content accordingly

---

## 8. Tools Setup Summary

| Tool | Purpose | Cost | Setup Time |
|------|---------|------|-----------|
| Google Search Console | Keyword rankings, indexing, errors | Free | 15 min |
| Google Analytics 4 | Traffic, user behavior, conversions | Free | 20 min |
| Google Business Profile | Local SEO, reviews, listings | Free | 10 min |
| Lighthouse | Performance audits | Free | 5 min |
| Ahrefs/Semrush | Rank tracking, competitor analysis | $99–120/mo | 1 hour |
| Monitorank | Simpler rank tracking | Free | 10 min |

---

## Quick Start (This Week)

**Day 1:** Set up Google Search Console + GA4
**Day 2:** Submit sitemaps
**Day 3:** Create weekly monitoring sheet
**Day 4:** Schedule weekly audit checklist
**Day 5:** Send first monthly report to stakeholders

