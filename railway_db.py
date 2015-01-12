# -*- coding: utf-8 -*-
import sqlite3
import sys
import os
# easy_install lxml==3.4.1
from lxml import etree
from peewee import *

database_proxy = Proxy()
database = None


class BaseModel(Model):
    """
    モデルクラスのベース
    """
    class Meta:
        database = database_proxy


class Curve(BaseModel):
    """
    曲線情報モデル
    """
    curve_id = CharField(index=True, unique=False)
    lat = DoubleField()
    lng = DoubleField()


class RailRoadSection(BaseModel):
    """
    鉄道区間情報モデル
    """
    gml_id = CharField(primary_key=True)
    # 外部キーは主キーまたは一意制約をもっていないといけないので、
    # 複数あるデータに関しては外部キーとしては指定できない。
    location = CharField(index=True)
    railway_type = IntegerField()
    service_provider_type = IntegerField()
    railway_line_name = CharField(index=True)
    operation_company = CharField(index=True)


class Station(BaseModel):
    """
    駅情報モデル
    """
    gml_id = CharField(primary_key=True)
    # 外部キーは主キーまたは一意制約をもっていないといけないので、
    # 複数あるデータに関しては外部キーとしては指定できない。
    location = CharField(index=True)
    railway_type = IntegerField()
    service_provider_type = IntegerField()
    railway_line_name = CharField(index=True)
    operation_company = CharField(index=True)
    station_name = CharField(index=True)
    railroad_section = ForeignKeyField(
        db_column='railroad_section_id',
        rel_model=RailRoadSection,
        to_field='gml_id',
        index=True
    )


def setup(path):
    """
    データベースのセットアップ
    @param path データベースのパス
    """
    global database
    database = SqliteDatabase(path)
    database_proxy.initialize(database)
    database.create_tables([Curve, RailRoadSection, Station], True)


