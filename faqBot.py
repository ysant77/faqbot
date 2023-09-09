#!/usr/bin/env python



from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot.conversation import Statement
from chatterbot.response_selection import get_first_response
from chatterbot.comparisons import JaccardSimilarity
import pandas as pd



learning_bot = ChatBot('FAQ Bot', storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3', logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": JaccardSimilarity,
            "response_selection_method": get_first_response
        }
    ])
#trainer = ListTrainer(learning_bot)

trainer = ChatterBotCorpusTrainer(learning_bot)

trainer.train("chatterbot.corpus.english")
list_trainer = ListTrainer(learning_bot)
learning_bot.storage.create_database()

#code to get user feedback, would continuously ask until user either enters good or bad
def process_user_feedback():
    user_feedback = input()
    user_feedback = user_feedback.lower()
    if user_feedback == "good":
        return True
    elif user_feedback == "bad":
        return False
    else:
        print("Please enter good/bad")
        process_user_feedback()
        
while True:
    
    print('Enter exit to stop')
    input_statement = Statement(text=input())
    if input_statement.text == 'exit':
        break
    
    response = learning_bot.get_response(input_statement)
    print("(A) : {}".format(response.text))
    print("\nAre you satisified with the above response? Please enter good/bad \n")


    if process_user_feedback() is False:
        print("Please enter the correct response")
        correct_response = Statement(text=input())
        list_trainer.train([input_statement.text, correct_response.text])

        print("Response added to bot")
    else:
        learning_bot.learn_response(response, input_statement)
        list_trainer.train([input_statement.text, response.text])

