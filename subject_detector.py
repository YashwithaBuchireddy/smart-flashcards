def detect_subject(text):
    text = text.lower()

    keywords = {
        "physics": ["newton", "force", "acceleration", "velocity", "energy", "gravity", "mass", "momentum", "friction", "wave"],
        "biology": ["photosynthesis", "cell", "mitosis", "dna", "gene", "evolution", "organism", "bacteria", "virus", "ecosystem"],
        "chemistry": ["atom", "molecule", "reaction", "acid", "base", "compound", "element", "periodic", "chemical", "formula"],
        "math": ["algebra", "calculus", "geometry", "equation", "theorem", "integral", "derivative", "add", "subtract", "multiply", "divide", "sum", "fraction", "+", "-", "*", "/", "=", "solve", "calculate", "number"],
        "history": ["war", "revolution", "empire", "king", "queen", "dynasty", "president", "battle", "ancient", "medieval"],
        "geography": ["capital", "country", "continent", "ocean", "mountain", "river", "city", "state", "nation", "location", "map"],
        "literature": ["wrote", "author", "novel", "poem", "book", "shakespeare", "play", "story", "character", "plot"],
        "science": ["experiment", "hypothesis", "theory", "research", "laboratory", "scientific", "method", "data"]
    }

    for subject, words in keywords.items():
        if any(word in text for word in words):
            return subject.capitalize()

    return "General"
