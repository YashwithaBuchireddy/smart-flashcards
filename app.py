from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

# ---------------- Subject Detection Logic ---------------- #
def detect_subject(text):
    text = (text or "").lower()

    keywords = {
        "physics": ["newton", "force", "acceleration", "velocity", "energy", "gravity", "momentum"],
        "biology": ["photosynthesis", "cell", "mitosis", "dna", "gene", "evolution", "organism"],
        "chemistry": ["atom", "molecule", "reaction", "acid", "base", "compound", "ph"],
        "math": ["algebra", "calculus", "geometry", "equation", "theorem", "integral", "derivative"],
        "history": ["war", "revolution", "empire", "king", "queen", "dynasty", "treaty"]
    }

    for subject, words in keywords.items():
        if any(word in text for word in words):
            return subject.capitalize()

    return "General"

# ---------------- Flask App Setup ---------------- #
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- Database Model ---------------- #
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(50), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# ---------------- Task 1: Add Flashcard ---------------- #
@app.route("/flashcard", methods=["POST"])
def add_flashcard():
    data = request.get_json() or {}
    student_id = data.get("student_id")
    question = data.get("question")
    answer = data.get("answer")

    if not (student_id and question and answer):
        return jsonify({"error": "student_id, question, and answer are required"}), 400

    subject = detect_subject(question)
    new_card = Flashcard(student_id=student_id, question=question, answer=answer, subject=subject)
    db.session.add(new_card)
    db.session.commit()

    return jsonify({"message": "Flashcard added successfully", "subject": subject}), 201

# ---------------- Task 2: Get Mixed Subject Flashcards ---------------- #
@app.route("/get-subject", methods=["GET"])
def get_flashcards():
    student_id = request.args.get("student_id")
    limit = int(request.args.get("limit", 5))

    if not student_id:
        return jsonify({"error": "student_id query param required"}), 400

    # Fetch all flashcards for this student
    cards = Flashcard.query.filter_by(student_id=student_id).all()

    # Group cards by subject
    subject_groups = {}
    for card in cards:
        subject_groups.setdefault(card.subject, []).append(card)

    # Round-robin pick until limit reached
    result_cards = []
    while len(result_cards) < limit and any(subject_groups.values()):
        for subject in list(subject_groups.keys()):
            if subject_groups[subject]:
                result_cards.append(subject_groups[subject].pop(0))
            if not subject_groups[subject]:  # remove empty subjects
                del subject_groups[subject]
            if len(result_cards) >= limit:
                break

    # Shuffle results to mix subjects
    random.shuffle(result_cards)

    return jsonify([
        {"question": c.question, "answer": c.answer, "subject": c.subject}
        for c in result_cards
    ]), 200

# ---------------- Run App ---------------- #
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
