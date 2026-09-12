"""
Tradenza International Private Limited - Database Layer
SQLite storage for RFQs, Buyer Inquiries, Supplier Registrations, and Contact Messages.
"""

import sqlite3
import os
import csv
import io
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'tradenza.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,                  -- 'rfq', 'buyer', 'supplier', 'contact'
        status TEXT NOT NULL DEFAULT 'New',  -- 'New', 'Contacted', 'Qualified', 'Closed'
        name TEXT NOT NULL,
        company TEXT,
        country TEXT,
        email TEXT NOT NULL,
        phone TEXT,
        product TEXT,
        product_category TEXT,
        quantity TEXT,
        specifications TEXT,
        packaging TEXT,
        target_price TEXT,
        destination_country TEXT,
        delivery_timeline TEXT,
        manufacturing_capacity TEXT,
        export_experience TEXT,
        website TEXT,
        location TEXT,
        message TEXT,
        notes TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON submissions(type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON submissions(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON submissions(created_at)')

    # Seed sample representative inquiries if empty so dashboard is immediately inspectable
    cursor.execute('SELECT COUNT(*) as count FROM submissions')
    count = cursor.fetchone()['count']
    if count == 0:
        seed_sample_leads(cursor)

    init_public_requirements(cursor)

    conn.commit()
    conn.close()


def seed_sample_leads(cursor):
    samples = [
        (
            'rfq', 'New', 'Ahmed Al-Mansoor', 'Gulf Agro Commodities LLC', 'United Arab Emirates',
            'ahmed.m@gulfagro.ae', '+971 50 123 4567', 'Premium Indian Basmati Rice 1121 XXL',
            'Rice & Grains', '500 Metric Tons (20x40ft containers)',
            'Parboiled 1121 Basmati, 8.35mm grain length, max 12% moisture, 0.5% broken',
            '50kg non-woven master bags with inner poly liner', 'Target: Competitive CIF Jebel Ali',
            'UAE - Port Jebel Ali', 'Within 45 days', '', '', '', '',
            'Looking for reliable millers from Punjab/Haryana with direct export capabilities.',
            'Initial inquiry logged. Awaiting sample lot certificate verification.'
        ),
        (
            'buyer', 'Contacted', 'Marcus Vance', 'Vance Industrial Supplies Ltd', 'United Kingdom',
            'm.vance@vanceindustrial.co.uk', '+44 20 7946 0912', 'Vitrified Porcelain Floor & Wall Tiles',
            'Tiles & Building Materials', '4x20ft Full Container Loads monthly',
            '600x1200mm & 800x1600mm glazed vitrified tiles, polished finish',
            'Export wooden pallet packaging with shrink wrap', 'FOB Mundra',
            'United Kingdom - Port of Felixstowe', 'Quarterly recurring', '', '', '', '',
            'We are expanding commercial distribution across the UK and require reliable Morbi tile manufacturing partners.',
            'Followed up via WhatsApp and email. Catalogs shared.'
        ),
        (
            'supplier', 'Qualified', 'Rajesh Patel', 'Shreeji Organic Agro Exports', 'India',
            'exports@shreejiorganics.in', '+91 98765 43210', 'Cumin, Coriander & Turmeric Finger',
            'Spices', '', 'Whole seeds, machine cleaned, 99.5% purity, sorting ready',
            '25kg / 50kg jute and PP bags with brand private labelling', '', '', '',
            '1,200 Metric Tons per season', '5+ years exporting to Middle East & Europe',
            'https://shreejiorganics.example.in', 'Unjha, Gujarat, India',
            'We are manufacturer-processors with direct farm procurement in Gujarat and Rajasthan.',
            'Verified supplier credentials. Suitable for upcoming UAE and EU inquiries.'
        ),
        (
            'contact', 'New', 'Elena Rostova', 'Global Health Trade Partners', 'Germany',
            'e.rostova@globalhealthtrade.de', '+49 30 5678 9012', 'Medical Consumables & Surgical Gloves',
            'Medical & Healthcare Supplies', 'Pilot order: 100,000 pairs nitrile examination gloves',
            'EN455, ISO 13485 compliant examination gloves', 'Dispenser boxes of 100 pcs',
            '', 'Germany - Hamburg Port', 'Urgent sourcing required', '', '', '', '',
            'Please let us know your sourcing capabilities and onboarding timeline for European CE medical requirements.',
            'New inquiry received via corporate contact form.'
        )
    ]

    for item in samples:
        cursor.execute('''
        INSERT INTO submissions (
            type, status, name, company, country, email, phone, product, product_category,
            quantity, specifications, packaging, target_price, destination_country,
            delivery_timeline, manufacturing_capacity, export_experience, website,
            location, message, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', item)


def insert_submission(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO submissions (
        type, status, name, company, country, email, phone, product,
        product_category, quantity, specifications, packaging, target_price,
        destination_country, delivery_timeline, manufacturing_capacity,
        export_experience, website, location, message, notes
    ) VALUES (
        :type, 'New', :name, :company, :country, :email, :phone, :product,
        :product_category, :quantity, :specifications, :packaging, :target_price,
        :destination_country, :delivery_timeline, :manufacturing_capacity,
        :export_experience, :website, :location, :message, ''
    )
    ''', {
        'type': data.get('type', 'rfq'),
        'name': data.get('name', '').strip(),
        'company': data.get('company', '').strip(),
        'country': data.get('country', '').strip(),
        'email': data.get('email', '').strip(),
        'phone': data.get('phone', '').strip(),
        'product': data.get('product', '').strip(),
        'product_category': data.get('product_category', '').strip(),
        'quantity': data.get('quantity', '').strip(),
        'specifications': data.get('specifications', '').strip(),
        'packaging': data.get('packaging', '').strip(),
        'target_price': data.get('target_price', '').strip(),
        'destination_country': data.get('destination_country', '').strip(),
        'delivery_timeline': data.get('delivery_timeline', '').strip(),
        'manufacturing_capacity': data.get('manufacturing_capacity', '').strip(),
        'export_experience': data.get('export_experience', '').strip(),
        'website': data.get('website', '').strip(),
        'location': data.get('location', '').strip(),
        'message': data.get('message', '').strip(),
    })
    sub_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # If RFQ or Buyer Requirement, mirror to public requirements
    if data.get('type') in ('rfq', 'buyer') and data.get('product'):
        try:
            req_data = dict(data)
            req_data['submission_id'] = sub_id
            add_public_requirement(req_data)
        except Exception as e:
            pass

    return sub_id


def get_submissions(type_filter=None, status_filter=None, search=None, limit=100, offset=0):
    conn = get_connection()
    cursor = conn.cursor()

    conditions = []
    params = []

    if type_filter and type_filter != 'all':
        conditions.append('type = ?')
        params.append(type_filter)

    if status_filter and status_filter != 'all':
        conditions.append('status = ?')
        params.append(status_filter)

    if search:
        conditions.append('(name LIKE ? OR company LIKE ? OR email LIKE ? OR product LIKE ? OR country LIKE ?)')
        wildcard = f"%{search.strip()}%"
        params.extend([wildcard, wildcard, wildcard, wildcard, wildcard])

    where_clause = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''

    # Get total count
    cursor.execute(f'SELECT COUNT(*) as total FROM submissions {where_clause}', params)
    total = cursor.fetchone()['total']

    # Get rows
    query = f'''
    SELECT * FROM submissions
    {where_clause}
    ORDER BY created_at DESC
    LIMIT ? OFFSET ?
    '''
    cursor.execute(query, params + [limit, offset])
    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {'total': total, 'items': rows}


def get_submission_by_id(sub_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM submissions WHERE id = ?', (sub_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_submission_status(sub_id, status):
    valid_statuses = ['New', 'Contacted', 'Qualified', 'Closed']
    if status not in valid_statuses:
        raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE submissions
    SET status = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    ''', (status, sub_id))
    conn.commit()
    conn.close()
    return True


def update_submission_notes(sub_id, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE submissions
    SET notes = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    ''', (notes, sub_id))
    conn.commit()
    conn.close()
    return True


def get_submission_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as total FROM submissions')
    total = cursor.fetchone()['total']

    cursor.execute('''
    SELECT
        SUM(CASE WHEN status = 'New' THEN 1 ELSE 0 END) as count_new,
        SUM(CASE WHEN status = 'Contacted' THEN 1 ELSE 0 END) as count_contacted,
        SUM(CASE WHEN status = 'Qualified' THEN 1 ELSE 0 END) as count_qualified,
        SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) as count_closed,
        SUM(CASE WHEN type = 'rfq' THEN 1 ELSE 0 END) as count_rfq,
        SUM(CASE WHEN type = 'buyer' THEN 1 ELSE 0 END) as count_buyer,
        SUM(CASE WHEN type = 'supplier' THEN 1 ELSE 0 END) as count_supplier,
        SUM(CASE WHEN type = 'contact' THEN 1 ELSE 0 END) as count_contact
    FROM submissions
    ''')
    stats = dict(cursor.fetchone())
    conn.close()
    stats['total'] = total
    return stats


def export_submissions_csv(type_filter=None, status_filter=None):
    res = get_submissions(type_filter=type_filter, status_filter=status_filter, limit=5000)
    items = res['items']

    output = io.StringIO()
    if not items:
        writer = csv.writer(output)
        writer.writerow(['No data available'])
        return output.getvalue()

    fieldnames = [
        'id', 'type', 'status', 'created_at', 'name', 'company', 'country', 'email', 'phone',
        'product', 'product_category', 'quantity', 'specifications', 'packaging',
        'target_price', 'destination_country', 'delivery_timeline',
        'manufacturing_capacity', 'export_experience', 'website', 'location', 'message', 'notes'
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for row in items:
        writer.writerow(row)

    return output.getvalue()


# ==========================================
# PUBLIC SOURCING REQUIREMENTS / BUY LEADS
# ==========================================

def init_public_requirements(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS public_requirements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_code TEXT NOT NULL UNIQUE,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        country TEXT NOT NULL,
        country_flag TEXT DEFAULT '🌐',
        destination_port TEXT,
        quantity TEXT NOT NULL,
        target_price TEXT,
        specifications TEXT,
        packaging TEXT,
        timeline TEXT,
        buyer_type TEXT DEFAULT 'International Importer',
        status TEXT DEFAULT 'Active Sourcing',
        is_featured INTEGER DEFAULT 0,
        submission_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_req_cat ON public_requirements(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_req_featured ON public_requirements(is_featured)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_req_status ON public_requirements(status)')

    cursor.execute('SELECT COUNT(*) as count FROM public_requirements')
    count = cursor.fetchone()['count']
    if count == 0:
        seed_public_requirements(cursor)


def seed_public_requirements(cursor):
    curated = [
        (
            'TRQ-1048', 'Premium Indian Basmati Rice 1121 XXL', 'Rice & Grains',
            'United Arab Emirates', '🇦🇪', 'Port Jebel Ali (Dubai)',
            '500 Metric Tons (20x40ft FCL)', 'Competitive CIF Jebel Ali',
            'Parboiled 1121 Basmati, 8.35mm avg grain length, max 12% moisture, 0.5% broken, silky finish',
            '50kg non-woven master bags with inner poly liner', 'Within 30–45 days',
            'Gulf Food Importer & Distributor', 'Active Sourcing', 1, None
        ),
        (
            'TRQ-1049', 'Polished Vitrified Floor & Wall Tiles (600x1200mm)', 'Tiles & Building Materials',
            'United Kingdom', '🇬🇧', 'Port of Felixstowe',
            '4x40ft Containers Monthly', 'FOB Mundra',
            'Porcelain body, polished nano finish, water absorption < 0.05%, rectified edges, grade AAA',
            'Export wooden pallet packing with protective corner guards & shrink film', 'Monthly recurring contract',
            'UK Building Materials Distributor', 'Shortlisting Indian Suppliers', 1, None
        ),
        (
            'TRQ-1050', 'Machine Cleaned Whole Spices (Cumin & Turmeric)', 'Spices',
            'Saudi Arabia', '🇸🇦', 'Jeddah Islamic Port',
            '54 Metric Tons (2x40ft FCL)', 'Target CIF Jeddah',
            'Cumin seeds 99% purity machine cleaned, Turmeric finger curcumin > 3.5%, phytosanitary ready',
            '25kg food-grade PP bags with moisture barrier liner', 'Within 25 days',
            'Saudi Wholesale Food Consortia', 'Verified Demand', 1, None
        ),
        (
            'TRQ-1051', '100% Combed Cotton Knitted T-Shirts & Polos', 'Textiles & Garments',
            'United States', '🇺🇸', 'Port of Newark / New York',
            '25,000 Pieces', 'Target FOB Tuticorin / Nhava Sheva',
            '180 GSM bio-washed 100% combed ringspun cotton, reactive dyed, OEKO-TEX certified, custom neck labels',
            'Individual polybag, 50 pcs per export master carton with barcode stickers', 'Within 60 days',
            'US Private Label Apparel Importer', 'Active Sourcing', 1, None
        ),
        (
            'TRQ-1052', 'Industrial Cast Iron & Stainless Steel Gate Valves', 'Industrial Products',
            'Germany', '🇩🇪', 'Port of Hamburg',
            '5,000 Units', 'FOB Nhava Sheva',
            'Class 150 & 300, Flanged ends according to ANSI B16.5, hydrostatic tested with mill test certs',
            'Fumigated wooden cases with corrosion inhibitor wrap and desiccants', 'Within 45 days',
            'European Pipeline & Industrial Supply Group', 'Shortlisting Indian Suppliers', 1, None
        ),
        (
            'TRQ-1053', 'Fresh Indian Cavendish Bananas (G9 Variety)', 'Fruits & Vegetables',
            'Oman', '🇴🇲', 'Port Sultan Qaboos / Sohar',
            '2x40ft High Cube Reefer Containers (Weekly)', 'CIF Sohar',
            'Length min 7.5 inches, calibration 39-47, pre-cooled, temperature controlled at 13.5°C in reefer',
            '13.5kg corrugated telescopic boxes with vacuum polybags & foam separator sheets', 'Immediate recurring weekly supply',
            'Gulf Fresh Produce Hypermarket Chain', 'Active Sourcing', 1, None
        ),
        (
            'TRQ-1054', 'Nitrile Examination Gloves & Medical Disposables', 'Medical & Healthcare Supplies',
            'France', '🇫🇷', 'Port of Le Havre',
            '200,000 Pairs (Pilot Consignment)', 'CIF Le Havre',
            'Powder-free, blue medical nitrile, EN455 Class 1, ISO 13485 & CE certified, non-sterile',
            '100 pcs dispenser box, 10 dispenser boxes per master shipping carton', 'Within 30 days',
            'European Healthcare Procurement Group', 'Verified Demand', 1, None
        ),
        (
            'TRQ-1055', 'Corrugated Shipping Master Cartons & FIBC Bags', 'Packaging Products',
            'Netherlands', '🇳🇱', 'Port of Rotterdam',
            '50,000 Master Cartons + 2,000 Bulk Bags', 'CIF Rotterdam',
            '5-ply kraft board, burst strength 14 kg/cm², UV stabilized FIBC bulk bags 1,000kg safe working load',
            'Strapped bundles on ISPM-15 treated heat-treated wooden pallets', 'Within 40 days',
            'Agri-Commodity Logistics Provider', 'Active Sourcing', 1, None
        ),
        (
            'TRQ-1056', 'Handcrafted Brass Artware & Metal Table Décor', 'Home & Lifestyle Products',
            'Canada', '🇨🇦', 'Port of Vancouver',
            '1x20ft Container (Assorted SKU Mix)', 'FOB Mundra',
            'Lacquered polished brass planters, candle stands, embossed bowls, and metal serving trays',
            'Individual bubble-wrapped inner gift boxes with 5-ply master export cartons', 'Within 60 days',
            'North American Home Goods Retailer', 'Shortlisting Indian Suppliers', 0, None
        ),
        (
            'TRQ-1057', 'Non-GMO Soya Meal & Animal Feed Pellets', 'Agricultural Products',
            'Vietnam', '🇻🇳', 'Hai Phong Port',
            '1,500 Metric Tons', 'CIF Hai Phong',
            'Crude protein min 48%, moisture max 11%, fiber max 6%, non-GMO certified with test certificate',
            'Bulk in 1,000kg PP jumbo tote bags with lifting loops', 'Within 35 days',
            'Southeast Asian Feed Mill Enterprise', 'Active Sourcing', 0, None
        ),
        (
            'TRQ-1058', 'Chakki Whole Wheat Flour & Sella Non-Basmati Rice', 'Food & Beverages',
            'Nepal', '🇳🇵', 'Birgunj Dry Port (Overland Transit)',
            '300 Metric Tons', 'CPT Birgunj',
            '100% stone ground whole wheat atta, high gluten, Sella non-basmati rice 5% broken max',
            '25kg and 50kg HDPE woven bags with inner poly liner', 'Within 14 days',
            'Regional Food Distribution Network', 'Verified Demand', 0, None
        ),
        (
            'TRQ-1059', 'Ceramic Sanitaryware & Vitreous China Water Closets', 'Tiles & Building Materials',
            'Kenya', '🇰🇪', 'Port of Mombasa',
            '2x40ft Containers', 'CIF Mombasa',
            'Dual flush rimless one-piece water closets, vitreous china body, soft-close seat covers, wash basins',
            '5-ply foam-protected individual cartons, palletized for container loading', 'Within 45 days',
            'East African Hardware & Plumbing Importer', 'Active Sourcing', 0, None
        )
    ]

    for item in curated:
        cursor.execute('''
        INSERT INTO public_requirements (
            ref_code, product_name, category, country, country_flag, destination_port,
            quantity, target_price, specifications, packaging, timeline,
            buyer_type, status, is_featured, submission_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', item)


def get_public_requirements(category=None, search=None, limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM public_requirements WHERE 1=1'
    params = []

    if category and category.lower() != 'all':
        query += ' AND (LOWER(category) = ? OR LOWER(category) LIKE ?)'
        params.extend([category.lower(), f'%{category.lower()}%'])

    if search and search.strip():
        term = f'%{search.strip().lower()}%'
        query += ' AND (LOWER(product_name) LIKE ? OR LOWER(specifications) LIKE ? OR LOWER(country) LIKE ? OR LOWER(destination_port) LIKE ? OR LOWER(category) LIKE ?)'
        params.extend([term, term, term, term, term])

    query += ' ORDER BY is_featured DESC, id DESC LIMIT ?'
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    items = [dict(r) for r in rows]
    conn.close()
    return items


def get_public_requirement_by_id(req_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM public_requirements WHERE id = ?', (req_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def add_public_requirement(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(id) as max_id FROM public_requirements')
    row = cursor.fetchone()
    max_id = (row['max_id'] if row and row['max_id'] else 1000) + 1
    ref_code = f"TRQ-{max_id + 50}"

    country_flags = {
        'united arab emirates': '🇦🇪', 'uae': '🇦🇪', 'saudi arabia': '🇸🇦',
        'united states': '🇺🇸', 'usa': '🇺🇸', 'united kingdom': '🇬🇧', 'uk': '🇬🇧',
        'germany': '🇩🇪', 'france': '🇫🇷', 'canada': '🇨🇦', 'australia': '🇦🇺',
        'oman': '🇴🇲', 'qatar': '🇶🇦', 'kuwait': '🇰🇼', 'nepal': '🇳🇵',
        'netherlands': '🇳🇱', 'kenya': '🇰🇪', 'vietnam': '🇻🇳', 'singapore': '🇸🇬'
    }
    c_lower = (data.get('country') or '').strip().lower()
    flag = country_flags.get(c_lower, '🌐')

    cursor.execute('''
    INSERT INTO public_requirements (
        ref_code, product_name, category, country, country_flag, destination_port,
        quantity, target_price, specifications, packaging, timeline,
        buyer_type, status, is_featured, submission_id
    ) VALUES (
        :ref_code, :product_name, :category, :country, :country_flag, :destination_port,
        :quantity, :target_price, :specifications, :packaging, :timeline,
        :buyer_type, :status, 0, :submission_id
    )
    ''', {
        'ref_code': ref_code,
        'product_name': data.get('product', '') or data.get('product_name', 'General Sourcing Requirement'),
        'category': data.get('product_category', '') or data.get('category', 'Custom Sourcing'),
        'country': data.get('country', 'International Market'),
        'country_flag': flag,
        'destination_port': data.get('destination_country', '') or data.get('destination_port', 'Global Port'),
        'quantity': data.get('quantity', 'FCL / Commercial Volume'),
        'target_price': data.get('target_price', 'Market Pricing'),
        'specifications': data.get('specifications', '') or data.get('message', 'Standard export grade specifications required.'),
        'packaging': data.get('packaging', 'Standard Export Packaging'),
        'timeline': data.get('delivery_timeline', '') or data.get('timeline', 'As per agreement'),
        'buyer_type': 'Verified International Buyer',
        'status': 'Active Sourcing',
        'submission_id': data.get('submission_id')
    })
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
