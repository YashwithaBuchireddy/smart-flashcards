# Smart Flashcards API

A Flask-based REST API for creating and managing flashcards with intelligent subject detection and mixed-subject retrieval.

## Features

- **Automatic Subject Detection**: Intelligently categorizes flashcards into subjects (Physics, Biology, Chemistry, Math, History) based on question content
- **Mixed Subject Retrieval**: Returns flashcards from different subjects in a round-robin fashion for balanced learning
- **Student Isolation**: Each student's flashcards are kept separate
- **RESTful API**: Clean HTTP endpoints for easy integration
- **SQLite Database**: Lightweight, file-based database storage

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or Download the Repository**
   ```bash
   git clone https://github.com/YashwithaBuchireddy/smart-flashcards.git
   cd smart-flashcards
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install flask flask_sqlalchemy
   ```
   
   Or if you have a requirements.txt file:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

   The application will start on `http://127.0.0.1:5000`

## API Documentation

### Base URL
```
http://127.0.0.1:5000
```

### Endpoints

#### 1. Add Flashcard
**POST** `/flashcard`

Creates a new flashcard with automatic subject detection.

**Request Body:**
```json
{
  "student_id": "string",
  "question": "string",
  "answer": "string"
}
```

**Response (201 Created):**
```json
{
  "message": "Flashcard added successfully",
  "subject": "Physics"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "student_id, question, and answer are required"
}
```

#### 2. Get Mixed Subject Flashcards
**GET** `/get-subject`

Retrieves flashcards for a student with mixed subjects using round-robin selection.

**Query Parameters:**
- `student_id` (required): ID of the student
- `limit` (optional, default=5): Maximum number of flashcards to return

**Example Request:**
```
GET /get-subject?student_id=stu001&limit=10
```

**Response (200 OK):**
```json
[
  {
    "question": "What is Newton's Second Law?",
    "answer": "Force equals mass times acceleration",
    "subject": "Physics"
  },
  {
    "question": "What is photosynthesis?",
    "answer": "The process by which plants make food using sunlight",
    "subject": "Biology"
  }
]
```

**Error Response (400 Bad Request):**
```json
{
  "error": "student_id query param required"
}
```

## Usage Examples

### Using cURL

1. **Add a Physics Flashcard:**
   ```bash
   curl -X POST http://127.0.0.1:5000/flashcard \
     -H "Content-Type: application/json" \
     -d '{
       "student_id": "stu001",
       "question": "What is Newton'\''s Second Law?",
       "answer": "Force equals mass times acceleration"
     }'
   ```

2. **Add a Biology Flashcard:**
   ```bash
   curl -X POST http://127.0.0.1:5000/flashcard \
     -H "Content-Type: application/json" \
     -d '{
       "student_id": "stu001",
       "question": "What is photosynthesis?",
       "answer": "The process by which plants make food using sunlight"
     }'
   ```

3. **Retrieve Mixed Flashcards:**
   ```bash
   curl "http://127.0.0.1:5000/get-subject?student_id=stu001&limit=5"
   ```

### Using Python Requests

```python
import requests
import json

# Add a flashcard
response = requests.post('http://127.0.0.1:5000/flashcard', 
    headers={'Content-Type': 'application/json'},
    json={
        'student_id': 'stu001',
        'question': 'What is the pH of pure water?',
        'answer': '7 (neutral)'
    }
)
print(response.json())

# Get flashcards
response = requests.get('http://127.0.0.1:5000/get-subject?student_id=stu001&limit=3')
flashcards = response.json()
for card in flashcards:
    print(f"Q: {card['question']}")
    print(f"A: {card['answer']}")
    print(f"Subject: {card['subject']}\n")
```

## Subject Detection

The application automatically detects subjects based on keywords in the question:

| Subject | Keywords |
|---------|----------|
| **Physics** | newton, force, acceleration, velocity, energy, gravity, momentum |
| **Biology** | photosynthesis, cell, mitosis, dna, gene, evolution, organism |
| **Chemistry** | atom, molecule, reaction, acid, base, compound, ph |
| **Math** | algebra, calculus, geometry, equation, theorem, integral, derivative |
| **History** | war, revolution, empire, king, queen, dynasty, treaty |
| **General** | Default for questions that don't match any specific subject |

## Mixed Subject Algorithm

When retrieving flashcards, the system:

1. Groups all flashcards by subject
2. Uses round-robin selection to pick one flashcard from each subject
3. Continues until the requested limit is reached
4. Shuffles the final result to mix subjects randomly
5. Returns the balanced set of flashcards

This ensures students get exposure to different subjects rather than all flashcards from one topic.

## Database

The application uses SQLite database (`flashcard.db`) with the following schema:

```sql
CREATE TABLE flashcard (
    id INTEGER PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    subject VARCHAR(50) NOT NULL
);
```

The database file is automatically created when you first run the application.

## Project Structure

```
smart-flashcards/
├── app.py              # Main Flask application
├── flashcard.db        # SQLite database (created automatically)
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── venv/              # Virtual environment (if created)
```

## Development

### Running in Development Mode

The application runs in debug mode by default, which provides:
- Automatic reloading when code changes
- Detailed error messages
- Debug console for errors

### Testing

You can test the API using:
- cURL commands (examples provided above)
- Postman or similar API testing tools
- Python requests library
- Browser for GET requests

## Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   - On macOS, AirPlay Receiver might be using port 5000
   - Disable it in System Preferences > General > AirDrop & Handoff
   - Or modify the port in `app.py`: `app.run(host="127.0.0.1", port=5001, debug=True)`

2. **Module not found errors**
   - Ensure your virtual environment is activated
   - Install dependencies: `pip install flask flask_sqlalchemy`

3. **Database permission errors**
   - Check that the application directory is writable
   - The SQLite database file needs write permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Feel free to use and modify as needed.

## Future Enhancements

- Add user authentication
- Implement spaced repetition algorithm
- Add flashcard categories and tags
- Export/import flashcard sets
- Web-based user interface
- More sophisticated subject detection using NLP
- Analytics and progress tracking
