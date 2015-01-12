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
    operation_company = railway_db.get_operation_company()
    return template('railway', operation_company=operation_company).replace('\n', '');

@app.get('/json/get_railway_line')
def getRailwayLine():
    operation_company = request.query.operation_company
    railways = railway_db.get_railway_line(operation_company)
    return json.dumps(railways)


@app.get('/json/get_railway_curve')
def getRailwayCurve():
    res = {'data' : None, 'result':0, 'error': ''}
    railway = request.query.railway
    operation_company = request.query.operation_company
    railroad_curve = railway_db.get_railroad_curve(railway_line=railway, operation_company=operation_company)
    station = railway_db.get_station_list(railway_line=railway, operation_company=operation_company)
    response.content_type = 'application/json;charset=utf-8'
    res['railroad_curve'] = railroad_curve
    res['station'] = station
    
    return json.dumps(res)
