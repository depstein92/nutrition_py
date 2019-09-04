
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

import sys
import os
import logging

sys.path.insert(0, os.path.abspath('..'))

engine = create_engine("sqlite:///data.db")
connection = engine.connect()
metadata = db.MetaData()

f = Figlet(font='slant')


while exit != 'exit': #infinite loop
    print(f.renderText('Nutrition Command Line'))

    questions = [
        {
         'type' : 'list',
         'name' : 'resource_selected',
         'message' : 'Pick a selection from the folowing resources: ',
         'choices' : [
           'Users',
           'Food',
           'Food_List'
         ]
        }
    ]

    answer = prompt(questions)

    print(answer['resource_selected'])

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

    if answer['resource_selected'] == 'Users':
        print(f.renderText('Users'))
        user = db.Table('user', metadata, autoload=True, autoload_with=engine)
        query = db.select([user])
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
    elif answer['resource_selected'] == 'Food':
        print(f.renderText('Food'))
        food = db.Table('food', metadata, autoload=True, autoload_with=engine)
        query = db.select([food])
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        print(ResultSet[:3])
    elif answer['resource_selected'] == 'Food_List':
        print('Food List Selected')
        print(f.renderText('Food List'))
        food_list = db.Table('food_list', metadata, autoload=True, autoload_with=engine)
        query = db.select([food_list])
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        print(ResultSet[:3])
    else:
        print('Not a viable selection')

    exit_or_continue = prompt(main_menu_or_exit_prompt)

    if exit_or_continue['exit'] == 'exit':
        print(f.renderText('Thanks for all the Fish...'))
        break
