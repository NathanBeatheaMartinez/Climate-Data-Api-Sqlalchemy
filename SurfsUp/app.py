# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

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
session = Session(engine)
    
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to my climate app!</br>"
        f"Available routes:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as json"""
# Calculate the date one year from the last date in data set.
    year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve all the dates and precipitation scores for the last 12 months
    prcp_last_12 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_before).all()

# Convert the query results from your precipitation analysis to a dictionary
    prcp_dict = dict(prcp_last_12)    
    
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return the stations data as json"""
# Calculate the date one year from the last date in data set.
    year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve all the dates and precipitation scores for the last 12 months
    prcp_last_12 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_before).all()

# Convert the query results from your precipitation analysis to a dictionary
    prcp_dict = dict(prcp_last_12)   

    dates = []
    for i in prcp_dict:
        dates.append(i)

    return jsonify(dates)

@app.route("//api/v1.0/tobs")
def tobs():
    """Return the most active station data as json"""
    # Calculate the date one year from the last date in data set.
    year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    active_last_12 = session.query(Measurement.date, Measurement.tobs).filter_by(station='USC00519281').filter(Measurement.date >= year_before).all()

    # Convert the query results to a dictionary
    active_dict = dict(active_last_12)

    return jsonify(active_dict)

@app.route("/api/v1.0/<start>")
def sum_by_start_date(start):
    session.close()
    starting_date = dt.datetime.strptime(start, "%m%d%Y")
    sel =  [func.max(Measurement.tobs), func.avg(Measurement.tobs), func.min(Measurement.tobs)]

     
    sum_list = session.query(*sel).filter(Measurement.date >= starting_date).all()
    session.close()
    conv_list = list(np.ravel(sum_list))
    return jsonify(conv_list)

@app.route(f"/api/v1.0/<start>/<end>")
def sum_by_end_date(start, end):
    session.close()
    starting_date = dt.datetime.strptime(start, "%m%d%Y")
    sel =  [func.max(Measurement.tobs), func.avg(Measurement.tobs), func.min(Measurement.tobs)]
    end_date = dt.datetime.strptime(end, "%m%d%Y")

    sum_list = session.query(*sel).filter(Measurement.date >= starting_date).filter(Measurement.date <= end_date).all()
    session.close()
    conv_list = list(np.ravel(sum_list))
    return jsonify(conv_list)
    
if __name__ == "__main__":
    app.run(debug=True)