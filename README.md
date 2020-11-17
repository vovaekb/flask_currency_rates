# flask_currency_rates
Simple Flask App for scraping currency rates from cbr.ru API and displaying currency rates stored in database as a table with filtering and sorting by header.

## Setup and running
We need to install Redis server. Then install all necessary python packages using requirements.txt

```bash
pip install -r requirements.txt
```

### Test in browser
Navigate to url http://127.0.0.1:5000/ in browser.

REST API endpoints:

* /parse (GET) - parsing currency rates from cbr.ru API. Saving currency rate results in PostgreSQL database. Returns JSON with message in format: {"message":"<num rates> rates retrieved"}.
* /rates?date_from=<date_from>&date_to=<date_to> (GET) - get status of job execution and get results. <date_from> and <date_to> in format dd/mm/yyyy. Displaying table of all currency rates stored in database.

## Demo
Demo on Heroku: https://flask-currency-rates.herokuapp.com/.

