# Security Headers & Server Configuration Guide

## HTTP Headers (_headers file for Netlify / static hosts)

Already created at `/workspaces/rhs/_headers`. For reference:

```
/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Feature-Policy: vibrate 'none'; geolocation 'none'
  Content-Security-Policy: default-src 'self' https:; img-src 'self' data: https:; script-src 'self' https://www.googletagmanager.com https://www.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; frame-ancestors 'none'
  Cache-Control: public, max-age=31536000, immutable
```

---

## Nginx Configuration (if self-hosted)

Save as `/etc/nginx/conf.d/rhs-security.conf`:

```nginx
# Security Headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self' https:; img-src 'self' data: https:; script-src 'self' https://www.googletagmanager.com https://www.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; frame-ancestors 'none'" always;

# Gzip Compression
gzip on;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
gzip_vary on;

# Cache Static Assets
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|webp)$ {
  expires 1y;
  add_header Cache-Control "public, immutable";
}

# Cache HTML (shorter, must revalidate)
location ~* \.html$ {
  expires 1h;
  add_header Cache-Control "public, must-revalidate";
}

# Disable caching for robots, sitemap
location ~* (robots\.txt|sitemap\.xml) {
  expires 1d;
  add_header Cache-Control "public, must-revalidate";
}

# Enable HTTP/2 Server Push (preload critical CSS)
http2_push /assets/css/style.css;
http2_push /assets/css/bootstrap.min.css;
```

---

## Apache Configuration (if using Apache)

Add to `.htaccess` or VirtualHost:

```apache
<IfModule mod_headers.c>
  Header set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
  Header set X-Frame-Options "DENY"
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set Content-Security-Policy "default-src 'self' https:; img-src 'self' data: https:; script-src 'self' https://www.googletagmanager.com https://www.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; frame-ancestors 'none'"
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/json application/javascript application/xml+rss
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>
```

---

## Deployment Checklist

- [ ] Enable HTTPS (Let's Encrypt free, or via hosting provider)
- [ ] Deploy `_headers` file to static host (Netlify auto-reads it)
- [ ] If nginx/Apache: add security headers config and reload
- [ ] Test headers: `curl -I https://rusumohighschool.org/ | grep -i security`
- [ ] Run SSL test: https://www.ssllabs.com/ssltest/analyze.html?d=rusumohighschool.org
- [ ] Run security headers test: https://securityheaders.com/?q=rusumohighschool.org&hide=on&followRedirects=on

---

## DNS & TLS Best Practices

### DNSSEC (optional but recommended)

```bash
# Check if domain supports DNSSEC
dig rusumohighschool.org DNSKEY
```

### CAA Record (optional, restricts which CAs can issue certs)

Add to your DNS provider (e.g., Porkbun):

```
CAA 0 issue "letsencrypt.org"
CAA 0 issuewild ";                     # prevents wildcard issuance
CAA 0 iodef "mailto:admin@rusumohighschool.rw"  # email for security issues
```

