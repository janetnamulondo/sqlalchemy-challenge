import pandas as pd
import numpy as np
import datetime as dt

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
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"Welcome to the Hawaii Climate API Home Page"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"

# #Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")

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

@app.route("/api/v1.0/stations")
def station():
     print("Server received request for 'stations' page...")
#Return a JSON list of stations from the dataset.
results = session.query(Station.name, Station.station).all()
session.close()

#Create a dictionary before jsonfying
all_stations =[]
for station, name in results:
    station_dict ={}
    station_dict["station"] = station
    station_dict["name"] = name
    all_stations.append(station_dict)
#Return JSON representation of the station_dictionary 
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def station():
     print("Server received request for 'tobs' page...")

#query for the dates and temperature observations from a year from the last data point.
#Create variable for date to query with. 
lastdate= dt.date(2017,8,23) - dt.timedelta(days=365)

results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= lastdate).all()
session.close()

#Return a JSON list of Temperature Observations (tobs) for the previous year.
#create a list in a dictionary for all the observed tobs in the last year. 
all_tobs =[]
for date, tobs in results:
    tobs_dict ={}
    tobs_dict["date"] = date
    tobs_dict["tobs"] = tobs
    all_tobs.append(tobs_dict)

#Create JSON file
    return jsonify(all_tobs)
    
if __name__ == "__main__":
    app.run(debug=True)

# app = Flask(__name__)