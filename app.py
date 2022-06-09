import numpy as np
import datetime as dt
import sqlalchemy
from pandocfilters import Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, session

# Database Setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    session.close()
    precip = {date: prcp for date, prcp in results}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    station = list(np.ravel(results))
    return jsonify(station)


@app.route("/api/v1.0/temperature")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= prev_year).all()
    tobs = list(np.ravel(results))
    return jsonify(tobs)


@app.route("/api/v1.0/temp/<start>")
def stats(start):
    return start


@app.route("/api/v1.0/temp/<start>/<end>")
def window(start, end):
    sel = [func.min(Table.col), func.avg(Table.col), func.max(Table.col)]
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    site = list(np.ravel(results))
    return jsonify(tobs)


if __name__ == '__main__':
    app.run();