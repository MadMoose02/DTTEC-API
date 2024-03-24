from json import load
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_entry, headword_exists_in_list )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    word_list = []
    last_headword = ""
    with open("DTTEC_FULL.json", "r", encoding="utf-8") as f:
        for entry in load(f): 
            headword = entry['headword'].split(" ")[0]
            if headword == '' or headword is None or len(headword) < 1: continue
            if headword in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']: continue
            if headword == last_headword: continue
            if headword_exists_in_list(word_list, headword): continue
            last_headword = headword
            pronunciation = entry['pronunciation']
            if pronunciation == '' or pronunciation is None or len(pronunciation) < 1: continue
            if len(pronunciation) > len(headword) + 5: continue
            pronunciation = pronunciation[0]
            print(f"\r[{len(word_list) + 1}] {entry['headword']} : {pronunciation}", end=" " * 20)
            create_entry(entry['headword'], pronunciation)
            word_list.append(headword)
            
    print('\nDatabase intialised')