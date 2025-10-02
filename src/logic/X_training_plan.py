'''
This is used for generating a plan based on the user input from the questionnaire. This is to be used in a later version of the program
This is the brain of our app
'''

class TrainingPlan:
    def __init__(self, answers):
        """
        Initialize the TrainingPlan with user answers.

        Args:
            answers (dict): A dictionary of user responses from the questionnaire.
        """
        self.goal = answers.get("goal", "General Fitness")
        self.duration = answers.get("duration", 30)  # in minutes
        self.frequency = answers.get("frequency", 3)  # times per week
        self.exercises = self._generate_exercises()

    def _generate_exercises(self):
        """Generate exercises based on the goal."""
        if self.goal == "Strength":
            return ["Squats", "Deadlifts", "Bench Press"]
        elif self.goal == "Cardio":
            return ["Running", "Cycling", "Rowing"]
        elif self.goal == "Flexibility":
            return ["Yoga", "Stretching"]
        else:
            return ["Bodyweight Exercises", "Walking"]

    def update_goal(self, new_goal):
        """Update the goal and regenerate exercises."""
        self.goal = new_goal
        self.exercises = self._generate_exercises()

    def update_duration(self, new_duration):
        """Update the duration of the training sessions."""
        self.duration = new_duration

    def update_frequency(self, new_frequency):
        """Update the frequency of the training sessions."""
        self.frequency = new_frequency

    def to_dict(self):
        """Convert the training plan to a dictionary."""
        return {
            "goal": self.goal,
            "duration": f"{self.duration} minutes per session",
            "frequency": f"{self.frequency} times per week",
            "exercises": self.exercises
        }
