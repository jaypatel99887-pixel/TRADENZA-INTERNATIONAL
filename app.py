"""
Tradenza International Private Limited - Web Application Server
Production-grade Flask application providing corporate website routes and lead management API.
"""

from flask import Flask, render_template, request, jsonify, Response, send_from_directory
import os
import re
from datetime import datetime
import database

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tradenza-secret-key-international-trade')

# Initialize database on start
database.init_db()


def validate_email(email):
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email.strip()) is not None


# ==========================================
# PAGE ROUTES
# ==========================================

@app.route('/')
def index():
    featured_reqs = database.get_public_requirements(limit=6)
    return render_template('index.html', active_page='home', featured_requirements=featured_reqs)


@app.route('/requirements')
def requirements():
    cat = request.args.get('category', 'all')
    search = request.args.get('search', '')
    items = database.get_public_requirements(category=cat, search=search, limit=50)
    return render_template('requirements.html', active_page='requirements', requirements=items, current_category=cat, current_search=search)


@app.route('/products')
def products():
    return render_template('products.html', active_page='products')


@app.route('/rfq')
def rfq():
    category = request.args.get('category', '')
    product = request.args.get('product', '')
    return render_template('rfq.html', active_page='rfq', prefill_category=category, prefill_product=product)


@app.route('/buyers')
def buyers():
    return render_template('buyers.html', active_page='buyers')


@app.route('/suppliers')
def suppliers():
    req_id = request.args.get('requirement_id')
    prefill_req = database.get_public_requirement_by_id(int(req_id)) if req_id and req_id.isdigit() else None
    return render_template('suppliers.html', active_page='suppliers', prefill_requirement=prefill_req)


@app.route('/about')
def about():
    return render_template('about.html', active_page='about')


@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')


@app.route('/admin')
def admin():
    return render_template('admin.html', active_page='admin')


# ==========================================
# SUBMISSION API ENDPOINTS
# ==========================================

@app.route('/api/rfq', methods=['POST'])
def submit_rfq():
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    product = data.get('product', '').strip()

    if not name or not email or not product:
        return jsonify({'success': False, 'message': 'Please provide your name, email, and the required product.'}), 400

    if not validate_email(email):
        return jsonify({'success': False, 'message': 'Please provide a valid email address.'}), 400

    payload = {
        'type': 'rfq',
        'name': name,
        'company': data.get('company', ''),
        'country': data.get('country', ''),
        'email': email,
        'phone': data.get('phone', ''),
        'product': product,
        'product_category': data.get('product_category', ''),
        'quantity': data.get('quantity', ''),
        'specifications': data.get('specifications', ''),
        'packaging': data.get('packaging', ''),
        'target_price': data.get('target_price', ''),
        'destination_country': data.get('destination_country', ''),
        'delivery_timeline': data.get('delivery_timeline', ''),
        'message': data.get('message', '')
    }

    sub_id = database.insert_submission(payload)
    return jsonify({
        'success': True,
        'id': sub_id,
        'message': 'Thank you. Your requirement has been received. The Tradenza International team will review it and contact you.'
    })


@app.route('/api/buyer', methods=['POST'])
def submit_buyer():
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    product = data.get('product', '').strip()

    if not name or not email or not product:
        return jsonify({'success': False, 'message': 'Please provide your full name, email, and required product.'}), 400

    if not validate_email(email):
        return jsonify({'success': False, 'message': 'Please provide a valid email address.'}), 400

    payload = {
        'type': 'buyer',
        'name': name,
        'company': data.get('company', ''),
        'country': data.get('country', ''),
        'email': email,
        'phone': data.get('phone', ''),
        'product': product,
        'product_category': data.get('product_category', ''),
        'quantity': data.get('quantity', ''),
        'target_price': data.get('target_price', ''),
        'destination_country': data.get('destination_country', ''),
        'message': data.get('message', '') or data.get('additional_requirements', '')
    }

    sub_id = database.insert_submission(payload)
    return jsonify({
        'success': True,
        'id': sub_id,
        'message': 'Thank you. Your sourcing requirement has been logged. Our international desk will connect with you.'
    })


