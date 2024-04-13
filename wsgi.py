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
    ipa_map = load(open("ipa-map.json", "r", encoding="utf-8"))
    with open("DTTEC_FULL.json", "r", encoding="utf-8") as f:
        for entry in load(f): 
            headword      = str(entry['headword'].split(" ")[0]).lower().strip()
            pronunciation = entry['pronunciation'][0] if entry['pronunciation'] else None
            h_len         = len(headword)
            
            # Check headword length. Skip if too long, shorter than 4 chars, is a number or already added
            if  headword == '' or \
                headword is None or \
                len(headword) > 20 or \
                len(headword) < 4: continue
            
            if headword in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']: continue
            if headword == last_headword or headword in word_list: continue
            last_headword = headword
            
            # Check pronunciation length. Skip if longer than headword (+5) or is empty
            if  type(pronunciation) == str and pronunciation == '' or \
                pronunciation is None or \
                1 > len(pronunciation) > (h_len + 5): continue
                
            # Convert any of the detected incorrect IPA symbols to the correct one
            for k, v in ipa_map.items():
                if k in pronunciation:
                    pronunciation = pronunciation.replace(k, v)  
            
            # Show entry being added
            print(f"\r[{len(word_list) + 1}] {headword} : {pronunciation}", end=" " * 20)
            create_entry(headword, pronunciation)
            word_list.append(headword)
            
            # Add alternate spellings as well
            for alternate in entry['alternate_spelling']:
                alternate = str(alternate).lower().strip()
                
                # Enforce same rules for alternate spellings as for headwords
                if  alternate == '' or \
                    alternate is None or \
                    len(alternate) > 20 or \
                    len(alternate) < 4: continue
                
                create_entry(alternate, pronunciation)
                print(f"\r[{len(word_list) + 1}] {headword} : {pronunciation}", end=" " * 20)
                word_list.append(alternate)
            
    print('\nDatabase intialised')