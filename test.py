
class Exercise:
    def __init__(self, name, reps, sets):
        self.name = name
        self.weight = weight
        self.reps = reps
        self.sets = sets
        

    def __str__(self):
        return f"{self.name}: {self.weight} {self.sets} sets of {self.reps} reps"


class WorkoutPlan:
    def __init__(self):
        self.exercises = []

    def add_exercise(self, name, reps, sets):
        exercise = Exercise(name, reps, sets)
        self.exercises.append(exercise)

    def show_plan(self):
        for exercise in self.exercises:
            print(exercise)


def main():
    workout_plan = WorkoutPlan()
    
    while True:
        name = input("Enter exercise name (or 'done' to finish): ")
        if name.lower() == 'done':
            break
        reps = int(input("Enter number of reps: "))
        sets = int(input("Enter number of sets: "))
        workout_plan.add_exercise(name, reps, sets)

    print("\nYour Workout Plan:")
    workout_plan.show_plan()


if __name__ == "__main__":
    main()
