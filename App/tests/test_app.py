import pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
from App.models import Entry
from App.controllers import ( create_entry, get_entry )


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class EntryUnitTests(unittest.TestCase):
    
    entry: Entry = Entry("word", "pronunciation")

    def test_new_entry(self):
        assert self.entry.headword == "word"

    def test_get_json(self):
        entry_json = self.entry.get_json()
        self.assertDictEqual(entry_json, {"id":1, "headword":"word", "pronunciation":"pronunciation"})

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class EntryIntegrationTests(unittest.TestCase):
    
    headword = "word"
    pronunciation = "pronunciation"

    def test_create_user(self):
        entry = create_entry(self.headword, self.pronunciation)
        assert entry.headword == self.headword

    def test_headword_exists(self):
        assert get_entry(self.headword).headword == self.headword
        assert get_entry("test") == None