import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app=Flask(__name__)


@app.route("/")
def home():
    print("Server received a request")
    return (
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/start-end"
            
         )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    prcp_year = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>='2016-08-23').all()
    session.close()
    
    prcp_query = list(np.ravel(prcp_year))
    return jsonify(prcp_query)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    stations=session.query(Station.station, Station.name, func.count(Measurement.date)).\
    filter(Station.station == Measurement.station).\
    group_by(Station.name).\
    order_by(func.count(Measurement.date).desc()).all()
    session.close()
    
    station_query = list(np.ravel(stations))
    return jsonify(station_query)



@app.route("/api/v1.0/tobs")
def tobs():

    station_id = 'USC00519281'
    session = Session(engine)
    temp_year=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>='2016-08-23').\
    filter(Measurement.station == station_id).all()
    session.close()
    
    tobs_query = list(np.ravel(temp_year))
    return jsonify(tobs_query)


@app.route("/api/v1.0/<start>")
def start_date(start):

    station_id = 'USC00519281'
    session = Session(engine)
    starting_date = start
    
    highest=session.query(Measurement.station,func.max(Measurement.tobs)).\
    filter(Measurement.station == station_id).\
    filter(Measurement.date >= starting_date).\
    group_by(Measurement.station).first()

    lowest=session.query(Measurement.station,func.min(Measurement.tobs)).\
    filter(Measurement.station == station_id).\
    filter(Measurement.date >= starting_date).\
    group_by(Measurement.station).first()

    average=session.query(Measurement.station,func.avg(Measurement.tobs)).\
    filter(Measurement.station == station_id).\
    filter(Measurement.date >= starting_date).\
    group_by(Measurement.station).first()


    session.close()

    temp_dict = {"Max": highest, "Min": lowest, "Avg": average}
    return jsonify(temp_dict)



if __name__ == '__main__':
    app.run(debug=True)
