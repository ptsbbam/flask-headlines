#imports feedparser 
import feedparser

#imports Flask from the package flask
from flask import Flask

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
#Python decorator for all the publications:
@app.route("/")
@app.route("/<publication>")
#Get_News function which gathers the RSS Feed
def get_news(publication='bbc'):
  feed = feedparser.parse(RSS_FEEDS[publication])
  first_article = feed['entries'][0]
  return """<html>
    <body>
      <h1> Headlines </h1>
      <b>{0}</b> <br/>
      <i>{1}</i> <br/>
      <p>{2}</p> <br/>
    </body>
    </html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))
  
#Python idiom that evaluates to true if the application is run directly. Prevents python scripts form being unintentionally run when they are imported into other Python files. 
if __name__ == '__main__':

  #starts the Flask's development server on our local machine. Port 5000 for local, 80 for production, set the debug to True which will help us see detailed errors directly on the web browser. 
  app.run(port=5000, debug = True) 
