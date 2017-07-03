#import datetime module
import datetime

#imports feedparser
import feedparser

#imports Flask from the package flask
from flask import Flask

#imports the make_response function
from flask import make_response

#imports the render_template for HTML using Jinja
from flask import render_template

#imports the request module
from flask import request

#import modules for retrieving and parsing JSON in Python
import json
import urllib2
import urllib


#Obtain the WEATHER_URL
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f6efd50d80a9b93d27ce0f7dd0168d53"

#Obtain the CURRENCY_URL
CURRENCY_URL = "https://openexchangerates.org/api/latest.json?app_id=953721683613432186bcdead707e4060"

#Obtain the RSS feeds
RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml', 'cnn':'http://rss.cnn.com/rss/edition.rss', 'fox':'http://feeds.foxnews.com/foxnews/latest', 'iol':'http://rss.iol.io/iol/news'}

#Creates an instance of Flask object using our module's name as a parameter.
app = Flask(__name__)

"""
---This is static routing---
#Python decorator. Means that the function directly below it should be called whenever a user visits the main root page of our web application ("/")
@app.route("/")
def main():
  return "Visit /bbc, /cnn, or /fox to view their respective RSS Feeds."
#Python decorate when routed to bbc
@app.route("/bbc")
def bbc():
  return get_news('bbc')

#Python decorate when routed to cnn
@app.route("/cnn")
def cnn():
  return get_news('cnn')

#Python decorate when routed to fox
@app.route("/fox")
def fox():
  return get_news('fox')
"""


"""
---This is dynamic routing---
"""

#Default values for home
DEFAULTS = {'publication':'bbc', 'city':'Seattle, WA, USA', 'currency_from':'GBP', 'currency_to':'USD'}

#fallback function
def get_value_with_fallback(key):
  if request.args.get(key):
    return request.args.get(key)
  if request.cookies.get(key):
    return request.cookies.get(key)
  return DEFAULTS[key]

#Python decorator for all the publications:
@app.route("/")#Get_News function which gathers the RSS Feed
def home():
  #Get customized headlines, based on user input or default publication
  publication = get_value_with_fallback("publication")
  articles = get_news(publication)

  #get customized weather based on user input or default city
  city = get_value_with_fallback("city")
  weather = get_weather(city)

  #get customized currency based on user input or default
  currency_from = get_value_with_fallback("currency_from")
  currency_to = get_value_with_fallback("currency_to")

  rate, currencies = get_rates(currency_from, currency_to)

  #passing dynamic data to the template

  response = make_response(render_template("home.html", articles = articles, weather = weather, currency_from = currency_from, currency_to = currency_to, rate = rate, currencies=sorted(currencies)))

  expires = datetime.datetime.now() + datetime.timedelta(days=365)
  response.set_cookie("publication", publication, expires=expires)
  response.set_cookie("city", city, expires=expires)
  response.set_cookie("currency_from", currency_from, expires=expires)
  response.set_cookie("currency_to", currency_to, expires=expires)
  return response

#news function
def get_news(query):
  if not query or query.lower() not in RSS_FEEDS:
    publication = DEFAULTS['publication']
  else:
    publication = query.lower()
  feed = feedparser.parse(RSS_FEEDS[publication])
  return feed['entries']

  #Grab the weather forecast
  weather = get_weather("Seattle,WA,USA")

#weather function
def get_weather(query):
  #uses the quote() function to retrieve weather from cities that may contain spaces (translates spaces to %20)
  query = urllib.quote(query)

  #loads data over HTTP into a Python string by using the urllib2 library
  url = WEATHER_URL.format(query)
  data = urllib2.urlopen(url).read()

  #JSON's loads() function to convert the JSON string to a Python dictionary
  parsed = json.loads(data)
  weather = None

  #Parse the JSON string to retrieve attributes we want
  if parsed.get("weather"):
    weather = {"description":parsed["weather"][0]["description"],"temperature":parsed["main"]["temp"],"city":parsed["name"], 'country':parsed['sys']['country']}

  return weather


#currency function
def get_rates(frm, to):
  all_currency = urllib2.urlopen(CURRENCY_URL).read()
  parsed = json.loads(all_currency).get('rates')
  frm_rate = parsed.get(frm.upper())
  to_rate = parsed.get(to.upper())
  return (to_rate/frm_rate, parsed.keys())

#Python idiom that evaluates to true if the application is run directly. Prevents python scripts form being unintentionally run when they are imported into other Python files.
if __name__ == '__main__':

  #starts the Flask's development server on our local machine. Port 5000 for local, 80 for production, set the debug to True which will help us see detailed errors directly on the web browser.
  app.run(port=5000, debug = True)
