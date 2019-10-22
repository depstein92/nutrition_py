
from __future__ import print_function
from db import db
from pyfiglet import figlet_format, Figlet
from PyInquirer import prompt, style_from_dict, Token, prompt
from sqlalchemy import *


from models.food import Food
from models.food_list import Food_List_Model
from models.user import UserModel


import pandas as pdf
import sys
import os
import logging
import requests
import asyncio

sys.path.insert(0, os.path.abspath('..'))

engine = create_engine("sqlite:///data.db")
connection = engine.connect()
metadata = MetaData()

f = Figlet(font='slant')

#
# celery_app = Celery('test_celery',
#              broker='amqp://dan:dan@localhost/dan_vhost',
#              backend='rpc://',
#              include=['test_celery.tasks'])

def reset_table(model_name, table_name):
    if not engine.dialect.has_table(engine, table_name):
       model_name.__table__.create(engine)
    else:
       model_name.__table__.drop(engine)


# @celery_app.task
# def fetch_sample_data():
#     fda_data = response.get('https://api.nal.usda.gov/ndb/V2/reports?ndbno=01009&ndbno=01009&ndbno=45202763&ndbno=35193&type=b&format=json&api_key=DEMO_KEY')
#     # user_data = response.get('')
#     food_list = ['obj', 'obj', 'obj']
#     print(' this is FDA DATA: {}'.format(fda_data))
#     # print(' this is USER DATA: {}'.format(user_data))



while 1: #infinite loop
    questions = [
        {
         'type' : 'list',
         'name' : 'resource_selected',
         'message' : 'Pick a selection from the folowing resources: ',
         'choices' : [
           'Users',
           'Food',
           'Food_List',
           'Reset Database',
           'Seed Database',
           'Exit',
         ]
        }
    ]

    main_menu_or_exit_prompt = [
      {
       'type' : 'list',
       'name' : 'exit',
       'message' : 'Pick a selection from the folowing resources: ',
       'choices' : [
         'exit',
         'continue'
       ]
      }
    ]

    table_to_drop_menu = [
       {
        'type' : 'list',
        'name' : 'table',
        'message' : 'Pick a table to reset.',
        'choices' : [
          'Foods',
          'Users',
          'Food Lists'
        ]
       }
    ]

    print(f.renderText('Nutrition Command Line'))

    answer = prompt(questions)

    if answer['resource_selected'] == 'Exit':
        print(f.renderText('Thanks for all the Fish...'))
        break

    def convert_to_dict(columns, rows):
        arr = []
        i = 0
        for row in rows:
          map = {}
          for r in row:
            if i == len(row) - 1:
              i = 0
              arr.append(map)
            map['{}'.format(columns[i])] = row[i]
            i += 1
        return arr

    def create_rows_and_columns(resource, *args):
        if resource == 'User':
            columns = ['username', 'password', 'id']
            return convert_to_dict(columns, *args)
        elif resource == 'Food':
            columns = [
            'type', 'sr', 'ndbno', 'name',
            'sd', 'fg', 'ds', 'food_list_id'
            ]
            # rows_and_columns = create_rows_and_columns(data, answer['resource_selected'])
            return convert_to_dict(columns, *args)
        elif resource == 'Food_List':
            columns = ['id', 'name', 'food']
            return convert_to_dict(columns, *args)
        else:
            raise AttributeError(f'{resource} is not a known resource')

    if answer['resource_selected'] == 'Users':
        print(f.renderText('Users'))
        if not engine.dialect.has_table(engine, 'user'):
            print(' There is no table {}, '.format(answer['resource_selected']))
        else:
            user = db.Table('user', metadata, autoload=True, autoload_with=engine)
            query = db.select([user])
            ResultProxy = connection.execute(query)
            data = ResultProxy.fetchall()
            if len(data) is 0:
               print('There are no {} sir.'.format(answer['resource_selected']))
            else:
               columns = ['type', 'sr', 'ndbno', 'name','sd', 'fg', 'ds', 'food_list_id']
               rows_and_columns = create_rows_and_columns(answer['resource_selected'], data)
               for i in range(len(rows_and_columns)):
                   df = pdf.DataFrame(rows_and_columns[i], index=[i])
                   print(df[columns])
    elif answer['resource_selected'] == 'Food':
        print(f.renderText('Food'))
        if not engine.dialect.has_table(engine, 'food'):
            print(' There is no table {}, '.format(answer['resource_selected']))
        else:
            food = db.Table('food', metadata, autoload=True, autoload_with=engine)
            query = db.select([food])
            ResultProxy = connection.execute(query)
            data = ResultProxy.fetchall()
            if len(data) is 0:
               print('There are no {} sir.'.format(answer['resource_selected']))
            else:
               columns = ['type', 'sr', 'ndbno', 'name', 'sd', 'fg', 'ds', 'food_list_id']
               rows_and_columns = create_rows_and_columns(answer['resource_selected'], data)
               for i in range(len(rows_and_columns)):
                   df = pdf.DataFrame(rows_and_columns[i], index=[i])
                   print(df[columns])
    elif answer['resource_selected'] == 'Food_List':
        print('Food List Selected')
        if not engine.dialect.has_table(engine, 'food_list'):
            print(' There is no table {}, '.format(answer['resource_selected']))
        else:
            print(f.renderText('Food List'))
            food_list = db.Table('food_list', metadata, autoload=True, autoload_with=engine)
            query = db.select([food_list])
            ResultProxy = connection.execute(query)
            data = ResultProxy.fetchall()
            if len(data) is 0:
                print('There are no {} sir.'.format(answer['resource_selected']))
            else:
                columns = ['id', 'name']
                rows_and_columns = create_rows_and_columns(answer['resource_selected'], data)
                for i in range(len(rows_and_columns)):
                    df = pdf.DataFrame(rows_and_columns[i], index=[i])
                    print(df[columns])
    elif answer['resource_selected'] == 'Reset Database':

        table_to_drop_answer = prompt(table_to_drop_menu)

        if table_to_drop_answer['table'] == 'Foods':
            if not engine.dialect.has_table(engine, 'food'):
               Food.__table__.create(bind=engine)
               print('Food table has been created')
            else:
               Food.__table__.drop(bind=engine)
               print('Food table has been dropped')
        elif table_to_drop_answer['table'] == 'Food Lists':
            if not engine.dialect.has_table(engine, 'food_list'):
               Food_List_Model.__table__.create(bind=engine)
               print('Food List table has been created')
            else:
               Food_List_Model.__table__.drop(bind=engine)
               print('Food List table has been dropped')
        elif table_to_drop_answer['table'] == 'Users':
            if engine.dialect.has_table(engine, 'user'):
               UserModel.__table__.drop(bind=engine)
               print('User table has been dropped')
            else:
               UserModel.__table__.create(bind=engine)
               print('User table has been created')
    #elif answer['resource_selected'] == 'Reset Database':



    exit_or_continue = prompt(main_menu_or_exit_prompt)



    if exit_or_continue['exit'] == 'exit':
        print(f.renderText('Thanks for all the Fish...'))
        break
