import json
import random
import spacy
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

class NLPProcessor:
    def __init__(self, intents_path="data/intents.json"):
        self.intents_path = intents_path
        self.responses = {}
        self.vectorizer = CountVectorizer()
        self.model = LogisticRegression(max_iter=1000)
        self.nlp = spacy.load("en_core_web_sm")

        self.load_data()

    def preprocess(self, text):
        # Use spaCy to remove punctuation and lemmatize
        doc = self.nlp(text.lower())
        tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
        return " ".join(tokens)

    def load_data(self):
        with open(self.intents_path, "r") as f:
            intents = json.load(f)

        X = []
        y = []

        for intent in intents["intents"]:
            tag = intent["tag"]
            self.responses[tag] = intent["responses"]
            for pattern in intent["patterns"]:
                X.append(self.preprocess(pattern))
                y.append(tag)

        X_vec = self.vectorizer.fit_transform(X)
        self.model.fit(X_vec, y)

    def predict_intent(self, user_input):
        user_input = self.preprocess(user_input)
        user_vec = self.vectorizer.transform([user_input])
        return self.model.predict(user_vec)[0]

    def get_response(self, user_input):
        tag = self.predict_intent(user_input)
        return random.choice(self.responses.get(tag, ["Sorry, I didn't understand that."]))


if __name__ == "__main__":
    bot = NLPProcessor("data/intents.json")
    while True:
        msg = input("You: ")
        if msg.lower() in ["quit", "exit"]:
            break
        print("Bot:", bot.get_response(msg))
