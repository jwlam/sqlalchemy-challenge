import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)


@app.route('/')
def home():
    '''List of available api routes.'''
    return(
        f'Precipitation: /api/v1.0/precipitation<br/>'
        f'List of Stations: /api/v1.0/stations<br/>'
        f'Temperatures for one year: /api/v1.0/tobs<br/>'
        f'Temperatures from the start date(yyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>'
        f'Temperatures from start to end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    qr = session.query(measurement.date, measurement.prcp).all()
    session.close()

    prcp_all = []
    for date, prcp in qr:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_all.append(prcp_dict)

    return jsonify(prcp_all)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    qr = session.query(station.station, station.name).all()
    session.close()

    station_all = []
    for station, name in qr:
        station_dict = {}
        station_dict[station] = name
        station_all.append(station_dict)

    return jsonify(station_all)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    lastyear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    qr = session.query(measurement.tobs, measurement.date).filter(measurement.date >= lastyear).all()
    session.close()

    tobs_all = []
    for tobs, date in qr:
        tobs_dict = {}
        tobs_dict[tobs] = date
        tobs_all.append(tobs_dict)

    return jsonify(tobs_all)

@app.route('/api/v1.0/<start>')
def start(start):
    session = Sesson(engine)
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    qr = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_dt).all()
    session.close()

    temp_all = []
    for min, avg, max in qr:
        temp_dict = {}
        temp_dict['min'] = min
        temp_dict['average'] = avg
        temp_dict['max'] = max
        temp_all.append(temp_dict)

    return jsonify(temp_all)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    session = Session(engine)
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    end_dt = dt.datetime.strptime(end, '%Y-%m-%d')
    qr = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_dt).filter(measurement.date <= end_dt)
    session.close()

    temp_all = []
    for min, avg, max in qr:
        temp_dict = {}
        temp_dict['min'] = min
        temp_dict['average'] = avg
        temp_dict['max'] = max
        temp_all.append(temp_dict)

    return jsonify(temp_all)

if __name__ == '__main__':
    app.run(debug=True)







