import spacy
import heapq
import re

# Load spaCy's medium-sized model (supports similarity comparisons)
nlp = spacy.load("en_core_web_md")

# Predefined danger levels
danger_keywords = {
    # High Danger (Immediate Life-Threatening Situations)
    10: [
        "car crash", "collision", "gun", "explosion", "falling object", "fire", "electric shock",
        "attack", "violence", "earthquake", "tornado", "hurricane", "flood", "tsunami", "building collapse",
        "gas leak", "bomb", "armed person", "stampede"
    ],

    # ⚠️ Severe Danger (Very Risky but Avoidable with Immediate Action)
    9: [
        "speeding", "uncontrolled", "train approaching", "incoming truck", "falling debris",
        "heavy traffic", "icy road", "high voltage", "breaking glass", "wild animal ahead",
        "unstable ground", "deep hole", "bridge collapse"
    ],

    # High Risk (Hazards That Require Quick Awareness & Avoidance)
    8: [
        "car coming", "child in front", "moving bicycle", "sharp turn", "steep drop",
        "motorcycle approaching", "large crowd", "low-hanging object", "narrow passage",
        "construction zone", "roadwork", "blocked sidewalk", "crosswalk signal ending"
    ],

    # ⚠️ Moderate Risk (Potential Danger if Not Careful)
    7: [
        "slippery", "construction", "hazard", "curb ahead", "stairs going down",
        "stairs going up", "pothole", "uneven surface", "broken sidewalk",
        "low visibility", "dark alley", "missing handrail", "loose gravel"
    ],

    # Caution (Situations That Need Some Attention)
    6: [
        "be aware", "caution", "door closing", "elevator not working",
        "bike lane merging", "wet floor", "noisy environment", "low ceiling",
        "tight space", "crowded area", "temporary barrier", "shifting terrain"
    ],

    # Low Risk (Routine Instructions or Mild Awareness Needed)
    5: [
        "approaching intersection", "listen for beeping", "crosswalk ahead",
        "wait for signal", "sidewalk ends", "unknown surface",
        "changing floor texture", "traffic light changing"
    ],

    # Basic Instructions (Navigational Cues)
    4: [
        "use handrail", "step forward", "step down", "step up",
        "path curves", "door ahead", "escalator up", "escalator down"
    ],

    # Low-Level Guidance (Simple Directional Instructions)
    3: [
        "walk left", "turn right", "turn left", "look around", "walk slowly",
        "follow the path", "stay straight", "slight right", "slight left",
        "adjust course", "continue forward"
    ],

    # Informational (Non-Essential Context)
    2: [
        "bench on the right", "wall on the left", "tree nearby",
        "building entrance ahead", "rest area", "public restroom",
        "water fountain", "trash can ahead", "bus stop nearby"
    ],

    # Minimal Guidance (Non-urgent, Situational Context)
    1: [
        "clear path", "open space", "wide sidewalk", "safe crossing",
        "quiet area", "low traffic", "smooth pavement", "well-lit area"
    ]
}# Convert keywords to spaCy docs for similarity comparison
danger_docs = {score: [nlp(word) for word in words] for score, words in danger_keywords.items()}

def get_danger_score(phrase):
    """
    Assigns a danger score (1-10) based on predefined keywords and spaCy similarity.
    """
    phrase_doc = nlp(phrase)
    best_score = 1  # Default minimum score

    for score, keyword_docs in danger_docs.items():
        for keyword_doc in keyword_docs:
            similarity = phrase_doc.similarity(keyword_doc)
            if similarity > 0.6:  # Threshold for relevance
                best_score = max(best_score, score)

    return best_score

def rank_phrases(phrases):
    """
    Ranks phrases based on their danger score in descending order.
    Uses a priority queue (max-heap).
    """
    phrase_scores = [(get_danger_score(phrase), phrase) for phrase in phrases]
    phrase_scores.sort(reverse=True, key=lambda x: x[0])  # Sort by danger level (highest first)
    return phrase_scores

# Example phrases to rank
phrases = [
    "turn right",
    "turn left",
    "walk straight",
    "there's a tree in front of you",
    "there is a speeding car coming in front of you",
    "there is violence ahead",
    "do not go forward"
]

# Rank and print results
ranked_phrases = rank_phrases(phrases)

print("\nRanked Danger Phrases")
for score, phrase in ranked_phrases:
    print(f"{phrase}: {score}/10")