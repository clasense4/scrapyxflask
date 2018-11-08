from orator import DatabaseManager
import json
import yaml

with open("orator.yml", 'r') as stream:
    config = yaml.load(stream)

db = DatabaseManager(config['databases'])

with open('company_profile.json', encoding='utf-8-sig') as json_file:
    text = json_file.read()
    json_data = json.loads(text)

    for data in json_data:
        company = {
            'name': data['name'],
            'url': data['url'],
            'ticker_symbol': data['ticker_symbol'],
            'country': data['country'],
            'business': data['business'],
            'listing_bourse': data['listing_bourse'],
            'email': data['email'],
            'website': data['website'],
            'description': data['description'],
            'address': data['address'],
            'revenue': data['revenue'],
            'phone': json.dumps(data['phone']),
            'auditing_company': json.dumps(data['auditing_company']),
            'financial_summary': json.dumps(data['financial_summary']),
            'business_registration': json.dumps(data['business_registration'])
        }
        db.table('company').insert(company)
