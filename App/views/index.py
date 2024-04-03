from json import load
from flask import Blueprint, jsonify
from App.models import db
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
    with open("DTTEC_FULL.json", "r", encoding="utf-8") as f:
        for entry in load(f): 
            headword = entry['headword'].split(" ")[0]
            if len(headword) > 20: continue
            if headword == '' or headword is None or len(headword) < 1: continue
            if headword in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']: continue
            if headword == last_headword: continue
            if headword_exists_in_list(word_list, headword): continue
            last_headword = headword
            pronunciation = entry['pronunciation']
            if pronunciation == '' or pronunciation is None or len(pronunciation) < 1: continue
            if len(pronunciation) > len(headword) + 5: continue
            pronunciation = pronunciation[0]
            print(f"\r[{len(word_list) + 1}] {headword} : {pronunciation}", end=" " * 20)
            create_entry(str(headword).lower(), pronunciation)
            word_list.append(headword)
            
    return jsonify(message='Databse initialised')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify(status="OK", message="The server is up and running", code=200)

@index_views.route('/get-pronunciation/<string:word>', methods=['GET'])
def get_pronunciation(word: str):
    result = get_entry(word)
    pronunciation = result.pronunciation if result else None
    status = "OK" if result else "Not Found"
    return jsonify(headword=word, pronunciation=pronunciation, status=status)