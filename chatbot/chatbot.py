import random
from chatbot.nlp_engine import NLPProcessor
from finance.api_handler import get_mutual_fund_nav,get_stock_price, get_gold_price, calculate_sip, calculate_fd

class ChatBot:
    def __init__(self, intents_path="data/intents.json"):
        # Initialize the NLP processor with intents configuration
        self.nlp = NLPProcessor(intents_path)

    def get_response(self, user_input: str) -> str:
        """
        Process user input, determine intent, and return the appropriate response.
        """
        # Predict the intent tag from user input
        intent = self.nlp.predict_intent(user_input)

        # Route to the appropriate handler based on intent
        if intent == "stock_price":
            return get_stock_price(user_input)
        elif intent == "gold_price":
            return get_gold_price()
        elif intent == "sip_calculator":
            return calculate_sip(user_input)
        elif intent == "fd_calculator":
            return calculate_fd(user_input)
        elif intent == "mutual_fund_nav":
            return get_mutual_fund_nav(user_input)

        # Fallback to default NLP-based response
        return self.nlp.get_response(user_input)
