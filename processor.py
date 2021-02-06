import re
import nltk
import operator
from db import db
from models import Result
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup

class Processor:

    def __init__(self, url, r):
        self.url = url
        self.r = r
        self.errors = []
        self.results = {}

    def process(self):
        raw = BeautifulSoup(self.r.text, 'html.parser').get_text()
        nltk.data.path.append('./nltk_data/') # set the path
        tokens = nltk.word_tokenize(raw)
        text = nltk.Text(tokens)
        # remove punctuation, count raw words
        nonPunct = re.compile('.*[A-Za-z].*')
        raw_words = [w for w in text if nonPunct.match(w)]
        raw_word_count = Counter(raw_words)
        #stop words
        non_stop_words = [w for w in raw_words if w.lower() not in stops]
        non_stop_words_count = Counter(non_stop_words)
        self.results = sorted(
            non_stop_words_count.items(),
            key=operator.itemgetter(1),
            reverse=True
        ) # add [:10] to limit to first 10
        try:
            result = Result(
                url=self.url,
                result_all=raw_word_count,
                result_no_stop_words=non_stop_words_count
            )
            db.session.add(result)
            db.session.commit()
        except Exception as error:
            print("Unable to add item to database.", error)
            self.errors.append("Unable to add item to database.")
        return {"errors": self.errors, "results": self.results}
