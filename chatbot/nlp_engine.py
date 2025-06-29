import json
import random
import numpy as np
import nltk
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

nltk.download('punkt')

class NLPProcessor:
    def __init__(self, intents_path):
        self.intents_path = intents_path
        self.model = None
        self.vectorizer = None
        self.tags = []
        self.load_data()

    def preprocess(self, text):
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        return text

    def load_data(self):
        with open(self.intents_path, 'r') as f:
            intents = json.load(f)

        self.X = []
        self.y = []
        self.responses = {}

        for intent in intents["intents"]:
            tag = intent["tag"]
            self.tags.append(tag)
            self.responses[tag] = intent["responses"]
            for pattern in intent["patterns"]:
                self.X.append(self.preprocess(pattern))
                self.y.append(tag)

        self.model = make_pipeline(CountVectorizer(), MultinomialNB())
        self.model.fit(self.X, self.y)

    def predict_intent(self, user_input):
        user_input = self.preprocess(user_input)
        return self.model.predict([user_input])[0]

    def get_response(self, user_input):
        intent = self.predict_intent(user_input)
        return random.choice(self.responses[intent])
    

    
if __name__ == "__main__":
    bot = NLPProcessor("data/intents.json")
    while True:
        msg = input("You: ")
        if msg.lower() in ["quit", "exit"]:
            break
        print("Bot:", bot.get_response(msg))
