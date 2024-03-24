from App.models import Entry
from App.database import db

def create_entry(headword, pronunciation):
    new_entry = Entry(headword, pronunciation)
    db.session.add(new_entry)
    db.session.commit()
    return new_entry

def get_entry(word):
    return Entry.query.filter_by(headword=word).first()

def headword_exists_in_list(master, headword):
    return binary_search(master, headword)

def binary_search(word_list: list, word: str):
    low = 0
    high = len(word_list) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_word = word_list[mid]

        # Last word in word list is alphabetically before the target word
        if word_list[high] < word: return False
        if mid_word == word: return True
        elif word < mid_word: high = mid - 1
        else: low = mid + 1

    return False