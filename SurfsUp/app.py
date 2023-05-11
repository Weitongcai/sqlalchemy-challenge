# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
#Define the welcome page
@app.route("/")
def welcome():
    # List all available api routes.
    return(
        f"Welcome to the Honolulu, Hawaii Trip planning!"
        f"Avaliable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
    
#######Precipitation#########
@app.route("/api/v1.0/precipitation")
def Precipitation():
    #Create the session from Python to DB
    session_1 = Session(engine)
    prcp_results = session_1.query(Measurement.date, Measurement.prcp).filter(Measurement.date >='2016-08-23').filter(Measurement.date <='2017-08-23').order_by(Measurement.date).all()
    session_1.close()
    # Create a Python dictionary from the row data and append to a list
    prcp_output = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        prcp_output.append(prcp_dict)
    #Return the JSON representation of your dictionary.
    return jsonify(prcp_output)

################Stations###################
@app.route("/api/v1.0/stations")
def station():
    #Create the session from Python to DB
    session_2 = Session(engine)
    station_results = session_2.query(Station.station).all()
    session_2.close()
    #Return a JSON list of stations from the dataset.
    stations = list(np.ravel(station_results))
    return jsonify(stations)

##################Tobs###########################
@app.route("/api/v1.0/tobs")
def tobs():
    #Query the dates and temperature observations of the most-active station for the previous year of data
    session_3 = Session(engine)
    tobs_results = session_3.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-18").filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all()
    session_3.close()
    # Create a dictionary from the row data and append to a list
    tobs_output = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temperature Observations"] = tobs
        tobs_output.append(tobs_dict)
    #Return a JSON list of temperature observations for the previous year.
    return jsonify(tobs_output)

################Start Date#########################
@app.route("/api/v1.0/<start>")
def start_date(start=None):
    # Query all the stations and for the given date. 
    session_4 = Session(engine)
    #Calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    results_4 =session_4.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session_4.close()
    # Create a dictionary from the row data and append to a list
    start_output = []
    for tmin, tmax, tavg in results_4:
        start_dict = {}
        start_dict['minimum temperature'] = tmin
        start_dict['maximum temperature'] = tmax
        start_dict['average temperature'] = tmavg
        start_output.append(start_dict)
    #Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date
    return jsonify(start_output)


##############start date to the end date range##########################
@app.route("/api/v1.0/<start>/<end>")
def range_date(start = None, end = None):
    # Query all the stations and for the given range of dates.
    session_5 = Session(engine)
    range_results = session_5.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session_5.close()
    # Create a dictionary from the row data and append to a list
    range_output = []
    for tmin, tmax, tavg in range_results:
        range_dict = {}
        range_dict['minimum temperature'] = tmin
        range_dict['maximum temperature'] = tmax
        range_dict['average temperature'] = tmavg
        range_output.append(range_dict)
    
    return jsonify(range_output)

# app.run statement
if __name__ == "__main__":
    app.run(debug=True)



