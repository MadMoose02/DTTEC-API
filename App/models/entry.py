from App.database import db
from sqlalchemy import Column, String, Integer

class Entry(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    headword =  Column(String(20), nullable=False)
    pronunciation = Column(String(25), nullable=False)

    def __init__(self, headword, pronunciation):
        self.headword = headword
        self.pronunciation = pronunciation

    def get_json(self):
        return {
            'id': self.id,
            'headword': self.headword,
            'pronunciation': self.pronunciation
        }