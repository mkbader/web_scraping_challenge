from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars


app = Flask(__name__)



@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)



 

if __name__ == '__main__':
	app.run(debug=True)