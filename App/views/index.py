from json import load
from flask import Blueprint, jsonify
from App.models import db, Entry
from App.controllers import create_entry, get_entry, headword_exists_in_list

index_views = Blueprint('index_views', __name__, template_folder='../templates')
word_list = []

@index_views.route('/', methods=['GET'])
def index_page():
    return jsonify(message="Dictionary for English/Creole of Trinidad and Tobago", status=200)

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    word_list = []
    last_headword = ""
    ipa_map = load(open("ipa-map.json", "r", encoding="utf-8"))
    with open("DTTEC_FULL.json", "r", encoding="utf-8") as f:
        for entry in load(f): 
            headword      = str(entry['headword'].split(" ")[0]).lower()
            pronunciation = entry['pronunciation'][0] if entry['pronunciation'] else None
            h_len         = len(headword)
            
            # Check headword length. Skip if too long, shorter than 4 chars, is a number or already added
            if  headword == '' or \
                headword is None or \
                4 > len(headword) > 20: continue
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
            create_entry(str(headword).lower(), pronunciation)
            word_list.append(headword)
            
            # Add alternate spellings as well
            for alternate in entry['alternate_spelling']:
                create_entry(str(alternate).lower(), pronunciation)
                print(f"\r[{len(word_list) + 1}] {headword} : {pronunciation}", end=" " * 20)
                word_list.append(alternate)
            
    print('\nDatabase intialised')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify(status="OK", message="The server is up and running", code=200)

@index_views.route('/get-pronunciation/<string:word>', methods=['GET'])
def get_pronunciation(word: str):
    result: Entry = get_entry(word)
    pronunciation = result.pronunciation if result else None
    status = "OK" if result else "Not Found"
    return jsonify(headword=word, pronunciation=pronunciation, status=status)