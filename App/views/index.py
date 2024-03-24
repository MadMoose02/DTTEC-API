from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
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
            if headword_exists(word_list, headword): continue
            last_headword = headword
            pronunciation = entry['pronunciation']
            if pronunciation == '' or pronunciation is None or len(pronunciation) < 1: continue
            if len(pronunciation) > len(headword) + 5: continue
            pronunciation = pronunciation[0]
            print(f"\r[{len(word_list) + 1}] {entry['headword']} : {pronunciation}", end=" " * 20)
            create_entry(entry['headword'], pronunciation)
            word_list.append(headword)
            
    return jsonify(message='Databse initialised')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})