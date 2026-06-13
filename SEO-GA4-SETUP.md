# GA4 Setup & Conversion Event Tracking

## Quick Setup (Replace GA4 ID)

Replace `G-PNQVXH2VSV` in all HTML files with your actual GA4 Measurement ID.

```bash
# Find your GA4 ID in: Google Analytics → Admin → Property → Data Streams → Web
# Replace placeholder (example):
grep -r "G-PNQVXH2VSV" /workspaces/rhs --include="*.html" | head
sed -i 's/G-PNQVXH2VSV/G-YOUR-ACTUAL-ID/g' /workspaces/rhs/**/*.html
```

---

## Recommended Conversion Events

### 1. **Phone Click** (Contact)
Tracks when users click the phone number or WhatsApp link.

```html
<!-- In Contact.html and footer -->
<a href="tel:0788871560" onclick="gtag('event', 'phone_click', {'phone': '0788871560'});">0788871560</a>
<a href="https://wa.me/0788871560" onclick="gtag('event', 'whatsapp_click', {'phone': '0788871560'});">WhatsApp</a>
```

### 2. **Contact Form Submit**
Tracks form submissions (admissions, inquiries).

```html
<!-- In Contact.html -->
<form onsubmit="gtag('event', 'contact_form_submit', {'form_name': 'General Inquiry'}); return true;">
  <!-- form fields -->
</form>
```

### 3. **Admissions Interest**
Tracks clicks to admissions/applications pages.

```html
<!-- In index.html hero CTA and nav -->
<a href="admissions/Admissions.html" onclick="gtag('event', 'admissions_click', {'page': 'homepage'});">Apply Now</a>
```

### 4. **Document Download** (if added later)
Tracks PDF downloads (prospectus, fees, etc.).

```html
<a href="assets/pdf/prospectus.pdf" onclick="gtag('event', 'file_download', {'file_name': 'prospectus.pdf'});">Download Prospectus</a>
```

### 5. **Page View / Scroll Depth**
GA4 auto-tracks page views; you can add scroll depth:

```javascript
document.addEventListener('scroll', function() {
  let scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
  if (scrolled > 50 && !window.ga_scroll_50) {
    window.ga_scroll_50 = true;
    gtag('event', 'scroll_depth', {'depth': '50%'});
  }
  if (scrolled > 90 && !window.ga_scroll_90) {
    window.ga_scroll_90 = true;
    gtag('event', 'scroll_depth', {'depth': '90%'});
  }
});
```

---

## GA4 Dashboard Setup

Once GA4 is running:

1. Go to **Google Analytics → Admin → Events → Custom definitions**
2. Create custom events for the above (GA4 will auto-detect `phone_click`, `contact_form_submit`, etc.)
3. Create a custom report:
   - **Rows:** Event Name
   - **Values:** Event Count
   - **Filter:** By event name

---

## Testing

1. Visit your site.
2. Perform actions (click phone, submit form, click Apply).
3. In GA4: **Realtime → Events** should show new events within 1–2 seconds.

---

## Notes

- Replace `G-PNQVXH2VSV` with your Measurement ID before deploying.
- Conversion events appear in **GA4 Admin → Conversions** (you may need to "Mark as Conversion" after first events fire).
- All events are automatically sent to GA4 and appear in reports within 24 hours.

