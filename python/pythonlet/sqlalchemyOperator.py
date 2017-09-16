#!/usr/bin/env Python
# -*- utf-8 -*-

''' to create a table stock in db in memory

    <xml...
        <items>
            <item1 name='aaa' shelf='shelf1' grid='grid1'/>
            <item2 name='222' shelf='shelf1' grid='gridx'/>
            ...
'''
import random

# DB-API: sqlite3
# import sqlite3
# db = sqlite3.connect(':memory:')
# cursor = db.cursor()
# engine = create_engine('sqlite:///./sqlalchemy.db', echo = True)
# metadata = MetaData(engine)
# stock_table = Table('stock', metadata,
#                     0)
# stock_table.create()

# ORM: MySql
from sqlalchemy import Column, String, SMALLINT, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Stock(Base):
    __tablename__ = 'stock'

    id = Column(SMALLINT(), primary_key=True)
    name = Column(String(20))
    shelf = Column(SMALLINT()) 
    grid = Column(SMALLINT()) 

conn_str = r'mysql+mysqldb://root:xxxxxx@localhost:3306/test'
engine = create_engine(conn_str, encoding='utf-8', echo=True)
Base.metadata.create_all(engine)
print('SQLAlchemy db localhost:3306/test is created.')
DBSession = sessionmaker(bind = engine)
session = DBSession()

# hard-code limitation
N = 100
GridNum = 16
# hard-code
stockData = []



# DB-API: sqlite3
def initdb_sqlite3():
    cmd = 'create table stock(id integer primary key, name varchar(10) UNIQUE, shelf integer, grid integer)'
    cursor.execute(cmd)
    db.commit()

def addStockData_sqlite3():
    x, y = random.randrange(0, N), random.randrange(0, N)
    for i in xrange(N):
        id, name, shelf, grid = i, 'item{0}'.format(i), x, y
        # item = Stock(id = i, name = 'item{0}'.format(i), shelf = x, grid = y)
        # session.add(item)
        values = (id, name, shelf, grid)
        cursor.execute('insert into stock values (?,?,?,?)', values)
        db.commit()

    # session.commit()
    print('items data is put into stock.')

def queryStock_sqlite3():
    cursor.execute('select * from stock')
    data = cursor.fetchall()
    # close db connection
    cursor.close()
    db.close()

    print data
    return data



def convertStockDataToJson_sqlite3(data):
    for i, v in enumerate(data):
        stockData.extend([{'id': v[0], 'name': v[1], 'shelf': v[2], 'grid': v[3]}])
    print(stockData)
    return stockData



# ORM: MySql
def addStockData():
    data = []
    for i in xrange(20):
        x, y = random.randrange(0, N), random.randrange(0, N)
        data.append(Stock(name='item{0}'.format(i), shelf=x, grid=y))
    session.add_all(data)
    session.commit()

def queryStock():
    query = session.query(Stock).filter(Stock.shelf == 2)
    data = query.all()
    print('[INFO] data:\n{0}'.format(len(data)))
    return data


def convertStockDataToJson(data):
    for d in data:
        stockData.append({'id': d.id, 'name': d.name, 'shelf': d.shelf, 'grid': d.grid})
    print('[INFO] data in json:\n{0}'.format(stockData))
    return stockData



RestPath = '/warehouse/orderId'
from flask import Flask, jsonify
app = Flask(__name__)
@app.route(RestPath, methods=['GET'])
def get_orderData():
# only for demo of a REST url: in case that db is down.
#    tmpData = [
# only for demo of a REST url: in case that db is down.
#    tmpData = [
#    {'id': 1, 'name': u'item0', 'shelf': 50, 'grid': 22},
#    {'id': 2, 'name': u'item1', 'shelf': 10, 'grid': 20}
#    ]
# jsonData = jsonify({'stock': tmpData})
    jsonData = jsonify({'stock': stockData})
    print(jsonData)
    return jsonData



if __name__ == '__main__':
    # DB-API: sqlite3
    # initdb_sqlite3()
    # addStockData_sqlite3()
    # data = queryStock_sqlite3()
    # convertStockDataToJson_sqlite3(data)

    # ORM: MySql
    # addStockData()
    data = queryStock()
    stockData = convertStockDataToJson(data)
    app.run(debug = True)

