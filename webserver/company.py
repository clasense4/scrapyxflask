from flask import request
from flask_api import FlaskAPI
from flask_orator import Orator
import yaml
import json

app = FlaskAPI(__name__)
with open("orator.yml", 'r') as stream:
    config = yaml.load(stream)

app.config['ORATOR_DATABASES'] = config['databases']
db = Orator(app)

@app.route('/company', methods=['GET'])
def company():
    try:
        if request.args.get('company_name'):
            search_string = request.args.get('company_name')
            companies = db.table('company').where(
                'name','ilike',"%" + search_string + "%"
            ).get().to_json()
        elif request.args.get('industry'):
            search_string = request.args.get('industry')
            companies = db.table('company').where(
                'industry','ilike',"%" + search_string + "%"
            ).get().to_json()
        elif request.args.get('revenue_gte'):
            search_string = request.args.get('revenue_gte')
            companies = db.table('company').where(
                'revenue', '>=', search_string
            ).get().to_json()
        else:
            companies = db.table('company').get().to_json()

        return {
            "status_code": 200,
            "message": "successful",
            "data": json.loads(companies)
        }
    except:
        return {
            "status_code": 400,
            "message": "bad request"
        }

if __name__ == "__main__":
    app.run(debug=True)