@app.route('/api/supplier', methods=['POST'])
def submit_supplier():
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get('name', '').strip()
    company = data.get('company', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()

    if not name or not company or not email:
        return jsonify({'success': False, 'message': 'Please provide contact name, company name, and email.'}), 400

    if not validate_email(email):
        return jsonify({'success': False, 'message': 'Please provide a valid email address.'}), 400

    payload = {
        'type': 'supplier',
        'name': name,
        'company': company,
        'country': 'India',
        'email': email,
        'phone': phone,
        'product': data.get('products', '') or data.get('product', ''),
        'product_category': data.get('product_category', ''),
        'manufacturing_capacity': data.get('manufacturing_capacity', ''),
        'location': data.get('location', ''),
        'website': data.get('website', ''),
        'export_experience': data.get('export_experience', ''),
        'message': data.get('message', '')
    }

    sub_id = database.insert_submission(payload)
    return jsonify({
        'success': True,
        'id': sub_id,
        'message': 'Thank you for registering with Tradenza International. Our supplier procurement desk will evaluate your profile.'
    })


@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({'success': False, 'message': 'Please provide your name, email, and message.'}), 400

    if not validate_email(email):
        return jsonify({'success': False, 'message': 'Please provide a valid email address.'}), 400

    payload = {
        'type': 'contact',
        'name': name,
        'company': data.get('company', ''),
        'country': data.get('country', ''),
        'email': email,
        'phone': data.get('phone', ''),
        'product': data.get('subject', 'General Trade Inquiry'),
        'message': message
    }

    sub_id = database.insert_submission(payload)
    return jsonify({
        'success': True,
        'id': sub_id,
        'message': 'Thank you. Your message has been delivered to Tradenza International. We will get back to you shortly.'
    })


# ==========================================
# PUBLIC REQUIREMENTS / BUY LEADS API
# ==========================================

@app.route('/api/requirements', methods=['GET'])
def api_get_requirements():
    cat = request.args.get('category', 'all')
    search = request.args.get('search', '')
    limit = int(request.args.get('limit', 50))
    items = database.get_public_requirements(category=cat, search=search, limit=limit)
    return jsonify({
        'success': True,
        'count': len(items),
        'items': items
    })


@app.route('/api/requirements/<int:req_id>', methods=['GET'])
def api_get_requirement(req_id):
    item = database.get_public_requirement_by_id(req_id)
    if not item:
        return jsonify({'success': False, 'message': 'Requirement not found.'}), 404
    return jsonify({'success': True, 'item': item})


# ==========================================
# ADMIN API ENDPOINTS
# ==========================================

@app.route('/api/admin/submissions', methods=['GET'])
def list_submissions():
    type_filter = request.args.get('type', 'all')
    status_filter = request.args.get('status', 'all')
    search = request.args.get('search', '')
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))

    result = database.get_submissions(
        type_filter=type_filter,
        status_filter=status_filter,
        search=search,
        limit=limit,
        offset=offset
    )
    return jsonify(result)


@app.route('/api/admin/submissions/<int:sub_id>', methods=['GET'])
def get_submission(sub_id):
    sub = database.get_submission_by_id(sub_id)
    if not sub:
        return jsonify({'success': False, 'message': 'Not found'}), 404
    return jsonify({'success': True, 'item': sub})


@app.route('/api/admin/submissions/<int:sub_id>/status', methods=['PATCH'])
def update_status(sub_id):
    data = request.get_json(silent=True) or {}
    new_status = data.get('status')
    if not new_status:
        return jsonify({'success': False, 'message': 'Status is required'}), 400

    try:
        database.update_submission_status(sub_id, new_status)
        return jsonify({'success': True, 'message': f'Status updated to {new_status}'})
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/api/admin/submissions/<int:sub_id>/notes', methods=['POST'])
def update_notes(sub_id):
    data = request.get_json(silent=True) or {}
    notes = data.get('notes', '')
    database.update_submission_notes(sub_id, notes)
    return jsonify({'success': True, 'message': 'Notes updated successfully'})


@app.route('/api/admin/stats', methods=['GET'])
def get_stats():
    stats = database.get_submission_stats()
    return jsonify(stats)


@app.route('/api/admin/export', methods=['GET'])
def export_csv():
    type_filter = request.args.get('type', 'all')
    status_filter = request.args.get('status', 'all')
    csv_content = database.export_submissions_csv(type_filter, status_filter)

    filename = f"tradenza_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', active_page='404'), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Tradenza International server starting at http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
