from flask import Flask, _app_ctx_stack, render_template, request, jsonify, Response
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import SQLAlchemyError
import requests
from bs4 import BeautifulSoup
import xmltodict
from pprint import pprint
import datetime
from models import CurrencyRate # models
# from .models import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

# Create custom exception class
class CustomError(Exception):
	"""Input parameter error."""

@app.errorhandler(CustomError)
def handle_custom_exception(error):
    details = error.args[0]
    resp = Response(details['message'], status=200, mimetype='text/plain')
    return resp


@app.route('/parse', methods=['GET'])
def parse():
    errors = []
    records= []
    date_from = request.args.get('date_from')
    date_to= request.args.get('date_to')
    url = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=%s&date_req2=%s&VAL_NM_RQ=R01235' % (date_from, date_to)
    r = requests.get(url)
    currency_rates_records = []
    
    d = xmltodict.parse(r.text)
    curs_data = d['ValCurs']
    record_data = curs_data['Record']
    for record_item in record_data:
        record_date = datetime.datetime.strptime(record_item['@Date'], '%d.%m.%Y').date()
        value = float(record_item['Value'].replace(',', '.'))
        try:
            record = CurrencyRate(
                date=record_date,
                nominal=int(record_item['Nominal']),
                value=value
            )
            app.session.add(record)
            app.session.commit()
            records.append(record)
            print("Record saved")
        except SQLAlchemyError as e:
            print("Unable to add item to database.")
            error = e.__dict__['orig']
            raise CustomError({'message': 'Error when saving rate to database: %s' % error})
    
    return jsonify({'message': '%s rates retrieved' % len(records)}), 200

@app.route('/rates', methods=['GET'])
def rates():
    errors = []
    rates = app.session.query(CurrencyRate).all()
    return render_template('index.html', errors=errors, rates=rates)
