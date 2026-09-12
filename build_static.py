"""
Tradenza International Private Limited - Production Static Site Generator
Compiles the entire web platform into a zero-dependency static build inside 'dist/'.

Target Deployments:
- Netlify / Vercel / Cloudflare Pages / GitHub Pages
- AWS S3 + CloudFront / Azure Static Web Apps / Google Cloud Storage
- Traditional Apache / Nginx / cPanel web hosting
"""

import os
import shutil
import json
from app import app
import database

PAGES = [
    ('/', 'index.html', 'home'),
    ('/requirements', 'requirements.html', 'requirements'),
    ('/products', 'products.html', 'products'),
    ('/rfq', 'rfq.html', 'rfq'),
    ('/buyers', 'buyers.html', 'buyers'),
    ('/suppliers', 'suppliers.html', 'suppliers'),
    ('/about', 'about.html', 'about'),
    ('/contact', 'contact.html', 'contact'),
    ('/admin', 'admin.html', 'admin'),
    ('/404', '404.html', '404'),
]


def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(base_dir, 'dist')

    print("==================================================")
    print("Tradenza International - Building Production Site")
    print("==================================================")

    # Clean existing dist
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir, exist_ok=True)

    # 1. Copy static assets (CSS, JS, Images, Logo)
    src_static = os.path.join(base_dir, 'static')
    dst_static = os.path.join(dist_dir, 'static')
    shutil.copytree(src_static, dst_static)
    print(" Copied static assets (css, js, images, logos)")

    # 2. Render HTML pages with Flask test client
    client = app.test_client()

    for route, filename, active_page in PAGES:
        res = client.get(route)
        if res.status_code in (200, 404):
            content = res.data.decode('utf-8')
            
            # Write primary HTML file (e.g. dist/requirements.html)
            out_file = os.path.join(dist_dir, filename)
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f" Rendered: {filename}")

            # Also create folder-based clean URL (e.g. dist/requirements/index.html)
            # This enables clean URLs without .html extension on any static web server
            if filename != 'index.html' and filename != '404.html':
                slug = filename.replace('.html', '')
                folder_path = os.path.join(dist_dir, slug)
                os.makedirs(folder_path, exist_ok=True)
                folder_index = os.path.join(folder_path, 'index.html')
                with open(folder_index, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ↳ Created clean-URL mirror: {slug}/index.html")
        else:
            print(f" Error rendering {route}: Status {res.status_code}")

    # 3. Export static JSON data for public requirements API
    api_dir = os.path.join(dist_dir, 'api')
    os.makedirs(api_dir, exist_ok=True)
    reqs_api_dir = os.path.join(api_dir, 'requirements')
    os.makedirs(reqs_api_dir, exist_ok=True)

    reqs_res = client.get('/api/requirements')
    if reqs_res.status_code == 200:
        reqs_json = reqs_res.data.decode('utf-8')
        # api/requirements.json
        with open(os.path.join(api_dir, 'requirements.json'), 'w', encoding='utf-8') as f:
            f.write(reqs_json)
        # api/requirements/index.json
        with open(os.path.join(reqs_api_dir, 'index.json'), 'w', encoding='utf-8') as f:
            f.write(reqs_json)
        print(" Exported static public requirements JSON endpoints")

    # 4. Create Netlify _redirects and headers for SPA/Clean URLs
    redirects_content = """# Tradenza International - Clean URL Routing & Fallbacks
/requirements       /requirements.html      200
/products           /products.html          200
/rfq                /rfq.html               200
/buyers             /buyers.html            200
/suppliers          /suppliers.html         200
/about              /about.html             200
/contact            /contact.html           200
/admin              /admin.html             200
/api/requirements   /api/requirements.json  200
/*                  /404.html               404
"""
    with open(os.path.join(dist_dir, '_redirects'), 'w', encoding='utf-8') as f:
        f.write(redirects_content)

    # 5. Create netlify.toml inside dist and root
    netlify_toml = """[build]
  publish = "dist"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/static/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
"""
    with open(os.path.join(dist_dir, 'netlify.toml'), 'w', encoding='utf-8') as f:
        f.write(netlify_toml)
    with open(os.path.join(base_dir, 'netlify.toml'), 'w', encoding='utf-8') as f:
        f.write(netlify_toml)

    # 6. Create vercel.json for Vercel Static deployment
    vercel_json = {
        "version": 2,
        "cleanUrls": True,
        "trailingSlash": False,
        "headers": [
            {
                "source": "/static/(.*)",
                "headers": [
                    {
                        "key": "Cache-Control",
                        "value": "public, max-age=31536000, immutable"
                    }
                ]
            }
        ]
    }
    with open(os.path.join(dist_dir, 'vercel.json'), 'w', encoding='utf-8') as f:
        json.dump(vercel_json, f, indent=2)
    with open(os.path.join(base_dir, 'vercel.json'), 'w', encoding='utf-8') as f:
        json.dump(vercel_json, f, indent=2)

    print("==================================================")
    print(" Production build completed successfully!")
    print(f" Distribution folder: {dist_dir}")
    print(" Ready for 1-click deployment to Netlify, Vercel, GitHub Pages, or S3.")
    print("==================================================")


if __name__ == '__main__':
    build()
