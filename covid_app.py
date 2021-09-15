from flask import Flask, render_template, redirect, url_for
import pymongo
from pymongo import MongoClient
import scraper

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
client = MongoClient('127.0.0.1', 27017)
db = client["covid_app"]
col = db["collection"]


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    
    # Find one record of data from the mongo database
    displayed_data = col.find()
    # Return template and data
    return render_template("index.html", sickly=displayed_data)
    
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    col.drop()
    # Run the scrape function
    covid_data = scraper.scrape_info()

    print(covid_data)
    # Update the Mongo database using update and upsert=True
    col.insert_many(covid_data)

    # Redirect back to home page
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)