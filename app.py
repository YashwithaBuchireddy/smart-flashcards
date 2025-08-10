from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from subject_detector import detect_subject
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Smart Flashcards API", "endpoints": {
        "POST /flashcard": "Add a new flashcard",
        "GET /get-subject": "Get flashcards for a student (params: student_id, limit)"
    }})

@app.route("/flashcard", methods=["POST"])
def add_flashcard():
    data = request.get_json()
    student_id = data.get("student_id")
    question = data.get("question")
    answer = data.get("answer")

    subject = detect_subject(question)
    new_card = Flashcard(student_id=student_id, question=question, answer=answer, subject=subject)
    db.session.add(new_card)
    db.session.commit()

    return jsonify({"message": "Flashcard added successfully", "subject": subject})

@app.route("/get-subject", methods=["GET"])
def get_flashcards():
    student_id = request.args.get("student_id")
    limit = int(request.args.get("limit", 5))

    cards = Flashcard.query.filter_by(student_id=student_id).all()

    # Group by subject
    subject_groups = {}
    for card in cards:
        subject_groups.setdefault(card.subject, []).append(card)

    # Pick 1 from each subject until limit is reached
    result = []
    while len(result) < limit and subject_groups:
        for subject in list(subject_groups.keys()):
            if subject_groups[subject]:
                result.append(subject_groups[subject].pop(0))
            if not subject_groups[subject]:
                del subject_groups[subject]
            if len(result) >= limit:
                break

    # Shuffle to mix
    random.shuffle(result)

    return jsonify([
        {"question": c.question, "answer": c.answer, "subject": c.subject}
        for c in result
    ])

if __name__ == "__main__":
    app.run(debug=True, port=5001)
