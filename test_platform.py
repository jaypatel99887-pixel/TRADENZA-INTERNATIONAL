"""
Tradenza International - Automated System Test Suite
Verifies all web pages, REST API endpoints, database operations, and export utilities.
"""

import unittest
import json
from app import app
import database

class TradenzaPlatformTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.init_db()
        cls.client = app.test_client()

    def test_01_homepage_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("Tradenza International Private Limited", content)
        self.assertIn("Connecting Global Buyers with", content)
        self.assertIn("tradenzainternationalprivateli@gmail.com", content)
        self.assertIn("+91 98251 15213", content)
        self.assertIn("Source From India. Trade Globally.", content)
        self.assertIn("How It Works", content)
        self.assertIn("Why Choose Tradenza?", content)
        self.assertIn("From India to Global Markets", content)

    def test_02_products_page_renders_all_12_categories(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        categories = [
            "Agricultural Products",
            "Food & Beverages",
            "Spices",
            "Fruits & Vegetables",
            "Rice & Grains",
            "Textiles & Garments",
            "Home & Lifestyle Products",
            "Tiles & Building Materials",
            "Medical & Healthcare",
            "Industrial Products",
            "Packaging Products",
            "Consumer Products"
        ]
        for cat in categories:
            self.assertIn(cat, content, f"Category '{cat}' should be present in products page")

    def test_03_auxiliary_pages_render(self):
        for path in ['/rfq', '/buyers', '/suppliers', '/about', '/contact', '/admin']:
            res = self.client.get(path)
            self.assertEqual(res.status_code, 200, f"Path {path} returned status {res.status_code}")

    def test_04_api_rfq_submission(self):
        payload = {
            'name': 'Jean-Luc Picard',
            'company': 'Enterprise Sourcing SAS',
            'country': 'France',
            'email': 'jl.picard@enterpriseglobal.fr',
            'phone': '+33 1 42 68 55 00',
            'product': 'Organic Turmeric & Black Pepper',
            'product_category': 'Spices',
            'quantity': '20 Metric Tons',
            'specifications': 'Curcumin > 5%, sortex cleaned',
            'packaging': '25kg Kraft paper bags',
            'destination_country': 'Port of Le Havre, France',
            'delivery_timeline': 'Within 60 days',
            'message': 'Looking for quarterly continuous supply.'
        }
        res = self.client.post('/api/rfq', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertIn("Your requirement has been received", data.get('message'))
        self.assertTrue(data.get('id') > 0)
        self.rfq_id = data.get('id')

    def test_05_api_buyer_submission(self):
        payload = {
            'name': 'Tariq Mansoor',
            'company': 'Emirates Wholesale Group',
            'country': 'UAE',
            'email': 'tariq@emirateswholesale.ae',
            'phone': '+971 50 999 8888',
            'product': '1121 Parboiled Basmati Rice',
            'quantity': '10x40ft Containers',
            'target_price': 'Competitive CIF Jebel Ali',
            'destination_country': 'Jebel Ali Port, UAE',
            'message': 'Require samples sent to Dubai office.'
        }
        res = self.client.post('/api/buyer', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))

    def test_06_api_supplier_submission(self):
        payload = {
            'name': 'Deepak Sharma',
            'company': 'Shiva Ceramics & Vitrified Tiles',
            'product_category': 'Tiles & Building Materials',
            'products': '600x1200mm Glazed Vitrified Tiles',
            'manufacturing_capacity': '20 Containers per month',
            'location': 'Morbi, Gujarat, India',
            'email': 'exports@shivaceramics.in',
            'phone': '+91 98250 11122',
            'website': 'https://shivaceramics.example.in',
            'export_experience': 'Currently supplying to GCC and East Africa'
        }
        res = self.client.post('/api/supplier', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))

    def test_07_api_contact_submission(self):
        payload = {
            'name': 'Sarah Jenkins',
            'company': 'London Trade House',
            'country': 'United Kingdom',
            'email': 's.jenkins@londontradehouse.co.uk',
            'phone': '+44 20 8900 1234',
            'subject': 'General Trade Facilitation',
            'message': 'We would like to arrange an introductory call regarding sourcing Indian textiles.'
        }
        res = self.client.post('/api/contact', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))

    def test_08_admin_api_list_and_stats(self):
        # Stats
        res_stats = self.client.get('/api/admin/stats')
        self.assertEqual(res_stats.status_code, 200)
        stats = res_stats.get_json()
        self.assertGreaterEqual(stats.get('total', 0), 4)

        # List
        res_list = self.client.get('/api/admin/submissions?limit=100')
        self.assertEqual(res_list.status_code, 200)
        leads = res_list.get_json()
        self.assertIn('items', leads)
        self.assertGreaterEqual(len(leads['items']), 4)

        first_id = leads['items'][0]['id']
        
        # Update Status
        res_status = self.client.patch(f'/api/admin/submissions/{first_id}/status', 
                                      data=json.dumps({'status': 'Qualified'}),
                                      content_type='application/json')
        self.assertEqual(res_status.status_code, 200)

        # Update Notes
        res_notes = self.client.post(f'/api/admin/submissions/{first_id}/notes',
                                     data=json.dumps({'notes': 'Test verified qualification'}),
                                     content_type='application/json')
        self.assertEqual(res_notes.status_code, 200)

    def test_09_admin_csv_export(self):
        res = self.client.get('/api/admin/export')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, 'text/csv')
        csv_data = res.data.decode('utf-8')
        self.assertIn('name', csv_data)
        self.assertIn('company', csv_data)
        self.assertIn('product', csv_data)


    def test_10_requirements_page_renders(self):
        response = self.client.get('/requirements')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("Live International Sourcing Demands", content)
        self.assertIn("Sourcing Board", content)
        self.assertIn("Supply This Demand", content)
        self.assertIn("TRQ-", content)

    def test_11_api_requirements_list_and_filter(self):
        # Full list
        res = self.client.get('/api/requirements')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertGreaterEqual(data.get('count', 0), 12)
        items = data.get('items', [])
        self.assertTrue(len(items) > 0)
        first_item = items[0]
        self.assertIn('ref_code', first_item)
        self.assertIn('product_name', first_item)
        self.assertIn('country', first_item)

        # Category filter
        res_cat = self.client.get('/api/requirements?category=Rice%20%26%20Grains')
        self.assertEqual(res_cat.status_code, 200)
        cat_data = res_cat.get_json()
        self.assertTrue(cat_data.get('success'))
        for item in cat_data.get('items', []):
            self.assertEqual(item.get('category'), 'Rice & Grains')

        # Keyword search
        res_search = self.client.get('/api/requirements?search=Tiles')
        self.assertEqual(res_search.status_code, 200)
        search_data = res_search.get_json()
        self.assertTrue(search_data.get('success'))
        self.assertGreaterEqual(search_data.get('count', 0), 1)

    def test_12_api_requirement_detail(self):
        res = self.client.get('/api/requirements/1')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        item = data.get('item', {})
        self.assertEqual(item.get('id'), 1)
        self.assertIn('ref_code', item)
        self.assertIn('specifications', item)

    def test_13_suppliers_page_prefill_requirement(self):
        res = self.client.get('/suppliers?requirement_id=1')
        self.assertEqual(res.status_code, 200)
        content = res.data.decode('utf-8')
        self.assertIn("Sourcing Lead: #", content)
        self.assertIn("TRQ-", content)


    def test_14_custom_404_page(self):
        res = self.client.get('/non-existent-page-test-404')
        self.assertEqual(res.status_code, 404)
        content = res.data.decode('utf-8')
        self.assertIn("Sourcing Route Not Found", content)
        self.assertIn("404", content)


if __name__ == '__main__':
    unittest.main()
