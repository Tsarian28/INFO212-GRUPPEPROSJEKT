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


from utils.helpers import validate_answers

class Questionnaire:
    """
    A class to represent the questionnaire for collecting user input.
    Encapsulates logic for retrieving questions and validating answers.
    """

    def __init__(self):
        """
        Initialize the Questionnaire with predefined questions.
        """
        self.questions = [
            {"question": "What is your fitness goal?", "key": "goal"},
            {"question": "How long should each session be (in minutes)?", "key": "duration"},
            {"question": "How many times per week do you want to train?", "key": "frequency"}
        ]

    def get_questions(self):
        """
        Retrieve the list of questions.

        Returns:
            list: A list of questions for the user.
        """
        return self.questions

    def validate_answers(self, answers):
        """
        Validate and sanitize user answers.

        Args:
            answers (dict): A dictionary of user responses.

        Returns:
            dict: Validated and sanitized answers.
        """
        return validate_answers(answers)