# SAIT Cybersecurity CTF Jeopardy

A retro-styled Jeopardy trivia game designed for cybersecurity CTF events at SAIT (Southern Alberta Institute of Technology).

## Features

- **Retro Terminal Aesthetic**: Green-on-black styling with flicker effects and scan lines
- **Multiple Categories**: 
  - Trojan Territory (SAIT-specific questions)
  - Cyber Frontlines (Cybersecurity fundamentals)
  - Life in Wasteland (Fallout game references)
  - Pop Culture Hacked (Tech/hacking in media)
  - Human Exploits (Social engineering)
  - Tech Lore & History (Computing history)
- **Team Management**: Add teams, track scores, award/deduct points
- **Interactive Gameplay**: Click tiles to reveal questions, show answers
- **Progress Tracking**: Visual progress bar and tile state management

## Requirements

- Python 3.7+
- Streamlit

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/FalloutTrivia.git
cd FalloutTrivia
```

2. Install dependencies:
```bash
pip install streamlit
```

## Usage

Run the application:
```bash
streamlit run trivia.py
```

The game will open in your web browser at `http://localhost:8501`

## Game Rules

1. Teams take turns selecting question tiles by point value
2. Host reads the question aloud
3. First team to answer correctly gets the points
4. Wrong answers can optionally deduct points (configurable)
5. Game continues until all tiles are revealed or time runs out

## Customization

Questions can be easily modified by editing the `QUESTIONS` dictionary in `trivia.py`. Each category contains questions with point values from 100-1000.

## Contributing

Feel free to submit pull requests with:
- Additional question categories
- New styling themes
- Feature improvements
- Bug fixes

## License

MIT License - feel free to use and modify for your own events!

---
*Designed for SAIT Cybersecurity CTF events with love for retro computing aesthetics* 🖥️