def import_railway(xml):
    """
    国土数値院のN02-XX.xmlから路線と駅情報をインポートする
    TODO:
      外部キーがらみのインポートの効率がわるい
    @param xml XMLのパス
    """
    commit_cnt = 2000  # ここで指定した数毎INSERTする
    f = None
    contents = None
    namespaces = {
        'ksj': 'http://nlftp.mlit.go.jp/ksj/schemas/ksj-app',
        'gml': 'http://www.opengis.net/gml/3.2',
        'xlink': 'http://www.w3.org/1999/xlink',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    with database.transaction():
        insert_buff = []
        context = etree.iterparse(
            xml,
            events=('end',),
            tag='{http://www.opengis.net/gml/3.2}Curve',
            recover=True
        )
        for event, curve in context:
            curveId = curve.get('{http://www.opengis.net/gml/3.2}id')
            print (curveId)
            posLists = curve.xpath('.//gml:posList', namespaces=namespaces)
            for posList in posLists:
                points = posList.text.split("\n")
                for point in points:
                    pt = point.strip().split(' ')
                    if len(pt) != 2:
                        continue
                    insert_buff.append({
                        'curve_id': curveId,
                        'lat': float(pt[0]),
                        'lng': float(pt[1])
                    })
                    if len(insert_buff) >= commit_cnt:
                        Curve.insert_many(insert_buff).execute()
                        insert_buff = []
        if len(insert_buff):
            Curve.insert_many(insert_buff).execute()
        insert_buff = []
        context = etree.iterparse(
            xml,
            events=('end',),
            tag='{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}RailroadSection',
            recover=True
        )
        for event, railroad in context:
            railroadSectionId = railroad.get(
                '{http://www.opengis.net/gml/3.2}id'
            )
            locationId = railroad.find(
                'ksj:location',
                namespaces=namespaces
            ).get('{http://www.w3.org/1999/xlink}href')[1:]
            railwayType = railroad.find(
                'ksj:railwayType', namespaces=namespaces
            ).text
            serviceProviderType = railroad.find(
                'ksj:serviceProviderType',
                namespaces=namespaces
            ).text
            railwayLineName = railroad.find(
                'ksj:railwayLineName',
                namespaces=namespaces
            ).text
            operationCompany = railroad.find(
                'ksj:operationCompany',
                namespaces=namespaces
            ).text
            insert_buff.append({
                'gml_id': railroadSectionId,
                'location': locationId,
                'railway_type': railwayType,
                'service_provider_type': serviceProviderType,
                'railway_line_name': railwayLineName,
                'operation_company': operationCompany
            })
            print (railroadSectionId)
            if len(insert_buff) >= commit_cnt:
                RailRoadSection.insert_many(insert_buff).execute()
                insert_buff = []
        if len(insert_buff):
            RailRoadSection.insert_many(insert_buff).execute()

        insert_buff = []
        context = etree.iterparse(
            xml,
            events=('end',),
            tag='{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}Station',
            recover=True
        )
        for event, railroad in context:
            stationId = railroad.get('{http://www.opengis.net/gml/3.2}id')
            locationId = railroad.find(
                'ksj:location', namespaces=namespaces
            ).get('{http://www.w3.org/1999/xlink}href')[1:]
            railwayType = railroad.find(
                'ksj:railwayType',
                namespaces=namespaces
            ).text
            serviceProviderType = railroad.find(
                'ksj:serviceProviderType',
                namespaces=namespaces
            ).text
            railwayLineName = railroad.find(
                'ksj:railwayLineName',
                namespaces=namespaces
            ).text
            operationCompany = railroad.find(
                'ksj:operationCompany',
                namespaces=namespaces
            ).text
            stationName = railroad.find(
                'ksj:stationName',
                namespaces=namespaces
            ).text
            railroadSection = railroad.find(
                'ksj:railroadSection',
                namespaces=namespaces
            ).get('{http://www.w3.org/1999/xlink}href')[1:]
            print (stationId)
            insert_buff.append({
                'gml_id': stationId,
                'location': locationId,
                'railway_type': railwayType,
                'service_provider_type': serviceProviderType,
                'railway_line_name': railwayLineName,
                'operation_company': operationCompany,
                'station_name': stationName,
                'railroad_section': RailRoadSection.get(
                    RailRoadSection.gml_id == railroadSection
                )
            })
            if len(insert_buff) >= commit_cnt:
                Station.insert_many(insert_buff).execute()
                insert_buff = []
        if len(insert_buff):
            Station.insert_many(insert_buff).execute()


def get_railway_line():
    ret = []
    rows = Station.select(fn.Distinct(Station.railway_line_name))
    for r in rows:
        ret.append(r.railway_line_name)
    return ret


def get_operation_company():
    ret = []
    rows = Station.select(fn.Distinct(Station.operation_company))
    for r in rows:
        ret.append(r.operation_company)
    return ret


def get_station_list(operation_company=None, railway_line=None):
    ret = {}
    query = Curve.select(
        Curve,
        Station,
        RailRoadSection
    ).join(
        Station,
        JOIN_LEFT_OUTER,
        on=(Curve.curve_id == Station.location).alias('station')
    ).join(
        RailRoadSection,
        JOIN_INNER,
        on=(RailRoadSection.gml_id == Station.railroad_section).alias('railroadsection')
    )
    cond = None
    if railway_line:
        cond = (Station.railway_line_name == railway_line)
    if operation_company:
        if cond:
            cond = cond & (Station.operation_company == operation_company)
        else:
            cond = (Station.operation_company == operation_company)
    rows = query.where(cond)
    for r in rows: # ここでSQLを発行する
        if not r.station.gml_id in ret:
            ret[r.station.gml_id] = {}
            ret[r.station.gml_id]['name'] = r.station.station_name
            ret[r.station.gml_id]['railroad_section'] = r.station.railroadsection.gml_id
            ret[r.station.gml_id]['curve'] = []
        ret[r.station.gml_id]['curve'].append((r.lat, r.lng))
    return ret


def get_railroad_curve(operation_company=None, railway_line=None):
    ret = {}
    query = Curve.select(
        Curve,
        RailRoadSection
    ).join(
        RailRoadSection,
        JOIN_LEFT_OUTER,
        on=(Curve.curve_id == RailRoadSection.location).alias('railroadsection')
    )
    cond = None
    if railway_line:
        cond = (RailRoadSection.railway_line_name == railway_line)
    if operation_company:
        if cond:
            cond = cond & (RailRoadSection.operation_company == operation_company)
        else:
            cond = (RailRoadSection.operation_company == operation_company)
    rows = query.where(cond)
    for r in rows: # ここでSQLを発行する
        if not r.railroadsection.gml_id in ret:
            ret[r.railroadsection.gml_id] = []
        ret[r.railroadsection.gml_id].append((r.lat, r.lng))
    return ret
