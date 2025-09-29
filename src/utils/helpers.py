def validate_answers(answers):
    """
    Validate the user answers to ensure they are complete and correct.

    Args:
        answers (dict): A dictionary of user responses from the questionnaire.

    Returns:
        dict: A validated and sanitized version of the answers.
    """
    valid_goals = {"Strength", "Cardio", "Flexibility", "General Fitness"}
    goal = answers.get("goal", "General Fitness")
    if goal not in valid_goals:
        goal = "General Fitness"

    duration = answers.get("duration", 30)
    if not isinstance(duration, int) or duration <= 0:
        duration = 30

    frequency = answers.get("frequency", 3)
    if not isinstance(frequency, int) or frequency <= 0:
        frequency = 3

    return {
        "goal": goal,
        "duration": duration,
        "frequency": frequency
    }


def format_training_plan(plan):
    """
    Format the training plan dictionary into a human-readable string.

    Args:
        plan (dict): A dictionary representing the training plan.

    Returns:
        str: A formatted string representation of the training plan.
    """
    formatted_plan = (
        f"Goal: {plan['goal']}\n"
        f"Duration: {plan['duration']}\n"
        f"Frequency: {plan['frequency']}\n"
        f"Exercises: {', '.join(plan['exercises'])}"
    )
    return formatted_plan


def get_default_answers():
    """
    Provide default answers for the questionnaire.

    Returns:
        dict: A dictionary of default answers.
    """
    return {
        "goal": "General Fitness",
        "duration": 30,
        "frequency": 3
    }

