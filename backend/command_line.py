
# See this link for references: https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df
# 1) import needed models
# 2) determine and plan structure
# 3) use conditional structure to return formatted response
# 4) format response

from __future__ import print_function
from db import db
from pyfiglet import figlet_format, Figlet
from PyInquirer import prompt, style_from_dict, Token, prompt
from sqlalchemy import create_engine, inspect

import pandas as pdf
import sys
import os
import logging

sys.path.insert(0, os.path.abspath('..'))

engine = create_engine("sqlite:///data.db")
connection = engine.connect()
metadata = db.MetaData()

f = Figlet(font='slant')


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
           'Exit'
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
        print(f.renderText('Food List'))
        food_list = db.Table('food_list', metadata, autoload=True, autoload_with=engine)
        query = db.select([food_list])
        ResultProxy = connection.execute(query)
        data = ResultProxy.fetchall()
        if len(data) is 0:
            print('There are no {} sir.'.format(answer['resource_selected']))
        else:
            rows_and_columns = create_rows_and_columns(answer['resource_selected'], data)
            for i in range(len(rows_and_columns)):
                df = pdf.DataFrame(rows_and_columns[i], index=[i])
                print(df[columns])

    exit_or_continue = prompt(main_menu_or_exit_prompt)

    if exit_or_continue['exit'] == 'exit':
        print(f.renderText('Thanks for all the Fish...'))
        break
