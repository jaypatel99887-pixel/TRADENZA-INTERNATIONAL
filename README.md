# Tradenza International Private Limited
### Global Import, Export, Sourcing & Trade Facilitation Platform

A luxury, high-performance, responsive corporate website and B2B trade facilitation platform for **Tradenza International Private Limited**, an India-based global sourcing enterprise connecting international buyers with verified Indian manufacturers and suppliers.

---

## ⚡ Technology Stack Overview

> **Technology Classification:**
> - **Frontend**: **Plain HTML5, Tailwind CSS (via CDN) + Custom Luxury CSS3, and Vanilla JavaScript (ES6+)**.
> - **Build Architecture**: **Zero Node.js, Zero React, Zero Next.js, Zero Vite**.
> - **Backend (Optional/Dynamic)**: **Python 3 (Flask + SQLite)** providing REST APIs, lead intake, status pipelines, and CSV export.
> - **Static Export**: Pre-rendered into standalone **`dist/`** containing pure static HTML, CSS, JavaScript, JSON API endpoints, and media assets.

| Category | Technology | Description |
|---|---|---|
| **Frontend Framework** | Plain HTML5 + Vanilla JS | Ultra-fast, zero client-side bundle overhead, SEO optimized |
| **Styling** | Tailwind CSS + Custom CSS | Obsidian & Rose Gold luxury styling (`#120D0E`, `#EAA6B1`, `#191214`) |
| **Dynamic Backend** | Python Flask (3.0+) | REST API routes (`/api/rfq`, `/api/buyer`, `/api/supplier`, `/api/requirements`) |
| **Database** | SQLite 3 (`tradenza.db`) | Lightweight, self-contained, transactional lead & requirement store |
| **WSGI Server** | Gunicorn / Waitress | Production-grade WSGI servers via `wsgi.py` and `Procfile` |
| **Static Deployment** | Pre-rendered `dist/` | 1-click deployable to Netlify, Vercel, GitHub Pages, Cloudflare Pages, S3 |

---

## 🏢 Corporate Profile & Verified Credentials

- **Company Name**: Tradenza International Private Limited
- **Business**: Global Import, Export, Sourcing & Trade Facilitation
- **Base**: India
- **Official Email**: `tradenzainternationalprivateli@gmail.com`
- **Phone / WhatsApp**: `+91 98251 15213`
- **Official Logo**: Embedded luxury rose-gold branding (`static/images/tradenza-official-logo.png`)
- **Compliance Policy**: Zero unsupported claims (no fake certifications, warehouse volume, or fictitious licenses). Sourcing sectors are explicitly presented as sourcing facilitation capabilities.

---

## 🚀 Production Deployment Options

### Option 1: Static Hosting (Netlify, Vercel, Cloudflare Pages, GitHub Pages, cPanel)
*Best for ultra-fast CDN delivery, zero server maintenance, and highest reliability.*

1. Run the static site generator:
   ```bash
   python build_static.py
   ```
2. The output is generated inside the **`dist/`** directory.
3. Deploy the **`dist/`** folder:
   - **Netlify**: Drag and drop the `dist/` folder into Netlify Drop, or connect your Git repo and set Publish directory to `dist`. (Pre-configured `netlify.toml` and `_redirects` are included).
   - **Vercel**: Deploy with `vercel deploy` or connect your Git repo (pre-configured `vercel.json` included).
   - **GitHub Pages**: Push the contents of `dist/` to the `gh-pages` branch.
   - **cPanel / Apache / Nginx**: Upload the contents of `dist/` directly into `public_html/`.

*Note: In static mode, form submissions automatically fall back to browser storage, display a verified confirmation modal, and generate direct WhatsApp trade desk click-to-chat links with pre-filled inquiry details.*

---

### Option 2: Full-Stack Dynamic Hosting (Render, Railway, Heroku, DigitalOcean, VPS)
*Best if you require live SQLite lead storage, the Admin Dashboard (`/admin`), and CSV export in production.*

1. **Prerequisites**: Python 3.10+ and dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. **WSGI Production Command (Linux)**:
   ```bash
   gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2
   ```
3. **WSGI Production Command (Windows / Cross-platform)**:
   ```powershell
   waitress-serve --port=5000 wsgi:app
   ```
