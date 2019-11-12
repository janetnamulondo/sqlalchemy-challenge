#Import from numpy
import numpy as np

#import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

#Import flask and json 
from flask import Flask, jsonify

#Create an app, being sure to pass __name__
app = Flask(__name__)


#Define what to do when a user hits the index route
@app.route("/")
def Welcome():
    print("Server received request for 'Home' page...")
    """List all available API routes."""
    return (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

# #Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")

# Create our session (link) from Python to the DB
    session = Session(engine)

#Convert the query results to a Dictionary using date as the key and prcp as the value.
results = session.query(Measurement.date, Measurement.prcp).all()
session.close()

# Create a dictionary from the row data and append to a list of all_measurements
all_measurements = []
for date, prcp in results:
    measurement_dict = {}
    measurement_dict["date"] = date
    measurement_dict["prcp"] = prcp
    all_measurements.append(measurement_dict)

#Return the JSON representation of your dictionary.

return jsonify(all_measurements)


# if __name__ == "__main__":
#     app.run(debug=True)


# app = Flask(__name__)