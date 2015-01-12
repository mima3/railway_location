# coding=utf-8
from bottle import get, post, template, request, Bottle, response, redirect, abort
from json import dumps
import os
import json
from collections import defaultdict
import time
import cgi
import urllib
import railway_db
import peewee


app = Bottle()


def setup(conf):
    global app
    railway_db.setup(conf.get('database', 'path'))


@app.get('/railway')
def homePage():
    railways = railway_db.get_railway_line()
    return template('railway', railways=railways).replace('\n', '');


@app.get('/json/get_railway_curve')
def getRailwayCurve():
    res = {'data' : None, 'result':0, 'error': ''}
    railway = request.query.railway
    railroad_curve = railway_db.get_railroad_curve(railway_line=railway)
    station = railway_db.get_station_list(railway_line=railway)
    response.content_type = 'application/json;charset=utf-8'
    res['railroad_curve'] = railroad_curve
    res['station'] = station
    
    return json.dumps(res)
