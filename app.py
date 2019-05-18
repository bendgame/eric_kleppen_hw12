from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scraper

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_db = mongo.db.mars_db.find_one()

    # Return template and data
    return render_template("index.html", mars_db_insert = mars_db)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

   #scrape the data
    mars_data = mars_scraper.mars_news()
    mongo.db.mars_db.update({}, mars_data, upsert=True)

    mars_data = mars_scraper.feature_mars_img()
    mongo.db.mars_db.update({}, mars_data, upsert=True)

    mars_data = mars_scraper.mars_weather()
    mongo.db.mars_db.update({}, mars_data, upsert=True)

    mars_data = mars_scraper.mars_facts()
    mongo.db.mars_db.update({}, mars_data, upsert=True)

    mars_data = mars_scraper.mars_hemis()
    mongo.db.mars_db.update({}, mars_data, upsert=True)
    

    #Redirect 
    return redirect("/",code=302)


if __name__ == "__main__":
    app.run(debug=True)
