from dataclasses import dataclass, field
from typing import List, Dict, Any, Literal, Tuple
import math

# -----------------------------
# 1) Datamodell & mapping
# -----------------------------

Experience = Literal["Nybegynner", "Viderekommen", "Erfaren", "Profesjonell"]
Goal = Literal["Komme i bedre form", "Bedre livsstil", "Øke utholdenheten", "Bli sterkere", "Redusere vekten"]
Preference = Literal["Styrketrening", "Løping", "Sykling", "Svømming", "Variert"]

@dataclass
class UserProfile:
    """Intern representasjon av brukersvar fra skjemaet.
    Vi mappe norske nøkler til engelske felt for intern bruk, men beholder norsk semantikk.
    """
    experience: Experience
    goal: Goal
    preference: Preference
    frequency_choice: str          # f.eks. "1-2", "3-4", "5-7"
    duration_min: int              # ønsket varighet per økt (minutter)

    def resolved_frequency(self) -> int:
        """Velg et heltall for antall økter/uke fra intervallet brukeren valgte.
        - Strategi: velg øvre del av intervallet for måloppnåelse, men begrens av ACSM/WHO.
        """
        mapping = {"1-2": (1, 2), "3-4": (3, 4), "5-7": (5, 7)}
        low, high = mapping.get(self.frequency_choice, (3, 4))
        # For nybegynnere – ofte bedre å starte midt/øvre av intervallet, men uten å overdrive
        if self.experience == "Nybegynner":
            return min(high, 3)
        if self.experience == "Viderekommen":
            return high
        # Erfaren/Profesjonell kan tåle høyere frekvens
        return high

# -----------------------------
# 2) Hjelpefunksjoner og kunnskapsregler
# -----------------------------

def who_min_weekly_minutes(goal: Goal) -> int:
    """WHO: 150–300 min/uke moderat eller 75–150 min/uke hard.
    For helse/fett-tap -> sikte minst 150 min/uke. For styrke -> behold styrkefokus men anbefal supplering.
    Kilde: WHO retningslinjer (2020)."""
    if goal in ("Komme i bedre form", "Bedre livsstil", "Redusere vekten", "Øke utholdenheten"):
        return 150  # kan skaleres opp til 300
    return 90  # hvis primært styrke, anbefal minst ~90 min kondisjon som støtte (3x30)

def acsm_strength_frequency(experience: Experience) -> Tuple[int, int]:
    """ACSM-frekvensintervaller for styrketrening.
    Returnerer (min, maks) anbefalte styrkeøkter/uke.
    Kilde: ACSM position stand."""
    if experience == "Nybegynner":
        return (2, 3)
    if experience == "Viderekommen":
        return (3, 4)
    return (4, 5)  # Erfaren/Profesjonell

def weekly_progression_factor(week: int) -> float:
    """Progresjon ≤10% pr uke uke 2–3, deload uke 4 (–25%).
    Kilder: ACSM 2–10% økning, generell 10% tommelfingerregel.
    """
    if week == 1:
        return 1.0
    if week == 2:
        return 1.05
    if week == 3:
        return 1.10
    if week == 4:
        return 0.75  # deload
    return 1.0

# -----------------------------
# 3) Øvelsesbibliotek
# -----------------------------

EXERCISES = {
    "Styrke_helkropp": [
        {"name": "Knebøy", "sets": 3, "reps": (8, 12), "rpe": (6, 8)},
        {"name": "Benkpress / Armhevinger", "sets": 3, "reps": (8, 12), "rpe": (6, 8)},
        {"name": "Roing med manual/kabel", "sets": 3, "reps": (8, 12), "rpe": (6, 8)},
        {"name": "Skulderpress", "sets": 2, "reps": (10, 12), "rpe": (6, 8)},
        {"name": "Markløft (lett/teknikk) eller Rumenske markløft", "sets": 2, "reps": (6, 10), "rpe": (6, 7)},
        {"name": "Planke/Sideplanke", "sets": 2, "hold_sec_range": (30, 45), "rpe": (6, 8)}
    ],
    "Løping": [
        {"name": "Rolig sone-2 løp", "duration_min": 30, "rpe": 4},
        {"name": "Tempointervall (f.eks. 3x8 min)", "duration_min": 40, "rpe": 7},
        {"name": "Langkjøring rolig", "duration_min": 45, "rpe": 5},
    ],
    "Sykling": [
        {"name": "Sone-2 sykkel", "duration_min": 40, "rpe": 4},
        {"name": "Intervaller 4x4 min", "duration_min": 35, "rpe": 7},
        {"name": "Langtur rolig", "duration_min": 60, "rpe": 5},
    ],
    "Svømming": [
        {"name": "Teknikk + rolig sammenhengende", "duration_min": 30, "rpe": 4},
        {"name": "Pyramide-intervaller", "duration_min": 35, "rpe": 7},
        {"name": "Kontinuerlig svømming", "duration_min": 40, "rpe": 5},
    ],
    "Variert": [
        {"name": "Sirkeltrening (kroppsvekt)", "duration_min": 30, "rpe": 6},
        {"name": "Rask gange/jogg", "duration_min": 30, "rpe": 4},
        {"name": "Mobilitet/yoga", "duration_min": 20, "rpe": 3},
    ]
}

