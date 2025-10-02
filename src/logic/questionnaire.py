#this should be a class as it represents a entity that doesnt neccesarily change
#supporting funcitons but mainly class
# Implement answer validation to the questions here: to encapsulate logic , better for when we implement the chatbot
#could look like:
'''
logic/questionnaire.py

Class: Questionnaire

Methods:

get_questions() (returns list of Qs).

evaluate_answers(answers) (basic scoring).
'''


class Questionnaire:
    def __init__(self):
        self.questions = [
            {
                "key": "Erfaring",
                "text": "Hvilket treningsnivå befinner du deg på?",
                "type": "radio",
                "options": ["Nybegynner", "Viderekommen", "Erfaren", "Profesjonell"],
                "default": "Nybegynner"
            },
            {
                "key": "Mål",
                "text": "Hvilket mål ønsker du å oppnå ved hjelp av treningen?",
                "type": "radio",
                "options": ["Komme i bedre form", "Bedre livsstil", "Øke utholdenheten", "Bli sterkere", "Redusere vekten"],
                "default": "Komme i bedre form"
            },
            {
                "key": "Preferanse",
                "text": "Hvilken type trening foretrekker du?",
                "type": "radio",
                "options": ["Styrketrening", "Løping", "Sykling", "Svømming", "Variert"],
                "default": "Styrketrening"
            },
            {
                "key": "Antall",
                "text": "Hvor mange økter ønsker du i løpet av uken?",
                "type": "radio",
                "options": ["1-2", "3-4", "5-7"],
                "default": "1-2"
            },
            {
                "key": "Varighet",
                "text": "Hvor lenge ønsker du at en økt varer?",
                "type": "entry",
                "default": "90"
            }
        ]

    def get_questions(self):
        return self.questions
