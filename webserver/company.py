from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_orator import Orator
import yaml
import json

app = FlaskAPI(__name__)
with open("orator.yml", 'r') as stream:
    config = yaml.load(stream)

app.config['ORATOR_DATABASES'] = config['databases']
db = Orator(app)

@app.route('/company', methods=['GET'])
def hello_world():
    companies = db.table('company').get().to_json()

    return {
        "status_code": 200,
        "message": "successful",
        "data": json.loads(companies)
    }

if __name__ == "__main__":
    app.run(debug=True)

