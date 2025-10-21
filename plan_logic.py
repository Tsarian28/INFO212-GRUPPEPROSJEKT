from __future__ import annotations
def generate_plan(goal: str, level: str, gear: str):
    base = []
    def push(name, sets, reps, weight=0):
        base.append({"name": name, "sets": sets, "reps": reps, "weight": weight})
    if goal == "styrke":
        push("Knebøy", 5, 5)
        push("Benkpress", 5, 5)
        push("Markløft", 3, 5)
    if goal == "hypertrofi":
        push("Skrå benk m/manualer", 4, 10)
        push("Nedtrekk/Bor", 4, 10)
        push("Skulderpress", 3, 12)
    if goal == "spenst":
        push("Box jumps", 5, 5)
        push("Medisinball-kast", 4, 6)
        push("Bulgarian split squat", 4, 8)
    if goal == "utholdenhet":
        push("Roing (meter)", 3, 500)
        push("Sykling intervall (min)", 6, 2)
        push("Kjernesirkel (reps)", 3, 15)
    mult = 0.8 if level == "nybegynner" else 1.2 if level == "avansert" else 1.0
    for e in base:
        e["sets"] = max(1, round(e["sets"] * mult))
        e["reps"] = max(1, round(e["reps"] * mult))
    if gear == "kroppsvekt":
        for e in base:
            lname = e["name"].lower()
            if "benk" in lname:
                e["name"] = "Push-ups variant"
            if "mark" in lname:
                e["name"] = "Hip hinge (kroppsvekt)"
    if gear == "hjemme_enkle":
        for e in base:
            if e["name"] == "Knebøy":
                e["name"] = "Goblet squat"
    return base