# -----------------------------
# 4) Plan-generator
# -----------------------------

@dataclass
class Session:
    day: str
    focus: str            # "Styrke", "Kondisjon", "Variert"
    blocks: List[Dict]    # øvelser eller kondisjonsblokker
    duration_min: int
    rpe_target: str       # f.eks. "RPE 6–8"
    notes: str = ""

@dataclass
class WeeklyPlan:
    week: int
    sessions: List[Session] = field(default_factory=list)

@dataclass
class TrainingPlan:
    user: UserProfile
    weeks: List[WeeklyPlan] = field(default_factory=list)
    total_weekly_minutes: int = 0

    def generate(self, num_weeks: int = 4) -> "TrainingPlan":
        """Generer 4-ukers plan med progresjon og deload.
        - Fordeler økter per uke
        - Velger innhold i hver økt basert på mål og preferanse
        - Bruker RPE og sett/reps fra biblioteket
        """
        freq = self.user.resolved_frequency()
        minutes_per_session = max(20, int(self.user.duration_min))  # sikkerhetsnett
        self.total_weekly_minutes = freq * minutes_per_session

        # Sikre WHO-minimum for relevante mål ved å justere kondisjonsandel om nødvendig
        required = who_min_weekly_minutes(self.user.goal)
        needs_extra_cardio = self.total_weekly_minutes < required and self.user.goal in (
            "Komme i bedre form", "Bedre livsstil", "Redusere vekten", "Øke utholdenheten"
        )

        # Styrkeandel etter ACSM hvis preferanse/mål tilsier
        strength_min, strength_max = acsm_strength_frequency(self.user.experience)
        target_strength_sessions = 0
        if self.user.preference == "Styrketrening" or self.user.goal == "Bli sterkere":
            target_strength_sessions = min(freq, max(strength_min, min(strength_max, math.ceil(freq*0.6))))
        elif self.user.preference == "Variert":
            target_strength_sessions = min(freq, max(2, math.floor(freq/2)))
        else:
            target_strength_sessions = min(freq, 2)  # legg inn noe styrke selv om kondisjonspreferanse

        # Sterk prioritet hvis "Øke utholdenheten"
        if self.user.goal == "Øke utholdenheten":
            target_strength_sessions = max(1, min(2, target_strength_sessions))

        # Fordel dager i uken
        day_names = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"]
        # Spre jevnt: eksempelvis Man-Ons-Fre for 3 økter
        chosen_days = [day_names[i*(7//freq)] for i in range(freq)] if freq < 7 else day_names

        for w in range(1, num_weeks+1):
            week_factor = weekly_progression_factor(w)
            sessions: List[Session] = []
            strength_left = target_strength_sessions
            for d in chosen_days:
                # Bestem fokus for denne økten
                if strength_left > 0:
                    focus = "Styrke"
                    strength_left -= 1
                else:
                    focus = "Kondisjon" if self.user.preference != "Variert" else "Variert"

                # Bygg innhold
                if focus == "Styrke":
                    blocks = EXERCISES["Styrke_helkropp"]
                    rpe_text = "RPE 6–8"
                    notes = "Oppvarming 5–10 min. Øk belastning gradvis. Teknikk først."
                    # Anvend progresjon: øk sett/reps/last lett i uke 2–3, deload uke 4
                    adj_blocks = []
                    for b in blocks:
                        b = dict(b)  # kopi
                        reps = b.get("reps", None)
                        if (
                            isinstance(reps, tuple)
                            and len(reps) == 2
                            and all(isinstance(x, int) for x in reps)
                        ):
                            lo, hi = reps
                            if w == 1:
                                hi_adj = hi
                            elif w == 2:
                                hi_adj = int(round(hi * 1.05))
                            elif w == 3:
                                hi_adj = int(round(hi * 1.10))
                            else:  # uke 4 deload
                                hi_adj = max(lo, int(round(hi * 0.85)))
                            b["reps"] = (lo, hi_adj)

                        adj_blocks.append(b)

                    duration = minutes_per_session
                    blocks_out = adj_blocks

                elif focus == "Kondisjon":
                    lib_key = self.user.preference if self.user.preference in ("Løping", "Sykling", "Svømming") else "Variert"
                    # velg en passende øktmal syklisk
                    template = EXERCISES[lib_key][(w-1) % len(EXERCISES[lib_key])]
                    base_dur = template["duration_min"]
                    duration = min(minutes_per_session, int(base_dur * week_factor))
                    rpe_text = f"RPE {template['rpe']} (styrt av pust/prat-test)"
                    notes = "Oppvarming 5–10 min rolig. Nedtrapping 5 min."
                    blocks_out = [template]

                else:  # Variert
                    template = EXERCISES["Variert"][(w-1) % len(EXERCISES["Variert"])]
                    duration = min(minutes_per_session, int(template["duration_min"] * week_factor))
                    rpe_text = f"RPE {template['rpe']}"
                    notes = "Oppvarming 5–10 min. Fokus på teknikk og kontroll."
                    blocks_out = [template]

                sessions.append(Session(
                    day=d, focus=focus, blocks=blocks_out,
                    duration_min=duration, rpe_target=rpe_text, notes=notes
                ))

            # Dersom WHO-minimum ikke oppfylles, merk uken med tips om ekstra lavterskel-kondisjon
            if needs_extra_cardio:
                sessions.append(Session(
                    day="Valgfri", focus="Ekstra-kondisjon",
                    blocks=[{"name": "Rask gange / sone-2", "duration_min": 20, "rpe": 3}],
                    duration_min=20, rpe_target="RPE 3", notes="Lav terskel for å nå 150 min/uke."
                ))

            self.weeks.append(WeeklyPlan(week=w, sessions=sessions))

        return self

# -----------------------------
# 5) Adapter: fra Tkinter-svar -> UserProfile
# -----------------------------

def map_tkinter_answers_to_profile(ans: Dict[str, Any]) -> UserProfile:
    """Forventede nøkler fra eksisterende GUI:
    'Erfaring', 'Mål', 'Preferanse', 'Antall', 'Varighet' (str/int)
    """
    # Normaliser varighet
    try:
        duration = int(str(ans.get("Varighet", "45")).strip())
    except ValueError:
        duration = 45

    return UserProfile(
        experience=ans.get("Erfaring", "Nybegynner"),
        goal=ans.get("Mål", "Komme i bedre form"),
        preference=ans.get("Preferanse", "Variert"),
        frequency_choice=ans.get("Antall", "3-4"),
        duration_min=duration
    )

# -----------------------------
# 6) Hjelpefunksjon for serialisering
# -----------------------------

def plan_to_dict(plan: TrainingPlan) -> Dict[str, Any]:
    out = {"weeks": []}
    for w in plan.weeks:
        week_dict = {"week": w.week, "sessions": []}
        for s in w.sessions:
            week_dict["sessions"].append({
                "day": s.day,
                "focus": s.focus,
                "duration_min": s.duration_min,
                "rpe_target": s.rpe_target,
                "notes": s.notes,
                "blocks": s.blocks
            })
        out["weeks"].append(week_dict)
    return out

# -----------------------------
# 7) Eksempelbruk
# -----------------------------
if __name__ == "__main__":
    # Eksempel: simulerer svar fra eksisterende Tkinter-skjema
    answers_no = {
        "Erfaring": "Nybegynner",
        "Mål": "Redusere vekten",
        "Preferanse": "Variert",
        "Antall": "3-4",
        "Varighet": "45"
    }
    profile = map_tkinter_answers_to_profile(answers_no)
    plan = TrainingPlan(user=profile).generate(num_weeks=4)
    plan_dict = plan_to_dict(plan)

    # Pretty-print kort sammendrag
    import json
    print(json.dumps(plan_dict, ensure_ascii=False, indent=2))
