# Fretboard Master

Fretboard Master is an interactive guitar training tool built with Python and CustomTkinter. It helps users practice guitar notes, chords, and scales through a virtual fretboard. The app provides real-time feedback and audio, allowing users to train their ears while learning essential music theory.

## Features

- **Interactive Fretboard**: Clickable frets and strings that play corresponding guitar notes.
- **Practice Modes**:
  - **Notes**: Select specific notes to practice and receive feedback on your accuracy.
  - **Chords**: Practice guitar chords and get precise feedback on finger placement.
  - **Scales**: Practice major and pentatonic scales with precise feedback on finger placement.
- **Audio Feedback**: Pre-recorded guitar sounds for each note, chord, and scale played.
- **Progress Tracking**: The app tracks user performance.
- **Learning Modules**: Fingering guides for learning the notes and chords on the fretboard.
- **Login/Register System**: Users can create accounts to save progress.
- **Settings Customization**: Change the theme (dark/light) and resolution for a personalized experience.

## Installation

### Requirements

- Python 3.10 or higher
- Required Python packages:
  - `customtkinter`
  - `simpleaudio`
  - `sqlite3`
  - `bcrypt` (for account creation)
  - `matplotlib` (for stat visualization)
  
Install the required packages via pip:
```bash
pip install customtkinter simpleaudio bcrypt matplotlib
```
Clone the repository or download the source code:
```bash
git clone https://github.com/swhoque/Fretboard-Master.git
```
Go to project folder and start:
```bash
python3 Fretboard-Master
```
## TODO
1. Implement machine learning model to recognize chord charts and add them into chord database.
2. Implement machine learning model that recognizes user progress and queries OpenAI client for feedback.
## Contributing
Feel free to submit pull requests and contact me about adding features.