4. **PaaS Configuration**:
   - `Procfile` is pre-configured with: `web: gunicorn wsgi:app`
   - `wsgi.py` is pre-configured as the application entrypoint.
   - Set environment variable `SECRET_KEY` in your hosting dashboard.

---

## 🧪 Verification & Automated Testing

Run the automated test suite to verify all web routes, form submissions, public requirements, 404 handler, and database operations:
```powershell
python test_platform.py
```
All **14 automated unit and integration tests** execute and verify:
- Homepage, Catalog, RFQ, Buyer Desk, Supplier Portal, About, Contact, Admin
- Public Buyer Sourcing Board (`/requirements`) & Live REST API (`/api/requirements`)
- Sourcing Lead Pre-fill on Supplier Portal (`/suppliers?requirement_id=1`)
- Form Submissions (RFQ, Buyer Inquiries, Supplier Applications, Contact)
- Admin Status Pipeline & CSV Data Export
- Custom Luxury 404 Error Page

---

## 📁 Project Structure

```
tradenza-international/
├── app.py                     # Flask server with REST API & route controllers
├── database.py                # SQLite database management, queries, status transitions
├── wsgi.py                    # Production WSGI entry point (Gunicorn/Waitress)
├── Procfile                   # Process configuration for PaaS (Heroku/Render/Railway)
├── vercel.json                # Vercel deployment configuration
├── netlify.toml               # Netlify headers and clean-URL configuration
├── run.py                     # Local development launcher
├── test_platform.py           # Automated test suite (14 test cases)
├── build_static.py            # Static site generator for standalone CDN deployment
├── requirements.txt           # Python dependencies (Flask, Gunicorn, Waitress)
├── README.md                  # Project documentation & deployment guide
├── tradenza.db                # SQLite database with 12 seeded public buyer demands
├── dist/                      # Pre-rendered standalone production static build
│   ├── index.html             # Homepage
│   ├── requirements.html      # Public Buyer Sourcing Board
│   ├── products.html          # Sourcing Catalog
│   ├── rfq.html               # RFQ Intake Form
│   ├── buyers.html            # International Buyer Desk
│   ├── suppliers.html         # Indian Supplier Registration
│   ├── about.html             # Corporate Story & Trade Pillars
│   ├── contact.html           # Contact & Communication Desk
│   ├── admin.html             # Administrative Lead Management Dashboard
│   ├── 404.html               # Custom Luxury 404 Error Page
│   ├── _redirects             # Clean URL rewrites for Netlify/Cloudflare
│   ├── api/requirements.json  # Pre-rendered static JSON API
│   ├── requirements/          # Clean-URL mirror (requirements/index.html)
│   ├── products/              # Clean-URL mirror (products/index.html)
│   ├── rfq/                   # Clean-URL mirror (rfq/index.html)
│   ├── buyers/                # Clean-URL mirror (buyers/index.html)
│   ├── suppliers/             # Clean-URL mirror (suppliers/index.html)
│   ├── about/                 # Clean-URL mirror (about/index.html)
│   ├── contact/               # Clean-URL mirror (contact/index.html)
│   ├── admin/                 # Clean-URL mirror (admin/index.html)
│   └── static/                # Static assets bundle
├── static/
│   ├── css/
│   │   └── style.css          # Custom luxury styling, animations, rose-gold accents
│   ├── js/
│   │   ├── main.js            # Sticky navbar, modals, form submission, WhatsApp
│   │   ├── map.js             # Interactive SVG world trade route visualizer
│   │   └── admin.js           # Admin dashboard lead management & CSV export
│   └── images/
│       ├── tradenza-official-logo.png # Official brand logo
│       ├── logo.svg           # Luxury vector brand logo
│       ├── logo-light.svg     # White/gold logo for dark backgrounds
│       └── favicon.svg        # Vector tab icon
└── templates/
    ├── base.html              # Layout, SEO tags, sticky navbar & footer
    ├── index.html             # Corporate homepage
    ├── requirements.html      # Public Buyer Sourcing Board
    ├── products.html          # Sourcing catalog with category filters
    ├── rfq.html               # Dedicated RFQ procurement form
    ├── buyers.html            # International buyer sourcing desk
    ├── suppliers.html         # Indian manufacturer onboarding
    ├── about.html             # Corporate story and trade pillars
    ├── contact.html           # Contact details and communication hub
    ├── admin.html             # Administrative dashboard
    └── 404.html               # Custom 404 error page
```
